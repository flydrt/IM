from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db
from models import User, Friend, Message, Group
from forms import LoginForm, RegisterForm, ProfileForm, SearchForm


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password!')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Register success!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.signature = form.signature.data
        current_user.introduction = form.introduction.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your changes have been save')
        return redirect(url_for('profile'))
    form.signature.data = current_user.signature
    form.introduction.data = current_user.introduction
    return render_template('edit_profile.html', form=form)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            return redirect(url_for('add', username=user.username))
        flash('The user does not exist!')
    return render_template('search.html', form=form)


@app.route('/add/<username>')
@login_required
def add(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('The user does not exist!')
        return redirect(url_for('index'))
    return render_template('add.html', user=user)


@app.route('/add-contact/<username>')
@login_required
def add_contact(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('The user does not exist!')
        return redirect(url_for('search'))
    if username == current_user.username:
        flash('Can not add yourself!')
        return redirect(url_for('search'))

    friend = Friend.query.filter_by(uid=current_user.id, fid=user.id).first()
    if friend is not None:
        flash('You have already added the contact!')
        return redirect(url_for('search'))
    friend = Friend(uid=current_user.id, fid=user.id)
    friend2 = Friend(uid=user.id, fid=current_user.id)
    db.session.add(friend)
    db.session.add(friend2)
    db.session.commit()
    flash('Add success!')
    return redirect(url_for('index'))


@app.route('/list')
@login_required
def list():
    list = []
    for friend in Friend.query.filter_by(uid=current_user.id).all():
        user = User.query.filter_by(id=friend.fid).first()
        list.append(user.username)
    return render_template('list.html', list=list)


@app.route('/chat/<name>')
@login_required
def chat(name):
    friend = User.query.filter_by(username=name).first()
    if friend is None:
        flash('The user does not exist!')
        return redirect(url_for('list'))

    result = Friend.query.filter_by(uid=current_user.id, fid=friend.id).first()
    if result is None:
        flash('The user is not your friend!')
        return redirect(url_for('list'))

    set_room_map(current_user.id, friend.id)
    return render_template('chat.html', user=current_user, friend=friend)


roomMap = {}


def set_room_map(id1, id2):
    if id1 < id2:
        roomMap[id1] = str(id1) + str(id2)
    else:
        roomMap[id1] = str(id2) + str(id1)