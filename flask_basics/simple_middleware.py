from flask import Flask

app = Flask(__name__)

# 定义一个简单的 WSGI 中间件
class SimpleMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # 请求预处理
        print("Before request processing")

        # 调用原始的 Flask 应用
        response = self.app(environ, start_response)

        # 响应后处理
        print("After request processing")
        return response

# 将中间件应用到 Flask 应用
app.wsgi_app = SimpleMiddleware(app.wsgi_app)


if __name__ == '__main__':
    app.run(debug=True)


