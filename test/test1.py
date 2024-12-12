import cv2
import csv

# Global variables to store selected ROIs and their IDs
rois = []
roi_id = 0
drawing = False

def draw_rectangle(event, x, y, flags, param):
    global roi_id, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        rois.append({'id': roi_id, 'top_left': (x, y)})
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rois[-1]['bottom_right'] = (x, y)
        roi_id += 1

def save_rois_to_csv(filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'top_left_x', 'top_left_y', 'bottom_right_x', 'bottom_right_y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for roi in rois:
            writer.writerow({
                'id': roi['id'],
                'top_left_x': roi['top_left'][0],
                'top_left_y': roi['top_left'][1],
                'bottom_right_x': roi['bottom_right'][0],
                'bottom_right_y': roi['bottom_right'][1]
            })

# Load the image
image = cv2.imread('5.jpg')

# Create a window and set the mouse callback function
cv2.namedWindow('Select ROI')
cv2.setMouseCallback('Select ROI', draw_rectangle)

# Main loop to interactively select and save ROIs
while True:
    # Copy the original image to avoid overwriting
    img_copy = image.copy()

    # Draw rectangles for selected ROIs
    for roi in rois:
        if 'bottom_right' in roi:
            cv2.rectangle(img_copy, roi['top_left'], roi['bottom_right'], (0, 255, 0), 2)

    # Display the image
    cv2.imshow('Select ROI', img_copy)

    # Check for key events
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Press 'q' to exit
        break
    elif key == ord('s'):  # Press 's' to save ROIs to CSV
        save_rois_to_csv('rois.csv')
        print("ROIs saved to 'rois.csv'.")

# Close all OpenCV windows
cv2.destroyAllWindows()
