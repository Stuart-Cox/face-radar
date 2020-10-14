import cv2
import time
from camera_recognition import CameraRecog

# Create new instance of Camera controller class
camera_recog = CameraRecog()

while True:

    # Slow loop down
    time.sleep(0.5)

    # Read the frame
    frame = camera_recog.get_next_frame()

    # Find faces in the frame
    faces = camera_recog.get_faces_from_frame(frame)

    # Draw square around faces & calulate distance & position in frame
    face_locations = camera_recog.detect_faces(faces, frame)

    # Make put request to RESTful API
    camera_recog.send_request_of_faces(face_locations)

    # Draw Window that shows face detection
    camera_recog.draw_window(frame)

    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release the VideoCapture object
camera_recog.end_stream()
