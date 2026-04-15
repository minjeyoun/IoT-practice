from picamera2 import Picamera2
import cv2
import numpy as np

# 얼굴 감지를 위한 가스케이드(Cascade) 파일 로드
# 가장 기본이 되는 정면 얼굴 감지 모델입니다.
cascade_filename = 'haarcascade_frontalface_alt.xml'
cascade = cv2.CascadeClassifier(cascade_filename)

# 모델의 정확도를 높이기 위한 평균값(Mean Values) 설정
# 학습된 모델이 사용하는 이미지의 평균 색상 값을 빼서 연산을 정규화합니다.
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)

# Caffe 프레임워크 기반의 학습된 딥러닝 모델 로드
# age_net: 나이 예측 모델, gender_net: 성별 예측 모델
age_net = cv2.dnn.readNetFromCaffe('deploy_age.prototxt', 'age_net.caffemodel')
gender_net = cv2.dnn.readNetFromCaffe('deploy_gender.prototxt', 'gender_net.caffemodel')

# 예측된 결과 인덱스에 대응하는 라벨 리스트
age_list = ['(0 ~ 2)', '(4 ~ 6)', '(8 ~ 12)', '(15 ~ 20)', '(25 ~ 32)', '(38 ~ 43)', '(48 ~ 53)', '(60 ~ 100)']
gender_list = ['Male', 'Female']

def main():
    # 라즈베리 파이 카메라(Picamera2) 초기화 및 설정
    picam2 = Picamera2()
    # RGB888 포맷, 640x480 해상도로 카메라 스트리밍 설정
    config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    while True:
        # 카메라로부터 현재 프레임 한 장을 NumPy 배열 형태로 캡처
        img = picam2.capture_array()
        
        if img is None:
            print("이미지 캡처에 실패했습니다.")
            continue

        # 얼굴 인식을 위해 컬러 이미지를 흑백(Grayscale)으로 변환
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 흑백 이미지에서 얼굴 찾기 (감도 및 최소 크기 설정)
        results = cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20)
        )

        # 감지된 각 얼굴 영역(box)에 대해 분석 수행
        for box in results:
            x, y, w, h = box
            # 원본 이미지에서 얼굴 부분만 잘라내기(Copy)
            face = img[y:y+h, x:x+w].copy()
            
            # 잘라낸 얼굴 이미지를 딥러닝 모델 입력 형식(Blob)으로 변환
            # 모델 요구 크기인 227x227로 리사이징 수행
            blob = cv2.dnn.blobFromImage(face, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

            # 성별(Gender) 예측 실행
            gender_net.setInput(blob)
            gender_preds = gender_net.forward()
            gender = gender_list[gender_preds[0].argmax()] # 가장 확률이 높은 결과 선택

            # 나이(Age) 예측 실행
            age_net.setInput(blob)
            age_preds = age_net.forward()
            age = age_list[age_preds[0].argmax()] # 가장 확률이 높은 결과 선택

            # 화면에 표시할 라벨 생성 (예: Male, (25 ~ 32))
            label = f"{gender}, {age}"
            # 얼굴 주위에 파란색 사각형 그리기
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # 사각형 위에 성별과 나이 정보 텍스트 표시
            cv2.putText(img, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # 최종 처리된 영상을 'Face Detection' 창에 출력
        cv2.imshow('Face Detection', img)

        # 'q' 키를 누르면 프로그램 종료 (대기 시간 10ms)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # 카메라 정지 및 모든 윈도우 창 닫기
    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
