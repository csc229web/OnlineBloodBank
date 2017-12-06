# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
#from flask_sqlalchemy import SQLAlchemy
from contextlib import closing

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
#def execute_query(query, args=()):
#    cur = get_db().execute(query, args)
#    rows = cur.fetchall()
#    cur.close()
#    return rows

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/add', methods=['POST'])
# def add_entry():
#    if not session.get('logged_in'):
#        abort(401)
#    db = get_db()
#    db.execute('insert into donor_login (donor_username, donor_password) values (?, ?)', \
#                 [request.form['donor_username'], request.form['donor_password']])
#    db.commit()
#    flash('New entry was successfully posted')
#    return redirect(url_for('show_entries'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('donor_profile'))
#     return render_template('login.html', error=error)

@app.route('/donor', methods=['GET', 'POST'])
def donor():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('donor_profile'))
        return redirect(url_for('donor_profile'))
    return render_template('donor.html', error=error)

@app.route('/donor_register', methods=['GET', 'POST'])
def donor_register():
    error = None
    if request.method == 'POST':
        db = get_db()
        # needs to be updated
        db.execute('insert into donor_login (donor_username, donor_password, donor_firstname, donor_lastname, donor_email, donor_telephone, donor_address_street, donor_address_street_opt, donor_address_city, donor_address_state, donor_address_postalcode, donor_address_country, donor_birthdate, donor_gender, donor_height, donor_weight, donor_history, donor_history_date, donor_history_reason, donor_participation, donor_bloodtype) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', [request.form['donor_username'], request.form['donor_password'], request.form['donor_firstname'], request.form['donor_lastname'], request.form['donor_email'], request.form['donor_telephone'], request.form['donor_address_street'], request.form['donor_address_street_opt'], request.form['donor_address_city'], request.form['donor_address_state'], request.form['donor_address_postalcode'], request.form['donor_address_country'],request.form['donor_birthdate'], request.form['donor_gender'], request.form['donor_height'], request.form['donor_weight'], request.form['donor_history'], request.form['donor_history_date'], request.form['donor_history_reason'], request.form['donor_participation'], request.form['donor_bloodtype']])
        
        db.commit()
        flash('You have added a blood donor profile.')
        return redirect(url_for('donor_profile'))
    return render_template('donor_register.html', error=error)

@app.route('/donor_profile')
def donor_profile():
    db = get_db()
    cur = db.execute('select donor_id, donor_username, donor_firstname, donor_lastname, donor_email, donor_telephone, donor_address_street, donor_address_street_opt, donor_address_city, donor_address_state, donor_address_postalcode, donor_address_country, donor_birthdate, donor_gender, donor_height, donor_weight, donor_history, donor_history_date, donor_history_reason, donor_participation, donor_bloodtype from donor_login order by donor_id desc')
    donor_login = cur.fetchall()
    return render_template('donor_profile.html', donor_login=donor_login)

@app.route('/search', methods=['GET', 'POST'])
def search():
    error = None
    if request.method == 'POST':
        return redirect(url_for('search_results'))
    return render_template('search.html', error=error)

#@app.route('/search', methods=['POST'])
#def search():
#    db = get_db()
#    cur = db.execute('select donor_id, donor_username, donor_email, donor_participation, donor_bloodtype from donor_login #order by donor_id desc, [request.form['donor_bloodtype'],]')
#    donor_login = cur.fetchall()
#    return render_template('search.html', donor_login=donor_login)

@app.route('/search_results')
def search_results():
    db = get_db()
    cur = db.execute('select donor_id, donor_username, donor_participation, donor_bloodtype from donor_login order by donor_bloodtype desc')
    donor_login = cur.fetchall()
    return render_template('search_results.html', donor_login=donor_login)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if session.get('logged_in'):
        abort(401)
    #db = get_db()
    #db.execute('insert into entries (title, text) values (?, ?)', \
    #             [request.form['title'], request.form['text']])
    #db.commit()
    flash('Check you email for instructions')
    return redirect(url_for('donor'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('donor'))

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == '__main__':
    app.run()