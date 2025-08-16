import os
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import mediapipe as mp
from PIL import Image
import json
import threading
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'cropped_images'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size (increased from 16MB)
app.config['MAX_CONTENT_PATH'] = None  # Allow longer file paths

# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Initialize MediaPipe - using correct import structure
mp_face_detection = mp.solutions.face_detection

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_face_and_tie(image_path):
    """Detect face and tie area using AI for ID card style cropping"""
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            return None, "Could not read image"
        
        # Convert to RGB for MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Initialize face detection with latest MediaPipe
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
                # ID card style: face + upper chest area with tie
                expanded_height = int(height * 2.5)  # Include chest area
                expanded_width = int(width * 1.8)   # Include shoulders
                
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
        # Target aspect ratio: 1:1.285 = 0.778
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
        
        # Save cropped image with correct aspect ratio
        cv2.imwrite(output_path, cropped)
        return True, "Success"
        
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return jsonify({'status': 'Server is working!', 'message': 'Flask application is running successfully'})

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        print(f"Upload request received. Files: {request.files}")
        
        if 'files[]' not in request.files:
            print("No files[] in request")
            return jsonify({'error': 'No files selected'}), 400
        
        files = request.files.getlist('files[]')
        print(f"Number of files: {len(files)}")
        
        if not files or files[0].filename == '':
            print("No valid files found")
            return jsonify({'error': 'No files selected'}), 400
        
        uploaded_files = []
        for i, file in enumerate(files):
            print(f"Processing file {i+1}: {file.filename}")
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                print(f"Saving to: {filepath}")
                
                # Ensure upload folder exists
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                file.save(filepath)
                uploaded_files.append(filepath)
                print(f"Successfully saved: {filepath}")
            else:
                print(f"File {file.filename} not allowed or invalid")
        
        print(f"Total uploaded: {len(uploaded_files)}")
        return jsonify({
            'message': f'{len(uploaded_files)} files uploaded successfully',
            'files': uploaded_files
        })
        
    except Exception as e:
        print(f"Upload error: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/process', methods=['POST'])
def process_images():
    data = request.get_json()
    image_paths = data.get('image_paths', [])
    
    if not image_paths:
        return jsonify({'error': 'No images to process'}), 400
    
    results = []
    total = len(image_paths)
    
    for i, image_path in enumerate(image_paths):
        try:
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
                
                results.append({
                    'input': image_path,
                    'output': output_path if success else None,
                    'success': success,
                    'message': crop_message or message,
                    'crop_coords': crop_coords if success else None
                })
            else:
                results.append({
                    'input': image_path,
                    'output': None,
                    'success': False,
                    'message': message,
                    'crop_coords': None
                })
                
        except Exception as e:
            results.append({
                'input': image_path,
                'output': None,
                'success': False,
                'message': str(e),
                'crop_coords': None
            })
    
    return jsonify({
        'total_processed': len(results),
        'results': results
    })

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

@app.route('/status')
def status():
    upload_count = len(os.listdir(app.config['UPLOAD_FOLDER']))
    output_count = len(os.listdir(app.config['OUTPUT_FOLDER']))
    
    return jsonify({
        'uploaded_files': upload_count,
        'cropped_images': output_count
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
