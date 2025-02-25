from flask import Flask, url_for, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
import os
app = Flask(__name__)

# 设置密钥，否则会话和消息闪现等不可用
# app.secret_key = 'jh6 secret key'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'jh6 secret key')


# URL规则
@app.route('/hello1')
@app.route('/hello2')
def hello():
    return '<h1>Hello World!</h1>'

@app.route('/name/<string:name>')
def say_name(name):
    # url_for视图函数对应的 URL
    print(url_for('hello'))
    print(url_for('hello', name='xxx'))
    print(url_for('hello', num=1))

    return f'User: {escape(name)} '

@app.route('/hello')
def say_hello(name=None):
    return render_template('hello.html', name=name)



# The Request Object和表单
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('必填项输入为空.')
            return redirect(url_for('login'))

        if username == 'jh6' and validate_password(password):
            flash('登录成功')
            return render_template('index.html', name=username)

        flash('用户名或密码错误')
        return redirect(url_for('login'))

    return render_template('login.html')


def validate_password(password):
    my_password = generate_password_hash('123')
    return check_password_hash(my_password, password)
