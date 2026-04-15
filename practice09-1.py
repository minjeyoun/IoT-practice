import tkinter  # tkinter 모듈을 임포트하여 GUI를 생성
import tkinter.font  # tkinter의 폰트 모듈을 임포트하여 텍스트 스타일 설정
import os  # 운영 체제와 상호작용하기 위한 os 모듈 임포트
import time  # 시간 관련 기능을 사용하기 위해 time 모듈 임포트

def time1000mS():
    # vcgencmd를 사용하여 CPU 온도를 측정
    temp = os.popen("vcgencmd measure_temp").readline()
    # 측정된 온도 문자열에서 'temp='와 "'C"를 제거하여 순수한 온도 값만 추출
    temp = temp.replace("temp=", "").replace("'C", "")
    print(temp)  # 콘솔에 온도 출력
    label.config(text=temp)  # GUI의 레이블에 온도 표시
    window.after(1000, time1000mS)  # 1초 후에 다시 time1000mS 함수 호출

# tkinter 윈도우 생성
window = tkinter.Tk()
window.title("CPU TEMPERATURE")  # 윈도우 제목 설정
window.geometry("400x100")  # 윈도우 크기 설정
window.resizable(False, False)  # 윈도우 크기 조절 불가능 설정

# 폰트 설정
font = tkinter.font.Font(size=30)
# 레이블 생성 및 설정
label = tkinter.Label(window, text="hello", font=font)
label.pack()  # 레이블을 윈도우에 추가

time1000mS()  # 온도 측정 함수 호출

window.mainloop()  # 이벤트 루프 시작
