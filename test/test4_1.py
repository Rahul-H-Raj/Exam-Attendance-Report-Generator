import cv2
import numpy as np
import pandas as pd
import os
import ast

# Function to safely parse vertices strings
def safe_literal_eval(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return val

# Function to draw a quadrilateral
def draw_quadrilateral(event, x, y, flags, param):
    global vertices, drawing, image_id, saved_regions

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(vertices) < 4:
            vertices.append((x, y))
            drawing = True
        else:
            vertices.clear()  # Clear vertices if already 4 points selected

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing and len(vertices) < 4:
            temp_img = img.copy()
            for i in range(len(vertices)):
                cv2.circle(temp_img, vertices[i], 3, (0, 255, 0), -1)
            cv2.imshow('Image', temp_img)

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing and len(vertices) == 4:
            drawing = False
            cv2.line(img, vertices[-1], vertices[0], (0, 255, 0), 2)  # Connect last point to first
            for i in range(3):
                cv2.line(img, vertices[i], vertices[i+1], (0, 255, 0), 2)  # Connect rest of the points
            cv2.imshow('Image', img)
            saved_regions.append((image_id, vertices.copy()))  # Save region with ID
            vertices = []  # Clear vertices for next region
            image_id += 1  # Increment ID for the next region

# Load existing regions from CSV
csv_file = 'regions.csv'
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file, header=None, names=['ID', 'Vertices'], skiprows=1)
    # Convert the Vertices column from string representation to list of tuples using safe_literal_eval
    df['Vertices'] = df['Vertices'].apply(safe_literal_eval)
else:
    df = pd.DataFrame(columns=['ID', 'Vertices'])

# Load image
img = cv2.imread('5.jpg')
vertices = []  # List to store selected vertices
drawing = False  # Flag to track drawing mode
image_id = 13  # ID for the image
saved_regions = []  # List to store saved regions

# Create a window and bind the mouse callback function
cv2.imshow('Image', img)
cv2.setMouseCallback('Image', draw_quadrilateral)

# Wait for the user to select regions and save them
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        # Update the DataFrame with new or modified regions
        for img_id, verts in saved_regions:
            # Convert vertices to string format for storage
            verts_str = str(verts)
            if not df[df['ID'] == img_id].empty:
                # Update existing entry
                df.loc[df['ID'] == img_id, 'Vertices'] = verts_str
            else:
                # Add new entry
                df = pd.concat([df, pd.DataFrame([(img_id, verts_str)], columns=['ID', 'Vertices'])], ignore_index=True)
        
        # Remove duplicate IDs, keeping the last occurrence
        df.drop_duplicates(subset=['ID'], keep='last', inplace=True)

        # Save the DataFrame to CSV with proper header
        df.to_csv(csv_file, mode='w', header=['ID', 'Vertices'], index=False)

        print("Updated region coordinates saved to regions.csv")
        
        # Clear the saved regions after saving
        saved_regions.clear()
    elif key == 27:
        break

cv2.destroyAllWindows()
