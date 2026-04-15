import cv2

# 모델에 사전 학습된 클래스 목록 (COCO 데이터셋 기준 90종)
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

# 클래스 ID를 받아 대응하는 이름(문자열)을 반환하는 함수
def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value

# 텐서플로우(TensorFlow)로 학습된 SSD MobileNet 모델 로드
# .pb: 가중치 파일 / .pbtxt: 네트워크 구조 설정 파일
model = cv2.dnn.readNetFromTensorflow('models/frozen_inference_graph.pb',
                                      'models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

# 분석할 이미지 읽기
image = cv2.imread("image4.jpeg")
image_height, image_width, _ = image.shape

# 이미지를 모델 입력에 적합한 '블롭(Blob)' 형태로 변환
# 크기 300x300으로 조절, swapRB=True는 BGR을 RGB 순서로 변경함을 의미
model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))

# 네트워크를 통해 추론 실행 (객체 탐지 시작)
output = model.forward()

# 탐지된 각 객체 정보를 순회하며 분석
for detection in output[0, 0, :, :]:
    confidence = detection[2] # 탐지 결과의 신뢰도 (0~1 사이)
    
    # 신뢰도가 0.5(50%) 이상인 경우만 화면에 표시
    if confidence > .5:
        class_id = detection[1] # 탐지된 객체의 클래스 번호
        class_name = id_class_name(class_id, classNames) # 번호를 이름으로 변환
        
        # 탐지 정보 출력 (ID, 신뢰도, 이름)
        print(str(str(class_id) + " " + str(detection[2]) + " " + class_name))
        
        # 모델은 0~1 사이의 상대 좌표를 반환하므로, 실제 이미지 크기를 곱해 절대 좌표 계산
        box_x = detection[3] * image_width
        box_y = detection[4] * image_height
        box_width = detection[5] * image_width
        box_height = detection[6] * image_height
        
        # 찾은 물체 주위에 사각형(경계 상자) 그리기
        cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23, 230, 210), thickness=1)
        
        # 사각형 위에 물체 이름 텍스트 표시
        cv2.putText(image, class_name, (int(box_x), int(box_y + .05 * image_height)), 
                    cv2.FONT_HERSHEY_SIMPLEX, (.005 * image_width), (0, 0, 255))

# 결과 화면 표시
cv2.imshow('image4', image)

# 아무 키나 누를 때까지 창 유지 후 종료
cv2.waitKey(0)
cv2.destroyAllWindows()
