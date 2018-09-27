#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import os
import sys

from flask import Flask, g
from lwp.config import config
#~ from lwp import SESSION_SECRET_FILE
from lwp.views import main, auth, api
from peewee import *
from playhouse.flask_utils import FlaskDB
SESSION_SECRET_FILE = '/etc/lwp/session_secret'
try:
    SECRET_KEY = open(SESSION_SECRET_FILE, 'br').read()
except IOError:
    print(' * Missing session_secret file, your session will not survive server reboot. Run with --generate-session-secret to generate permanent file.')
    SECRET_KEY = os.urandom(24)

DEBUG = config.getboolean('global', 'debug')
DATABASE = config.get('database', 'file')
ADDRESS = config.get('global', 'address')
PORT = int(config.get('global', 'port'))
PREFIX = config.get('global', 'prefix')

#~ from lwp.database.models import db
# Flask app
#~ from playhouse.flask_utils import FlaskDB

#~ database = FlaskDB()

app = Flask('lwp', static_url_path="{0}/static".format(PREFIX))
app.config.from_object(__name__)
app.register_blueprint(main.mod, url_prefix=PREFIX)
app.register_blueprint(auth.mod, url_prefix=PREFIX)
app.register_blueprint(api.mod, url_prefix=PREFIX)

if '--profiling' in sys.argv[1:]:
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    app.debug = True  # also enable debug


@app.before_request
def before_request():
    """
    executes functions before all requests
    """
    pass
    from lwp.utils import check_session_limit
    check_session_limit()
    #~ g.db = connect_db(app.config['DATABASE'])


@app.teardown_request
def teardown_request(exception):
    """
    executes functions after all requests
    """
    if hasattr(g, 'db'):
        g.db.close()
