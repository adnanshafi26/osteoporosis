import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from image_analysis.xray_predict import analyze_xray

def test_inference():
    # Find a test image
    test_dir = "BoneFractureDataset/testing/fractured"
    images = [f for f in os.listdir(test_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]
    
    if not images:
        print("No test images found.")
        return
        
    test_image = os.path.join(test_dir, images[0])
    print(f"Testing inference on: {test_image}")
    
    try:
        # Move to backend to ensure paths are correct
        os.chdir("backend")
        result = analyze_xray(os.path.join("..", test_image))
        print("\nAnalysis Result:")
        for k, v in result.items():
            print(f"{k}: {v}")
    except Exception as e:
        print(f"Inference failed: {e}")

if __name__ == "__main__":
    test_inference()
