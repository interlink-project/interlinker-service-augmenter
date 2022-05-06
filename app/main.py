
from __future__ import print_function
from werkzeug.middleware.proxy_fix import ProxyFix

import os
import logging
import sys
import time

from flask import Flask, g, current_app, redirect, url_for, session, flash, abort
from flask_mail import Mail, Message

import elasticsearch
from flask import request
from api import es, annotation, auth, authz, document, notification, store, description, survey
from api.survey import Survey
from authInterlink import authInterlink
from views import views
import secrets
from tests.helpers import MockUser, MockConsumer, MockAuthenticator
from tests.helpers import mock_authorizer

from datetime import datetime
import arrow
from flask_swagger_ui import get_swaggerui_blueprint
from flask_babel import Babel
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from authInterlink.user import User
import secrets
from app.config import settings

#from  flask_socketio import SocketIO,emit

logging.basicConfig(format='%(asctime)s %(process)d %(name)s [%(levelname)s] '
                           '%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
logging.getLogger('elasticsearch').setLevel(logging.WARN)
logging.getLogger('urllib3').setLevel(logging.WARN)
log = logging.getLogger('annotator')

here = os.path.dirname(__file__)


def create_app():
    app = Flask(__name__)
    app.debug = True

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    #print("Entra hasta aqui")
    app.config.from_object(settings)

    # We do need to set this one (the other settings have fine defaults)
    default_index = app.name
    es.index = app.config.get('ELASTICSEARCH_INDEX', default_index)

    if app.config.get('AUTHZ_ON') is not None:
        es.authorization_enabled = app.config['AUTHZ_ON']

    with app.test_request_context():
        try:

            # Borro todos las tablas:
            # annotation.Annotation.drop_all()
            # notification.Notification.drop_all(index="notification")
            # survey.Survey.drop_all(index="survey")
            # description.Description.drop_all(index="description")
            # document.Document.drop_all()

            # Creo los indices necesarios:
            annotation.Annotation.create_all()
            notification.Notification.create_all(index="notification")
            survey.Survey.drop_all(index="survey")
            survey.Survey.create_all(index="survey")
            description.Description.create_all(index="description")
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

    login_manager = LoginManager()

    login_manager.login_view = "authInterlink.login"

    login_manager.init_app(app)


    # Setting Socket:
    
    # socketio=SocketIO(app)

    # @socketio.on('event')
    # def event(data):
       
    #     import time
       
    #     while True:
    #         time.sleep(5)
            
    #         from api.annotation import Annotation
    #         res = []
            
    #         descriptionId=data['descriptionId']
    #         actualLastAnnotations=data['annotationsIds']
        

    #         res = Annotation._get_by_multiple(Annotation, textoABuscar='', estados={
    #                                   'InProgress': True, 'Archived': False, 'Approved': True}, 
    #                                   descriptionId=descriptionId, category='', 
    #                                   notreply=False, page='all')
            
    #         annotationsGrabadas=res['annotations']
            
    #         #Obtengo la lista de Identificadores
    #         listIdGrabadas=[]
    #         for annotationG in annotationsGrabadas:
    #             listIdGrabadas.append(annotationG['id'])

    #         #Miro si hay annotaciones agregadas:
    #         listAnnotationsAgregadas=[]
    #         for annotationG in annotationsGrabadas:
    #             if(annotationG['id'] not in actualLastAnnotations):
    #                 annotationG['notpublish']=True
    #                 listAnnotationsAgregadas.append(annotationG) 
    #                 actualLastAnnotations.append(annotationG['id'])
                    
            
    #         #Las anotations a incrementadas son:
    #         if(len(listAnnotationsAgregadas)>0):
    #             emit('event',{'accion':'add','list':listAnnotationsAgregadas})
               
    #         #Miro si hay annotaciones borradas:
    #         listAnnotationsBorradas=[]
    #         for annotationA in actualLastAnnotations:
    #             if(annotationA not in listIdGrabadas):
    #                 listAnnotationsBorradas.append(annotationA) 
    #                 actualLastAnnotations.remove(annotationA)
            
    #         #Las anotations a borradas son:
    #         if(len(listAnnotationsBorradas)>0):
    #             emit('event',{'accion':'remove','list':listAnnotationsBorradas})
            
             

        

    # Babel Settings

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        # if a user is logged in, use the locale from the user settings

        user = getattr(g, 'user', None)
        user = current_user

        if request.args.get('lang'):
            session['lang'] = request.args.get('lang')
            return session.get('lang', session['lang'])

        # if user is not None:
        #    return user.locale

        # otherwise try to guess the language from the user accept
        # header the browser transmits.  We support de/fr/en in this
        # example.  The best match wins.

        return request.accept_languages.best_match(['en', 'lv', 'es', 'it'])

        # return 'en'

    @babel.timezoneselector
    def get_timezone():
        user = getattr(g, 'user', None)
        if user is not None:
            return user.timezone

    # Additional Flask Filters:

    @app.template_filter('datetimeformat')
    def datetimeformat(value, formatText='', localeZone='en'):

        if (formatText != ''):
            dateTimeTemp = arrow.get(value)
            local = dateTimeTemp.to('Europe/Berlin')

            return local.format(formatText)

        else:

            dateTimeTemp = arrow.get(value)
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

    # Define the initial user:

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
        g.user = MockUser('Anonymous')

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

    # Define the static folder:

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    # BluePrints:

    app.register_blueprint(store.store)
    app.register_blueprint(authInterlink.authInterlink)
    app.register_blueprint(views.views)

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        app.config['SWAGGER_URL'],
        app.config['API_URL'],
        config={  # Swagger UI config overrides
            'app_name': "Annotator Swagger"
        },

    )
    app.register_blueprint(swaggerui_blueprint)

    return app
