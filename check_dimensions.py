from PIL import Image
import os

def check_image_dimensions():
    # Check original image
    original_path = "uploads/DSC_6555.JPG"
    cropped_path = "cropped_images/DSC_6555_cropped.JPG"
    
    if os.path.exists(original_path):
        with Image.open(original_path) as img:
            print(f"Original image dimensions: {img.size[0]} x {img.size[1]}")
            print(f"Original aspect ratio: {img.size[0]/img.size[1]:.3f}")
    
    if os.path.exists(cropped_path):
        with Image.open(cropped_path) as img:
            print(f"Cropped image dimensions: {img.size[0]} x {img.size[1]}")
            print(f"Cropped aspect ratio: {img.size[0]/img.size[1]:.3f}")
            
            # Check if it matches our target ratio (1:1.285 = 0.778)
            target_ratio = 1.0 / 1.285
            actual_ratio = img.size[0] / img.size[1]
            print(f"Target ratio: {target_ratio:.3f}")
            print(f"Difference: {abs(actual_ratio - target_ratio):.3f}")
            
            if abs(actual_ratio - target_ratio) < 0.01:
                print("✅ Aspect ratio is correct!")
            else:
                print("❌ Aspect ratio is not correct")

if __name__ == "__main__":
    check_image_dimensions()
