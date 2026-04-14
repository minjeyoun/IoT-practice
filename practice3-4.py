import RPi.GPIO as GPIO # RPi.GPIO 라이브러리를 임포트하여 Raspberry Pi의 GPIO 핀을 제어
import time # 시간 관련 기능을 사용하기 위해 time 라이브러리를 임포트

# LED와 스위치 핀 번호 설정
ledWhite = 12 # 흰색 LED 핀 번호
swPin = 21    # 스위치 핀 번호

# GPIO 핀 번호 체계를 BCM으로 설정
GPIO.setmode(GPIO.BCM)

# LED 핀을 출력 모드로 설정
GPIO.setup(ledWhite, GPIO.OUT)

# 스위치 핀을 입력 모드로 설정하고 풀다운 저항을 사용
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# PWM 객체 생성, 주파수 500Hz로 설정
ledWhitePwm = GPIO.PWM(ledWhite, 500)
ledWhitePwm.start(0) # PWM 시작, 초기 듀티 사이클 0%

swState = 0 # 스위치 상태 초기화

newSw = 0 # 새로운 스위치 상태 초기화
oldSw = 0 # 이전 스위치 상태 초기화

def swOn():
    global newSw
    global oldSw
    newSw = GPIO.input(swPin) # 현재 스위치 상태 읽기

    # 스위치 상태가 변경되었는지 확인
    if newSw != oldSw:
        oldSw = newSw # 이전 상태 업데이트
        if newSw == 1: # 스위치가 눌렸다면
            return 1 # 상태 변경 신호 반환

    return 0 # 상태가 변경되지 않았다면 0 반환

try:
    while True: # 무한 루프 시작
        if swOn() == 1: # 스위치 상태가 변경되었는지 확인
            swState = swState + 1 # 스위치 상태 증가
            if swState >= 4: # 상태가 4 이상이면 초기화
                swState = 0
            time.sleep(0.2) # 디바운싱을 위해 0.2초 대기

            print(swState) # 현재 스위치 상태 출력

            # 각 상태에 따라 PWM 듀티 사이클 변경
            if swState == 0:
                ledWhitePwm.ChangeDutyCycle(0) # 듀티 사이클 0%
                print("duty:0")
            elif swState == 1:
                ledWhitePwm.ChangeDutyCycle(30) # 듀티 사이클 30%
                print("duty:30")
            elif swState == 2:
                ledWhitePwm.ChangeDutyCycle(60) # 듀티 사이클 60%
                print("duty:60")
            elif swState == 3:
                ledWhitePwm.ChangeDutyCycle(100) # 듀티 사이클 100%
                print("duty:100")

except KeyboardInterrupt: # 키보드 인터럽트(CTRL+C)가 발생하면
    pass # 아무 작업도 하지 않고 루프를 종료

# GPIO 설정을 초기화하여 사용한 핀을 정리
GPIO.cleanup()