from flask import Flask, render_template  # Flask와 render_template 모듈을 임포트합니다.

app = Flask(__name__)  # Flask 앱 인스턴스를 생성합니다.

@app.route('/')  # 루트 URL ('/')에 대한 라우트를 정의합니다.
def index():  # 루트 URL에 접속할 때 실행될 함수입니다.
    return render_template('html_test.html')  # 'html_test.html' 템플릿을 렌더링하여 반환합니다.

if __name__ == '__main__':  # 이 파일이 메인 프로그램으로 실행될 때
    app.run(debug=True, port=80, host='0.0.0.0')  # 디버그 모드로 포트 80에서 모든 호스트에서 앱을 실행합니다.
