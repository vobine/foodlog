import string
import random
import datetime as dt
import collections as coll

import flask
import flask_login
from . import app
from . import models

import sqlalchemy

# configuration
DATABASE = 'sqlite:////tmp/foodlog.db'
SECRET_KEY = 'TYd3QTCe4pRR41F3BPrnt6XE'

# Configure Foodlog
app.config.from_object (__name__)
app.config.from_envvar ('FOODLOG_SETTINGS', silent=True)

# Initialize the database
models.init_db  (DATABASE)

# AAA machinery
login_manager = flask_login.LoginManager ()
login_manager.init_app (app)
login_manager.login_view = 'root'

@login_manager.user_loader
def load_user (user_id):
    """Load user corresponding to ID from DB."""
    return models.session.query (models.User) \
                         .filter_by (name=user_id) \
                         .one_or_none ()

@app.teardown_appcontext
def shutdown_session (exception=None):
    models.session.remove ()

@app.route ('/')
def root ():
    """Root page."""
    if flask_login.current_user.is_authenticated:
        earliest = models.session.query (models.FoodLog) \
                                 .filter_by (user=flask_login.current_user) \
                                 .order_by (models.FoodLog.timestamp.desc ()) \
                                 .first ()
        kinds = models.session.query (models.Kind) \
                              .order_by (models.Kind.name)
        weight = models.session.query (models.Weight) \
                               .filter_by (user=flask_login.current_user) \
                               .order_by (models.Weight.timestamp.desc ()) \
                               .first ()

    else:
        earliest = kinds = weight = None

    return flask.render_template ('root.html',
                                  log=earliest,
                                  kinds=kinds,
                                  weight=weight)

@app.route ('/today')
@flask_login.login_required
def today ():
    """Display activity summary for the current day."""
    logs = models.session.query (models.FoodLog) \
                         .filter_by (user=flask_login.current_user) \
                         .filter (models.FoodLog.timestamp >= dt.date.today ()) \
                         .join (models.Kind)
    for log in logs:
        print (log)

    return flask.render_template ('lately.html', logs=logs)

@app.route('/weekly')
@flask_login.login_required
def weekly ():
    """Display activity summary for the past week."""
    begin = dt.date.today () - dt.timedelta (days=8)
    logs = models.session.query (models.FoodLog) \
                         .filter_by (user=flask_login.current_user) \
                         .filter (models.FoodLog.timestamp >= begin) \
                         .join (models.Kind)
    days = coll.defaultdict (coll.Counter)
    for log in logs:
        days[log.timestamp.date ()][log.kind.name] += 1

    return flask.render_template ('weekly.html', days=days)


@app.route ('/lately')
@flask_login.login_required
def lately ():
    """Display the most recent day of entries."""
    # Show all entries more recent than one day before the most recent.
    earliest = models.session.query (
        models.FoodLog,
        sqlalchemy.func.max (models.FoodLog.timestamp)) \
                             .filter_by (user=flask_login.current_user) \
                             .one_or_none ()
    if earliest is None or len (earliest) == 0 or earliest[0] is None:
        logs = None
    else:
        earliest = earliest[0].timestamp - dt.timedelta (days=1)

        logs = models.session.query (models.FoodLog) \
                             .filter_by (user=flask_login.current_user) \
                             .filter (models.FoodLog.timestamp >= earliest) \
                             .order_by (
                                 sqlalchemy.desc (models.FoodLog.timestamp)) \
                             .join (models.Kind)

    return flask.render_template ('lately.html', logs=logs)

@app.route ('/add', methods=['POST'])
@flask_login.login_required
def add ():
    """Add a new entry to the log."""
    form = dict (kind_id=flask.request.form['kind'],
                 user=flask_login.current_user)

    # Interpret form values to match model, especially the defaults
    if flask.request.form['quantity']:
        form['quantity'] = flask.request.form['quantity']
    if flask.request.form['note']:
        form['notes'] = flask.request.form['note']

    newlog = models.FoodLog (**form)
    models.session.add (newlog)
    models.session.commit ()

    return flask.redirect (flask.url_for ('root'))

@app.route ('/weight')
@flask_login.login_required
def weight ():
    """Display the most recent entry."""
    log = models.session.query (models.Weight) \
                         .filter_by (user=flask_login.current_user) \
                         .order_by (models.Weight.timestamp.desc ()) \
                         .first ()

    return flask.render_template ('weight.html', log=log)

@app.route ('/weighin', methods=['POST'])
@flask_login.login_required
def weighin ():
    """Add a new entry to the log."""
    form = dict (user=flask_login.current_user)

    # Interpret form values to match model, especially the defaults
    if flask.request.form['value']:
        form['weight'] = flask.request.form['value']
    if flask.request.form['note']:
        form['note'] = flask.request.form['note']

    newlog = models.Weight (**form)
    models.session.add (newlog)
    models.session.commit ()

    return flask.redirect (flask.url_for ('weight'))

@app.route ('/login', methods=['POST'])
def login ():
    """Check credentials."""
    user = flask.request.form['username']
    jobo = load_user (user)
    if jobo and jobo.checkPass (flask.request.form['password']):
        flask_login.login_user (jobo)
        flask.flash ('Welcome, {0:s}'.format (user))
    else:
        flask.flash ('Invalid login attempt. Try again?')

    return flask.redirect (flask.url_for ('root'))

@app.route ('/register', methods=['POST'])
def register ():
    """Apply to register a new account."""
    # Is the account already taken?
    user = flask.request.form['email']
    if load_user (user):
        flask.flash ('That user ID is already taken, try a different one.')
        return flask.redirect (flask.url_for ('root'))

    # Generate an initial password.
    password = ''.join (random.choice (string.ascii_letters + string.digits)
                        for _ in range (24))
    print ('Temporary password for "{0:s}" is {1:s}'.format (user, password))
    flask.flash (
        'Check {0:s} for a temporary password (kidding!)'.format (user))

    # Store new user to the database
    newid = models.User (user, password)
    models.session.add (newid)
    models.session.commit ()

    # Sign in as new user
    flask_login.login_user (newid)
    return flask.render_template ('register.html')

@app.route ('/logout')
@flask_login.login_required
def logout ():
    """Disconnect the session."""
    flask_login.logout_user ()
    flask.flash ('You are now logged out.')
    return flask.redirect (flask.url_for ('root'))
