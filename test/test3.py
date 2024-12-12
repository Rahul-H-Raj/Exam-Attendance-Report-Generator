import cv2
import numpy as np

# Function to draw a quadrilateral
def draw_quadrilateral(event, x, y, flags, param):
    global vertices, drawing

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

# Load image
img = cv2.imread('5.jpg')
vertices = []  # List to store selected vertices
drawing = False  # Flag to track drawing mode

# Create a window and bind the mouse callback function
cv2.imshow('Image', img)
cv2.setMouseCallback('Image', draw_quadrilateral)

# Wait for the user to select 4 points and draw the quadrilateral
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
