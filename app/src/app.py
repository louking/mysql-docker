'''
app.py is only used to support flask commands

server execution from run.py
'''

# standard
import os.path

# pypi
from flask_migrate import Migrate
from mysql_docker.model import db

# homegrown
from mysql_docker import create_app, appname
from mysql_docker.settings import Production
from scripts import InitCli

abspath = os.path.abspath('/config')
configpath = os.path.join(abspath, f'{appname}.cfg')
configfiles = [configpath]
userconfigpath = os.path.join(abspath, 'users.cfg')
# userconfigpath first so configpath can override
configfiles.insert(0, userconfigpath)

# init_for_operation=False because when we create app this would use database and cause
# sqlalchemy.exc.OperationalError if one of the updating tables needs migration
app = create_app(Production(configfiles), configfiles, init_for_operation=False)

# set up flask command processing
migrate_cli = Migrate(app, db, compare_type=True)
init_cli = InitCli(app, db)

## Needed only if serving web pages
# # implement proxy fix (https://github.com/sjmf/reverse-proxy-minimal-example)
# from werkzeug.middleware.proxy_fix import ProxyFix
# app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_port=1, x_proto=1, x_prefix=1)

# if __name__ == "__main__":
#     app.run(host ='0.0.0.0', port=5000)