import RPi.GPIO as GPIO # RPi.GPIO 라이브러리를 임포트하여 Raspberry Pi의 GPIO 핀을 제어
import time # 시간 관련 기능을 사용하기 위해 time 라이브러리를 임포트

# LED와 스위치 핀 번호 설정
ledRed = 23 # 빨간 LED 핀 번호
ledGreen = 24 # 초록 LED 핀 번호
swPin = 21 # 스위치 핀 번호

# GPIO 핀 번호 체계를 BCM으로 설정
GPIO.setmode(GPIO.BCM)

# LED 핀을 출력 모드로 설정
GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)

# 스위치 핀을 입력 모드로 설정하고 풀다운 저항을 사용
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

swState = 0 # 스위치 상태 초기화
try:
    while True: # 무한 루프 시작
        swValue = GPIO.input(swPin) # 스위치의 현재 상태 읽기

        # 스위치가 눌렸는지 확인
        if swValue == 1:
            # 스위치 상태가 0에서 1로 변경되면 상태를 토글
            if swState == 0:
                swState = 1 # 스위치가 켜짐
            else:
                swState = 0 # 스위치가 꺼짐
            time.sleep(0.5) # 디바운싱을 위해 0.5초 대기

        # 스위치가 켜져 있는 경우
        if swState == 1:
            # 빨간 LED를 켜고 초록 LED를 끔
            GPIO.output(ledRed, GPIO.HIGH)
            GPIO.output(ledGreen, GPIO.LOW)
            time.sleep(0.1) # 0.1초 대기

            # 빨간 LED를 끄고 초록 LED를 켬
            GPIO.output(ledRed, GPIO.LOW)
            GPIO.output(ledGreen, GPIO.HIGH)
            time.sleep(0.1) # 0.1초 대기
        else:
            # 스위치가 꺼져 있는 경우 LED를 모두 끔
            GPIO.output(ledRed, GPIO.LOW)
            GPIO.output(ledGreen, GPIO.LOW)

except KeyboardInterrupt: # 키보드 인터럽트(CTRL+C)가 발생하면
    pass # 아무 작업도 하지 않고 루프를 종료

# GPIO 설정을 초기화하여 사용한 핀을 정리
GPIO.cleanup()
