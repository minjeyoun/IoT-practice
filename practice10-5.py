from picamera2 import Picamera2
import cv2
import numpy as np

# Load the cascade for face detection
cascade_filename = 'haarcascade_frontalface_alt.xml'
cascade = cv2.CascadeClassifier(cascade_filename)

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

age_net = cv2.dnn.readNetFromCaffe('deploy_age.prototxt', 'age_net.caffemodel')
gender_net = cv2.dnn.readNetFromCaffe('deploy_gender.prototxt', 'gender_net.caffemodel')

age_list = ['(0 ~ 2)', '(4 ~ 6)', '(8 ~ 12)', '(15 ~ 20)', '(25 ~ 32)', '(38 ~ 43)', '(48 ~ 53)', '(60 ~ 100)']
gender_list = ['Male', 'Female']

def main():
    picam2 = Picamera2()  # Initialize picamera2
    config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    while True:
        img = picam2.capture_array()  # Capture image as a NumPy array
        
        if img is None:
            print("Failed to capture image.")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        results = cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20)
        )

        for box in results:
            x, y, w, h = box
            face = img[y:y+h, x:x+w].copy()
            blob = cv2.dnn.blobFromImage(face, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = gender_list[gender_preds[0].argmax()]

            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = age_list[age_preds[0].argmax()]

            label = f"{gender}, {age}"
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(img, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Display the result (uncomment if display works)
        cv2.imshow('Face Detection', img)

        # Optional: Save the frame to check if display error persists
        # cv2.imwrite("output.png", img)

        if cv2.waitKey(10) & 0xFF == ord('q'):  # Adjusted delay to 10ms
            break

    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
