import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import cv2

# Load the SSD MobileNet V2 model from TensorFlow Hub
detector = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")

# Load class labels for COCO dataset
LABELS_PATH = "/Users/farazsaeed/traffic_detection/models/coco.names"
with open(LABELS_PATH, 'r') as f:
    classes = [line.strip() for line in f.readlines()]


# Function to process frames for traffic detection
def detect_traffic(frame):
    # Convert frame to tensor
    input_tensor = tf.convert_to_tensor(frame)
    input_tensor = input_tensor[tf.newaxis, ...]

    # Perform detection
    detector_output = detector(input_tensor)

    # Extract detection information
    class_ids = detector_output["detection_classes"][0].numpy().astype(np.int32)
    scores = detector_output["detection_scores"][0].numpy()
    boxes = detector_output["detection_boxes"][0].numpy()

    height, width, _ = frame.shape

    # Iterate over detections and draw bounding boxes
    for i in range(len(scores)):
        if scores[i] > 0.5:  # Only consider detections with confidence > 0.5
            class_id = class_ids[i]
            if class_id in [2, 3, 5, 7]:  # Filter for vehicles (car, bus, truck, etc.)
                box = boxes[i] * np.array([height, width, height, width])
                (y_min, x_min, y_max, x_max) = box.astype(int)

                label = f"{classes[class_id]}: {scores[i]:.2f}"
                color = (0, 255, 0)  # Green color for boxes
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)
                cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame
