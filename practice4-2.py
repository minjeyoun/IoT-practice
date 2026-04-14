import spidev
import time

def analog_read(channel):
    # 주어진 채널에서 아날로그 값을 읽어오는 함수
    r = spi.xfer2([1, (0x08 + channel) << 4, 0]) # SPI를 통해 ADC 요청
    adc_out = ((r[1] & 0x03) << 8) + r[2] # 읽은 데이터에서 ADC 값 계산
    return adc_out # 계산된 ADC 값 반환

# SPI 설정
spi = spidev.SpiDev()
spi.open(0, 0) # SPI 장치 0, 칩 선택 0으로 열기
spi.max_speed_hz = 1000000 # SPI 최대 속도 설정

try:
    while True:
        adc = analog_read(2) # 채널 2에서 아날로그 값 읽기
        voltage = adc * 3.3 / 1023 # ADC 값을 전압으로 변환
        print("ADC = %d Voltage = %.3fV" % (adc, voltage)) # ADC 값과 전압 출력
        time.sleep(0.5) # 0.5초 대기
    except KeyboardInterrupt:
        pass # 키보드 인터럽트 시 예외 처리
    finally:
        spi.close() # SPI 연결 닫기