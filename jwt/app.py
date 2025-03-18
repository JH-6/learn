from flask import Flask,request,jsonify
from util import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "reqweqwcasd!#$%456421&^%&^%"


@app.route('/testLogin', methods=["POST"])
def test_login():
    """
    登陆成功获取到数据获取token和刷新token
    :return:
    """
    obj = request.get_json(force=True)
    name = obj.get("name")
    if not obj or not name:
        return "参数错误"

    if name == "qin":
        access_token = generate_access_token(user_name=name)
        refresh_token = generate_refresh_token(user_name=name)
        data = {"access_token": access_token.encode("utf-8").decode("utf-8"),
        "refresh_token": refresh_token.encode("utf-8").decode("utf-8")}
        return jsonify(data)
    else:
        return "用户名或密码错误"


@app.route('/testGetData', methods=["GET"])
@login_required
def test_get_data():
    """
    测试登陆保护下获取数据
    :return:
    """
    name = session.get("user_name")

    return "{}，你好！！".format(name)


@app.route('/testRefreshToken', methods=["GET"])
def test_refresh_token():
    """
    刷新token，获取新的数据获取token
    :return:
    """
    refresh_token = request.args.get("refresh_token")
    if not refresh_token:
        return "参数错误"
    payload = decode_auth_token(refresh_token)
    if not payload:
        print(payload)
        print("111")
        return "请登陆"
    if "user_name" not in payload:
        print("user_name")
        print("222")
        return "请登陆"
    access_token = generate_access_token(user_name=payload["user_name"])
    data = {"access_token": access_token.encode("utf-8").decode("utf-8"), "refresh_token": refresh_token}
    return jsonify(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)

