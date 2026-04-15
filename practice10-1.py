import cv2import cv2          # OpenCV 라이브러리
import subprocess   # 외부 명령어(카메라 캡처) 실행을 위한 모듈
import numpy as np  # 수치 계산을 위한 라이브러리

# 얼굴과 눈 감지를 위한 분류기(CascadeClassifier) 초기화
# 학습된 모델 데이터(.xml 파일)를 로드합니다. 경로가 정확한지 꼭 확인하세요!
face_cascade = cv2.CascadeClassifier("/home/tommy/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("/home/tommy/opencv/data/haarcascades/haarcascade_eye.xml")

try:
    while True:
        # libcamera-still 명령어를 사용하여 이미지를 캡처하고 임시 파일로 저장합니다.
        # -o: 저장경로, --width/height: 해상도, -n: 미리보기 창 끔
        command = "libcamera-still -o /tmp/capture.jpg --width 640 --height 480 -n"
        subprocess.run(command, shell=True)

        # 캡처된 이미지를 OpenCV 형식으로 불러옵니다.
        img = cv2.imread('/tmp/capture.jpg')
        if img is None:
            print("이미지를 불러오는 데 실패했습니다.")
            break

        # 인식률을 높이고 연산 속도를 빠르게 하기 위해 이미지를 흑백(Grayscale)으로 변환합니다.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 얼굴 감지 실행 (이미지, 스케일 비율, 최소 인접 사각형 개수)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        print("감지된 얼굴 수:", len(faces))

        # 감지된 얼굴 영역에 사각형을 그리고, 그 안에서 눈을 찾습니다.
        for (x, y, w, h) in faces:
            # 얼굴 영역에 파란색(255, 0, 0) 사각형 그리기 (두께 1)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
            
            # 눈은 얼굴 안에 있으므로, 얼굴 영역만 따로 떼어냅니다(ROI: Region of Interest).
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]
            
            # 잘라낸 얼굴 영역(흑백)에서 눈 감지 실행
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                # 눈 영역에 녹색(0, 255, 0) 사각형 그리기
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)

        # 결과 프레임을 화면에 표시합니다.
        cv2.imshow('Face and Eye Detection', img)

        # 키 입력을 기다립니다. 'Esc' 키(ASCII 코드 27)를 누르면 루프를 종료합니다.
        if cv2.waitKey(30) & 0xFF == 27:
            break
finally:
    # 프로그램 종료 시 생성된 모든 창을 닫습니다.
    cv2.destroyAllWindows()
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
