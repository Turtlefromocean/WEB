from flask import Flask, render_template

app = Flask(__name__)


@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js'), 200, {'Content-Type': 'text/javascript'}


@app.route('/')
def home():
    return render_template('index.html')


# 인터넷 연결되면 뜨는 페이지
@app.route('/some-other-page')
def other_page():
    return render_template('other-page.html')


@app.route('/offline.html')
def offline():
    return app.send_static_file('offline.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)