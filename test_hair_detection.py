import cv2
import numpy as np
import os

def test_hair_detection():
    image_path = "uploads/DSC_6555.JPG"
    
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        print("Could not read image")
        return
    
    h, w, _ = image.shape
    print(f"Image dimensions: {w} x {h}")
    
    # Convert to grayscale for better edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Use Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)
    
    # Scan from top to bottom to find the first significant edge content
    hair_start_y = 0
    for scan_y in range(0, min(h//3, 300)):  # Scan top 33% or 300px
        # Get a horizontal slice of the edge image
        slice_edges = edges[scan_y:scan_y+1, :]
        
        # Count non-zero pixels (edges) in this slice
        edge_count = np.count_nonzero(slice_edges)
        
        print(f"Scan y={scan_y}: edge_count={edge_count}, threshold={w * 0.1}")
        
        # If we find significant edges (likely hair/head boundary), mark this position
        if edge_count > w * 0.1:  # If more than 10% of width has edges
            hair_start_y = scan_y
            print(f"Found hair start at y={hair_start_y}")
            break
    
    # Add 0.5cm above the detected hair start point
    # Assuming standard DPI, 0.5cm ≈ 19 pixels
    extra_space = 19
    start_y = max(0, hair_start_y - extra_space)
    
    print(f"Final crop start_y: {start_y}")
    
    # Save the edge detection result for visualization
    cv2.imwrite("edges_debug.jpg", edges)
    print("Saved edge detection result to edges_debug.jpg")

if __name__ == "__main__":
    test_hair_detection()
