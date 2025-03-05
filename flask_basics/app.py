from flask import Flask, url_for, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from markupsafe import escape
import os
app = Flask(__name__)

# 设置 SECRET_KEY 用于 CSRF 保护
# app.secret_key = 'jh6 secret key'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'jh6 secret key')



"""
url规则
"""
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

    print(url_for('static', filename='css/style.css'))

    return f'User: {escape(name)} '

@app.route('/hello/')
@app.route('/hello/<name>')
def say_hello(name=None):
    return render_template('hello.html', name=name)



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/me")
def me_api():
    return {
        "username": 'jh6',
        "age":  0
    }


# ## The Request Object和简易表单登录
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#
#         if not username or not password:
#             flash('必填项输入为空.')
#             return redirect(url_for('login'))
#
#         if username == 'jh6' and validate_password(password):
#             flash('登录成功')
#             return render_template('index.html', name=username)
#
#         flash('用户名或密码错误')
#         return redirect(url_for('login'))
#
#     return render_template('login.html')
#
# def validate_password(password):
#     my_password = generate_password_hash('123')
#     return check_password_hash(my_password, password)
#
# # 上传文件
# UPLOAD_FOLDER = 'uploads'
# if not os.path.exists(UPLOAD_FOLDER):
#     os.mkdir(UPLOAD_FOLDER)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if 'file' not in request.files:
#         flash('无上传文件！')
#         return render_template('index.html', name='jh6')
#     file = request.files['file']
#
#     # 如果用户没有选择文件，浏览器也会提交一个空文件名
#     if file.filename == '':
#         flash('请选择上传文件！')
#         return render_template('index.html', name='jh6')
#
#     if file and allowed_file(file.filename):
#         filename = file.filename
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         flash('文件上传成功！')
#     else:
#         flash('不允许的文件类型，请上传 txt、pdf、png、jpg、jpeg 或 gif 文件。')
#     return render_template('index.html', name='jh6')


"""
Flask-WTF
练习 
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField(
    '邮箱',
        validators=[
            DataRequired(message='邮箱不能为空'),
            Email(message='无效的邮箱格式')
        ]
    )
    password = PasswordField(
        '密码',
        validators=[
            DataRequired(message='密码不能为空'),
            Length(min=6, message='密码至少6位')
        ]
    )
    submit = SubmitField('登录')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # 自动处理 POST 并验证
        # 获取表单数据
        email = form.email.data
        password = form.password.data

        # 这里可以添加数据库验证逻辑
        print(f'email: {email}, password: {password}')
        flash('登录成功！', 'success')
        # return redirect(url_for('index'))
        return render_template('index.html', form=form)

    # 验证失败或 GET 请求时渲染模板
    flash('验证失败！')
    return render_template('login.html', form=form)



# flask-wtf 上传文件
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = 'uploads'  # 文件上传保存路径
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 限制上传文件大小为 2MB

# 确保上传目录存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


class UploadForm(FlaskForm):
    file = FileField('选择文件', validators=[
        FileRequired(message='请选择要上传的文件'),  # 必须选择文件
        FileAllowed(['jpg', 'png', 'jpeg', 'txt'], message='仅支持 JPG/PNG 图片和txt文本'),  # 允许的文件类型
        FileSize(max_size=app.config['MAX_CONTENT_LENGTH'], message='文件不超过2MB')
    ])
    submit = SubmitField('上传文件')

# 处理文件上传的路由
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        # 获取上传的文件对象
        uploaded_file = form.file.data

        # 安全处理文件名（防止路径遍历攻击）
        filename = secure_filename(uploaded_file.filename)

        # 保存文件到指定目录
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(file_path)

        flash(f'文件 {filename} 上传成功！', 'success')
        return redirect(url_for('upload_file'))

    if request.method == 'POST' and not form.validate():
        flash('文件上传失败，请检查格式和大小', 'danger')

    return render_template('upload.html', form=form)



"""
cookie
"""
from flask import make_response
@app.route('/set_cookie')
def set_cookie():
    # 创建响应对象
    resp = make_response('Cookie 已设置')
    resp.set_cookie('username', 'jh6', max_age=3600)
    return resp

@app.route('/get_cookie')
def get_cookie():
    # 从请求中获取名为 'username' 的 cookie 值
    username = request.cookies.get('username')
    if username:
        return f'读取到的 username cookie 值为: {username}'
    else:
        return '未找到 username cookie'

@app.route('/delete_cookie')
def delete_cookie():
    resp = make_response('Cookie 已删除')
    # 将 'username' cookie 的过期时间设置为 0，即立即删除
    resp.set_cookie('username', '', expires=0)
    return resp


"""
errors
"""
from flask import abort
@app.route('/error')
def show_error():
    abort(401)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404


"""
日志
"""
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


# # 配置基础日志
# logging.basicConfig(
#     level=logging.DEBUG,  # 设置日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('logs/app.log'),  # 输出到文件
#         logging.StreamHandler()          # 输出到控制台
#     ]
# )
#
# # 按文件大小轮转（每个文件最大 1MB，保留 3 个备份）
# size_handler = RotatingFileHandler(
#     'app.log',
#     maxBytes=1024 * 1024,
#     backupCount=3,
#     encoding='utf-8'
# )
#
# # 按时间轮转（每天轮转一次，保留 7 天日志）
# time_handler = TimedRotatingFileHandler(
#     'app.log',
#     when='D',
#     interval=1,
#     backupCount=7,
#     encoding='utf-8'
# )
#
# app.logger.addHandler(size_handler)
# app.logger.setLevel(logging.INFO)


# 文件处理器（按大小轮转）
file_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=1024 * 1024,
    backupCount=5,
    encoding='utf-8'
)
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
file_handler.setLevel(logging.INFO)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 添加处理器
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)

@app.route('/logs')
def logs():
    app.logger.info('test!')
    return "log log"

@app.route('/error1')
def trigger_error():
    try:
        1 / 0
    except Exception as e:
        app.logger.exception('发生除零错误')  # 自动记录堆栈信息
    return "触发错误", 500


"""
session
"""
from flask import session
@app.route('/set_session')
def set_session():
    # session.permanent = True  # 启用持久化Session
    session['username'] = 'john'
    return 'Session 已设置'

@app.route('/get_session')
def get_session():
    username = session.get('username')
    if username:
        return f'读取到的 username 为: {username}'
    else:
        return '未找到 username 信息'

@app.route('/delete_session')
def delete_session():
    session.pop('username', None)
    return 'Session 中的 username 已删除'

@app.route('/clear_session')
def clear_session():
    session.clear()
    return 'Session 已清空'

# 自定义Session存储
# from flask_session import Session
# app = Flask(__name__)
# app.secret_key = 'your-secret-key'
# app.config['SESSION_TYPE'] = 'redis'  # 使用 Redis 存储
# app.config['SESSION_PERMANENT'] = True
# app.config['SESSION_USE_SIGNER'] = True  # 签名 Cookie
# app.config['SESSION_REDIS'] = 'redis://localhost:6379/0'
# Session(app)

"""
蓝图
"""
from blueprints.auth import auth_bp
from blueprints.blog import blog_bp

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(blog_bp)



"""
SQLAlchemy
"""



