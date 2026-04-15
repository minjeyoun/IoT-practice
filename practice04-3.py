import spidev  # SPI 통신 라이브러리 (ADC 칩과 통신용)
import time  # 시간 지연 함수 사용


def analog_read(channel):
    # MCP3008 칩에 보낼 명령어 데이터 생성 (3바이트)
    # [시작비트, 채널 선택, 의미없는 데이터] 순서
    r = spi.xfer2([1, (0x08 + channel) << 4, 0])

    # 받은 3바이트 데이터 중 필요한 10비트 추출 (0 ~ 1023)
    adc_out = ((r[1] & 0x03) << 8) + r[2]
    return adc_out


# SPI 통신 설정
spi = spidev.SpiDev()
spi.open(0, 0)  # SPI 버스 0, 장치 0번 열기
spi.max_speed_hz = 1000000  # 통신 속도 1MHz 설정

try:
    while True:
        # 가변저항이 연결된 2번 채널(CH2)에서 값 읽기
        adc = analog_read(2)

        # 10비트 디지털 값(0-1023)을 실제 전압(0.0V-3.3V)으로 환산
        voltage = adc * 3.3 / 1023

        # 화면에 출력 (ADC 값과 계산된 전압)
        print("ADC = %d  Voltage = %.3fV" % (adc, voltage))

        time.sleep(0.5)  # 0.5초 간격으로 측정

except KeyboardInterrupt:
    # Ctrl+C를 누르면 안전하게 종료
    pass

finally:
    # 프로그램 종료 시 SPI 연결 해제
    spi.close()
