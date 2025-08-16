# 🤖 AI Bulk Image Cropper - ID Card Style

A powerful web application that automatically crops thousands of images for ID card style format using AI. The application detects faces and automatically crops images to include the face and tie knot area, perfect for professional ID cards.

## ✨ Features

- **AI-Powered Cropping**: Uses MediaPipe (Google's latest face detection model) to automatically detect faces
- **Bulk Processing**: Handle 2000+ images at once
- **ID Card Style**: Automatically crops to include face + tie knot area
- **Modern Web Interface**: Beautiful, responsive design with drag & drop
- **Multiple Formats**: Supports JPG, PNG, GIF, BMP, TIFF
- **Real-time Progress**: See processing status and results
- **Download Ready**: Get all cropped images ready for use

## 🚀 Quick Start

### Prerequisites

- **Windows 10/11** (tested on Windows 10)
- **Python 3.8 or higher** ([Download Python](https://python.org))
- **Internet connection** (for first-time package installation)

### Installation & Setup

1. **Download the project** to your computer
2. **Double-click `run_app.bat`** - this will:
   - Check if Python is installed
   - Install all required packages automatically
   - Test the setup
   - Create necessary folders
   - Start the web application

3. **Open your browser** and go to: `http://localhost:5000`

### Manual Setup (Alternative)

If you prefer to set up manually:

```bash
# Install Python packages
pip install -r requirements.txt

# Test setup
python test_setup.py

# Run the application
python app.py
```

## 📖 How to Use

### Step 1: Upload Images
- Drag & drop multiple images onto the upload area
- Or click "Choose Images" to select files
- Supports: JPG, PNG, GIF, BMP, TIFF (max 16MB per file)

### Step 2: Start Processing
- Click "🚀 Start AI Cropping Process"
- The AI will automatically:
  - Detect faces in each image using MediaPipe
  - Calculate the optimal crop area (face + tie knot)
  - Process all images in sequence

### Step 3: Download Results
- View processing results and statistics
- Download individual cropped images
- All cropped images are saved in the `cropped_images` folder

## 🔧 Technical Details

### AI Technology Used
- **MediaPipe Face Detection**: Google's latest and most advanced face detection model
- **OpenCV**: Latest version for image processing and manipulation
- **PIL (Pillow)**: Latest version for image handling and format support
- **Flask 3.0**: Latest web framework for the interface

### Crop Algorithm
1. **Face Detection**: Locates the primary face in the image using MediaPipe
2. **Area Expansion**: Expands the crop area to include:
   - Face (100% of detected face area)
   - Upper chest area (for tie knot visibility)
   - Shoulder area (for professional appearance)
3. **Boundary Checking**: Ensures crop area stays within image bounds
4. **Fallback**: If no face detected, uses center crop with minimum dimensions

### Performance
- **Processing Speed**: ~1-3 seconds per image (depending on image size)
- **Memory Usage**: Optimized for large batch processing
- **Scalability**: Can handle 2000+ images efficiently
- **Accuracy**: Improved with latest MediaPipe models

## 📁 Project Structure

```
bulk/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies (latest versions)
├── run_app.bat          # Windows setup & run script
├── test_setup.py        # Dependency verification script
├── README.md            # This file
├── config.py            # Configuration settings
├── templates/
│   └── index.html      # Web interface
├── uploads/            # Temporary uploaded images
└── cropped_images/     # Output cropped images
```

## 🛠️ Troubleshooting

### Common Issues

**"Python is not installed"**
- Download and install Python from [python.org](https://python.org)
- Make sure to check "Add Python to PATH" during installation

**"Failed to install packages"**
- Try running `run_app.bat` as Administrator
- Install Visual Studio Build Tools if needed
- Check your internet connection
- Try installing packages individually: `pip install Flask opencv-python numpy Pillow mediapipe Werkzeug python-dotenv`

**"Application won't start"**
- Make sure no other application is using port 5000
- Check if Python is properly installed
- Try running `python app.py` manually
- Run `python test_setup.py` to verify dependencies

**"Face detection not working"**
- Ensure images contain clear, front-facing faces
- Check image quality and lighting
- Some images may use fallback center crop
- MediaPipe works best with good lighting and clear faces

### Performance Tips

- **Image Size**: Smaller images process faster
- **Batch Size**: Process images in batches of 100-500 for optimal performance
- **System Resources**: Close other applications for better performance
- **Storage**: Ensure sufficient disk space for uploaded and processed images

## 🔒 Security & Privacy

- **Local Processing**: All images are processed locally on your computer
- **No Upload**: Images are not sent to external servers
- **Temporary Storage**: Uploaded images are stored temporarily
- **Automatic Cleanup**: Processed images are saved to output folder

## 📊 System Requirements

- **OS**: Windows 10/11 (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for application + image storage
- **Python**: 3.8 or higher
- **Browser**: Chrome, Firefox, Edge (modern browsers)

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Ensure all prerequisites are met
3. Try running as Administrator
4. Run `python test_setup.py` to check dependencies
5. Check Windows Event Viewer for error logs

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

---

**Made with ❤️ for efficient bulk image processing using latest AI technology**
