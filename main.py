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


inventory=[{"name":"item1",
            "idnum":"123456",
            "bidnum":"654321",
            "quantity": 10,
            "batch": 1},
              {"name":"item2",
            "idnum":"123457",
            "bidnum":"654322",
            "quantity": 5,
            "batch": 2},
                {"name":"item3",
            "idnum":"123458",
            "bidnum":"654323",
            "quantity": 20,
                 "batch": 3},
               ]

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


@app.route('/usermanagement/')
def user_management():
    if 'username' not in session:
        return redirect(url_for('login'))
    user_type="admin"
    ua=["hr","saabumised"]
    return render_template('userman.html', user_type=user_type, user_access=ua)

@app.route('/view/')
def view():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('view.html', inventory=inventory)

@app.route('/create_transfer/', methods=['GET', 'POST'])
def create_transfer():
    selected_ids = request.form.getlist('selected_items')
    
    print(selected_ids)
    # Optionally fetch full item info if needed
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