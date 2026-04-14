import I2C_LCD_driver # I2C LCD 드라이버 모듈을 가져옵니다.
# import time # time 모듈을 가져오지 않고, sleep 함수만 가져옵니다.
from time import sleep # time 모듈에서 sleep 함수를 가져옵니다.
from datetime import datetime # datetime 모듈에서 datetime 클래스를 가져옵니다.

# I2C LCD 인스턴스를 초기화합니다.
mylcd = I2C_LCD_driver.lcd()

# LCD 화면을 초기화하고 지웁니다.
mylcd.lcd_clear()

try:
    print("Writing to display") # LCD에 텍스트를 쓰기 시작합니다.
    # 첫 번째 줄에 "No time to waste"를 표시합니다.
    mylcd.lcd_display_string("No time to waste", 1) # 1은 첫 번째 줄을 의미합니다.

    while True:
        # 현재 시간을 두 번째 줄에 표시합니다.
        mylcd.lcd_display_string(str(datetime.now().time()), 2) # 현재 시간을 문자열로 변환하여 표시합니다.

        # 다음 줄을 주석 해제하면 1초 간격으로 루프를 실행합니다.
        # sleep(1) # 1초 대기합니다.

except KeyboardInterrupt:
    # 프로그램이 키보드 인터럽트(CTRL+C)로 중단되면 실행됩니다.
    print("Cleaning up!") # 정리 작업을 시작합니다.
    mylcd.lcd_clear() # LCD 화면을 지웁니다.
