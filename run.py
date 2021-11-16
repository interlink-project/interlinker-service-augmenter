#!/usr/bin/env python
"""
run.py: A simple example app for using the Annotator Store blueprint

This file creates and runs a Flask[1] application which mounts the Annotator
Store blueprint at its root. It demonstrates how the major components of the
Annotator Store (namely the 'store' blueprint, the annotation model and the
auth and authz helper modules) fit together, but it is emphatically NOT
INTENDED FOR PRODUCTION USE.

[1]: http://flask.pocoo.org
"""

from __future__ import print_function

import os
import logging
import sys
import time

from flask import Flask, g, current_app, redirect, url_for, session, flash
from flask_mail import Mail, Message

import elasticsearch
from flask import request
from annotator import es, annotation, auth, authz, document, store,description
from authInterlink import authInterlink
import secrets
from tests.helpers import MockUser, MockConsumer, MockAuthenticator
from tests.helpers import mock_authorizer

from datetime import datetime
import arrow


from flask_swagger_ui import get_swaggerui_blueprint

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from authInterlink.helpers import  config
from authInterlink.user import User
import secrets



logging.basicConfig(format='%(asctime)s %(process)d %(name)s [%(levelname)s] '
                           '%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logging.getLogger('elasticsearch').setLevel(logging.WARN)
logging.getLogger('urllib3').setLevel(logging.WARN)
log = logging.getLogger('annotator')

here = os.path.dirname(__file__)


def main(argv):
    app = Flask(__name__)

    cfg_file = 'annotator.cfg'
    if len(argv) == 2:
        cfg_file = argv[1]

    cfg_path = os.path.join(here, cfg_file)

    try:
        app.config.from_pyfile(cfg_path)
    except IOError:
        print("Could not find config file %s" % cfg_path, file=sys.stderr)
        print("Perhaps copy annotator.cfg.example to annotator.cfg",
              file=sys.stderr)
        sys.exit(1)

    if app.config.get('ELASTICSEARCH_HOST') is not None:
        es.host = app.config['ELASTICSEARCH_HOST']

    # We do need to set this one (the other settings have fine defaults)
    default_index = app.name
    es.index = app.config.get('ELASTICSEARCH_INDEX', default_index)

    if app.config.get('AUTHZ_ON') is not None:
        es.authorization_enabled = app.config['AUTHZ_ON']

    with app.test_request_context():
        try:
            annotation.Annotation.create_all()
            #description.Description.create_all(index="description")
            document.Document.create_all()
        except elasticsearch.exceptions.RequestError as e:
            if e.error.startswith('MergeMappingException'):
                date = time.strftime('%Y-%m-%d')
                log.fatal("Elasticsearch index mapping is incorrect! Please "
                          "reindex it. You can use reindex.py for this, e.g. "
                          "python reindex.py --host %s %s %s-%s",
                          es.host,
                          es.index,
                          es.index,
                          date)
            raise

    app.config.update({
        'SECRET_KEY': secrets.token_urlsafe(16)
    })


    #Configure server parameters
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = 'interlinkdeusto@gmail.com'
    app.config['MAIL_PASSWORD'] = '***REMOVED***'
    app.config['MAIL_DEFAULT_SENDER'] = 'interlinkdeusto@gmail.com'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_MAX_EMAILS'] = None
    app.config['MAIL_ASCII_ATTACHMENTS'] = False


 




    login_manager = LoginManager()
    login_manager.init_app(app)

    @app.template_filter('datetimeformat')
    def datetimeformat(value, formatText='',localeZone='en'):
        #Example of format: 'YYYY-MM-DD HH:mm:ss ZZ'
        #en es-es
        if (formatText!=''):
            dateTimeTemp=arrow.get(value)
            local = dateTimeTemp.to('Europe/Berlin')
            
            return local.format(formatText)


        else:

            dateTimeTemp=arrow.get(value)
            local = dateTimeTemp.to('Europe/Berlin')
            
            return local.humanize(locale=localeZone)

    @app.template_filter('estadosAnnotation')
    def estadosAnnotation(value):
        tabla_switch = {
            0: 'In Progress',
            1: 'Archived',
            2: 'Approved',
            3: 'Banned',
        }

        return tabla_switch.get(value, "NA")
       
            
       
     

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @app.before_request
    def before_request():
        
        # In a real app, the current user and consumer would be determined by
        # a lookup in either the session or the request headers, as described
        # in the Annotator authentication documentation[1].
        #
        # [1]: https://github.com/okfn/annotator/wiki/Authentication

   
        g.user = MockUser('alice')


        # By default, this test application won't do full-on authentication
        # tests. Set AUTH_ON to True in the config file to enable (limited)
        # authentication testing.
        if current_app.config['AUTH_ON']:
            g.auth = auth.Authenticator(lambda x: MockConsumer('annotateit'))
        else:
            g.auth = MockAuthenticator()

        # Similarly, this test application won't prevent you from modifying
        # annotations you don't own, deleting annotations you're disallowed
        # from deleting, etc. Set AUTHZ_ON to True in the config file to
        # enable authorization testing.
        if current_app.config['AUTHZ_ON']:
            g.authorize = authz.authorize
        else:
            g.authorize = mock_authorizer

    app.register_blueprint(store.store)

    app.register_blueprint(authInterlink.authInterlink,url_prefix="")

    from website.views import views

    app.register_blueprint(views,url_prefix='/website')

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static',path)
    
    SWAGGER_URL='/docs'
    API_URL='/static/swagger.yaml'
    

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Annotator Swagger"
        },
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )

   

    app.register_blueprint(swaggerui_blueprint)




    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port,debug=True)

 

if __name__ == '__main__':
    main(sys.argv)
