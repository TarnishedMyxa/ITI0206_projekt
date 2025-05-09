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

    ua=["1","2","3","4"]
    return render_template('dashboard.html', user_access=ua)


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


@app.route('/items/')
def items():
    if 'username' not in session:
        return redirect(url_for('login'))

    username=session['username']
    ul=db.get_userload(db_creds, username)

    access=False
    for l in ul:
        if l[1] in [1, 3, 4]:
            access=True
            break
    if not access:
        flash('You do not have access to this page.', 'error')
        return redirect(url_for('dashboard'))


    items=db.get_all_items(db_creds)
    #items came in as tuples, convert to dicts
    items = [dict(zip(['idnum', 'nimi', 'staatus', 'laius', 'pikkus', "created_at"], item)) for item in items]

    status_labels = {
        1: "Active",
        2: "Inactive",
        3: "In Maintenance",
        4: "Decommissioned"
    }

    return render_template('items.html',  items=items, sl=status_labels)

@app.route('/items/create', methods=['GET','POST'])
def create_item():
    if 'username' not in session:
        return redirect(url_for('login'))
    # (Optionally repeat your access check here)
    if request.method == 'POST':
        # Grab fields from form:
        nimi    = request.form['nimi']
        staatus = request.form['staatus']
        laius   = request.form['laius']
        pikkus  = request.form['pikkus']
        # Insert into DB
        db.add_item(db_creds, (nimi, staatus, laius, pikkus))
        return redirect(url_for('items'))
    # GET → show empty form
    return render_template('item_form.html', item=None)

@app.route('/items/edit/<int:idnum>', methods=['GET','POST'])
def edit_item(idnum):
    if 'username' not in session:
        return redirect(url_for('login'))
    # (Access check)
    item = db.get_item(db_creds, str(idnum))
    if request.method == 'POST':
        db.update_item(db_creds, (idnum, request.form['nimi'], request.form['staatus'], request.form['laius'], request.form['pikkus'] ))
        return redirect(url_for('items'))
    # GET → show form prefilled
    return render_template('item_form.html', item=item)

@app.route('/items/delete/<int:idnum>', methods=['POST'])
def delete_item(idnum):
    if 'username' not in session:
        return redirect(url_for('login'))
    # (Access check)
    db.delete_item(db_creds, idnum)
    return redirect(url_for('items'))

@app.route('/asukohad/')
def asukohad():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    ul = db.get_userload(db_creds, username)

    access = any(l[1] in [1, 3, 4] for l in ul)
    if not access:
        flash('You do not have access to this page.', 'error')
        return redirect(url_for('dashboard'))

    asukohad = db.get_all_asukohad(db_creds)
    # asukohad came in as tuples, convert to dicts
    asukohad = [dict(zip(['idnum', 'kood', 'laius', "pikkus"], asukoht)) for asukoht in asukohad]

    return render_template('asukohad.html', asukohad=asukohad)


@app.route('/asukohad/edit/<int:idnum>', methods=['GET', 'POST'])
def edit_asukoht(idnum):
    if 'username' not in session:
        return redirect(url_for('login'))
    # (Access check)
    asukoht = db.get_asukoht(db_creds, str(idnum))
    if request.method == 'POST':
        db.update_asukoht(db_creds, (idnum, request.form['kood'], request.form['laius'], request.form['pikkus']))
        return redirect(url_for('asukohad'))
    # GET → show form prefilled
    return render_template('asukoht_form.html', asukoht=asukoht)

@app.route('/asukohad/create', methods=['GET', 'POST'])
def create_asukoht():
    if 'username' not in session:
        return redirect(url_for('login'))
    # (Optionally repeat your access check here)
    if request.method == 'POST':
        # Insert into DB
        db.add_asukoht(db_creds, (request.form['kood'], request.form['laius'], request.form['pikkus']))
        return redirect(url_for('asukohad'))
    # GET → show empty form
    return render_template('asukoht_form.html', asukoht=None)

