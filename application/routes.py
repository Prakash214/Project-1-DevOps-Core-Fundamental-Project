from application import app, db
from application.models import *
from datetime import date, timedelta
from flask import request, redirect, url_for, render_template
from application.forms import *

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/view-animes')
def view_all_animes():
    animes = Anime.query.all()
    return render_template('view_all.html', entity='Anime', animes=animes)

@app.route('/add-anime', methods=['GET', 'POST'])
def add_new_anime():
    form = AnimeForm()
    users = User.query.all()
    form.assigned_to.choices = [(user.uid, f"{user.username}") for user in users]
    if form.validate_on_submit():
        anime_name = form.anime_name.data
        anime_desc = form.anime_desc.data
        released_date = form.released_date.data
        uid = form.assigned_to.data
        anime_status = form.anime_status.data
        new_anime = Anime(anime_name=anime_name, anime_desc=anime_desc, anime_status=anime_status, released_date=released_date, assigned_to=uid)
        db.session.add(new_anime)
        db.session.commit()
        return redirect(url_for('view_all_animes'))
    form.released_date.data = date.today()
    errors = form.released_date.errors
    errors += form.anime_name.errors
    return render_template('anime_form.html', form = form, errors = errors)

@app.route('/update-anime/<int:id>', methods=['GET', 'POST'])
def update_anime(id):
    anime_to_update = Anime.query.get(id)
    form = AnimeForm()
    users = User.query.all()
    form.assigned_to.choices = [(user.uid, f"{user.username}") for user in users]
    if form.validate_on_submit():
        anime_to_update.anime_name = form.anime_name.data
        anime_to_update.anime_desc = form.anime_desc.data
        anime_to_update.released_date = form.released_date.data
        anime_to_update.status = form.anime_status.data
        anime_to_update.assigned_to = form.assigned_to.data
        db.session.commit()
        return redirect(url_for('view_all_animes'))
    form.anime_name.data = anime_to_update.anime_name
    form.anime_desc.data = anime_to_update.anime_desc
    form.released_date.data = anime_to_update.released_date
    return render_template('anime_form.html', form=form)

@app.route('/delete-anime/<int:id>')
def delete_anime(id):
    anime_to_delete = Anime.query.get(id)
    db.session.delete(anime_to_delete)
    db.session.commit()
    return redirect(url_for('view_all_animes'))

@app.route('/view-users')
def view_all_users():
    users = User.query.all()
    return render_template('view_all.html', entity='User', animes=users)

@app.route('/get-user-by-id/<int:id>')
def get_user_by_id(id):
    user = User.query.get(id)
    return render_template('view_all.html', user_string=str(user))


@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('view_all_users'))
    return render_template('user_form.html', form=form)

@app.route('/update-user/<int:id>', methods = ['GET', 'POST'])
def update_user(id):
    user_to_update = User.query.get(id)
    form = UserForm()
    if form.validate_on_submit():
        username= form.username.data
        user_to_update.username = username
        db.session.commit()
        return redirect(url_for('view_all_users'))
    form.username.data = user_to_update.username
    return render_template('user_form.html', form=form)

@app.route('/delete-user/<int:id>')
def delete_user(id):
    user_to_delete = User.query.get(id)
    for anime in user_to_delete.animes:
        db.session.delete(anime)
    db.session.delete(user_to_delete)
    db.session.commit()
    return redirect(url_for('view_all_users'))