import cv2
import time


# convert square size to distane from camera in meters (rounded to 0.5 meters)
def width_to_distance(width):
    # 0.5 meters = 280 pixels
    # 1.0 meters = 140 pixels
    # 1.5 meters = 93.333... pixels

    # equation to convert pixels to meters (roughly)
    raw_meters = 140 / width
    base = 0.5
    rounded_meters = base * round(raw_meters / base)
    # print("{} - {} - {}".format(width, raw_meters, rounded_meters))
    return "{} meters".format(rounded_meters)


# Load the cascade
face_cascade = cv2.CascadeClassifier(
    'config/haarcascade_frontalface_default.xml'
)

# To capture video from webcam.
video_stream = cv2.VideoCapture(0)
while True:
    # Slow loop down
    time.sleep(0.2)

    # Read the frame
    _, frame = video_stream.read()

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        print(x)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(
            frame,
            width_to_distance(w),
            (x, y),
            cv2.FONT_HERSHEY_SIMPLEX, 1, 255)
    # show frames
    cv2.imshow('Facial Recog', frame)
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
# Release the VideoCapture object
video_stream.release()
