import cv2
from flask import Flask, render_template, Response
import sys
import os

# Add the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import traffic_detection  # Import the detection function

app = Flask(__name__)

# Replace with your phone's IP and port from the IP Webcam app
video_capture = cv2.VideoCapture("http://10.131.4.205:8080/video")  # Example IP

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # Process the frame for traffic detection
            frame = traffic_detection.detect_traffic(frame)

            # Encode the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Use the yield statement to return a response in a streaming fashion
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
