#!/usr/bin/env python3
"""
Simple test script to verify MediaPipe imports work
"""

try:
    import mediapipe as mp
    print("✅ MediaPipe imported successfully")
    
    # Test face detection import
    mp_face_detection = mp.solutions.face_detection
    print("✅ Face detection module imported successfully")
    
    # Test if we can create a face detection instance
    face_detection = mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5)
    print("✅ Face detection instance created successfully")
    
    print("\n🎉 All MediaPipe tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying to fix...")
    
    # Try to install the latest available version
    import subprocess
    import sys
    
    try:
        print("Installing latest MediaPipe version...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mediapipe==0.10.21", "--force-reinstall"])
        print("✅ MediaPipe reinstalled successfully")
        
        # Test again
        import mediapipe as mp
        mp_face_detection = mp.solutions.face_detection
        print("✅ MediaPipe now works correctly!")
        
    except Exception as e2:
        print(f"❌ Failed to fix: {e2}")
        print("\nPlease run: pip install mediapipe==0.10.21 --force-reinstall")
