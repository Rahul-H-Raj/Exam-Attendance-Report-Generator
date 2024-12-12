from flask import Flask, render_template, request, jsonify
import cv2
import os
import time

app = Flask(__name__)

# Path to your video file
VIDEO_PATH = 'During-Exam.mp4'
# Folder to save extracted frames
FRAMES_FOLDER = 'static'

# Ensure the folder exists
os.makedirs(FRAMES_FOLDER, exist_ok=True)

# Function to extract frames from the video at regular intervals
def extract_frames(interval_sec):
    cap = cv2.VideoCapture(VIDEO_PATH)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    interval_frames = int(interval_sec * frame_rate)
    current_frame = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if current_frame % interval_frames == 0:
            # Save the frame as an image
            image_path = os.path.join(FRAMES_FOLDER, f'frame_{current_frame // interval_frames}.jpg')
            cv2.imwrite(image_path, frame)
            yield image_path, time.strftime('%Y-%m-%d %H:%M:%S'), current_frame // interval_frames

        current_frame += 1

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract_frames', methods=['POST'])
def extract_frames_route():
    interval_sec = int(request.form.get('interval'))
    extracted_frames = []

    for image_path, extraction_time, index in extract_frames(interval_sec):
        extracted_frames.append({'image_path': image_path, 'extraction_time': extraction_time, 'index': index})

    return jsonify(extracted_frames)

if __name__ == '__main__':
    app.run(debug=True)
