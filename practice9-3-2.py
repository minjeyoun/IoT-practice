import requests  # HTTP 요청을 보내기 위한 requests 모듈 임포트
import re  # 정규 표현식 처리를 위한 re 모듈 임포트
import datetime  # 날짜 및 시간 관련 기능을 사용하기 위한 datetime 모듈 임포트
import tkinter  # tkinter 모듈을 임포트하여 GUI를 생성
import tkinter.font  # tkinter의 폰트 모듈을 임포트하여 텍스트 스타일 설정


def checkCovid19():
    # 현재 날짜와 시간을 가져옴
    now = datetime.datetime.now()
    # 'YYYYMMDD' 형식으로 날짜 문자열 생성
    yyyymmdd = now.strftime('%Y%m%d')
    print(yyyymmdd)  # 생성된 날짜 문자열 출력

    # COVID-19 데이터를 가져올 API URL 설정
    url = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey="
    apiKey = "fFWLxGIoKo8cQCIuS5Is1fVoiKXkdls%2FU5DSGRwzmbiwIBI0nlz5V6jllexlrGLKR9y8wV3E3i0SMPTLtAhyvw%3D%3D"
    pageNo = "&pageNo=1&numOfRows=30&"  # 페이지 번호와 한 페이지당 행 수 설정
    today = "startCreateDt=" + yyyymmdd + "&endCreateDt=" + yyyymmdd  # 요청 날짜 설정

    # API에 GET 요청을 보내고 응답 받기
    response = requests.get(url + apiKey + pageNo + today)

    # 정규 표현식을 사용하여 응답 텍스트에서 구분(gubun) 정보 추출
    gubun = re.findall(r'<gubun>(.+?)</gubun>', response.text)
    # 정규 표현식을 사용하여 응답 텍스트에서 신규 확진자 수(incDec) 정보 추출
    incDec = re.findall(r'<incDec>(.+?)</incDec>', response.text)

    # '합계'의 인덱스를 찾아 신규 확진자 수 추출
    findHab = gubun.index('합계')
    print(incDec[findHab])  # '합계'에 해당하는 신규 확진자 수 출력

    # GUI 레이블에 날짜와 신규 확진자 수 표시
    yyyymmddLabel.config(text=yyyymmdd)
    findHabLabel.config(text=incDec[findHab])
    # 1시간(60000ms * 60) 후에 checkCovid19 함수 다시 호출
    window.after(60000 * 60, checkCovid19)


# tkinter 윈도우 생성
window = tkinter.Tk()
window.title("COVID 19")  # 윈도우 제목 설정
window.geometry("400x200")  # 윈도우 크기 설정
window.resizable(False, False)  # 윈도우 크기 조절 불가능 설정

# 폰트 설정
font = tkinter.font.Font(size=30)
# 날짜 레이블 생성 및 설정
yyyymmddLabel = tkinter.Label(window, text="RED LED", font=font)
# 신규 확진자 수 레이블 생성 및 설정
findHabLabel = tkinter.Label(window, text="GREEN LED", font=font)
yyyymmddLabel.pack()  # 날짜 레이블을 윈도우에 추가
findHabLabel.pack()  # 신규 확진자 수 레이블을 윈도우에 추가

checkCovid19()  # COVID-19 정보 확인 함수 호출

window.mainloop()  # 이벤트 루프 시작