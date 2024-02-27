# app/app.py
from flask import render_template, request, Response
from app import app
import cv2
import base64

cap = cv2.VideoCapture(0)  # Accessing the default camera (back camera)

def gen_frames():
    while True:
        success, frame = cap.read()  # Read frames from camera
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    _, frame = cap.read()
    ret, buffer = cv2.imencode('.jpg', frame)
    img_str = base64.b64encode(buffer)
    return img_str

@app.route('/record')
def record():
    return "Recording feature is not implemented yet!"

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
