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
    return "<h1>IT-4320 Trip Reservation System</h1>"

app.run()