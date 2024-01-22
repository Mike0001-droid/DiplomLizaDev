from flask import Flask, render_template, url_for, request, flash, g, abort
import sqlite3
import os
from DataBase import DataBase
#Конфигурация 
DATABASE = '/tmp/database.db'
DEBUG = True
SECRET_KEY = 'gadsgsf123&81230><asd,'
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route("/")
def index():
    db = get_db()
    dbase = DataBase(db)
    return render_template('index.html', menu = dbase.getMenu())

@app.route("/auth")
def auth():
    return render_template('authorization.html')


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено')
        else:
            flash('Ошибка отправки')
    return render_template('contact.html')

@app.route("/add_post", methods= ["POST", "GET"])
def addPost():
    db = get_db()
    dbase = DataBase(db)
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Ошибка добавления статьи', category= 'error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=dbase.getMenu(), title="Добавление статьи")


@app.route("/update_status", methods= ["POST", "GET"])
def updateStatus():
    db = get_db()
    dbase = DataBase(db)
    if request.method == "POST":
        res = dbase.updateStatus(request.form['statuss'])
        if not res:
            flash('Ошибка обновления статуса', category= 'error')
        else:
            flash('Статус успешно обновлен', category='success')
    else:
        flash('Ошибка обновления статуса', category='error')
    return render_template('admin.html', menu=dbase.getMenu())


@app.route("/post/<int:id_post>")
def showPost(id_post):
    db = get_db()
    dbase = DataBase(db)
    title, content = dbase.getPost(id_post)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, content=content)


if __name__ == "__main__":
    app.run(debug=True) 