@app.route('/asukohad/delete/<int:idnum>', methods=['POST'])
def delete_asukoht(idnum):
    if 'username' not in session:
        return redirect(url_for('login'))
    # (Access check)
    db.delete_asukoht(db_creds, idnum)
    return redirect(url_for('asukohad'))


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

    items= db.get_all_items(db_creds)
    # items came in as tuples, convert to dicts
    items = [dict(zip(['idnum', 'nimi', 'staatus', 'laius', 'pikkus', "created_at"], item)) for item in items]

    # Redirect or render another page showing the transfer order creation
    return render_template('create_transfer.html', items=items, selected_items=selected_items)

@app.route('/submit_transfer/', methods=['POST'])
def submit_transfer():
    #get the json
    data = request.get_json()

    # Extract the relevant fields from the JSON   {'transfer_type': 'outbound', 'transfer_date': '2025-05-20', 'destination': 'fdnsajklsdn', 'items': [{'item_id': '2', 'quantity': '123'}]}

    transfer_type = data['transfer_type']
    transfer_date = data['transfer_date']
    destination = data['destination']
    items = data['items']

    if transfer_type == 'inbound':
        tt = 1
    elif transfer_type == 'outbound':
        tt = 2

    # Convert items to a list of tuples
    items_list = [(item['item_id'], item['quantity']) for item in items]
    # Insert the transfer into the database   #(user, created_date, staatus, aadress, tyyp)
    db.add_transfer(db_creds, (session['username'], transfer_date, "1", destination, str(tt)))
    # Get the last inserted transfer ID
    last_transfer_id = db.get_last_transfer_id(db_creds)

    #add lines
    for item in items_list:
        # Check if the item exists in the database
        item_id = item[0]
        quantity = item[1]

        # Add the transfer line to the database
        db.add_transfer_line(db_creds, (str(last_transfer_id), str(item_id), str(quantity)))

    return jsonify({'success': True})

@app.route('/transfers/')
def transfers():
    if 'username' not in session:
        return redirect(url_for('login'))

    trans=db.get_all_transfers(db_creds)
    # transfers came in as tuples, convert to dicts  #idnum', 'user', 'created_date', 'staatus', 'aadress', 'tyyp
    trfs = [dict(zip(['idnum', 'user', 'created_date', 'staatus', 'aadress', 'tyyp'], transfer)) for transfer in trans]

    return render_template('transfers.html', transfers=trfs)


@app.route('/transfers/edit/<int:idnum>', methods=['GET', 'POST'])
def update_transfer(idnum):
    if 'username' not in session:
        return redirect(url_for('login'))
    # (Access check)
    transfer = db.get_transfer(db_creds, str(idnum))[0]

    t_lines= db.get_transfer_lines(db_creds, str(idnum))


    t={
        "idnum": transfer[0],
        "user": transfer[1],
        "created_date": transfer[2],
        "staatus": transfer[3],
        "aadress": transfer[4],
        "tyyp": transfer[5],
        "items": [dict(zip(['idnum', 'trans_id', 'item_id', 'quantity', "nimi"], line)) for line in t_lines]
    }

    items= db.get_all_items(db_creds)
    # items came in as tuples, convert to dicts
    items = [dict(zip(['idnum', 'nimi', 'staatus', 'laius', 'pikkus', "created_at"], item)) for item in items]
    if request.method == 'POST':
        db.update_transfer(db_creds, (idnum, request.form['transfer_date'], request.form['staatus'], request.form['aadress'], request.form['tyyp']))
        return redirect(url_for('transfers'))
    # GET → show form prefilled
    return render_template('transfer_form.html', transfer=t, items=items)

@app.route('/move')
def move():
    return 0

@app.route('/reports')
def reports():
    return 0


if __name__ == '__main__':
    if ENVIROP=='PROD':
        app.run()
    elif ENVIROP=='LOCAL':
        app.run(debug=True)
    else:
        raise Exception("Invalid environment variable")