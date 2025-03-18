from flask import Flask, jsonify

app = Flask(__name__)
app.config["SECRET_KEY"] = "my SECRET KEY"


@app.before_request
def before_request():
    """
    这个钩子会在每次客户端访问视图的时候执行
    # 可以在请求之前进行用户的身份识别，以及对于本次访问的用户权限等进行判断。..
    """
    print("----before_request----")
    print("每一次接收到客户端请求时,执行这个钩子方法")
    print("一般可以用来判断权限,或者转换路由参数或者预处理客户端请求的数据")


@app.after_request
def after_request(response):
    print("----after_request----")
    print("在处理请求以后,执行这个钩子方法")
    print("一般可以用于记录会员/管理员的操作历史,浏览历史,清理收尾的工作")

    response.headers["Content-Type"] = "application/json"
    response.headers["Company"] = "python.Edu..."

    # 必须返回response参数
    return response


@app.teardown_request
def teardown_request(exc):
    print("----teardown_request----")
    print("在每一次请求以后,执行这个钩子方法")
    print("如果有异常错误,则会传递错误异常对象到当前方法的参数中")
    # 在项目关闭了DEBUG模式以后，则异常信息就会被传递到exc中，我们可以记录异常信息到日志文件中
    print(f"错误提示：{exc}")  # 异常提示


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Page not found"}), 404

@app.route('/')
def index():
    print("-----------视图函数执行了---------------")
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)

