import cv2
from picamera2 import Picamera2
import time

classNames = {0: 'background',
              1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
              7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',
              13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',
              18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',
              24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',
              32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',
              37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
              41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',
              46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
              51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
              56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
              61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
              67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
              75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
              80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
              86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}

def id_class_name(class_id, classes):
    # Retrieve the class name corresponding to the class ID
    return classes.get(class_id, "Unknown")

# Initialize Picamera2 for capturing video
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

def main():
    try:
        # Load the TensorFlow model with OpenCV DNN module
        model = cv2.dnn.readNetFromTensorflow(
            '/home/tommy/OpencvDnn/models/frozen_inference_graph.pb',
            '/home/tommy/OpencvDnn/models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
        )

        while True:
            # Exit loop if 'q' key is pressed
            keyValue = cv2.waitKey(1)
            if keyValue == ord('q'):
                break
            
            # Capture a frame using Picamera2
            image = picam2.capture_array()

            # Convert RGBA (4-channel) image to BGR (3-channel) if needed
            if image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

            image_height, image_width, _ = image.shape

            # Set the image as input to the model
            model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
            output = model.forward()

            # Iterate over detected objects
            for detection in output[0, 0, :, :]:
                confidence = detection[2]
                if confidence > .5:
                    # Get class ID and class name
                    class_id = int(detection[1])
                    class_name = id_class_name(class_id, classNames)
                    print(f"{class_id} {confidence:.2f} {class_name}")
                    
                    # Compute bounding box coordinates
                    box_x = int(detection[3] * image_width)
                    box_y = int(detection[4] * image_height)
                    box_width = int(detection[5] * image_width)
                    box_height = int(detection[6] * image_height)
                    
                    # Draw bounding box and label on the image
                    cv2.rectangle(image, (box_x, box_y), (box_width, box_height), (23, 230, 210), thickness=1)
                    cv2.putText(image, class_name, (box_x, box_y + int(0.05 * image_height)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
            # Display the image with detections
            cv2.imshow('image', image)
            time.sleep(0.1)  # Delay to reduce CPU load

    except KeyboardInterrupt:
        pass
    finally:
        # Clean up resources
        picam2.stop()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
