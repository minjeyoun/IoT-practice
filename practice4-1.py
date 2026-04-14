import spidev
import RPi.GPIO as GPIO
import time

ledWhite = 18 # LED 핀 번호 설정

# GPIO 모드 설정
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledWhite, GPIO.OUT) # LED 핀을 출력으로 설정

# SPI 설정
spi = spidev.SpiDev()
spi.open(0, 0) # SPI 장치 0, 칩 선택 0으로 열기
spi.max_speed_hz = 1000000 # SPI 최대 속도 설정

def analogRead(ch):
# 아날로그 값을 읽기 위한 함수
buf = [1, (8 + ch) << 4, 0] # ADC 요청 버퍼 생성
buf = spi.xfer2(buf) # SPI를 통해 데이터 전송
adcValue = ((buf[1] & 3) << 8) | buf[2] # ADC 값 계산
return adcValue # 계산된 ADC 값 반환

try:
    while True:
        cdsValue = analogRead(0) # 채널 0에서 아날로그 값 읽기
        print(cdsValue) # 읽은 값 출력
        time.sleep(0.2) # 0.2초 대기

    except KeyboardInterrupt:
        pass # 키보드 인터럽트 시 예외 처리

# GPIO 및 SPI 정리
GPIO.cleanup()
spi.close()