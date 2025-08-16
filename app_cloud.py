import os
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
from werkzeug.utils import secure_filename
import mediapipe as mp
from PIL import Image
import json
import threading
import time
import uuid
import base64
from datetime import datetime, timedelta
import tempfile

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'temp_uploads'  # Temporary storage
app.config['OUTPUT_FOLDER'] = 'temp_outputs'  # Temporary storage
app.config['SESSION_TIMEOUT'] = 3600  # 1 hour session timeout

# Create temporary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Initialize MediaPipe
mp_face_detection = mp.solutions.face_detection

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# Store user sessions and their files (in production, use Redis or database)
user_sessions = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_session():
    """Get or create user session"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['created_at'] = datetime.now().isoformat()
        user_sessions[session['user_id']] = {
            'uploads': [],
            'processed': [],
            'created_at': datetime.now()
        }
    return session['user_id']

def cleanup_old_sessions():
    """Clean up old sessions and temporary files"""
    current_time = datetime.now()
    expired_sessions = []
    
    for user_id, user_data in user_sessions.items():
        if current_time - user_data['created_at'] > timedelta(hours=1):
            expired_sessions.append(user_id)
            # Clean up user files
            for file_path in user_data['uploads'] + user_data['processed']:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except:
                    pass
    
    for user_id in expired_sessions:
        del user_sessions[user_id]

def detect_face_and_tie(image_path):
    """Detect face and tie area using AI for ID card style cropping"""
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            return None, "Could not read image"
        
        # Convert to RGB for MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Initialize face detection
        with mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5) as face_detection:
            
            results = face_detection.process(rgb_image)
            
            if results.detections:
                # Get the first detected face
                detection = results.detections[0]
                bbox = detection.location_data.relative_bounding_box
                
                h, w, _ = image.shape
                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)
                
                # Expand the crop area to include tie knot area
                expanded_height = int(height * 2.5)
                expanded_width = int(width * 1.8)
                
                # Adjust coordinates to stay within image bounds
                start_x = max(0, x - (expanded_width - width) // 2)
                start_y = max(0, y - (expanded_height - height) // 2)
                end_x = min(w, start_x + expanded_width)
                end_y = min(h, start_y + expanded_height)
                
                # Ensure minimum dimensions
                if end_x - start_x < 200:
                    center_x = (start_x + end_x) // 2
                    start_x = max(0, center_x - 100)
                    end_x = min(w, center_x + 100)
                
                if end_y - start_y < 300:
                    center_y = (start_y + end_y) // 2
                    start_y = max(0, center_y - 150)
                    end_y = min(h, center_y + 150)
                
                return {
                    'x': start_x,
                    'y': start_y,
                    'width': end_x - start_x,
                    'height': end_y - start_y
                }, None
            else:
                # Fallback: use center crop if no face detected
                h, w, _ = image.shape
                center_x, center_y = w // 2, h // 2
                crop_size = min(w, h) // 2
                
                return {
                    'x': max(0, center_x - crop_size // 2),
                    'y': max(0, center_y - crop_size // 2),
                    'width': min(crop_size, w),
                    'height': min(crop_size, h)
                }, "No face detected, using center crop"
                
    except Exception as e:
        return None, str(e)

def crop_image(image_path, crop_coords, output_path):
    """Crop image based on detected coordinates and maintain 1:1.285 aspect ratio"""
    try:
        image = cv2.imread(image_path)
        if image is None:
            return False, "Could not read image"
        
        # First crop the image based on detected coordinates
        cropped = image[
            crop_coords['y']:crop_coords['y'] + crop_coords['height'],
            crop_coords['x']:crop_coords['x'] + crop_coords['width']
        ]
        
        # Now resize to maintain 1:1.285 aspect ratio
        target_ratio = 1.0 / 1.285  # width/height ratio
        
        h, w = cropped.shape[:2]
        current_ratio = w / h
        
        if current_ratio > target_ratio:
            # Image is too wide, need to reduce width
            new_width = int(h * target_ratio)
            new_height = h
            # Center crop horizontally
            start_x = (w - new_width) // 2
            cropped = cropped[:, start_x:start_x + new_width]
        elif current_ratio < target_ratio:
            # Image is too tall, need to reduce height
            new_width = w
            new_height = int(w / target_ratio)
            # Center crop vertically
            start_y = (h - new_height) // 2
            cropped = cropped[start_y:start_y + new_height, :]
        
        # Save cropped image
        cv2.imwrite(output_path, cropped)
        return True, "Success"
        
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    """Main page with session management"""
    user_id = get_user_session()
    cleanup_old_sessions()
    
    # Get user's files
    user_data = user_sessions.get(user_id, {'uploads': [], 'processed': []})
    
    return render_template('index_cloud.html', 
                         uploads=user_data['uploads'],
                         processed=user_data['processed'])

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads with user session management"""
    try:
        user_id = get_user_session()
        user_data = user_sessions[user_id]
        
        if 'files[]' not in request.files:
            return jsonify({'error': 'No files selected'}), 400
        
        files = request.files.getlist('files[]')
        
        if not files or files[0].filename == '':
            return jsonify({'error': 'No files selected'}), 400
        
        uploaded_files = []
        for file in files:
            if file and allowed_file(file.filename):
                # Create unique filename
                filename = secure_filename(file.filename)
                unique_filename = f"{user_id}_{int(time.time())}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                
                file.save(filepath)
                uploaded_files.append(filepath)
                
                # Add to user's upload list
                user_data['uploads'].append(filepath)
        
        return jsonify({
            'message': f'{len(uploaded_files)} files uploaded successfully',
            'files': [os.path.basename(f) for f in uploaded_files]
        })
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/process', methods=['POST'])
def process_images():
    """Process images with user session management"""
    data = request.get_json()
    image_paths = data.get('image_paths', [])
    
    if not image_paths:
        return jsonify({'error': 'No images to process'}), 400
    
    user_id = get_user_session()
    user_data = user_sessions[user_id]
    
    results = []
    
    for image_path in image_paths:
        try:
            # Verify file belongs to user
            if image_path not in user_data['uploads']:
                continue
                
            # Detect face and tie area
            crop_coords, message = detect_face_and_tie(image_path)
            
            if crop_coords:
                # Generate output filename
                filename = os.path.basename(image_path)
                name, ext = os.path.splitext(filename)
                output_filename = f"{name}_cropped{ext}"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                
                # Crop the image
                success, crop_message = crop_image(image_path, crop_coords, output_path)
                
                if success:
                    # Add to user's processed list
                    user_data['processed'].append(output_path)
                
                results.append({
                    'input': os.path.basename(image_path),
                    'output': os.path.basename(output_path) if success else None,
                    'success': success,
                    'message': crop_message or message
                })
            else:
                results.append({
                    'input': os.path.basename(image_path),
                    'output': None,
                    'success': False,
                    'message': message
                })
                
        except Exception as e:
            results.append({
                'input': os.path.basename(image_path),
                'output': None,
                'success': False,
                'message': str(e)
            })
    
    return jsonify({
        'total_processed': len(results),
        'results': results
    })

@app.route('/download/<filename>')
def download_file(filename):
    """Download processed file with user verification"""
    user_id = get_user_session()
    user_data = user_sessions.get(user_id, {'processed': []})
    
    # Check if file belongs to user
    file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if file_path in user_data['processed']:
        return send_from_directory(app.config['OUTPUT_FOLDER'], filename)
    else:
        return jsonify({'error': 'File not found or access denied'}), 404

@app.route('/clear_session', methods=['POST'])
def clear_session():
    """Clear user session and files"""
    user_id = get_user_session()
    user_data = user_sessions.get(user_id, {})
    
    # Remove user files
    for file_path in user_data.get('uploads', []) + user_data.get('processed', []):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except:
            pass
    
    # Clear session
    session.clear()
    if user_id in user_sessions:
        del user_sessions[user_id]
    
    return jsonify({'message': 'Session cleared successfully'})

@app.route('/status')
def status():
    """Get user's file status"""
    user_id = get_user_session()
    user_data = user_sessions.get(user_id, {'uploads': [], 'processed': []})
    
    return jsonify({
        'uploaded_files': len(user_data['uploads']),
        'processed_images': len(user_data['processed']),
        'session_id': user_id
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
