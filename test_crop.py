import requests
import json
import os

# Test the cropping functionality
def test_cropping():
    # First upload a test image
    test_image_path = "uploads/DSC_6555.JPG"
    
    if not os.path.exists(test_image_path):
        print(f"Test image not found: {test_image_path}")
        return
    
    # Upload the image
    with open(test_image_path, 'rb') as f:
        files = {'files[]': (os.path.basename(test_image_path), f, 'image/jpeg')}
        response = requests.post('http://localhost:5000/upload', files=files)
    
    if response.status_code == 200:
        upload_result = response.json()
        print("Upload successful:", upload_result)
        
        # Now process the uploaded image
        image_paths = [test_image_path]
        process_data = {'image_paths': image_paths}
        
        process_response = requests.post('http://localhost:5000/process', 
                                       json=process_data,
                                       headers={'Content-Type': 'application/json'})
        
        if process_response.status_code == 200:
            process_result = process_response.json()
            print("Processing result:", json.dumps(process_result, indent=2))
            
            # Check if new cropped image was created
            if process_result['results'] and process_result['results'][0]['success']:
                output_path = process_result['results'][0]['output']
                print(f"New cropped image created: {output_path}")
                
                # Check file sizes
                original_size = os.path.getsize(test_image_path)
                cropped_size = os.path.getsize(output_path)
                print(f"Original size: {original_size} bytes")
                print(f"Cropped size: {cropped_size} bytes")
                print(f"Size ratio: {cropped_size/original_size:.2f}")
            else:
                print("Processing failed:", process_result['results'][0]['message'])
        else:
            print("Processing request failed:", process_response.status_code)
    else:
        print("Upload failed:", response.status_code)

if __name__ == "__main__":
    test_cropping()
