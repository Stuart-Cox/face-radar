import cv2
from datetime import datetime
import requests


class CameraRecog():
    # Load the cascade
    face_cascade = cv2.CascadeClassifier(
        'config/haarcascade_frontalface_default.xml'
    )
    # To capture video from webcam.
    video_stream = cv2.VideoCapture(0)
    max_width = video_stream.get(cv2.CAP_PROP_FRAME_WIDTH)

    def width_to_distance(self, width):
        # 0.5 meters = 280 pixels
        # 1.0 meters = 140 pixels
        # 1.5 meters = 93.333... pixels

        # equation to convert pixels to meters (roughly)
        raw_meters = 140 / width
        base = 0.5
        rounded_meters = base * round(raw_meters / base)
        # print("{} - {} - {}".format(width, raw_meters, rounded_meters))
        return rounded_meters

    def get_next_frame(self):
        _, frame = self.video_stream.read()
        return frame

    def get_faces_from_frame(self, frame):
        # Convert to grayscale
        grey_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = self.face_cascade.detectMultiScale(grey_scale, 1.1, 4)
        return faces

    def detect_faces(self, faces, frame):
        face_locations = []

        for (x, y, w, h) in faces:
            face = {
                "distance": self.width_to_distance(w),
                "x_cord": (x + (w/2)) / self.max_width,
                'timestamp': datetime.timestamp(datetime.now()),
            }
            face_locations.append(face)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(
                frame,
                "{} meters".format(self.width_to_distance(w)),
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
        return face_locations

    def send_request_of_faces(self, face_locations):
        url = 'http://localhost:5000/current_faces'
        resp = requests.put(
            url,
            json={"json_data": {"seen_faces": face_locations}}
        )
        print("{} - {}".format(resp.status_code, resp.reason))
        print(resp.__dict__)

    def draw_window(self, frame):
        cv2.imshow('Facial Recog', frame)

    def end_stream(self):
        self.video_stream.release()
