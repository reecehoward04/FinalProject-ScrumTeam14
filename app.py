#get sql connection
def get_db_connection():
    #create connection
    conn = sqlite3.connect('reservations.db')

    #allow name-based access to columns
    #return rows like python dict
    conn.row_factory = sqlite3.Row

    #return connection
    return conn