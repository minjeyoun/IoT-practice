from flask import Flask, request, render_template  # Flask, request, render_template 모듈을 임포트합니다.
import RPi.GPIO as GPIO  # Raspberry Pi GPIO 라이브러리를 임포트합니다.

LED = 4  # GPIO 핀 번호 4를 LED로 정의합니다.
GPIO.setmode(GPIO.BCM)  # BCM 핀 번호 체계를 사용합니다.
GPIO.setup(LED, GPIO.OUT)  # LED 핀을 출력 모드로 설정합니다.

app = Flask(__name__)  # Flask 앱 인스턴스를 생성합니다.

@app.route('/led_control')  # '/led_control' 경로에 대한 라우트를 정의합니다.
def led_control():
    return render_template('led_control.html')  # 'led_control.html' 템플릿을 렌더링하여 반환합니다.

@app.route('/led_control_act', methods=['GET'])  # '/led_control_act' 경로에 대한 GET 요청을 처리하는 라우트를 정의합니다.
def led_control_act():
    if request.method == 'GET':  # 요청이 GET일 경우
        status = ''  # 상태 변수를 초기화합니다.
        led = request.args["led"]  # URL 쿼리 매개변수에서 'led' 값을 가져옵니다.
        if led == '1':  # 'led' 값이 '1'일 경우
            GPIO.output(LED, True)  # LED를 켭니다.
            status = 'ON'  # 상태를 'ON'으로 설정합니다.
        else:  # 'led' 값이 '1'이 아닐 경우
            GPIO.output(LED, False)  # LED를 끕니다.
            status = 'OFF'  # 상태를 'OFF'로 설정합니다.
    return render_template('led_control.html', ret=status)  # 'led_control.html' 템플릿을 렌더링하며 상태를 전달합니다.

if __name__ == '__main__':  # 이 파일이 메인 프로그램으로 실행될 때
    app.run(debug=True, port=80, host='0.0.0.0')  # 디버그 모드로 포트 80에서 모든 호스트에서 앱을 실행합니다.
