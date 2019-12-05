from flask import Flask, render_template, request, redirect, url_for,session
import config
from app.model import User
from exts import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


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


@app.route('/sendpost/')
def sendpost():
    if request.method == 'GET':
        return render_template('sendpost.html')
    else:
        pass

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
