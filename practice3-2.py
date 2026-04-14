import RPi.GPIO as GPIO # RPi.GPIO 라이브러리를 임포트하여 Raspberry Pi의 GPIO 핀을 제어
import time # 시간 관련 기능을 사용하기 위해 time 라이브러리를 임포트

# 자동차 신호등 LED 핀 번호 설정
carLedRed = 2 # 자동차 신호등 빨간불
carLedYellow = 3 # 자동차 신호등 노란불
carLedGreen = 4 # 자동차 신호등 초록불

# 보행자 신호등 LED 핀 번호 설정
humanLedRed = 20 # 보행자 신호등 빨간불
humanLedGreen = 21 # 보행자 신호등 초록불

# GPIO 핀 번호 체계를 BCM으로 설정
GPIO.setmode(GPIO.BCM)

# 각 LED 핀을 출력 모드로 설정
GPIO.setup(carLedRed, GPIO.OUT)
GPIO.setup(carLedYellow, GPIO.OUT)
GPIO.setup(carLedGreen, GPIO.OUT)
GPIO.setup(humanLedRed, GPIO.OUT)
GPIO.setup(humanLedGreen, GPIO.OUT)

try:
    while True: # 무한 루프 시작
        # 자동차 신호등 초록불 켜고, 빨간불과 노란불 끔
        GPIO.output(carLedRed, GPIO.LOW)
        GPIO.output(carLedYellow, GPIO.LOW)
        GPIO.output(carLedGreen, GPIO.HIGH)

        # 보행자 신호등 빨간불 켜고, 초록불 끔
        GPIO.output(humanLedRed, GPIO.HIGH)
        GPIO.output(humanLedGreen, GPIO.LOW)

        # 3초 대기
        time.sleep(3.0)

        # 자동차 신호등 노란불 켜고, 빨간불과 초록불 끔
        GPIO.output(carLedRed, GPIO.LOW)
        GPIO.output(carLedYellow, GPIO.HIGH)
        GPIO.output(carLedGreen, GPIO.LOW)

        # 보행자 신호등 빨간불 켜고, 초록불 끔
        GPIO.output(humanLedRed, GPIO.HIGH)
        GPIO.output(humanLedGreen, GPIO.LOW)

        # 1초 대기
        time.sleep(1.0)

        # 자동차 신호등 빨간불 켜고, 노란불과 초록불 끔
        GPIO.output(carLedRed, GPIO.HIGH)
        GPIO.output(carLedYellow, GPIO.LOW)
        GPIO.output(carLedGreen, GPIO.LOW)

        # 보행자 신호등 초록불 켜고, 빨간불 끔
        GPIO.output(humanLedRed, GPIO.LOW)
        GPIO.output(humanLedGreen, GPIO.HIGH)

        # 3초 대기
        time.sleep(3.0)

except KeyboardInterrupt: # 키보드 인터럽트(CTRL+C)가 발생하면
    pass # 아무 작업도 하지 않고 루프를 종료

# GPIO 설정을 초기화하여 사용한 핀을 정리
GPIO.cleanup()