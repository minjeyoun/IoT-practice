import smbus # SMBus 모듈을 가져옵니다.
import time # 시간 관련 함수를 사용하기 위해 time 모듈을 가져옵니다.

# I2C 버스를 초기화합니다. Raspberry Pi의 경우 일반적으로 1번 버스를 사용합니다.
bus = smbus.SMBus(1)

# I2C 주소와 AIN0, AIN3 레지스터 주소를 정의합니다.
addr = 0x48 # I2C 장치 주소
AIN0 = 0x40 # 첫 번째 아날로그 입력 채널 (CDS)
AIN3 = 0x43 # 네 번째 아날로그 입력 채널 (VR)

# 장치의 초기 바이트를 읽어와 설정을 완료합니다.
bus.read_byte(0x48)

# 무한 루프를 시작합니다.
while True:
    # AIN0에 해당하는 레지스터에 값을 씁니다 (CDS 읽기 준비).
    bus.write_byte(addr, AIN0)
    bus.read_byte(addr) # 데이터를 읽어오기 위해 다시 읽습니다 (dummy read).

    # CDS 값을 읽습니다.
    CDS = bus.read_byte(addr)

    # AIN3에 해당하는 레지스터에 값을 씁니다 (VR 읽기 준비).
    bus.write_byte(addr, AIN3)
    bus.read_byte(addr) # 데이터를 읽어오기 위해 다시 읽습니다 (dummy read).

    # VR 값을 읽습니다.
    VR = bus.read_byte(addr)

    # CDS와 VR 값을 출력합니다.
    print('CDS : ', CDS, 'VR : ', VR)

    # 0.1초 대기합니다.
    time.sleep(0.1)