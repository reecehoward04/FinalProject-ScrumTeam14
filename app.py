import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort 

#make flask app
app = Flask(__name__)
app.config['DEBUG'] = True

#get sql connection
def get_db_connection():
    #create connection
    conn = sqlite3.connect('reservations.db')

    #allow name-based access to columns
    #return rows like python dict
    conn.row_factory = sqlite3.Row

    #return connection
    return conn

#use app.route() to create index.html view function
@app.route('/')
def index():

    #return index.html
    return render_template('index.html')

@app.route('/admin/', methods=('GET', 'POST'))
def admin():

    #determine get or post request
    if request.method== 'POST':

        username = request.form['username']
        password = request.form['password']

        #check db for admin
        conn = get_db_connection()
        admin = conn.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()

        #display error if username or password are incorrect based on db
        if admin is None:
            flash("Invalid username or password")
            return redirect(url_for('admin'))
        
    return render_template('admin.html')

app.run()