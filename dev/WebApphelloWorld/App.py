from flask import Flask, request, redirect, url_for, session, render_template
import pyodbc

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# SQL Server connection details
server = 'KHI-PMO-TIRMIZI'   # Your server name
database = 'Webapp'          # Your database name

def get_db_connection():
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};DATABASE={database};'
        f'Trusted_Connection=yes;'
    )
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return '''
        <div class="container">
            <h1 class="page-title">About Page</h1>
            <p>This is the About page.</p>
        </div>
    '''

@app.route('/contact')
def contact():
    return '''
        <div class="container">
            <h1 class="page-title">Contact Page</h1>
            <p>Contact us at contact@example.com</p>
        </div>
    '''

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Fetch form data
        user = request.form['username']
        pwd = request.form['password']
        
        # Insert into SQL Server
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Users (Username, Password) VALUES (?, ?)', (user, pwd))
        conn.commit()
        cursor.close()
        conn.close()
        
        return f"<div class='container'><h2>Signup successful! Welcome, {user}!</h2></div>"
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Fetch form data
        user = request.form['username']
        pwd = request.form['password']
        
        # Check credentials from SQL Server
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Users WHERE Username = ? AND Password = ?', (user, pwd))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data:
            # If user found, store username in session
            session['username'] = user
            return redirect(url_for('dashboard'))
        else:
            return '<div class="container"><h2>Login failed. Invalid credentials.</h2></div>'
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove the username from session
    return redirect(url_for('home'))  # Redirect to home page

if __name__ == '__main__':
    app.run(debug=True)
