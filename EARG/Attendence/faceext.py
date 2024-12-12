import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

image = cv2.imread('Image dataset/IMG_20240325_133933.jpg')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

for i, (x, y, w, h) in enumerate(faces):

    face = image[y:y+h, x:x+w]


    cv2.imwrite(f'faces/face_{i}.jpg', face)

    cv2.imshow(f'Face {i}', face)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
