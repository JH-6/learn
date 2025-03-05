from flask import Blueprint, session, render_template

blog_bp = Blueprint('blog', __name__, template_folder='templates', static_folder='static')

# @blog_bp.route('/blog')
# def index():
#     return 'Blog Home Page'
#
# @blog_bp.route('/post/<int:post_id>')
# def post(post_id):
#     return f'Viewing post {post_id}'


@blog_bp.route('/blog')
def index():
    if 'user' in session:
        username = session['user']['username']
        return f'Welcome, {username}! This is your Blog Home Page'
    else:
        return 'Welcome to the Blog Home Page'

@blog_bp.route('/profile')
def profile():
    if 'user' in session:
        username = session['user']['username']
        return f'Hello, {username}! This is your Profile Page'
    else:
        return 'Please login to view your Profile'


@blog_bp.route('/about')
def about():
    return render_template('about.html')

