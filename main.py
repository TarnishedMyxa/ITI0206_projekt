from flask import Flask, jsonify, request, send_file, render_template, redirect, url_for, session, flash
from flask_cors import CORS
import json
import os
import datetime
import logging
import db
import hashlib


ENVIROP="LOCAL"     #PROD or LOCAL


#########################


if ENVIROP=="LOCAL":
    from dotenv import load_dotenv
    load_dotenv()
elif ENVIROP=="PROD":
    pass
else:
    raise Exception("WHAT ENVIRONMENT IS THIS?!")

FORMAT = '%(levelname)s; %(pathname)s; %(lineno)s; %(asctime)s;  %(message)s'


today=datetime.datetime.now().strftime("%Y-%m-%d")
#logging.basicConfig(filename='logs/'+str(today)+'.log', level=logging.INFO, format=FORMAT)
logging.basicConfig(filename='logs/main.log', level=logging.INFO, format=FORMAT)

logger = logging.getLogger(__name__)

app = Flask(__name__)

CORS(app)

app.secret_key = os.getenv("app_secret_key")

db_creds={
    'host': os.getenv("host"),
    'port': int(os.getenv("port")),
    'user': os.getenv("user"),
    'password': os.getenv("password"),
    'database': os.getenv("database")
}

logger.info('APPLICATION STARTED')

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('main_page'))
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users=db.get_users(db_creds)  # users is a list of tuples where each tuple is (username, passhash)

        # Convert list of tuples to a dictionary for easier access
        users = {user[0]: user[1] for user in users}

        # Check if username exists
        if username not in users:
            flash('Invalid credentials, please try again.', 'error')
            return redirect(url_for('login'))

        # Hash the password
        passhash= hashlib.sha256(password.encode()).hexdigest()
        # Check if password matches
        if users[username] == passhash:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'error')
            return redirect(url_for('login'))
    else:
        if 'username' in session:
            return redirect(url_for('main_page'))
        return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():

    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users=db.get_users(db_creds)

        # Check if user already exists
        if username in users:
            flash('User already exists!', 'error')
            return redirect(url_for('register_user'))

        # generate hash of password
        passhash= hashlib.sha256(password.encode()).hexdigest()

        # Add new user to the database
        db.add_user(db_creds, username, passhash)

        return redirect(url_for('login'))

    return render_template('register_user.html')

@app.route('/dashboard/')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_type="admin"
    ua=["hr","saabumised"]
    return render_template('dashboard.html', user_type=user_type, user_access=ua)


@app.route('/usermanagement/', methods=['GET', 'POST'])
def usermanagement():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        selected_user = request.form['username']

        # Get everything from the form other than the username
        newlods=dict(request.form)

        newl=[]
        for i in newlods:
            if i!="username":
                newl.append((selected_user,i))

        db.del_userloads(db_creds, selected_user)
        print(newl)
        db.add_userloads(db_creds, newl)

        users = db.get_users(db_creds)
        lubad = db.get_load(db_creds)
        return render_template('load.html', lubad=lubad, users=users)

    else:
        username=session['username']


        users=db.get_users(db_creds)
        lubad=db.get_load(db_creds)

        return render_template('load.html', lubad=lubad, users=users)

@app.route('/get-access-rights')
def get_access_rights():
    username = request.args.get('username')
    access_rights = db.get_userload(db_creds, username)
    return jsonify({'access_rights': access_rights})


@app.route('/view/')
def view():
    if 'username' not in session:
        return redirect(url_for('login'))
    inventory=[]
    return render_template('view.html', inventory=inventory)

@app.route('/create_transfer/', methods=['GET', 'POST'])
def create_transfer():
    selected_ids = request.form.getlist('selected_items')
    
    print(selected_ids)
    # Optionally fetch full item info if needed
    inventory = []
    selected_items = [item for item in inventory if str(item["idnum"]) in selected_ids]

    # Redirect or render another page showing the transfer order creation
    return render_template('create_transfer.html', selected_items=selected_items)

@app.route('/submit_transfer/', methods=['POST'])
def submit_transfer():
    # Process the transfer order
    transfer_data = request.form.to_dict()

    flash('Transfer order created successfully!', 'success')
    return redirect(url_for('view'))

@app.route('/move/')
def move():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_type="admin"
    ua=["hr","saabumised"]
    return render_template('move.html', user_type=user_type, user_access=ua)

if __name__ == '__main__':
    if ENVIROP=='PROD':
        app.run()
    elif ENVIROP=='LOCAL':
        app.run(debug=True)
    else:
        raise Exception("Invalid environment variable")