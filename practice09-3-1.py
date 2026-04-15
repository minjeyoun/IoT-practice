import requests  # HTTP 요청을 보내기 위한 requests 모듈 임포트
import re  # 정규 표현식 처리를 위한 re 모듈 임포트

# COVID-19 데이터를 가져올 API URL 설정
url = "http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19SidoInfStateJson?serviceKey=fFWLxGIoKo8cQCIuS5Is1fVoiKXkdls%2FU5DSGRwzmbiwIBI0nlz5V6jllexlrGLKR9y8wV3E3i0SMPTLtAhyvw%3D%3D&pageNo=1&numOfRows=30&startCreateDt=20210715&endCreateDt=20210715"

response = requests.get(url)  # API에 GET 요청을 보내고 응답 받기

# 정규 표현식을 사용하여 응답 텍스트에서 구분(gubun) 정보 추출
gubun = re.findall(r'<gubun>(.+?)</gubun>', response.text)
# 정규 표현식을 사용하여 응답 텍스트에서 신규 확진자 수(incDec) 정보 추출
incDec = re.findall(r'<incDec>(.+?)</incDec>', response.text)

# 추출된 구분 정보 출력
print(gubun)
# 추출된 신규 확진자 수 출력
print(incDec)
