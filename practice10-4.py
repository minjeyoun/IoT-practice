import cv2
from picamera2 import Picamera2
import time

# 모델에 사전 학습된 90가지 사물 클래스 목록
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
    # 클래스 ID에 해당하는 사물 이름을 반환 (없으면 "Unknown" 반환)
    return classes.get(class_id, "Unknown")

# 실시간 영상 캡처를 위한 Picamera2 초기화 및 설정
picam2 = Picamera2()
# 해상도를 640x480으로 설정하여 프리뷰 구성 생성
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

def main():
    try:
        # OpenCV DNN 모듈을 사용하여 텐서플로우 모델 파일 로드
        model = cv2.dnn.readNetFromTensorflow(
            '/home/tommy/OpencvDnn/models/frozen_inference_graph.pb',
            '/home/tommy/OpencvDnn/models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
        )

        while True:
            # 키보드 입력 대기, 'q' 키를 누르면 루프 종료
            keyValue = cv2.waitKey(1)
            if keyValue == ord('q'):
                break
            
            # 카메라로부터 현재 프레임 한 장을 배열 형태로 캡처
            image = picam2.capture_array()

            # 만약 이미지가 RGBA(4채널) 형식이라면 OpenCV에서 사용하는 BGR(3채널)로 변환
            if image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)

            image_height, image_width, _ = image.shape

            # 이미지를 모델 입력 크기(300x300)로 변환하여 입력 설정
            model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
            # 모델 추론 실행 (객체 탐지 결과 출력)
            output = model.forward()

            # 탐지된 모든 객체에 대해 반복문 수행
            for detection in output[0, 0, :, :]:
                confidence = detection[2] # 탐지 정확도(신뢰도)
                
                # 신뢰도가 0.5(50%)보다 높은 것만 선별
                if confidence > .5:
                    class_id = int(detection[1]) # 객체의 ID 번호
                    class_name = id_class_name(class_id, classNames) # ID를 이름으로 변환
                    print(f"{class_id} {confidence:.2f} {class_name}") # 터미널에 결과 출력
                    
                    # 0~1 사이의 비율인 좌표값을 실제 픽셀 좌표로 계산
                    box_x = int(detection[3] * image_width)
                    box_y = int(detection[4] * image_height)
                    box_width = int(detection[5] * image_width)
                    box_height = int(detection[6] * image_height)
                    
                    # 찾은 객체 주위에 민트색 사각형 그리기
                    cv2.rectangle(image, (box_x, box_y), (box_width, box_height), (23, 230, 210), thickness=1)
                    # 객체 이름 표시 (가독성을 위해 위치 조정)
                    cv2.putText(image, class_name, (box_x, box_y + int(0.05 * image_height)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
            
            # 탐지 결과가 그려진 최종 영상을 화면에 표시
            cv2.imshow('image', image)
            # CPU 과부하를 방지하기 위해 0.1초의 짧은 지연 시간 추가
            time.sleep(0.1)

    except KeyboardInterrupt:
        # 사용자가 Ctrl+C로 강제 종료했을 때 처리
        pass
    finally:
        # 프로그램 종료 시 카메라 정지 및 모든 창 닫기 (자원 해제)
        picam2.stop()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
