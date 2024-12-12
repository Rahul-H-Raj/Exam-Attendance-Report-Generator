import cv2
import os
import numpy as np

# Function to apply random augmentation
def augment_image(image, output_folder, filename_prefix, num_images):
    for i in range(num_images):
        # Apply random augmentation
        augmented_image = image.copy()

        # Randomly scale the image (0.8 to 1.2 scale factor)
        scale_factor = np.random.uniform(0.8, 1.2)
        augmented_image = cv2.resize(augmented_image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

        # Randomly shift the image horizontally and vertically (up to 10 pixels)
        tx = np.random.randint(-10, 10)
        ty = np.random.randint(-10, 10)
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        augmented_image = cv2.warpAffine(augmented_image, M, (augmented_image.shape[1], augmented_image.shape[0]))

        # Randomly adjust brightness and contrast
        alpha = np.random.uniform(0.8, 1.2)
        beta = np.random.randint(-20, 20)
        augmented_image = cv2.convertScaleAbs(augmented_image, alpha=alpha, beta=beta)

        # Save the augmented image
        output_path = os.path.join(output_folder, f'{filename_prefix}_{i}.jpg')
        cv2.imwrite(output_path, augmented_image)

# Iterate over each face
for i in range(1, 13):  # Assuming you have face_1.jpg, face_2.jpg, face_3.jpg, and face_4.jpg
    # Load the face image
    place_path = f'CLassrooms/A 201/benches/place_{i}.jpg'
    face = cv2.imread(place_path)

    # Augment the face and save to appropriate folders
    output_folder = f'CLassrooms/A 201/dataset'
    augment_image(face, output_folder, f'bench_{i}', 100)
