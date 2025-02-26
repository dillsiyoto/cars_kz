import sqlite3
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    session
)
import os

UPLOAD_FOLDER = 'static/img'

from models.users import start_db

app = Flask(__name__)
app.secret_key = 'parol'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

start_db()

@app.route('/', methods=['GET','POST'])
def get_main():
    conn = sqlite3.connect('post.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM post ')
    spisok:list = cursor.fetchall()
    conn.commit()
    conn.close()

    return render_template('base.html', spisok = spisok)



@app.route('/profile', methods=['GET','POST'])
def get_profile():
    login = session.get('login', 'Гость')
    return render_template('profile.html', login = login)


@app.route('/create_post', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = request.form['price']
        file = request.files['photo']

        if file:
            filename = file.filename

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

        conn = sqlite3.connect('post.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO post (title, description, price, photo_path)
            VALUES (?, ?, ?, ?)
        """, (title, description, price, file_path))

        conn.commit()
        conn.close()

        return redirect(url_for('get_main'))  

    return render_template('create_post.html')


@app.route('/log', methods=['GET', 'POST'])
def get_log():
    if request.method == 'POST':
        login = request.form.get('login', type=str)
        password = request.form.get('password', type=str)
        session[login] = request.form.get('login')
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password))
        user = cursor.fetchone()  
        if user:
            return redirect(url_for('get_main'))
        else:
            error_message = "Неверный логин или пароль"
            return render_template('log.html', error=error_message)

        conn.close()

    return render_template('log.html')


@app.route('/reg', methods=['GET','POST'])
def get_reg():
    if request.method == 'POST':
        login = request.form.get('login', type=str)
        email = request.form.get('email', type=str)
        password = request.form.get('password', type=str)
        session['login'] = request.form.get('login')
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO users (login, email, password) VALUES (?, ?, ?)', (login, email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('get_main'))

    return render_template('reg.html')


@app.route('/up', methods=['GET', 'POST'])
def get_up():
    conn = sqlite3.connect('post.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM post ORDER BY price')
    posts = cursor.fetchall()

    conn.close()
    return render_template('base.html', spisok = posts)


@app.route('/down', methods = ['GET', 'POST'])
def get_down():
    conn = sqlite3.connect('post.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM post ORDER BY price DESC')
    posts = cursor.fetchall()

    conn.close()
    return render_template('base.html', spisok = posts)


@app.route('/logout', methods=['GET', 'POST'])
def get_logout():
    session.pop('login', None)
    return redirect(url_for('get_main'))


@app.route('/post<int:id>', methods=['GET', 'POST'])
def get_details(id):
    conn = sqlite3.connect('post.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM post WHERE id = ?', (id,))
    post = cursor.fetchone()

    conn.close()
    return render_template('post.html', post = post)


@app.route('/search', methods=['GET', 'POST'])
def get_search():
    conn = sqlite3.connect('post.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM post')
    posts = cursor.fetchall()

    final = []
    search = request.form.get('search')
    for i in range(len(posts)):
        if search and ( search in posts[i][1] or search in posts[i][2]):
            final.append(posts[i])
        else:
            continue
    conn.close()

    return render_template('base.html', spisok = final)

if __name__ == '__main__':
    app.run(debug=True)