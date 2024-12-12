import cv2
import numpy as np
import pandas as pd

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
            saved_regions.append((image_id, vertices))  # Save region with ID
            vertices = []  # Clear vertices for next region
            image_id += 1  # Increment ID for the next region

# Load image
img = cv2.imread('5.jpg')
vertices = []  # List to store selected vertices
drawing = False  # Flag to track drawing mode
image_id = 9  # ID for the image
saved_regions = []  # List to store saved regions

# Create a window and bind the mouse callback function
cv2.imshow('Image', img)
cv2.setMouseCallback('Image', draw_quadrilateral)

# Wait for the user to select regions and save them
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        # Save the regions to a CSV file
        df = pd.DataFrame(saved_regions, columns=['ID', 'Vertices'])
        df.to_csv('regions.csv', mode='a', header=False, index=False)  # Append to existing CSV file
        print("Regions appended to regions.csv")
    elif key == ord('q'):
        break

cv2.destroyAllWindows()
