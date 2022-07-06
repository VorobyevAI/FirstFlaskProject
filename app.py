from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
from flask_sqlalchemy import SQLAlchemy
from  datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'fa34wq23dq45dq5q3wdw32'
db = SQLAlchemy(app)
ROLE_USER = 0
ROLE_ADMIN = 1


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posts = db.Column(db.String(30), nullable=False)
    date = db.Column(db.DateTime, default=datetime.today())


    def __repr__(self):
        return '<Users %r>' % (self.id)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), index=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return '<Users %r>' % (self.id)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True, nullable=False)
    article = db.Column(db.String(20), index=True)

    def __repr__(self):
        return '<Users %r>' % (self.id)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(20), index=True)
    text = db.Column(db.TEXT, nullable=False)

    def __repr__(self):
        return '<Users %r>' % (self.id)


@app.route('/index')
@app.route('/')
def index():
    user = Users.query.order_by(Users.username.desc()).all()
    return render_template('index.html', user=user)


@app.route('/about/<int:id>/delete')
def user_del(id):
    user = Users.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/about')
    except:
        return 'При удаление пользователя'


@app.route('/about', )
def about():
    user = Users.query.order_by(Users.username.desc()).all()
    return render_template('about.html', user=user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    user = Users.query.order_by(Users.username.desc()).all()
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'andrey' and request.form['password'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html')


@app.route('/exit')
def exit():
    if 'userLogged' in session:
        del session['userLogged']
        return redirect(url_for('index'))

    else:
        return "Вы не вошли "




@app.route('/regist', methods=['POST', 'GET'])
def regist():


    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        if len(username) <= 6 and len(password) <= 6:
            flash('Произошла ошибка при отправке', category='nenorm')
            return redirect('/regist')
        else:
            flash('Сообщение отправлено', category='norm')

            user = Users(username=username, password=password)

            try:
                db.session.add(user)
                db.session.commit()
                return redirect('/about')

            except:
                return 'ПРИ ДОБАВЛЕНИи СТАТЬИ ПРОИЗОШЛА ОШИБКА'

    else:
        return render_template('/regist.html')


@app.route('/profile/<username>')
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(404)
    else:
        return render_template('profile.html', username=username)


if __name__ == '__main__':
    app.run(debug=True)