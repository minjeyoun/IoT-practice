import requests  # HTTP 요청을 보내기 위한 requests 모듈 임포트
import re  # 정규 표현식 처리를 위한 re 모듈 임포트
import tkinter  # tkinter 모듈을 임포트하여 GUI를 생성
import tkinter.font  # tkinter의 폰트 모듈을 임포트하여 텍스트 스타일 설정


def tick1Min():
    # 기상청 RSS 피드를 통해 날씨 정보를 가져올 URL
    url = "https://www.weather.go.kr/w/rss/dfs/hr1-forecast.do?zone=2818586000"
    response = requests.get(url)  # URL에 GET 요청을 보내 응답 받기

    # 정규 표현식을 사용하여 응답 텍스트에서 온도와 습도 정보 추출
    temp = re.findall(r'<temp>(.+)</temp>', response.text)
    humi = re.findall(r'<reh>(.+)</reh>', response.text)

    # 온도와 습도를 문자열로 형식화하여 표시할 내용 생성
    display = str(temp[0]) + "C" + "   " + str(humi[0]) + "%"

    label.config(text=display)  # GUI의 레이블에 날씨 정보 표시
    window.after(60000, tick1Min)  # 1분(60000ms) 후에 tick1Min 함수 다시 호출


# tkinter 윈도우 생성
window = tkinter.Tk()
window.title("TEMP HUMI DISPLAY")  # 윈도우 제목 설정
window.geometry("400x100")  # 윈도우 크기 설정
window.resizable(False, False)  # 윈도우 크기 조절 불가능 설정

# 폰트 설정
font = tkinter.font.Font(size=30)
# 레이블 생성 및 설정
label = tkinter.Label(window, text="", font=font)
label.pack()  # 레이블을 윈도우에 추가

tick1Min()  # 날씨 정보 갱신 함수 호출

window.mainloop()  # 이벤트 루프 시작
