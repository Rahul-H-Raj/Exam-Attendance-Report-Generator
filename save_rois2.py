# image_region_selector.py

import cv2
import numpy as np
import pandas as pd
import os
import ast

# Global variables
vertices = []  # List to store selected vertices
drawing = False  # Flag to track drawing mode
image_id = 20  # ID for the image
saved_regions = []  # List to store saved regions
img = None  # Image variable

# Function to safely parse vertices strings
def safe_literal_eval(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return val

# Function to draw a quadrilateral
def draw_quadrilateral(event, x, y, flags, param):
    global vertices, drawing, image_id, saved_regions, img

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

def load_existing_regions(csv_file):
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file, header=None, names=['ID', 'Vertices'], skiprows=1)
        df['Vertices'] = df['Vertices'].apply(safe_literal_eval)
    else:
        df = pd.DataFrame(columns=['ID', 'Vertices'])
    return df

def save_regions_to_csv(df, csv_file):
    df.drop_duplicates(subset=['ID'], keep='last', inplace=True)
    df.to_csv(csv_file, mode='w', header=['ID', 'Vertices'], index=False)

def main(image_path, csv_file='regions.csv'):
    global img, image_id, saved_regions

    # Load existing regions from CSV
    df = load_existing_regions(csv_file)

    # Load image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load image at path: {image_path}")
        return

    # Create a window and bind the mouse callback function
    cv2.imshow('Image', img)
    cv2.setMouseCallback('Image', draw_quadrilateral)

    # Wait for the user to select regions and save them
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            for img_id, verts in saved_regions:
                verts_str = str(verts)
                if not df[df['ID'] == img_id].empty:
                    df.loc[df['ID'] == img_id, 'Vertices'] = verts_str
                else:
                    df = pd.concat([df, pd.DataFrame([(img_id, verts_str)], columns=['ID', 'Vertices'])], ignore_index=True)
            save_regions_to_csv(df, csv_file)
            print("Updated region coordinates saved to regions.csv")
            saved_regions.clear()
        elif key == 27:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main('frame_1.jpg')
