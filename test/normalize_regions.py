import cv2
import numpy as np
import pandas as pd
import ast

# Function to extract and save regions
def extract_and_save_regions(image, saved_regions):
    roi_data = []
    for region in saved_regions:
        region_id = region[0]
        vertices = ast.literal_eval(region[1])  # Convert string representation to tuple
        # Convert vertices to numpy array
        pts = np.array(vertices, dtype=np.int32)
        # Extract region from the image
        x, y, w, h = cv2.boundingRect(pts)
        region_img = image[y:y+h, x:x+w]
        # Save the region as a new image file inside the "benches" folder
        cv2.imwrite(f'benches/place_{region_id}.jpg', region_img)

        # Store bounding rectangle coordinates and region ID
        roi_data.append([region_id, x, y, w, h])
    
    # Convert the ROI data to a DataFrame
    roi_df = pd.DataFrame(roi_data, columns=['region_id', 'x', 'y', 'width', 'height'])
    # Save DataFrame to CSV
    roi_df.to_csv('roi.csv', index=False)

# Load image
img = cv2.imread('i5.jpg')

# Load saved regions from CSV
df = pd.read_csv('regions.csv')

# Extract and save regions
extract_and_save_regions(img, df.values)
