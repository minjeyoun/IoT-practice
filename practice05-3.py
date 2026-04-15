import smbus # SMBus 모듈을 가져옵니다.
import time # 시간 관련 함수를 사용하기 위해 time 모듈을 가져옵니다.

# I2C 버스를 초기화합니다. Raspberry Pi의 경우 일반적으로 1번 버스를 사용합니다.
bus = smbus.SMBus(1)

# I2C 장치 주소와 아날로그 입력/출력 레지스터 주소를 정의합니다.
addr = 0x48 # I2C 장치 주소
AIN0 = 0x40 # 첫 번째 아날로그 입력 채널
AIN3 = 0x43 # 세 번째 아날로그 입력 채널
AOUT = 0x40 # 아날로그 출력 레지스터 주소

# 무한 루프를 시작합니다.
while True:
    # AIN3에 해당하는 레지스터를 선택하여 값을 읽습니다.
    bus.write_byte(addr, AIN3)
    # AIN3에서 읽어온 값을 val에 저장합니다.
    val = bus.read_byte(addr)
    # 읽어온 값을 AOUT 레지스터에 출력합니다.
    bus.write_byte_data(addr, AOUT, val)
    # 읽어온 값을 콘솔에 출력합니다.
    print(val)
