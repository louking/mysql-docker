"""
init_cli - cli tasks needed for initialization
"""

# standard
from logging import basicConfig, DEBUG, INFO, getLogger

# pypi
from flask import current_app
from flask.cli import with_appcontext
from click import argument, group
from flask_security.recoverable import send_reset_password_instructions
from loutilities.user.applogging import setlogging
from loutilities.user.model import Application, Role, User

# homegrown
from mysql_docker.model import db
from scripts import catch_errors

# set up logging
basicConfig()

# debug
debug = False

# needs to be before any commands
@group()
def init():
    """Perform initialization tasks"""
    pass

@init.command()
@argument('email')
@argument('fullname')
@argument('firstname')
@with_appcontext
@catch_errors
def addsuperadmin(email, fullname, firstname, help='add superadmin user, app, and role'):
    # turn on logging
    setlogging()

    # must wait until user_datastore is initialized before import
    from mysql_docker import user_datastore
    appname = current_app.config['APP_LOUTILITY']
    
    # pick up or create application
    application = Application.query.filter_by(application=appname).one_or_none()
    if not application:
        application = Application(application=appname)
        db.session.add(application)
        db.session.flush()
        
    # pick up or create super-admin role
    superadmin = Role.query.filter_by(name='super-admin').one_or_none()
    if not superadmin:
        superadmin = Role(name='super-admin')
        db.session.add(superadmin)
        db.session.flush()
    if application not in superadmin.applications:
        superadmin.applications.append(application)
    
    # define owner, as super-admin
    superadmin_user = User.query.filter_by(email=email).one_or_none()
    if not superadmin_user:
        superadmin_user = user_datastore.create_user(email=email, name=fullname, given_name=firstname)
        user_datastore.add_role_to_user(superadmin_user, superadmin)

    # tell new user to reset password
    with current_app.test_request_context('/'):
        send_reset_password_instructions(superadmin_user)
    print(f'password reset instructions sent to {email}')
    
    # and we're done, let's accept what we did
    db.session.commit()

