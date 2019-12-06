from flask import Flask, render_template, request, redirect, url_for,session
from sqlalchemy import text

import config
from app.decorator import login_required
from app.model import User, Posts, Comment
from exts import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'postses': Posts.query.order_by(text('-create_time')).all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        usernumber = request.form.get('usernumber')
        password = request.form.get('password')
        user = User.query.filter(User.usernumber == usernumber, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # setting the function of no require login for 31 days
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return 'Error on User Number or Password, Please check and try again'


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        usernumber = request.form.get('usernumber')
        username = request.form.get('username')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')

    # make sure the usernumber is unique
        user = User.query.filter(User.usernumber == usernumber).first()
        if user:
            return 'This user number has been registered, please choose another one!'
        else:
            # password and password comfirmed is equal
            if password != cpassword:
                return 'The two passwords are not equal, please check and fill in again!'
            else:
                user = User(usernumber=usernumber, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                # register successful, jump to the login page
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/sendpost/', methods=['GET', 'POST'])
@login_required
def sendpost():
    if request.method == 'GET':
        return render_template('sendpost.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        posts = Posts(title=title, content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        posts.author = user
        db.session.add(posts)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<posts_id>')
def detail(posts_id):
    posts = Posts.query.filter(Posts.id == posts_id).first()
    comment_number = len(posts.comments)
    return render_template('detail.html', posts=posts, comment_number=comment_number)


@app.route('/comment/', methods=['POST'])
@login_required
def add_comment():
    content = request.form.get('comment_content')
    posts_id = request.form.get('posts_id')

    comment = Comment(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    comment.author = user
    posts = Posts.query.filter(Posts.id == posts_id).first()
    comment.posts = posts
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', posts_id=posts_id))


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
