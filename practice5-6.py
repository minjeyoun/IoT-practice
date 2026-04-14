import I2C_LCD_driver # I2C LCD 드라이버 모듈을 가져옵니다.
import time # 시간 관련 함수를 사용하기 위해 time 모듈을 가져옵니다.

# I2C LCD 인스턴스를 초기화합니다.
mylcd = I2C_LCD_driver.lcd()

# 카운터 변수를 초기화합니다.
#cnt = 0

# LCD 화면을 초기화하고 지웁니다.
mylcd.lcd_clear()

# 첫 번째 줄에 "Hello World" 메시지를 표시합니다.
mylcd.lcd_display_string(" Hello World", 1) # 1은 첫 번째 줄을 의미합니다.

# 두 번째 줄에 "IoT Class" 메시지를 표시합니다.
mylcd.lcd_display_string(" IoT Class", 2) # 2는 두 번째 줄을 의미합니다.

# 3초 동안 메시지를 표시합니다.
time.sleep(3)

# LCD 화면을 지웁니다.
mylcd.lcd_clear()

# 1초 대기합니다.
time.sleep(1)

# LCD 백라이트를 끕니다.
mylcd.backlight(0)
