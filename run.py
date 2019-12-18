import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import text, null

from app.forms import LoginForm, RegisterForm, NewPassword, AddComment

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


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', form=LoginForm())
    else:
        form = LoginForm(request.form)
        usernumber = form.usernumber.data
        password = form.password.data
        auto = request.form.get('auto_login')
        user = User.query.filter(User.usernumber == usernumber, User.password == password).first()
        if user:
            session['user_id'] = user.id
            if auto == 'on':
                # setting the function of no require login for 31 days
                session.permanent = True
            else:
                session.permanent = False
            return redirect(url_for('index'))
        else:
            flash('Error on User Number or Password, Please check and try again')
            return render_template('login.html', form=LoginForm())


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', form=RegisterForm())
    else:
        form = RegisterForm(request.form)
        usernumber = form.usernumber.data
        username = form.username.data
        password = form.password.data
        cpassword = form.cpassword.data
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
        sub_title = request.form.get('subtitle')
        content = request.form.get('content')
        posts = Posts(title=title, content=content, sub_title=sub_title)
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
    return render_template('detail.html', posts=posts, comment_number=comment_number, form=AddComment())


@app.route('/collect_posts/<posts_id>')
def collect(posts_id):
    add_collection = True
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    posts = Posts.query.get(posts_id)
    all_collections = user.postses.all()
    for collection in all_collections:
        if collection == posts:
            add_collection = False
            break
    if add_collection:
        user.postses.append(posts)
        db.session.add(posts)
        db.session.commit()
    return redirect(url_for('detail', posts_id=posts_id))


@app.route('/comment/', methods=['POST'])
@login_required
def add_comment():
    form = AddComment(request.form)
    content = form.content.data
    posts_id = form.posts_id.data
    comment = Comment(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    comment.author = user
    posts = Posts.query.filter(Posts.id == posts_id).first()
    comment.posts = posts
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', posts_id=posts_id))


@app.route('/personal/')
def personal():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    return render_template('Personal.html', user=user)


basedir = os.path.abspath(os.path.dirname(__file__))


@app.route('/change_personal/', methods=['POST'])
@login_required
def change_personal():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    username = request.form.get('username')
    img = request.files.get('avator')
    if img:
        path = basedir + "/static/images/"
        file_path = path + img.filename
        img.save(file_path)
        user.photo = "images/" + img.filename
    if username:
        user.username = username

    db.session.add(user)
    db.session.commit()
    return redirect(url_for('personal'))


@app.route('/change_password/', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html', form=NewPassword())
    else:
        form = NewPassword(request.form)
        user_id = session['user_id']
        user = User.query.filter(User.id == user_id).first()
        old_password = form.old_password.data
        new_password = form.new_password.data
        cpassword = form.cpassword.data
        if old_password == user.password:
            if new_password != cpassword:
                return 'The two passwords are not equal, please check and fill in again!'
            else:
                user.username = user.username
                user.password = new_password
                db.session.add(user)
                db.session.commit()
                # register successful, jump to the login page
                return redirect(url_for('personal'))
        else:
            return 'The original password is worry check out and try again!'


@app.route('/manage_comment/', methods=['GET', 'POST'])
@login_required
def manage_comment():
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        comments = {
            'comments': Comment.query.filter(Comment.author == user).order_by(text('-create_time')).all()
        }
        return render_template('manage_comment.html', **comments)
    else:
        comment_id = request.form.get('delete')
        comment = Comment.query.filter(Comment.id == comment_id).first()
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('manage_comment'))


@app.route('/manage_collections/', methods=['GET', 'POST'])
def manage_collections():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    context = {
        'postses': user.postses.all()
    }
    return render_template('manage_collections.html', **context)


@app.route('/delete_collection/<posts_id>', methods=['GET', 'POST'])
def delete_collection(posts_id):
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    post = user.postses.first()
    user.postses.remove(post)
    db.session.commit()
    return redirect(url_for('manage_collections'))


@app.route('/manage_posts/', methods=['GET', 'POST'])
def manage_posts():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    context = {
        'postses': Posts.query.filter(Posts.author == user).order_by(text('-create_time')).all()
    }
    return render_template('manage_posts.html', **context)


@app.route('/delete_posts/<posts_id>', methods=['GET', 'POST'])
def delete_posts(posts_id):
    posts = Posts.query.get(posts_id)
    comments = Comment.query.filter(Comment.posts_id == posts_id)
    for comment in comments:
        db.session.delete(comment)
    db.session.delete(posts)
    db.session.commit()
    return redirect(url_for('manage_posts'))


@app.route('/edit_posts/<posts_id>', methods=['GET', 'POST'])
def edit_posts(posts_id):
    posts = Posts.query.filter(Posts.id == posts_id).first()
    if request.method == 'GET':
        return render_template('edit_posts.html', posts=posts)
    else:
        sub_title = request.form.get('subtitle')
        content = request.form.get('content')
        if sub_title:
            posts.sub_title = sub_title
        if content:
            posts.content = content
        db.session.add(posts)
        db.session.commit()
        return redirect(url_for('manage_posts'))


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
