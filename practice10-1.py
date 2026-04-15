import cv2
import subprocess
import numpy as np

# Initialize CascadeClassifier for face and eye detection
face_cascade = cv2.CascadeClassifier("/home/tommy/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("/home/tommy/opencv/data/haarcascades/haarcascade_eye.xml")

try:
    while True:
        # Capture an image using libcamera-still and save it to a temporary file
        command = "libcamera-still -o /tmp/capture.jpg --width 640 --height 480 -n"
        subprocess.run(command, shell=True)

        # Load the captured image with OpenCV
        img = cv2.imread('/tmp/capture.jpg')
        if img is None:
            print("Failed to load image.")
            break

        # Convert to grayscale for face and eye detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        print("Number of faces detected:", len(faces))

        # Draw rectangles around detected faces and eyes
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)

        # Display the result frame
        cv2.imshow('Face and Eye Detection', img)

        # Press 'Esc' to exit
        if cv2.waitKey(30) & 0xFF == 27:
            break
finally:
    cv2.destroyAllWindows()
