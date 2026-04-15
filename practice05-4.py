import smbus # SMBus 모듈을 가져옵니다.
import time # 시간 관련 함수를 사용하기 위해 time 모듈을 가져옵니다.

# I2C 장치 주소를 정의합니다.
I2C_ADDRESS = 0x48

# I2C 버스를 정의하고 초기화합니다. Raspberry Pi의 경우 일반적으로 1번 버스를 사용합니다.
I2C_BUS = 1
bus = smbus.SMBus(I2C_BUS)

def read_adc(channel):
    """
    주어진 채널에서 ADC 값을 읽습니다.

    :param channel: 읽고자 하는 아날로그 입력 채널 (0-3)
    :return: ADC 값 (0-255)
    """
    # 선택한 채널에 해당하는 명령을 보내기 위해 비트를 OR 연산합니다.
    bus.write_byte(I2C_ADDRESS, 0x40 | channel)
    # 첫 번째 바이트는 더미 읽기로 사용합니다.
    bus.read_byte(I2C_ADDRESS)
    # 두 번째 바이트를 읽어 ADC 값을 가져옵니다.
    value = bus.read_byte(I2C_ADDRESS)
    return value

def lm35_to_temperature(adc_value):
    """
    LM35 센서의 ADC 값을 섭씨 온도로 변환합니다.

    :param adc_value: ADC 값 (0-255)
    :return: 섭씨 온도
    """
    # ADC 값을 전압으로 변환합니다. (3.3V 기준)
    voltage = adc_value / 255.0 * 3.3

    # 전압을 섭씨 온도로 변환합니다. (1V = 100°C)
    temperature = voltage * 100
    return temperature

try:
    # 무한 루프를 시작합니다
    while True:

        # ADC의 첫 번째 채널(0번)에서 값을 읽습니다.
        adc_value = read_adc(0)

        # 읽어온 ADC 값을 섭씨 온도로 변환합니다.
        temperature = lm35_to_temperature(adc_value)

        # 변환된 온도를 출력합니다.
        print(f"Temperature: {temperature:.2f} °C")

        # 1초 대기합니다.
        time.sleep(1)

except KeyboardInterrupt:
    # 프로그램이 키보드 인터럽트(CTRL+C)로 중단되면 메시지를 출력합니다.
    print("Program stopped")
