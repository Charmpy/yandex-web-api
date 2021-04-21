from data import db_session
import os
from data.users import User
from data.departments import Departments
from flask import Flask, redirect, render_template, request, abort
from data.jobs import Jobs
from forms.user import RegisterForm
from forms.login import LoginForm
from forms.job import JobForm
from forms.department import DepartmentForm

from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/mars_explorer.sqlite")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # db_sess = db_session.create_session()
    # db_sess.commit()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    return render_template("index.html", title='Миссия')


@app.route("/jobs_list")
def jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("jobs.html", jobs=jobs, title='Jobs')


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
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/job_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/jobs_list')


@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.title.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.category = form.category.data
        job.is_finished = form.is_finished.data
        db_sess.merge(current_user)
        db_sess.add(job)
        db_sess.commit()
        return redirect('/jobs_list')
    return render_template('jobs_form.html', title='Добавление работы',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         ((
                                              bool(1 == current_user.id)
                                         ) | (
                                              bool(
                                                  Jobs.team_leader == current_user.id
                                              )
                                         )
                                         )).first()
        if job:
            form.team_leader.data = job.team_leader
            form.title.data = job.job
            form.work_size.data = job.work_size
            form.collaborators.data = job.collaborators
            form.category.data = job.category
            form.is_finished.data = job.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == id,
                                         ((
                                            bool(1 == current_user.id)
                                         ) | (
                                            bool(Jobs.team_leader == current_user.id)
                                         )
                                         )).first()
        if job:
            job.team_leader = form.team_leader.data
            job.job = form.title.data
            job.work_size = form.work_size.data
            job.collaborators = form.collaborators.data
            job.category = form.category.data
            job.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/jobs_list')
        else:
            abort(404)
    return render_template('jobs_form.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route("/departments_list")
def departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Departments).all()
    print(departments)
    return render_template("departments.html", departments=departments, title='Departments')


@app.route('/departments',  methods=['GET', 'POST'])
@login_required
def add_dep():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        dep = Departments()

        dep.title = form.title.data
        dep.chief = form.chief.data
        dep.members = form.members.data
        dep.email = form.email.data

        db_sess.merge(current_user)
        db_sess.add(dep)
        db_sess.commit()
        return redirect('/departments_list')
    return render_template('departments_form.html', title='Добавление департамента',
                           form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_dep(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        dep = db_sess.query(Departments).filter(Departments.id == id,
                                         ((
                                              bool(1 == current_user.id)
                                         ) | (
                                              bool(
                                                  Departments.chief == current_user.id
                                              )
                                         )
                                         )).first()
        if dep:
            form.title.data = dep.title
            form.chief.data = dep.chief
            form.members.data = dep.members
            form.email.data = dep.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = db_sess.query(Departments).filter(Departments.id == id,
                                         ((
                                            bool(1 == current_user.id)
                                         ) | (
                                            bool(Departments.chief == current_user.id)
                                         )
                                         )).first()
        if dep:
            dep.title = form.title.data
            dep.chief = form.chief.data
            dep.members = form.members.data
            dep.email = form.email.data
            db_sess.commit()
            return redirect('/departments_list')
        else:
            abort(404)
    return render_template('departments_form.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def dep_delete(id):
    db_sess = db_session.create_session()
    dep = db_sess.query(Departments).filter(Departments.id == id,
                                      Departments.user == current_user
                                      ).first()
    if dep:
        db_sess.delete(dep)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments_list')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


if __name__ == '__main__':
    main()
