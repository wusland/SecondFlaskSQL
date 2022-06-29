from flask import Flask, request, render_template, g, url_for, redirect
import sqlite3 as sql

app = Flask(__name__)
DATABASE = 'database.db'

# @app.before_first_request
# def db_init():
#     con=sql.connect('database.db')
#     c=con.cursor()


def connect_db():
    return sql.connect(DATABASE)


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/addnew', methods=['POST', 'GET'])
def addnew():
    msg = ''
    if request.method == 'POST':
        try:
            c = g.db.cursor()
            name = request.form['name']
            ID = request.form['ID']
            gender = request.form['gender']
            GPA = request.form['GPA']

            # 不为空
            if name == '' or gender == '' or ID == '' or GPA == '':
                raise(1)
            c.execute(
                'INSERT INTO students(name,ID,gender,GPA) VALUES (?,?,?,?)', (name, ID, gender, GPA))
            g.db.commit()
            msg = '成功添加数据'
        except:
            msg = '添加数据失败'
        return render_template('addnew.html', msg=msg)
    else:
        return render_template('addnew.html', msg=msg)


@app.route('/show', methods=['GET', 'POST'])
def show():
    c = g.db.cursor()
    if request.method == 'POST':
        c.execute()

    c.execute('SELECT * FROM students')
    rows = c.fetchall()
    # for row in rows:
    #     print(row)
    return render_template('show.html', rows=rows)


@app.route("/delete/<ID>")
def delete(ID):
    c = g.db.cursor()
    c.execute('delete from students where ID='+ID)
    g.db.commit()
    return show()


@app.route("/update/<ID>", methods=['GET', 'POST'])
def update(ID):
    msg = ''

    if request.method == 'POST':
        try:
            c = g.db.cursor()
            name = request.form['name']
            # ID = request.form['ID']
            gender = request.form['gender']
            GPA = request.form['GPA']

            # 不为空
            if name == '' or gender == '' or ID == '' or GPA == '':
                raise(1)
            c.execute(
                'UPDATE students SET name="%s", gender="%s", GPA="%s" WHERE ID=%s' %
                (name, gender, GPA, ID))
            g.db.commit()
            msg = '成功修改数据'
        except:
            msg = '修改数据失败'

        return render_template("update.html", ID=ID, msg=msg)
    else:
        return render_template("update.html", ID=ID, msg=msg)


@app.route('/show/search', methods=['GET', 'POST'])
def show_search():
    context = request.form['search']
    c = g.db.cursor()
    c.execute('SELECT * FROM students WHERE name LIKE "%'+context+'%"')
    rows = c.fetchall()
    # for row in rows:
    #     print(row)
    return render_template('show.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
