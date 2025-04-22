from flask import Flask, jsonify, request, send_file, render_template, redirect, url_for, session, flash
from flask_cors import CORS
import json
import os
import datetime
import logging


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


users={
    'admin': 'admin123',
    'user': 'user123'
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

        #users=None  #get users from database!!!

        # Check if user exists and password matches
        if users.get(username) == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials, please try again.'

    return render_template('login.html')

@app.route('/dashboard/')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_type="admin"
    ua=["hr","saabumised"]
    return render_template('dashboard.html', user_type=user_type, user_access=ua)


@app.raoute('/usermanagement/')
def user_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_type="admin"
    ua=["hr","saabumised"]
    return render_template('user_management.html', user_type=user_type, user_access=ua)

@app.route('/transfer/')
def transfer():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_type="admin"
    ua=["hr","saabumised"]
    return render_template('transfer.html', user_type=user_type, user_access=ua)

@app.route('/move/')
def move():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_type="admin"
    ua=["hr","saabumised"]
    return render_template('move.html', user_type=user_type, user_access=ua)

@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    if ENVIROP=='PROD':
        app.run()
    elif ENVIROP=='LOCAL':
        app.run(debug=True)
    else:
        raise Exception("Invalid environment variable")