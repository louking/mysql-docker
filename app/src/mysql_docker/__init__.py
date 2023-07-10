'''
app - package
====================
'''

# standard
import os.path

# pypi
from flask import Flask, send_from_directory, g, session, request, render_template, current_app
from jinja2 import ChoiceLoader, PackageLoader
from flask_security import SQLAlchemyUserDatastore, current_user
from sqlalchemy.exc import NoReferencedTableError, ProgrammingError

# homegrown
import loutilities
from loutilities.configparser import getitems
from loutilities.user import UserSecurity
from loutilities.user.model import Interest, Application, User, Role
# from loutilities.flask_helpers.mailer import sendmail

appname = 'mysql-docker'

# define security globals
user_datastore = None
security = None

# hold application here
app = None

# create application
def create_app(config_obj, configfiles=None, init_for_operation=True):
    '''
    apply configuration object, then configuration files
    '''
    global app
    app = Flask(appname)
    app.config.from_object(config_obj)
    if configfiles:
        for configfile in configfiles:
            appconfig = getitems(configfile, 'app')
            app.config.update(appconfig)

    # tell jinja to remove linebreaks
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # define product name (don't import nav until after app.jinja_env.globals['_productname'] set)
    app.jinja_env.globals['_productname'] = app.config['THISAPP_PRODUCTNAME']
    app.jinja_env.globals['_productname_text'] = app.config['THISAPP_PRODUCTNAME_TEXT']
    # uncomment when flask security added (users.cfg)
    for configkey in ['SECURITY_EMAIL_SUBJECT_PASSWORD_RESET',
                      'SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE',
                      'SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE',
                      ]:
        if configkey in app.config:
            app.config[configkey] = app.config[configkey].format(productname=app.config['THISAPP_PRODUCTNAME_TEXT'])

    # initialize database
    from mysql_docker.model import db
    db.init_app(app)

    # # initialize uploads
    # if init_for_operation:
    #     init_uploads(app)

    # handle <interest> in URL - https://flask.palletsprojects.com/en/1.1.x/patterns/urlprocessors/
    @app.url_value_preprocessor
    def pull_interest(endpoint, values):
        try:
            g.interest = values.pop('interest', None)
        except AttributeError:
            g.interest = None
        finally:
            if not g.interest:
                g.interest = request.args.get('interest', None)

    # add loutilities tables-assets for js/css/template loading
    # see https://adambard.com/blog/fresh-flask-setup/
    #    and https://webassets.readthedocs.io/en/latest/environment.html#webassets.env.Environment.load_path
    # loutilities.__file__ is __init__.py file inside loutilities; os.path.split gets package directory
    loutilitiespath = os.path.join(os.path.split(loutilities.__file__)[0], 'tables-assets', 'static')

    @app.route('/loutilities/static/<path:filename>')
    def loutilities_static(filename):
        return send_from_directory(loutilitiespath, filename)

    # # bring in js, css assets here, because app needs to be created first
    # from .assets import asset_env, asset_bundles
    with app.app_context():
        # is database available?
        database_available = True
        try:
            users = User.query.all()
        except (NoReferencedTableError, ProgrammingError):
            database_available = False
    
        # g.loutility needs to be set before update_local_tables called and before UserSecurity() instantiated
        if database_available:
            g.loutility = Application.query.filter_by(application=app.config['APP_LOUTILITY']).one_or_none()
        # database tables haven't been created yet
        else:
            g.loutility = None

    #     # update LocalUser and LocalInterest tables
    #     if init_for_operation:
    #         update_local_tables()

        # # js/css files
        # asset_env.append_path(app.static_folder)
        # asset_env.append_path(loutilitiespath, '/loutilities/static')

        # templates
        loader = ChoiceLoader([
            app.jinja_loader,
            PackageLoader('loutilities', 'tables-assets/templates')
        ])
        app.jinja_loader = loader

    # Set up Flask-Security if database is available
    if database_available:
        global user_datastore, security
        user_datastore = SQLAlchemyUserDatastore(db, User, Role)
        security = UserSecurity(app, user_datastore)
        # security = UserSecurity(app, user_datastore, send_mail=security_send_mail)

    # need to force app context else get
    #    RuntimeError: Working outside of application context.
    #    RuntimeError: Attempted to generate a URL without the application context being pushed.
    # see http://kronosapiens.github.io/blog/2014/08/14/understanding-contexts-in-flask.html
    with app.app_context():
        # turn on logging
        from .applogging import setlogging
        setlogging()
        
        # set up scoped session
        from sqlalchemy.orm import scoped_session, sessionmaker
        # see https://github.com/pallets/flask-sqlalchemy/blob/706982bb8a096220d29e5cef156950237753d89f/flask_sqlalchemy/__init__.py#L990
        # use binds if defined
        if 'SQLALCHEMY_BINDS' in app.config and app.config['SQLALCHEMY_BINDS']:
            db.session = scoped_session(sessionmaker(autocommit=False,
                                                    autoflush=False,
                                                    binds=db.get_binds(app)
                                                    ))
        else:
            db.session = scoped_session(sessionmaker(autocommit=False,
                                                    autoflush=False,
                                                    bind=db.get_engine(),
                                                    ))
        db.query = db.session.query_property()

    # app back to caller
    return app




