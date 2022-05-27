from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required #neni mozne pristoupit na home page pokud neni logged in
def home():
    # show all todos
    todo_list = Note.query.all()
    return render_template('home.html', todo_list=todo_list, user=current_user)


@views.route("/add", methods=["POST"])
def add():
    # add new item
    title = request.form.get('title')  #titulek ziska z home.html formu
    new_todo = Note(data=title, complete=False, user_id=current_user.id)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("views.home"))  #presmeruje po dokonceni na home - show all todos


@views.route("/update/<int:todo_id>")
def update(todo_id):
    # update status of item
    todo = Note.query.filter_by(id=todo_id).first()
    todo.complete= not todo.complete
    db.session.commit()
    return redirect(url_for("views.home"))  #presmeruje po dokonceni na home - show all todos


@views.route("/delete/<int:todo_id>")
def delete(todo_id):
    # delete item
    todo = Note.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("views.home"))  #presmeruje po dokonceni na home - show all todos
