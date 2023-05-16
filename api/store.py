"""
This module implements a Flask-based JSON API to talk with the annotation store via the
Annotation model.
It defines these routes:
  * Root
  * Index
  * Create
  * Read
  * Update
  * Delete
  * Search
  * Raw ElasticSearch search
See their descriptions in `root`'s definition for more detail.
"""
from __future__ import absolute_import

import csv
import json
from operator import truediv

from elasticsearch.exceptions import TransportError
from flask import Blueprint, Response, session, redirect, flash
from flask import current_app, g
from flask import request
from flask import url_for
from flask_login import current_user
from six import iteritems

from api.atoi import atoi
from api.annotation import Annotation
from api.document import Document
from api.description import Description
from api.elasticsearch import RESULTS_MAX_SIZE
from api.notification import Notification
from api.survey import Survey
from app.config import settings
import logging
import requests

from app.messages import logapi

store = Blueprint('store', __name__)

CREATE_FILTER_FIELDS = ('updated', 'created', 'consumer')  # , 'id')
UPDATE_FILTER_FIELDS = ('updated', 'created', 'user', 'consumer')


# We define our own jsonify rather than using flask.jsonify because we wish
# to jsonify arbitrary objects (e.g. index returns a list) rather than kwargs.
def jsonify(obj, *args, **kwargs):
    try:
        res = json.dumps(obj, indent=None if request.is_xhr else 2)
    except:
        res = json.dumps(obj, indent=None if False else 2)
    return Response(res, mimetype='application/json', *args, **kwargs)


@store.before_request
def before_request():
    if not hasattr(g, 'annotation_class'):
        g.annotation_class = Annotation

    if not hasattr(g, 'notification_class'):
        g.notification_class = Notification

    if not hasattr(g, 'description_class'):
        g.description_class = Description

    user = g.auth.request_user(request)
    if user is not None:
        g.user = user
    elif not hasattr(g, 'user'):
        g.user = None


