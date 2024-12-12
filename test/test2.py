import cv2
import csv

def load_rois_from_csv(filename):
    rois = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            roi = {
                'id': int(row['id']),
                'top_left': (int(row['top_left_x']), int(row['top_left_y'])),
                'bottom_right': (int(row['bottom_right_x']), int(row['bottom_right_y']))
            }
            rois.append(roi)
    return rois

def display_rois_on_image(image, rois):
    img_copy = image.copy()
    for roi in rois:
        cv2.rectangle(img_copy, roi['top_left'], roi['bottom_right'], (0, 255, 0), 2)
        cv2.putText(img_copy, str(roi['id']), roi['top_left'], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Image with ROIs', img_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Load the image
image = cv2.imread('5.jpg')

# Load ROIs from CSV
rois = load_rois_from_csv('rois.csv')

# Display the ROIs on the image
display_rois_on_image(image, rois)
