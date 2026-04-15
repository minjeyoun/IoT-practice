from flask import Flask  # Flask 모듈을 임포트합니다.

app = Flask(__name__)  # Flask 앱 인스턴스를 생성합니다.

@app.route('/')  # 루트 URL ('/')에 대한 라우트를 정의합니다.
def hello():  # 루트 URL에 접속할 때 실행될 함수입니다.
    return 'Hello Flask'  # 클라이언트에게 'Hello Flask'라는 문자열을 반환합니다.

if __name__ == '__main__':  # 이 파일이 메인 프로그램으로 실행될 때
    app.run(debug=True, port=80, host='172.30.1.3')  # 디버그 모드로 포트 80에서 지정된 호스트 IP에서 앱을 실행합니다.
