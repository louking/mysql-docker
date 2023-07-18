'''
home - public views
=================================
'''

# pypi
from flask import render_template, jsonify
from flask.views import MethodView
from loutilities.flask_helpers.mailer import sendmail

# homegrown
from . import bp

# adapted from https://github.com/aiordache/demos/blob/c7aa37cc3e2f8800296f668138b4cf208b27380a/dockercon2020-demo/app/src/server.py
# similar to https://github.com/docker/awesome-compose/blob/e6b1d2755f2f72a363fc346e52dce10cace846c8/nginx-flask-mysql/backend/hello.py

@bp.route('/')
def hello_world():
    return 'Hello, Docker!'

# @bp.route('/blogs')
# def listBlog():
#     entries = Blog.query.all()

#     result = [e.title for e in entries]

#     return jsonify({"response": result})

@bp.route('/testmail')
def testMail():
    html = '<p>this is a test of your emergency mailing system</p>'
    sendmail(
        subject='test mail from app',
        fromaddr='lou@loutilities.us', 
        toaddr='lou.king@steeplechasers.org',
        html=html)
    return jsonify({"response": 'done!'})
