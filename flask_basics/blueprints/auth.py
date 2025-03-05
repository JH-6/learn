from flask import Blueprint, session

auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/login1')
# def login():
#     return 'Login Page'
#
# @auth_bp.route('/logout')
# def logout():
#     return 'Logout Page'

@auth_bp.route('/login1')
def login():
    # 模拟登录，将用户信息存储在session中
    session['user'] = {'username': 'jh6'}
    return 'Login Successful'


@auth_bp.route('/logout')
def logout():
    # 模拟登出，清除session中的用户信息
    session.pop('user', None)
    return 'Logout Successful'


