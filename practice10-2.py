import cv2
import numpy as np
from picamera2 import Picamera2

threshold_move = 50  # Threshold for pixel value difference
diff_compare = 10    # Threshold for the number of different pixels

# Initialize picamera2 for frame capturing
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

# Capture the first two frames for motion detection
img_first = picam2.capture_array()
img_second = picam2.capture_array()

while True:
    img_third = picam2.capture_array()  # Capture the third frame
    scr = img_third.copy()  # Create a copy for drawing motion indicators

    # Convert frames to grayscale
    img_first_gray = cv2.cvtColor(img_first, cv2.COLOR_BGR2GRAY)
    img_second_gray = cv2.cvtColor(img_second, cv2.COLOR_BGR2GRAY)
    img_third_gray = cv2.cvtColor(img_third, cv2.COLOR_BGR2GRAY)

    # Compute differences between frames
    diff_1 = cv2.absdiff(img_first_gray, img_second_gray)
    diff_2 = cv2.absdiff(img_second_gray, img_third_gray)

    # Apply threshold to highlight significant changes
    _, diff_1_thres = cv2.threshold(diff_1, threshold_move, 255, cv2.THRESH_BINARY)
    _, diff_2_thres = cv2.threshold(diff_2, threshold_move, 255, cv2.THRESH_BINARY)

    # Combine the thresholded differences
    diff = cv2.bitwise_and(diff_1_thres, diff_2_thres)

    # Count non-zero pixels to detect motion
    diff_cnt = cv2.countNonZero(diff)
    if diff_cnt > diff_compare:
        nzero = np.nonzero(diff)  # Get coordinates of non-zero pixels
        cv2.rectangle(scr, (min(nzero[1]), min(nzero[0])),
                      (max(nzero[1]), max(nzero[0])), (0, 255, 0), 1)
        cv2.putText(scr, "Motion Detected", (10, 10),
                    cv2.FONT_HERSHEY_DUPLEX, 0.3, (0, 255, 0))

    # Display the result with motion annotations
    cv2.imshow('Motion Detection', scr)

    # Update frames for the next comparison
    img_first = img_second
    img_second = img_third

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'ESC' to exit
        break

picam2.stop()
cv2.destroyAllWindows()
