import I2C_LCD_driver # I2C LCD 드라이버 모듈을 가져옵니다.
from time import * # 시간 관련 함수를 사용하기 위해 time 모듈에서 모든 함수를 가져옵니다.

# I2C LCD 인스턴스를 초기화합니다.
mylcd = I2C_LCD_driver.lcd()

# 카운터 변수를 초기화합니다.
cnt = 0

# LCD 화면을 초기화하고 지웁니다.
mylcd.lcd_clear()

# 첫 번째 줄에 날짜 정보를 표시합니다.
mylcd.lcd_display_string(" - 2024.10.11 - ", 1) # 1은 첫 번째 줄을 의미합니다.

# 무한 루프를 시작합니다.
while True:
    # 카운터를 1 증가시킵니다.
    cnt = cnt + 1

    # 두 번째 줄에 카운터 값을 표시합니다. (4는 시작 위치)
    mylcd.lcd_display_string("IoTtest: %d" % cnt, 2, 4)

    # 1초 대기합니다.
    sleep(1)