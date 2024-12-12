import os
import cv2
import numpy as np
from PIL import Image

def get_images_with_id(path):
    """
    Function to get images and their IDs from the given directory path.
    """
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    benches = []
    IDs = []

    for image_path in image_paths:
        try:
            bench_img = Image.open(image_path).convert('L')  # Convert image to grayscale
            bench_np = np.array(bench_img, 'uint8')
            ID = int(os.path.split(image_path)[-1].split('_')[1])
            benches.append(bench_np)
            IDs.append(ID)
            cv2.imshow("Training", bench_np)
            cv2.waitKey(10)
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")

    return np.array(IDs), benches

def train(path):
    """
    Function to train the LBPH face recognizer with images from the given directory path.
    """
    # Create the LBPH face recognizer
    detector = cv2.face.LBPHFaceRecognizer_create()

    # Get images and IDs
    Ids, benches = get_images_with_id(path)

    # Train the recognizer
    detector.train(benches, Ids)

    # Save the trained model
    save_path = os.path.join(os.path.dirname(path), 'detector', 'trainingData1.yml')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    detector.save(save_path)

    # Close all OpenCV windows
    cv2.destroyAllWindows()
    print(f"Training data saved to {save_path}")

