#!/usr/bin/env python3
"""
Test script to verify all dependencies are properly installed
Run this before using the main application
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        if package_name:
            importlib.import_module(module_name)
            print(f"✅ {package_name} imported successfully")
            return True
        else:
            importlib.import_module(module_name)
            print(f"✅ {module_name} imported successfully")
            return True
    except ImportError as e:
        print(f"❌ Failed to import {package_name or module_name}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {package_name or module_name} imported but with warning: {e}")
        return True

def main():
    print("=" * 50)
    print("AI Bulk Image Cropper - Dependency Test")
    print("=" * 50)
    print()
    
    # Test Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    else:
        print("✅ Python version is compatible")
    
    print()
    print("Testing required packages...")
    print()
    
    # Test all required packages (updated list)
    packages = [
        ("flask", "Flask"),
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("PIL", "Pillow"),
        ("mediapipe", "MediaPipe"),
        ("werkzeug", "Werkzeug"),
        ("dotenv", "python-dotenv")
    ]
    
    all_passed = True
    for module, name in packages:
        if not test_import(module, name):
            all_passed = False
    
    print()
    print("=" * 50)
    
    if all_passed:
        print("🎉 All dependencies are properly installed!")
        print("You can now run the application using:")
        print("   - Double-click 'run_app.bat' (Windows)")
        print("   - Or run 'python app.py' manually")
        print()
        print("The web interface will be available at: http://localhost:5000")
        return True
    else:
        print("❌ Some dependencies failed to import.")
        print("Please run 'pip install -r requirements.txt' again")
        print("Or try running as Administrator if on Windows")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
