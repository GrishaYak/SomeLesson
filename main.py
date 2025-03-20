from flask import Flask, render_template, redirect, make_response, jsonify
from data.users import User
from data.news import News
from forms.user import RegisterForm
from data.jobs import Jobs
from datetime import datetime
from data import db_session, news_api


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def add_some_guys():
    db_sess = db_session.create_session()
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    db_sess.add(user)

    user = User()
    user.name = "Grisha"
    user.surname = "Yakushevskiy"
    user.address = "TopSecret"
    user.age = int(1e9)
    db_sess.add(user)

    user = User()
    user.surname = "Smit"
    user.name = "John"
    user.age = 0
    user.speciality = "Aliens-Fighter"
    db_sess.add(user)

    user = User()
    user.name = "WhoAmI"
    user.surname = "?"
    user.speciality = "thinker"
    user.address = "HisOwnMind"
    user.age = -1
    db_sess.add(user)

    cptn = Jobs()
    cptn.team_leader = 1
    cptn.job = "deployment of residential modules 1 and 2"
    cptn.work_size = 15
    cptn.collaborators = "2, 3"
    cptn.start_date = datetime.now()
    cptn.is_finished = False
    db_sess.add(cptn)

    db_sess.commit()


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(news_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
