import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort 

#make flask app
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = "secret"

#get sql connection
def get_db_connection():
    #create connection
    conn = sqlite3.connect('reservations.db')

    #allow name-based access to columns
    #return rows like python dict
    conn.row_factory = sqlite3.Row

    #return connection
    return conn

#get the reservation code based on the pattern
def get_reservation_code(firstName):
    pattern = "INFOTC4320"
    code = ""

    min_len = min(len(firstName), len(pattern))

    #Make the letters intertwine
    for i in range(min_len):
        code += firstName[i] + pattern[i]
    
    #make sure the whole patter is used even if the name isn't the same length
    if len(pattern) > len(firstName):
        code += pattern[len(firstName):]
    
    return code

#use app.route() to create index.html view function
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/', methods=['GET', 'POST'])
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

@app.route('/reservations/', methods=['GET', 'POST'])
def reservations():

    conn = get_db_connection()

    #load reservations and build seating chart
    existing = conn.execute('SELECT seatRow, seatColumn FROM reservations').fetchall()

    #seating chart
    Rows = 12
    Columns = 4

    chart = [["O" for _ in range(Columns)] for _ in range(Rows)]

    for seat in existing:
        r = seat["seatRow"]
        c = seat["seatColumn"]
        chart[r][c] = "X"

    successMessage = None

    if request.method== 'POST':

        #get the passenger's info
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        seatRow = request.form['seatRow']
        seatColumn = request.form['seatColumn']

        if not firstName or not lastName:
            flash("first and last name required")
            return redirect(url_for('reservations'))
        
        if not seatRow or not seatColumn:
            flash("You must select both a seat row and seat column")
            conn.close()
            return redirect(url_for('reservations'))

        rows = int(seatRow)
        columns = int(seatColumn)

        taken = conn.execute('SELECT * FROM reservations WHERE seatRow=? AND seatColumn=?', (rows, columns)).fetchone()

        if taken:
            flash(f"Row: {rows+1} Seat: {columns+1} was already reserved, select another.")
            return redirect(url_for('reservations'))
        
        reservationCode = get_reservation_code(firstName)
        
        conn.execute('INSERT INTO reservations (passengerName, seatRow, seatColumn, eTicketNumber) VALUES (?,?,?,?)', (firstName +" "+lastName, seatRow, seatColumn, reservationCode))
        conn.commit()

        successMessage = (f"Congradulations {firstName}! Row: {rows+1}, Seat: {columns+1} is now reserved for you. Enjoy your trip!"
        f"Your eticket number is: {reservationCode}")

        conn.close()

    return render_template('reservations.html', chart=chart, successMessage=successMessage)

app.run()