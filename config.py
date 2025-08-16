# Configuration file for AI Bulk Image Cropper

# Flask Application Settings
FLASK_HOST = '0.0.0.0'  # Host to bind to (0.0.0.0 for all interfaces)
FLASK_PORT = 5000        # Port to run the application on
FLASK_DEBUG = True       # Debug mode (set to False for production)

# File Upload Settings
MAX_FILE_SIZE = 16 * 1024 * 1024  # Maximum file size in bytes (16MB)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# AI Processing Settings
FACE_DETECTION_CONFIDENCE = 0.5    # Minimum confidence for face detection
CROP_EXPANSION_HEIGHT = 2.5        # Height multiplier for crop area (includes tie area)
CROP_EXPANSION_WIDTH = 1.8         # Width multiplier for crop area (includes shoulders)
MIN_CROP_WIDTH = 200               # Minimum crop width in pixels
MIN_CROP_HEIGHT = 250              # Minimum crop height in pixels

# Folder Settings
UPLOAD_FOLDER = 'uploads'          # Folder for uploaded images
OUTPUT_FOLDER = 'cropped_images'   # Folder for processed images

# Performance Settings
BATCH_SIZE = 100                   # Process images in batches of this size
PROCESSING_DELAY = 0.1             # Delay between processing images (seconds)

# Output Settings
OUTPUT_PREFIX = '_cropped'         # Prefix for cropped image filenames
PRESERVE_ORIGINAL_FORMAT = True    # Keep original image format
OUTPUT_QUALITY = 95                # JPEG quality (if converting to JPEG)

