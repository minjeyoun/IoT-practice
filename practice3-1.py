import RPi.GPIO as GPIO # RPi.GPIO 라이브러리를 임포트하여 Raspberry Pi의 GPIO 핀을 제어
import time # 시간 관련 기능을 사용하기 위해 time 라이브러리를 임포트

# GPIO 핀 번호 체계를 BCM으로 설정
GPIO.setmode(GPIO.BCM)

# GPIO 핀 16, 20, 21을 출력 모드로 설정
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

try:
    while True: # 무한 루프 시작
        # 핀 16, 20, 21을 HIGH로 설정하여 전원을 켬
        GPIO.output(16, GPIO.HIGH)
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.HIGH)

        # 1초 대기
        time.sleep(1.0)

        # 핀 16, 20, 21을 LOW로 설정하여 전원을 끔
        GPIO.output(16, GPIO.LOW)
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)

        # 1초 대기
        time.sleep(1.0)

except KeyboardInterrupt: # 키보드 인터럽트(CTRL+C)가 발생하면
    pass # 아무 작업도 하지 않고 루프를 종료

# GPIO 설정을 초기화하여 사용한 핀을 정리
GPIO.cleanup()