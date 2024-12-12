import cv2
import pandas as pd

def draw_saved_regions(image, saved_regions):
    for region in saved_regions:
        x, y, width, height = region[1:]
        x, y, width, height = int(x), int(y), int(width), int(height)
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)  # Draw rectangle
        cv2.putText(image, f"ID: {region[0]}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)  # Add text with region ID

def display_image_with_regions(image_path, csv_path):
    img = cv2.imread(image_path)
    df = pd.read_csv(csv_path)

    while True:
        draw_img = img.copy()  # Create a copy of the original image to draw regions on
        draw_saved_regions(draw_img, df.values)  # Draw saved regions
        cv2.imshow('Image with Regions', draw_img)
        key = cv2.waitKey(0)
        if key == 27:  # Press Esc to exit
            break

    cv2.destroyAllWindows()
