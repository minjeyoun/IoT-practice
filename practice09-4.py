import cv2  # OpenCV 모듈 임포트

# 이미지 파일을 색상 모드로 읽기
img = cv2.imread("./img_1.png", cv2.IMREAD_COLOR)

# 이미지가 성공적으로 읽혔는지 확인
if img is not None:
    # 이미지를 회색조로 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 이미지의 크기를 600x400으로 변경
    img_resize = cv2.resize(img, (600, 400))
    # 회색조 이미지의 크기를 600x400으로 변경
    gray_resize = cv2.resize(gray, (600, 400))

    # 변경된 크기의 색상 이미지 표시
    cv2.imshow("img_resize", img_resize)
    # 변경된 크기의 회색조 이미지 표시
    cv2.imshow("gray_resize", gray_resize)

    # 키 입력을 기다림
    cv2.waitKey(0)
    # 모든 OpenCV 윈도우 닫기
    cv2.destroyAllWindows()
else:
    # 이미지 파일을 찾을 수 없을 경우 메시지 출력
    print("Image file not found")
