from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Set a secret key for flashing messages

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "77Pr@bhu77"
app.config['MYSQL_DB'] = "hoteldb1"

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])


def index():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login WHERE email = %s", (email,))
        user_tuple = cur.fetchone()  # Fetch the row as a tuple
        cur.close()

        if user_tuple is not None:
            stored_password = user_tuple[1]  # Access password using index
            if password == stored_password:
                session['logged_in'] = True
                flash("Login successful!", "success")
                return redirect(url_for('index'))
            else:
                flash("Incorrect password.", "error")
        else:
            flash("Email not found.", "error")

    return render_template('index.html')

@app.route('/home')
def home():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        flash("You need to log in first.", "error")
        return redirect(url_for('index'))


@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if request.method == 'POST':
        roomid = request.form['roomid']
        roomtype = request.form['roomtype']
        bedtype = request.form['bedtype']
        price = request.form['price']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO rooms (roomid, roomtype, bedtype, price) VALUES (%s, %s, %s, %s)",
                       (roomid, roomtype, bedtype, price))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('home'))  # Redirect to home page

    return render_template('add_room.html')




@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        cid = request.form['cid']
        cname = request.form['cname']
        phno = request.form['phno']
        email = request.form['email']
        nationality = request.form['nationality']
        idtype = request.form['idtype']
        idnumber = request.form['idnumber']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO customer (cid, cname, phno, email, nationality, idtype, idnumber) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (cid, cname, phno, email, nationality, idtype, idnumber))
        

        return redirect(url_for('home'))  # Redirect to home page

    return render_template('add_customer.html')


@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    if request.method == 'POST':
        reservationid = request.form['reservationid']
        noofguests = request.form['noofguests']
        cid = request.form['customerid']
        roomid = request.form['roomid']
        checkindate = request.form['checkin']
        checkoutdate = request.form['checkout']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO reservation (reservationid, noofguests, cid, roomid, checkindate, checkoutdate) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (reservationid, noofguests, cid, roomid, checkindate, checkoutdate))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('home'))  # Redirect to home page
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT roomid, roomtype, bedtype FROM rooms WHERE roomid NOT IN (SELECT roomid FROM reservation)")
    available_rooms = cursor.fetchall()
    cursor.close()

    return render_template('make_reservation.html', available_rooms=available_rooms)

@app.route('/reservation_data')
def reservation_data():
    # Execute a SQL query to join customer and reservation data based on cid
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT 
            r.reservationid, r.noofguests, c.cname, c.phno, r.roomid, r.checkindate, r.checkoutdate
        FROM 
            reservation r
        JOIN 
            customer c ON r.cid = c.cid
    """)
    data = cursor.fetchall()
    cursor.close()
    
    return render_template('reservation_data.html', data=data)




if __name__ == "__main__":
    app.run(debug=True)