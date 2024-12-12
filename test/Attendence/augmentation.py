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

# Create folders to save the augmented images
os.makedirs('augmented_face_1', exist_ok=True)
os.makedirs('augmented_face_2', exist_ok=True)
os.makedirs('augmented_face_3', exist_ok=True)
os.makedirs('augmented_face_4', exist_ok=True)

# Iterate over each face
for i in range(1, 5):  # Assuming you have face_1.jpg, face_2.jpg, face_3.jpg, and face_4.jpg
    # Load the face image
    face_path = f'faces/face_{i}.jpg'
    face = cv2.imread(face_path)

    # Augment the face and save to appropriate folders
    output_folder = f'augmented_face_{i}'
    augment_image(face, output_folder, f'face_{i}', 30)
