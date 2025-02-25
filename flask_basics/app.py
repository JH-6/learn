from flask import Flask, url_for, render_template, request, redirect, flash
from markupsafe import escape
app = Flask(__name__)



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
@app.route('/hello/<name>')
def say_hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            print("用户名或密码为空!")
            return render_template('login.html')

        print(f'用户名: {username}, 密码: {password}')
        if username == 'admin' and password == '123':
            return render_template('index.html', name=username)

    return render_template('login.html')


