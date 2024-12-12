import cv2

# Load the cascade
face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load the trained recognizer
rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("recognizer\\trainingData.yml")

# Define the font
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

# Read the image
img = cv2.imread('Image dataset/IMG_20240325_133933.jpg')
img = cv2.resize(img,(256,256))

# Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = face_detect.detectMultiScale(gray, 1.3, 5)

# Process each face
for (x, y, w, h) in faces:
    # Draw rectangle around the face
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Predict the face
    ide, conf = rec.predict(gray[y:y + h, x:x + w])
    
    # Define names for recognized IDs
    names = {1: "one", 2: "two", 3: "three"}
    
    # Identify the face
    if conf < 60:
        name = names.get(ide, "Unknown")
    else:
        name = "Unknown"
    
    # Put text on the image
    cv2.putText(img, str(name), (x, y - 10), font, 1, (255, 255, 255), 1)

# Display the output
cv2.imshow('Face Recognition', img)
cv2.waitKey(0)
cv2.destroyAllWindows()