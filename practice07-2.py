from flask import Flask, request, render_template  # Flask, request, render_template 모듈을 임포트합니다.

app = Flask(__name__)  # Flask 앱 인스턴스를 생성합니다.

@app.route('/method_post', methods=['GET', 'POST'])  # '/method_post' 경로에 GET과 POST 요청을 처리하는 라우트를 정의합니다.
def method_post():
    return render_template('method_post.html')  # 'method_post.html' 템플릿을 렌더링하여 반환합니다.

@app.route('/method_post_act', methods=['GET', 'POST'])  # '/method_post_act' 경로에 GET과 POST 요청을 처리하는 라우트를 정의합니다.
def method_post_act():
    if request.method == 'POST':  # 요청이 POST일 경우
        id = request.form["id"]  # POST 데이터에서 'id' 값을 가져옵니다.
        password = request.form["password"]  # POST 데이터에서 'password' 값을 가져옵니다.
        return render_template('method_post.html', id=id, password=password)  # 'method_post.html' 템플릿을 렌더링하면서 id와 password를 전달합니다.

if __name__ == '__main__':  # 이 파일이 메인 프로그램으로 실행될 때
    app.run(debug=True, port=80, host='0.0.0.0')  # 디버그 모드로 포트 80에서 모든 호스트에서 앱을 실행합니다.
