import cv2
import numpy as np
from picamera2 import Picamera2

# 설정값: 픽셀 값의 차이가 이 수치(50)보다 크면 움직임으로 간주함
threshold_move = 50  
# 설정값: 움직임이 감지된 픽셀의 개수가 이 수치(10)보다 많을 때 최종적으로 "움직임"으로 판단함
diff_compare = 10    

# 라즈베리 파이 카메라(Picamera2) 초기화 및 설정
picam2 = Picamera2()
# 카메라 화면 구성 (포맷: RGB, 해상도: 640x480)
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

# 움직임 비교를 위한 첫 번째와 두 번째 프레임을 미리 캡처함
img_first = picam2.capture_array()
img_second = picam2.capture_array()

while True:
    img_third = picam2.capture_array()  # 세 번째 프레임 캡처
    scr = img_third.copy()  # 화면 표시 및 사각형을 그리기 위한 복사본 생성

    # 연산 속도를 높이고 노이즈를 줄이기 위해 각 프레임을 흑백(Grayscale)으로 변환
    img_first_gray = cv2.cvtColor(img_first, cv2.COLOR_BGR2GRAY)
    img_second_gray = cv2.cvtColor(img_second, cv2.COLOR_BGR2GRAY)
    img_third_gray = cv2.cvtColor(img_third, cv2.COLOR_BGR2GRAY)

    # 프레임 간의 절대값 차이 계산 (연속된 두 장씩 비교)
    # diff_1: 1번과 2번 사진의 차이 / diff_2: 2번과 3번 사진의 차이
    diff_1 = cv2.absdiff(img_first_gray, img_second_gray)
    diff_2 = cv2.absdiff(img_second_gray, img_third_gray)

    # 설정한 문턱값(threshold_move)을 기준으로 이진화 작업 수행
    # 차이가 큰 부분(움직임)은 흰색(255), 나머지는 검은색(0)으로 바꿈
    _, diff_1_thres = cv2.threshold(diff_1, threshold_move, 255, cv2.THRESH_BINARY)
    _, diff_2_thres = cv2.threshold(diff_2, threshold_move, 255, cv2.THRESH_BINARY)

    # 두 개의 이진화된 이미지를 비트 연산(AND)으로 합침
    # 두 구간 모두에서 변한 부분만 "진짜 움직임"으로 판단하여 노이즈(먼지, 빛 번짐 등)를 제거함
    diff = cv2.bitwise_and(diff_1_thres, diff_2_thres)

    # 흰색(움직임이 감지된) 픽셀의 개수를 셉니다.
    diff_cnt = cv2.countNonZero(diff)
    
    # 설정값(10개 픽셀)보다 많은 움직임이 감지되었을 때만 화면에 표시
    if diff_cnt > diff_compare:
        nzero = np.nonzero(diff)  # 움직임이 발생한 모든 픽셀의 좌표를 찾음
        
        # 움직임 좌표의 최소/최대값을 구해 전체 움직임 영역을 감싸는 녹색 사각형을 그림
        cv2.rectangle(scr, (min(nzero[1]), min(nzero[0])),
                      (max(nzero[1]), max(nzero[0])), (0, 255, 0), 1)
        
        # 화면 왼쪽 상단에 "Motion Detected" 경고 문구 표시
        cv2.putText(scr, "Motion Detected", (10, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0))

    # 최종 결과 화면을 'Motion Detection' 창에 출력
    cv2.imshow('Motion Detection', scr)

    # 다음 비교를 위해 프레임을 한 칸씩 업데이트함
    # 1번 <- 2번, 2번 <- 3번
    img_first = img_second
    img_second = img_third

    # 'ESC' 키(ASCII 27)를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 카메라 정지 및 모든 윈도우 창 닫기
picam2.stop()
cv2.destroyAllWindows()
