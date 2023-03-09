from flask import Flask, request, render_template, redirect, url_for, flash, session
import sqlite3
from datetime import timedelta

app = Flask(__name__)

app.config["SECRET_KEY"] = "ABIORH"
app.permanent_session_lifetime = timedelta(hours=1)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/signup")
def signup():
    return render_template('signup.html')


@app.route("/signup", methods=['POST'])
def signup_post():
    conn = sqlite3.connect('myphonedb.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS signup_details (
        full_name STRING NOT NULL,
        email STRING NOT NULL,
        password STRING UNIQUE NOT NULL
    )
    """)
    conn.commit()

    full_name = request.form["full_name"]
    email = request.form["email"]
    password = request.form["password"]

    c.execute("SELECT * FROM signup_details WHERE email=?", (email,))
    user = c.fetchone()
    if user is not None:
        flash('Email address already exists')
        return redirect(url_for("login"))
    c.execute("INSERT INTO signup_details VALUES (?, ?, ?)", (full_name, email, password))
    conn.commit()
    flash('Signup successful. Please login.')
    return redirect(url_for('login'))


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/login", methods=['POST'])
def login_post():
    session.permanent = True
    conn = sqlite3.connect('myphonedb.db')
    c = conn.cursor()
    email = request.form["email"]
    password = request.form["password"]
    c.execute("SELECT * FROM signup_details WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    if user is not None:
        session['email'] = email
        conn.commit()
        return redirect(url_for('profile'))
    flash('Invalid email or password. Please try again.')
    return redirect(url_for('login'))


@app.route("/profile")
def profile():
    if "email" in session:
        conn = sqlite3.connect('myphonedb.db')
        c = conn.cursor()
        email = session['email']
        c.execute("SELECT full_name FROM signup_details WHERE email=?", (email,))
        full_name = c.fetchone()[0]
        conn.commit()
        return render_template('profile.html', full_name=full_name)
    flash('You have been sign out. Please login.')
    return redirect(url_for('login'))


@app.route('/add_phonenumber')
def add_phonenumber():
    return render_template('add_phonenumber.html')


@app.route('/add_phonenumber', methods=['POST'])
def add_phonenumber_post():
    conn = sqlite3.connect('myphonedb.db')
    c = conn.cursor()
    first_name = request.form['first_name']
    c.execute(f"""CREATE TABLE IF NOT EXISTS {first_name} (
        first_name STRING,
        last_name STRING,
        phone_number INTEGER,
        city STRING,
        state STRING,
        country STRING
        )
    """)
    conn.commit()

    # obtain the values for the table from the HTTP POST request
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone_number = int(request.form['phone_number'])
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']

    # insert the values into the table
    c.execute(f"INSERT INTO {first_name} VALUES (?, ?, ?, ?, ?, ?)",
              (first_name, last_name, phone_number, city, state, country))
    conn.commit()

    return "<h1>Phone details saved successfully</h>"


@app.route("/updatephone")
def update():
    if "email" in session:
        conn = sqlite3.connect('myphonedb.db')
        c = conn.cursor()
        email = session['email']
        c.execute("SELECT full_name FROM signup_details WHERE email=?", (email,))
        full_name = c.fetchone()[0]
        conn.commit()
        # return render_template('profile.html', full_name=full_name)
        return f'{full_name} this is update phone number page under development'
    flash('You have been sign out. Please login.')
    return redirect(url_for('login'))


@app.route("/viewphone")
def view():
    if "email" in session:
        conn = sqlite3.connect('myphonedb.db')
        c = conn.cursor()
        email = session['email']
        c.execute("SELECT full_name FROM signup_details WHERE email=?", (email,))
        full_name = c.fetchone()[0]
        conn.commit()
        c.execute(f"SELECT rowid, * FROM adedayo")
        full_details = c.fetchall()
        conn.commit()
        # return render_template('profile.html', full_name=full_name)
        return f'{full_details}'
    flash('You have been sign out. Please login.')
    return redirect(url_for('login'))


@app.route("/deletephone")
def delete():
    if "email" in session:
        conn = sqlite3.connect('myphonedb.db')
        c = conn.cursor()
        email = session['email']
        c.execute("SELECT full_name FROM signup_details WHERE email=?", (email,))
        full_name = c.fetchone()[0]
        conn.commit()
        return render_template('delete.html')
    flash('You have been sign out. Please login.')
    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    session.pop('email', None)
    flash('You have been sign out. Successfully.')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
