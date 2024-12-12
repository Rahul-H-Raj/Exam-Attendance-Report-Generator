import cv2
import pandas as pd

# Function to draw saved regions from CSV
def draw_saved_regions(image, saved_regions):
    for region in saved_regions:
        vertices = eval(region[1])  # Convert string representation to tuple
        for i in range(4):
            cv2.line(image, vertices[i], vertices[(i+1)%4], (0, 255, 0), 2)  # Draw lines between vertices
        cv2.putText(image, f"ID: {region[0]}", vertices[0], cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)  # Add text with region ID

# Load image
img = cv2.imread('5.jpg')

# Load saved regions from CSV
df = pd.read_csv('regions.csv')

# Create a window and display the image with saved regions
while True:
    draw_img = img.copy()  # Create a copy of the original image to draw regions on
    draw_saved_regions(draw_img, df.values)  # Draw saved regions
    cv2.imshow('Image with Regions', draw_img)
    key = cv2.waitKey(0)
    if key == 27:  # Press Esc to exit
        break

cv2.destroyAllWindows()
