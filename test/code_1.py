import cv2
import numpy as np
import pandas as pd

# Load saved LBPH model
lbph_model = cv2.face.LBPHFaceRecognizer_create()
lbph_model.read('Classrooms/A 201/detector/trainingData.yml')

# Function to predict on regions using LBPH model
def predict_on_regions(image, roi_df, lbph_model):
    predictions = []
    for index, row in roi_df.iterrows():
        x, y, w, h = row['x'], row['y'], row['width'], row['height']
        # Extract region from the image
        region_img = image[y:y+h, x:x+w]
        # Convert region image to grayscale
        gray_region = cv2.cvtColor(region_img, cv2.COLOR_BGR2GRAY)
        # Make prediction using LBPH model
        label, confidence = lbph_model.predict(gray_region)
        predictions.append((label, confidence))
    return predictions

# Load input image
img = cv2.imread('frame_1.jpg')

# Load ROIs coordinates from roi.csv
roi_df = pd.read_csv('roi.csv')

# Predict on regions
region_predictions = predict_on_regions(img, roi_df, lbph_model)

# Print predictions
for idx, (label, confidence) in enumerate(region_predictions):
    print(f"Region {idx+1}: Predicted Label: {label}, Confidence: {confidence}")