@store.after_request
def after_request(response):
    #print("LLEga al AFTER REQUEST")
    ac = 'Access-Control-'
    rh = response.headers

    rh[ac + 'Allow-Origin'] = request.headers.get('origin', '*')
    rh[ac + 'Expose-Headers'] = 'Content-Length, Content-Type, Location'

    if request.method == 'OPTIONS':
        rh[ac + 'Allow-Headers'] = ('Content-Length, Content-Type, '
                                    'X-Annotator-Auth-Token, X-Requested-With')
        rh[ac + 'Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        rh[ac + 'Max-Age'] = '86400'

    return response


# ROOT
@store.route('/api')
def root():
    return jsonify({
        'message': "Annotator Store API",
        'links': {
            'annotation': {
                'create': {
                    'method': 'POST',
                    'url': url_for('.create_annotation', _external=True),
                    'query': {
                        'refresh': {
                            'type': 'bool',
                            'desc': ("Force an index refresh after create "
                                     "(default: true)")
                        }
                    },
                    'desc': "Create a new annotation"
                },
                'read': {
                    'method': 'GET',
                    'url': url_for('.read_annotation',
                                   docid=':id',
                                   _external=True),
                    'desc': "Get an existing annotation"
                },
                'update': {
                    'method': 'PUT',
                    'url':
                    url_for(
                        '.update_annotation',
                        docid=':id',
                        _external=True),
                    'query': {
                        'refresh': {
                            'type': 'bool',
                            'desc': ("Force an index refresh after update "
                                     "(default: true)")
                        }
                    },
                    'desc': "Update an existing annotation"
                },
                'delete': {
                    'method': 'DELETE',
                    'url': url_for('.delete_annotation',
                                   docid=':id',
                                   _external=True),
                    'desc': "Delete an annotation"
                }
            },
            'search': {
                'method': 'GET',
                'url': url_for('.search_annotations', _external=True),
                'desc': 'Basic search API'
            },
            'search_raw': {
                'method': 'GET/POST',
                'url': url_for('.search_annotations_raw', _external=True),
                'desc': ('Advanced search API -- direct access to '
                         'ElasticSearch. Uses the same API as the '
                         'ElasticSearch query endpoint.')
            }
        }
    })


# INDEX
@store.route('/annotations')
def index():
    if current_app.config.get('AUTHZ_ON'):
        # Pass the current user to do permission filtering on results
        user = g.user
    else:
        user = None

    annotations = g.annotation_class.search(user=user)
    return jsonify(annotations)

# INDEX


@store.route('/notifications')
def notificationIndex():
    if current_app.config.get('AUTHZ_ON'):
        # Pass the current user to do permission filtering on results
        user = g.user
    else:
        user = None

    notifications = Notification._get_all()
    return jsonify(notifications)

# INDEX


@store.route('/surveys')
def surveysIndex():
    if current_app.config.get('AUTHZ_ON'):
        # Pass the current user to do permission filtering on results
        user = g.user
    else:
        user = None

    surveys = Survey._get_all()

    return jsonify(surveys['surveys'])

# READ


@store.route('/surveys/<docid>')
def read_survey(docid):
    survey = Survey.fetch(docid, index='survey')
    if not survey:
        return jsonify('Notification not found!', status=404)

    failure = _check_action(survey, 'read')
    if failure:
        return failure

    return jsonify(survey)


@store.route('/completeSurvey/<idAsset>')
def completeaSurvey(idAsset):
    # Tengo que poner la notificacion como realizada.

    notification = Notification._get_Notification_byAssetId(assetId=idAsset)

    notification = notification['notifications'][0]
    notification['resolved'] = True

    notification.updateFieldResolve(index="notification")

    return redirect(url_for('authInterlink.dashboard'))


@store.route('/saveSurvey/<idAsset>')
def saveSurvey(idAsset):

    # api-endpoint

    URL = settings.SURVEYINTERLINK_URL+"/assets/"+idAsset

    # logging.info(URL)
    r = requests.get(url=URL)
    # logging.info(r)
    data = r.json()

    # logging.info(data)

    # Obtengo los datos del survey:
    description = data['description']
    title = data['name']

    # Create a new survey:

    newSurvey = Survey(title=title,
                       description=description,
                       idAsset=idAsset,
                       isMandatory=True
                       )

    newSurvey.save(index="survey")

    return redirect(url_for('views.survey'))


@store.route('/updateSurvey')
def updateSurvey():

    # Tengo que poner la notificacion como realizada.
    idAsset = request.args.get('assetId')
    title = request.args.get('surveyTitle')
    description = request.args.get('surveyDesc')

    # Obtengo el survey usando el Assetid
    surveyEncontrado = Survey._get_Survey_byAssetId(idAsset=idAsset)

    surveyEncontrado = surveyEncontrado['surveys'][0]
    # Actualizo a new survey:

    surveyEncontrado['title'] = title
    surveyEncontrado['description'] = description

    Survey.updateFields(surveyEncontrado, index="survey")

    return redirect('/survey')


# CREATE
@store.route('/notifications', methods=['POST'])
def create_notification():
    # Only registered users can create annotations
    if g.user is None:
        return _failed_authz_response('create annotation')

    if request.json is not None:
        notification = g.notification_class(
            _filter_input(
                request.json,
                CREATE_FILTER_FIELDS))

        notification['consumer'] = g.user.consumer.key
        if _get_annotation_user(notification) != g.user.id:
            notification['user'] = g.user.id

            if 'username' in session:
                notification['user'] = session['username']
            else:
                notification['user'] = current_user.email

        #print("El id inicial es:"+annotation['id'])

        if hasattr(g, 'before_annotation_create'):
            g.before_annotation_create(notification)

        if hasattr(g, 'after_annotation_create'):
            notification.save(refresh=False)
            g.after_annotation_create(notification)

        refresh = request.args.get('refresh') != 'false'
        notification.save(refresh=refresh)

        #print("El id final es:"+annotation['id'])

        #location = url_for('.read_notification', docid=notification['id'])

        return jsonify(notification), 201  # , {'Location': location}
    else:
        return jsonify('No JSON payload sent. Annotation not created.',
                       status=400)


# READ
@store.route('/notifications/<docid>')
def read_notification(docid):
    notification = Notification.fetch(docid, index='notification')
    if not notification:
        return jsonify('Notification not found!', status=404)

    failure = _check_action(notification, 'read')
    if failure:
        return failure

    return jsonify(notification)


# UPDATE
@store.route('/notifications/<docid>', methods=['POST', 'PUT'])
def update_notification(docid):
    notification = Notification.fetch(docid, index='notification')
    if not notification:
        return jsonify('Notification not found! No update performed.',
                       status=404)

    failure = _check_action(notification, 'update')
    if failure:
        return failure

    if request.json is not None:
        updated = _filter_input(request.json, UPDATE_FILTER_FIELDS)
        updated['id'] = docid  # use id from URL, regardless of what arrives in
        # JSON payload

        changing_permissions = (
            'permissions' in updated and
            updated['permissions'] != notification.get('permissions', {}))

        if changing_permissions:
            failure = _check_action(notification,
                                    'admin',
                                    message='permissions update')
            if failure:
                return failure

        notification.updateFields(updated, index='notification')

        if hasattr(g, 'before_notification_update'):
            g.before_notification_update(notification)

        refresh = request.args.get('refresh') != 'false'
        notification.save(refresh=refresh)

        if hasattr(g, 'after_notification_update'):
            g.after_notification_update(notification)

    return jsonify(notification)


# DELETE
@store.route('/notifications/<docid>', methods=['DELETE'])
def delete_notification(docid):
    notification = Notification.fetch(docid, index='notification')

    if not notification:
        return jsonify('Notification not found. No delete performed.',
                       status=404)

    failure = _check_action(notification, 'delete')
    if failure:
        return failure

    if hasattr(g, 'before_notification_delete'):
        g.before_notification_delete(notification)

    notification.delete(index='notification')

    if hasattr(g, 'after_notification_delete'):
        g.after_notification_delete(notification)

    return '', 204


# DELETE
@store.route('/surveys/<docid>', methods=['DELETE'])
def delete_survey(docid):
    survey = Survey.fetch(docid, index='survey')

    if not survey:
        return jsonify('Survey not found. No delete performed.',
                       status=404)

    failure = _check_action(survey, 'delete')
    if failure:
        return failure

    if hasattr(g, 'before_survey_delete'):
        g.before_survey_delete(survey)

    survey.delete(index='survey')

    if hasattr(g, 'after_survey_delete'):
        g.after_survey_delete(survey)

    return '', 204


# INDEX
@store.route('/searchannotations', methods=["POST"])
def annotationsIndex():

    params = json.loads(request.data.decode('utf-8'))

    textoABuscar = params.get("textoABuscar")
    if(textoABuscar == None):
        textoABuscar = ""

    estados = params.get("estados")

    stateInProgress = estados['InProgress']
    stateArchived = estados['Archived']
    stateApproved = estados['Approved']

    justMyContributions = False
    if "justMyContributions" in params:
        justMyContributions = params.get("justMyContributions")

    category = params.get("category")

    descriptionId = params.get("descriptionId")
    descriptionActual = Description._get_Descriptions_byId(id=descriptionId)[0]

    page = params.get("page")
    if(page == None):
        page = "1"

    listUrl = []
    for url in descriptionActual['urls']:
        listUrl.append(url['url'])
    # Realizo la busqueda:
    annotations = Annotation._get_by_multiple(
        Annotation, textoABuscar=textoABuscar, estados=estados, descriptionId=descriptionId, category=category, notreply=True, page=page, justMyContributions=justMyContributions, user=current_user.email)

    #nroRegistros= Annotation._get_by_multipleCounts(Annotation,textoABuscar=textoABuscar,estados=estados,url=descriptionUri,page=page)
    numRes = annotations['numRes']
    annotations = annotations['annotations']

    # Cargo las replies de cada annotacion:
    stats = []
    # for urlItem in descriptionActual['urls']:
    stats = stats + \
        Annotation.annotationStats(Annotation, descriptionId=descriptionId)

    dictStats = {}
    for itemStat in stats:
        clave = itemStat['key']
        val = itemStat['doc_count']
        dictStats[clave] = val
    for itemRes in annotations:
        if itemRes['id'] in dictStats.keys():
            itemRes['nroReplies'] = dictStats[itemRes['id']]
        else:
            itemRes['nroReplies'] = 0

    return jsonify({'annotations': annotations, 'nroRegistros': numRes})

# READ


@store.route('/descriptions')
def descriptionsShow():
    if current_app.config.get('AUTHZ_ON'):
        # Pass the current user to do permission filtering on results
        user = g.user
    else:
        user = None

    descriptions = Description._get_all()

    return jsonify(descriptions)

# INDEX


@store.route('/descriptions', methods=["POST"])
def descriptionsIndex():

    params = json.loads(request.data.decode('utf-8'))

    textoABuscar = params.get("textoABuscar")
    if(textoABuscar == None):
        textoABuscar = ""

    padministration = params.get("padministration")
    if(padministration == None):
        padministration = ""

    domain = params.get("domain")
    if(domain == None):
        domain = ""

    page = params.get("page")
    if(page == None):
        page = 1

    byuser = params.get("byuser")
    if(byuser == None or byuser == 'False'):
        descriptions = Description._get_by_multiple(
            textoABuscar=textoABuscar, padministration=padministration, urlPrefix=domain, page=page)
    else:

        registroInicial = (int(page)-1)*10

        #logging.info(
        #    'El registro inicial (/description post) es:'+str(registroInicial))

        descriptions = Description._getDescriptionsUser_Stats_onSearch(
            textoABuscar=textoABuscar, padministration=padministration, domain=domain, registroInicial=registroInicial, user=current_user.email)

    nroRegistros = descriptions['numRes']
    descriptions = descriptions['descriptions']
    #nroRegistros= Description._get_by_multipleCounts(textoABuscar=textoABuscar,padministration=padministration,urlPrefix=domain)

    return jsonify({'descriptions': descriptions, 'nroRegistros': nroRegistros})


@store.route('/description/<path:urlDescription>', methods=["POST"])
def descriptionByUrl(urlDescription):

    params = json.loads(request.data.decode('utf-8'))
    url = params['url']
    description = Description._get_Descriptions_byURI(url=url)

    if len(description) == 0:
        return jsonify([])

    return jsonify(description[0])


# CREATE
@store.route('/annotations', methods=['POST'])
def create_annotation():
    # Only registered users can create annotations
    if g.user is None:
        return _failed_authz_response('create annotation')

    if request.json is not None:
        annotation = g.annotation_class(
            _filter_input(
                request.json,
                CREATE_FILTER_FIELDS))

        annotation['consumer'] = g.user.consumer.key
        if _get_annotation_user(annotation) != g.user.id:
            annotation['user'] = g.user.id
            annotation['user'] = session['username']

        #print("El id inicial es:"+annotation['id'])

        if hasattr(g, 'before_annotation_create'):
            g.before_annotation_create(annotation)

        if hasattr(g, 'after_annotation_create'):
            annotation.save(refresh=False)
            g.after_annotation_create(annotation)

        refresh = request.args.get('refresh') != 'false'
        annotation.save(refresh=refresh)

        #print("El id final es:"+annotation['id'])

        logapi(
            {"action": "new_annotation", "object_id": annotation['id'], "model": "annotation", 'annotation_data': annotation})

        location = url_for('.read_annotation', docid=annotation['id'])

        return jsonify(annotation), 201, {'Location': location}
    else:
        return jsonify('No JSON payload sent. Annotation not created.',
                       status=400)


# READ
@store.route('/annotations/<docid>')
def read_annotation(docid):
    annotation = g.annotation_class.fetch(docid)
    #annotation = Annotation._get_Annotation_byId(id=docid)[0]
    if not annotation:
        return jsonify('Annotation not found!', status=404)

    failure = _check_action(annotation, 'read')
    if failure:
        return failure

    return jsonify(annotation)


# UPDATE
@store.route('/annotations/<docid>', methods=['POST', 'PUT'])
def update_annotation(docid):
    annotation = g.annotation_class.fetch(docid)
    if not annotation:
        return jsonify('Annotation not found! No update performed.',
                       status=404)

    failure = _check_action(annotation, 'update')
    if failure:
        return failure

    if request.json is not None:
        updated = _filter_input(request.json, UPDATE_FILTER_FIELDS)
        updated['id'] = docid  # use id from URL, regardless of what arrives in
        # JSON payload

        changing_permissions = (
            'permissions' in updated and
            updated['permissions'] != annotation.get('permissions', {}))

        if changing_permissions:
            failure = _check_action(annotation,
                                    'admin',
                                    message='permissions update')
            if failure:
                return failure

        annotation.update(updated)

        if hasattr(g, 'before_annotation_update'):
            g.before_annotation_update(annotation)

        refresh = request.args.get('refresh') != 'false'
        annotation.save(refresh=refresh)

        if hasattr(g, 'after_annotation_update'):
            g.after_annotation_update(annotation)

        logapi(
            {"action": "update_annotation", "object_id": annotation['id'], "model": "annotation", 'annotation_data': annotation})

    return jsonify(annotation)


# DELETE
@store.route('/annotations/<docid>', methods=['DELETE'])
def delete_annotation(docid):
    annotation = g.annotation_class.fetch(docid)

    if not annotation:
        return jsonify('Annotation not found. No delete performed.',
                       status=404)

    failure = _check_action(annotation, 'delete')
    if failure:
        return failure

    if hasattr(g, 'before_annotation_delete'):
        g.before_annotation_delete(annotation)

    # Borro todas las replies
    Annotation._deleteReplies(annotation=annotation)

    # Booro la annotation.
    annotation.delete()

    if hasattr(g, 'after_annotation_delete'):
        g.after_annotation_delete(annotation)

    logapi(
        {"action": "delete_annotation", "object_id": annotation['id'], "model": "annotation", 'annotation_data': annotation})

    return '', 204


# SEARCH
@store.route('/search')
def search_annotations():
    params = dict(request.args.items())
    kwargs = dict()

    # Take limit and offset out of the parameters
    if 'offset' in params:
        kwargs['offset'] = atoi(params.pop('offset'), default=None)
    if 'limit' in params:
        kwargs['limit'] = atoi(params.pop('limit'), default=None)
    if 'sort' in params:
        kwargs['sort'] = params.pop('sort')
    if 'order' in params:
        kwargs['order'] = params.pop('order')
    kwargs['limit'] = 100000
    # All remaining parameters are considered searched fields.
    kwargs['query'] = params

    if current_app.config.get('AUTHZ_ON'):
        # Pass the current user to do permission filtering on results
        kwargs['user'] = g.user
    #print(f' Kwargs: {kwargs}')
    results = g.annotation_class.search(**kwargs)
    total = g.annotation_class.count(**kwargs)

    return jsonify({'total': total,
                    'rows': results})


# RAW ES SEARCH
@store.route('/search_raw', methods=['GET', 'POST'])
def search_annotations_raw():

    try:
        query, params = _build_query_raw(request)
    except ValueError:
        return jsonify('Could not parse request payload!',
                       status=400)

    if current_app.config.get('AUTHZ_ON'):
        user = g.user
    else:
        user = None

    try:
        res = g.annotation_class.search_raw(query, params, raw_result=True,
                                            user=user)
    except TransportError as err:
        if err.status_code != 'N/A':
            status_code = err.status_code
        else:
            status_code = 500
        return jsonify(err.error,
                       status=status_code)
    return jsonify(res, status=res.get('status', 200))


# Return the current user logged.
@store.route('/user', methods=['GET'])
def getUser():

    usuarioActivo = current_user.email if not current_user.is_anonymous else 'Anonymous'

    return jsonify(usuarioActivo)


def _filter_input(obj, fields):
    for field in fields:
        obj.pop(field, None)

    return obj


def _get_annotation_user(ann):
    """Returns the best guess at this annotation's owner user id"""
    user = ann.get('user')

    if not user:
        return None

    try:
        return user.get('id', None)
    except AttributeError:
        return user


def _check_action(annotation, action, message=''):
    if not g.authorize(annotation, action, g.user):
        return _failed_authz_response(message)


def _failed_authz_response(msg=''):
    user = g.user.id if g.user else None
    consumer = g.user.consumer.key if g.user else None

    if user:
        # If the user is authenticated but not authorized we send a 403.
        message = (
            "Cannot authorize request{0}. You aren't authorized to make this "
            "request. (user={user}, consumer={consumer})".format(
                ' (' + msg + ')' if msg else '', user=user, consumer=consumer))
        return jsonify(message), 403

    else:
        # If the user is not authenticated at all we send a 401.
        return jsonify("Cannot authorize request{0}. Perhaps you're not logged in "
                       "as a user with appropriate permissions on this "
                       "annotation? "
                       "(user={user}, consumer={consumer})".format(
                           ' (' + msg + ')' if msg else '',
                           user=user,
                           consumer=consumer),
                       status=401)


def _build_query_raw(request):
    query = {}
    params = {}

    if request.method == 'GET':
        for k, v in iteritems(request.args):
            _update_query_raw(query, params, k, v)

        if 'query' not in query:
            query['query'] = {'match_all': {}}

    elif request.method == 'POST':

        try:
            query = json.loads(request.json or
                               request.data or
                               request.form.keys()[0])
        except (ValueError, IndexError):
            raise ValueError

        params = request.args

    for o in (params, query):
        if 'from' in o:
            o['from'] = max(0, atoi(o['from']))
        if 'size' in o:
            o['size'] = min(RESULTS_MAX_SIZE, max(0, atoi(o['size'])))

    return query, params


def _update_query_raw(qo, params, k, v):
    if 'query' not in qo:
        qo['query'] = {}
    q = qo['query']

    if 'query_string' not in q:
        q['query_string'] = {}
    qs = q['query_string']

    if k == 'q':
        qs['query'] = v

    elif k == 'df':
        qs['default_field'] = v

    elif k in ('explain', 'track_scores', 'from', 'size', 'timeout',
               'lowercase_expanded_terms', 'analyze_wildcard'):
        qo[k] = v

    elif k == 'fields':
        qo[k] = _csv_split(v)

    elif k == 'sort':
        if 'sort' not in qo:
            qo[k] = []

        split = _csv_split(v, ':')

        if len(split) == 1:
            qo[k].append(split[0])
        else:
            fld = ':'.join(split[0:-1])
            drn = split[-1]
            qo[k].append({fld: drn})

    elif k == 'search_type':
        params[k] = v


def _csv_split(s, delimiter=','):
    return [r for r in csv.reader([s], delimiter=delimiter)][0]
