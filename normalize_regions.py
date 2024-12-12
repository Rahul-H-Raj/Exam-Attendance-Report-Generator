import cv2
import numpy as np
import pandas as pd
import ast
import os

# Function to extract and save regions
def extract_and_save_regions(image, csv_file):
    # Load saved regions from CSV
    df = pd.read_csv(csv_file)
    roi_data = []
    for region in df.values:
        region_id = region[0]
        vertices = ast.literal_eval(region[1])  # Convert string representation to tuple
        # Convert vertices to numpy array
        pts = np.array(vertices, dtype=np.int32)
        # Extract region from the image
        x, y, w, h = cv2.boundingRect(pts)
        region_img = image[y:y+h, x:x+w]# Define the directory path
        directory_path = f'Classrooms/A 201/benches'
        
        # Ensure the directory exists
        os.makedirs(directory_path, exist_ok=True)
        
        # Define the full file path
        file_path = os.path.join(directory_path, f'place_{region_id}.jpg')
        
        # Save the region image
        cv2.imwrite(file_path, region_img)
        print(f"Saved region image to {file_path}")

        # Store bounding rectangle coordinates and region ID
        roi_data.append([region_id, x, y, w, h])
    
    # Convert the ROI data to a DataFrame
    roi_df = pd.DataFrame(roi_data, columns=['region_id', 'x', 'y', 'width', 'height'])
    # Save DataFrame to CSV
    roi_df.to_csv('roi.csv', index=False)
