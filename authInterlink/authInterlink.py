from operator import add
from app.config import settings
import logging
from flask import Blueprint, jsonify, flash, send_file, send_from_directory, after_this_request
import requests
import math
from urllib.parse import urljoin, urlparse
import datetime
import uuid
import os
from docxtpl import DocxTemplate, RichText
from flask import current_app, g
from datetime import date

from flask_babel import format_number, gettext, format_decimal, format_currency, format_percent
from flask_babel import _

from flask import Flask, render_template, redirect, request, url_for, session
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from api.survey import Survey
from api.feedback import Feedback

from authInterlink.user import User

from api.annotation import Annotation
from api.description import Description
from api.notification import Notification
from app.languages import getLanguagesList
from authInterlink.authentication import get_current_active_user, get_current_user

authInterlink = Blueprint('authInterlink', __name__,
                          template_folder="./app/templates")

# Genero Secretos para los estados:
tok1 = uuid.uuid4()
tok2 = uuid.uuid4()

APP_STATE = tok1.hex
NONCE = tok2.hex


@authInterlink.route("/logina")
def logina():

    # LLamo al componente de authentication para verificar que existe un usuario en session
    usuario = get_current_user(request)

    # If the user is not logged in call a log in method of ath
    if usuario == None:

        paginaRedirigir = settings.REDIRECT_SERVICEPEDIA + \
            url_for('authInterlink.dashboard')

        # url = 'http://localhost:8929'+'/login'
        # user_agent = {'User-agent': 'Mozilla/5.0'}
        # PARAMS = {'redirect_on_callback':paginaRedirigir}

        # response = requests.get(url,params=PARAMS, headers=user_agent)

        # print(response.status_code)

        # return redirect(response.url)

        redirectToAuth = settings.AUTHINTERLINK_URL + \
            '/login'+'?redirect_on_callback='+paginaRedirigir
        #logging.info('Pagina de login:')
        # logging.info(redirectToAuth)
        return redirect(redirectToAuth)

    unique_id = usuario["sub"]
    user_email = usuario["email"]
    user_name = usuario["given_name"]

    user = User(
        id_=unique_id, name=user_name, email=user_email
    )

    if not User.get(unique_id):
        User.create(unique_id, user_name, user_email)

    login_user(user)
   # g.user =user

    session.pop('_flashes', None)

    # la pagina que se pretende ingresar es:
    paginaNext = ''
    if 'next' in session.keys():
        paginaNext = session['next']

    if paginaNext != "":
        return redirect(paginaNext)
    else:
        return redirect(url_for("authInterlink.dashboard"))


@authInterlink.route("/login")
def login():

    # Intento con el componente de Julen

    # LLamo al componente de authentication para verificar que existe un usuario en session
    usuario = get_current_user(request)

    # If the user is not logged in call a log in method of ath
    if usuario != None:
        unique_id = usuario["sub"]
        user_email = usuario["email"]
        user_name = usuario["given_name"]

        user = User(
            id_=unique_id, name=user_name, email=user_email
        )

        if not User.get(unique_id):
            User.create(unique_id, user_name, user_email)

        login_user(user)

        session.pop('_flashes', None)

        # la pagina que se pretende ingresar es:
        paginaNext = ''
        if 'next' in session.keys():
            paginaNext = session['next']

        if paginaNext != "":
            return redirect(paginaNext)
        else:
            return redirect(url_for("authInterlink.dashboard"))

    else:

        # LLamo al componente de authentication para verificar que existe un usuario en session
        usuario = current_user

        # If the user is not logged in call a log in method of ath
        if usuario.is_anonymous:

            redirecttoCallback = settings.REDIRECT_URI
            if(redirecttoCallback.endswith('interlink-project.eu/callback')):
                # if(redirecttoCallback=='https://dev.interlink-project.eu/callback' or redirecttoCallback=='https://demo.interlink-project.eu/callback' ):
                redirecttoCallback = settings.REDIRECT_SERVICEPEDIA+'/callback'

            # get request params
            query_params = {'client_id': current_app.config["CLIENT_ID"],
                            'redirect_uri': redirecttoCallback,
                            'scope': "openid email profile",
                            'state': APP_STATE,
                            'nonce': NONCE,
                            'response_type': 'code',
                            'response_mode': 'query'}
            #logging.info('parametros de configuracion auth:')
            # logging.info(query_params)

            # build request_uri
            request_uri = "{base_url}?{query_params}".format(
                base_url=current_app.config["AUTH_URI"],
                query_params=requests.compat.urlencode(query_params)
            )

            return redirect(request_uri)
        else:
            # la pagina que se pretende ingresar es:
            paginaNext = ''
            if 'next' in session.keys():
                paginaNext = session['next']

            if paginaNext != "":
                return redirect(paginaNext)
            else:
                return redirect(url_for("authInterlink.dashboard"))


@authInterlink.route("/logout", methods=["GET", "POST"])
@login_required
def logout():

    # Quito el usuario loggeado del componente auth

    # Quito el usuario de la session de flask
    logout_user()

    # #response = redirect(config["end_session_endpoint"])
    # payload = {'id_token_hint': session['id_token'],
    #            'post_logout_redirect_uri': settings.REDIRECT_SERVICEPEDIA+"/home",
    #            'state': APP_STATE}
    # #headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # r = requests.get(
    #     current_app.config["END_SESSION_ENDPOINT"],
    #     params=payload,
    # )
    # r.url
    # r.text
    session.clear()
    # # return response
    # # return render_template("home.html")
    # # Por ahora queda asi.
    return redirect(current_app.config["END_SESSION_ENDPOINT"])


@authInterlink.route("/logouta", methods=["GET", "POST"])
@login_required
def logouta():

    # Quito el usuario loggeado del componente auth

    # Quito el usuario de la session de flask
    logout_user()

    # #response = redirect(config["end_session_endpoint"])
    # payload = {'id_token_hint': session['id_token'],
    #            'post_logout_redirect_uri': settings.REDIRECT_SERVICEPEDIA+"/home",
    #            'state': APP_STATE}
    # #headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # r = requests.get(
    #     current_app.config["END_SESSION_ENDPOINT"],
    #     params=payload,
    # )
    # r.url
    # r.text
    session.clear()
    # # return response
    # # return render_template("home.html")
    # # Por ahora queda asi.
    # return redirect(current_app.config["END_SESSION_ENDPOINT"])
    paginaToRedirect = settings.REDIRECT_SERVICEPEDIA+url_for('views.inicio')

    return redirect(settings.AUTHINTERLINK_URL+'/logout'+'?redirect_on_callback='+paginaToRedirect)

@authInterlink.route("/storefeedback", methods=["GET","POST"])
@login_required
def storefeedback():
    argumentos = request.form.to_dict()

    emailOp = argumentos.pop("emailOp")
    feedtext = argumentos.pop("feedtext")
    user_id = current_user.email
    pregunta_1 = argumentos.pop("pregunta_1")
    pregunta_2 = argumentos.pop("pregunta_2")
    pregunta_3 = argumentos.pop("pregunta_3")
    pregunta_4 = argumentos.pop("pregunta_4")
    pregunta_5 = argumentos.pop("pregunta_5")


    newfeedback = Feedback(emailOp=emailOp,user_id=user_id, feedtext=feedtext,
                                     pregunta_1=pregunta_1, pregunta_2=pregunta_2,
                                     pregunta_3=pregunta_3,
                                     pregunta_4=pregunta_4, pregunta_5=pregunta_5
                                     )

    newfeedback.save(index="feedback")

   # resultados=allfeedbacks=newfeedback._get_all()

   # return jsonify(resultados['feedbacks'])
    listNotifications, numRes = cargarNotifications()

    flash("Feedback registrado correctamente.", "info")

    return render_template("feedback.html",notifications=listNotifications)



@authInterlink.route("/feedback")
@login_required
def feedback():
    listNotifications, numRes = cargarNotifications()
    
    return render_template("feedback.html",notifications=listNotifications, notificationNum=numRes)

@authInterlink.route("/feedbacks")
@login_required
def feedbacks():
    myfeedback = Feedback()
    resultados=allfeedbacks=myfeedback._get_all()
    return jsonify(resultados['feedbacks'])



@authInterlink.route("/dashboard")
@login_required
def dashboard():

    # Cargo los combos:

    vectorUrls = Description._get_uniqueValuesUrl()
    urlList = []
    for urls in vectorUrls:
        key = urls["key"]
        if(key != ""):
            domain = urlparse(key).netloc
            if not (domain in urlList):
                urlList.append(domain)
    # print(urlList)

    vectorPAs = Description._get_uniqueValues(campo="padministration")
    paList = []
    for pas in vectorPAs:
        key = pas["key"]

        if key == "":
            key = 'Unassigned'

        paList.append(key)

    if not ('Global' in paList):
        paList.insert(0, 'Global')
    # print(paList)

    textoABuscar = request.args.get("searchText")
    padministration = request.args.get("padministration")
    domain = request.args.get("domain")

    page = request.args.get("page", 1)
    registroInicial = (int(page)-1)*10

    totalRegistros = 0

    res = Description._getDescriptionsUser_Stats_onSearch(
        textoABuscar=textoABuscar, padministration=padministration, domain=domain, registroInicial=registroInicial, user=current_user.email)

    totalRegistros = res['numRes']
    res = res['descriptions']

    logging.info('El registro inicial es')
    logging.info(registroInicial)
    logging.info('Num of registers obtained')
    logging.info(len(res))

    logging.info('El numero de registro es ')
    logging.info(totalRegistros)

    pagesNumbers = math.ceil(totalRegistros/10)

    paginacion = {'page': page, 'pagesNumbers': pagesNumbers, 'totalRegisters': totalRegistros,
                  'searchBox': textoABuscar, 'padministration': padministration, 'url': domain}

    listNotifications, numRes = cargarNotifications()

    return render_template("dashboard.html", descriptions=res, urls=urlList, publicsa=paList, paginacion=paginacion, notifications=listNotifications, notificationNum=numRes)


@authInterlink.route("/access/<iduser>/<uemail>")
def access(iduser, uemail):

    if(iduser == 'a'):

        unique_id = 'anonymous'
        user_email = 'anonymous'
        user_name = 'anonymous'
    else:

        unique_id = uemail
        user_email = uemail
        user_name = iduser

    user = User(
        id_=unique_id, name=user_name, email=user_email
    )

    if not User.get(unique_id):
        User.create(unique_id, user_name, user_email)

    login_user(user)
   # g.user =user

    session['username'] = user_email
    session['userId'] = user_email

    session.pop('_flashes', None)

    return redirect(url_for("authInterlink.dashboard"))


@authInterlink.route("/moderate")
@login_required
def moderate():

    textoABuscar = request.args.get("searchText")

    page = request.args.get("page", 1)
    registroInicial = (int(page)-1)*10

    res = Description._get_Descript_byModerEmail(
        email=current_user.email, page=page)

    totalRegistros = res['numRes']
    res = res['descriptions']

    pagesNumbers = math.ceil(totalRegistros/10)

    paginacion = {'page': page, 'pagesNumbers': pagesNumbers, 'totalRegisters': totalRegistros,
                  'searchBox': textoABuscar}

    # Cargo las Notificaciones
    listNotifications, numRes = cargarNotifications()

    return render_template("moderate.html", descriptions=res, paginacion=paginacion, notifications=listNotifications, notificationNum=numRes)


@authInterlink.route("/survey")
@login_required
def survey():

    textoABuscar = request.args.get("searchText")

    page = request.args.get("page", 1)
    registroInicial = (int(page)-1)*10

    totalRegistros = 0

    # Searchs:
    """ if(textoABuscar==None or textoABuscar==''):
        res= Survey.search(offset=registroInicial)
        totalRegistros= Survey.count()
    else:
        res= Survey._get_Surveys(textoABuscar=textoABuscar,offset=registroInicial) """

    resTemp = Survey._get_all()
    res = resTemp['surveys']
    totalRegistros = resTemp['numRes']

    pagesNumbers = math.ceil(totalRegistros/10)

    paginacion = {'page': page, 'pagesNumbers': pagesNumbers,
                  'totalRegisters': totalRegistros, 'searchBox': textoABuscar}

    # Cargo las Notificaciones
    listNotifications, numRes = cargarNotifications()

    # Defino la direccion del SurveyHost
    surveyHost = current_app.config['SURVEYINTERLINK_URL']

    today = date.today()

    return render_template("surveys.html", surveys=res, paginacion=paginacion, notifications=listNotifications, notificationNum=numRes, surveyHost=surveyHost, now=today.strftime("%Y-%m-%d"))


@authInterlink.route("/surveyInstantiator", methods=["POST"])
def surveyInstantiator():

    # Redirecciono al editor:
    # return redirect(current_app.config['SURVEYINTERLINK_URL']+"/assets/"+"instantiate")
    return redirect(settings.SURVEYINTERLINK_URL+"/assets/"+"instantiate")


def obtainUsersEmail(listItemsBucket=[]):
    listUsers = []
    for itemBucket in listItemsBucket:
        userEmail = itemBucket['key']
        if userEmail != 'Anonymous':
            listUsers.append(userEmail)
    return listUsers


@authInterlink.route("/lauchSurvey", methods=["POST"])
def surveyLauchProcess():

    # Obtengo los valores del Survey:SS
    selTargetUsers = request.form.get("selTargetList")
    listUsersArea = request.form.get("listUsersArea")
    is_optional = request.form.get("is_optional")
    ini_date = request.form.get("ini_date")
    selEvent = request.form.get("selEvent")

    mandatory = True
    if is_optional == 'on':
        mandatory = False

    # Creo la notification:
    idAsset = request.form.get('assetId')
    title = request.form.get('surveyTitle')
    description = request.form.get('surveyDesc')

    # Defino the users:
    listUsersEmails = []
    if selTargetUsers == "everybody":

        listUsersWhoAnnotated = obtainUsersEmail(
            Annotation.currentActiveUsers())
        listUsersWhoModerate = obtainUsersEmail(
            Description.currentActiveUsersModerators())
        listUsersEmails = list(set(listUsersWhoAnnotated+listUsersWhoModerate))

    else:
        listUsersEmails = listUsersArea.split(";")

    for userEmail in listUsersEmails:

        email = userEmail
        target_url = current_app.config['SURVEYINTERLINK_URL'] + \
            "/assets/"+idAsset+"/answer"

        newNotification = Notification(
            title=title,
            email=email,
            description=description,
            target_url=target_url,
            resolved=False,
            category="survey",
            idAsset=idAsset,
            triggerEvent=selEvent,
            triggerDate=ini_date,
            isMandatory=mandatory
        )

        newNotification.save(index="notification")

    # Se ha lanzado exitosamente el suvey:
    flash("The survey has been lauched.", "info")

    return redirect(url_for("authInterlink.survey"))


@authInterlink.route('/advanceSearch',)
def advanceSearch():

    res = Annotation.search(query={'user': current_user.email})

    return render_template("advanceSearch.html", user=current_user, anotations=res)


def addFormatConversation(listAnnotationsApproved, rootAnnotationId, level=0):
    listFormatoCorrecto = []
    # recorro todas las anotaciones base
    for itemAnnotation in listAnnotationsApproved:
        if (itemAnnotation['idAnotationReply'] == 'annotation-'+rootAnnotationId):
            itemAnnotation['level'] = level
            listFormatoCorrecto.append(itemAnnotation)

            listFormatoCorrecto.extend(addFormatConversation(
                listAnnotationsApproved, itemAnnotation['id'], level+1))

    return listFormatoCorrecto


@authInterlink.route('/genReport/<string:descriptionId>',)
def genReport(descriptionId=None):

    # Obtain description data:

    description = Description._get_Descriptions_byId(id=descriptionId)[0]
    fechaActual = datetime.datetime.now()
    fechaActual = fechaActual.strftime("%d/%m/%y")

    # Obtain approved annotations of a description data:
    listAnnotationsApproved = Annotation._get_AnnotationsApproved_by_DescriptionIds(
        descriptionId=descriptionId)
    listAnnotationsApproved = listAnnotationsApproved['annotations']

    # Obtengo todos los replies de esta description:
    res = Annotation._get_by_multiple(Annotation, textoABuscar='', estados={
        'InProgress': True, 'Archived': False, 'Approved': True}, descriptionId=descriptionId, category='reply', notreply=False, page='all')
    replies = res['annotations']

    # Obtengo todas las replies approved:
    for itemAnnotationApproved in listAnnotationsApproved:
        listreplies = []
        for itemReply in replies:
            if(itemReply['idReplyRoot'] == itemAnnotationApproved['id']):

                raw_html = itemReply['text']
                from bs4 import BeautifulSoup
                cleantext = BeautifulSoup(raw_html, "lxml").text
                itemReply['text'] = cleantext

                userEmail = itemReply['user']
                userlabel = userEmail.split('@', 1)
                itemReply['userlabel'] = userlabel[0]

                listreplies.append(itemReply)

        listreplies = listreplies[::-1]
        # Doy el formato indicado:
        listreplies = addFormatConversation(
            listAnnotationsApproved=listreplies, rootAnnotationId=itemAnnotationApproved['id'])

        # Agrego todos los replies al listado
        itemAnnotationApproved['replies'] = listreplies
        # itemAnnotationApproved['replies']=[]

    txtRaiz = ''
    protocoltxt = 'http://'
    # if(settings.DOMAIN == "localhost"):
    #     doc = DocxTemplate('static/servicepediaReport_template.docx')
    # else:

    doc = DocxTemplate('app/static/servicepediaReport_template.docx')
    txtRaiz = 'app/'
    protocoltxt = 'https://'

    # Agrego los hyperlinks (con el formato adecuado):
    for itemAnnotation in listAnnotationsApproved:
        enlaceTemp = itemAnnotation['uri']
        enlaceTemptoPage = settings.REDIRECT_SERVICEPEDIA+'/augment/'+enlaceTemp + \
            '?description='+descriptionId+'&annotationId='+itemAnnotation['id']

        import urllib.parse

        # Codifico el enlace a la pagina original:
        rt1 = RichText('')
        linkEncoded1 = urllib.parse.quote(enlaceTemp)
        rt1.add(enlaceTemp, underline=True, color='#A7A7A7',
                url_id=doc.build_url_id(linkEncoded1))

        # Codifico el enlace a la pagina augmentada:
        rt = RichText('')
        linkEncoded = urllib.parse.quote(enlaceTemptoPage)
        rt.add(enlaceTemptoPage, underline=True, color='#2F759E',
               url_id=doc.build_url_id(linkEncoded))

        itemAnnotation['enlaceaugmentado'] = settings.REDIRECT_SERVICEPEDIA+'/augment/' + \
            enlaceTemp+'?description='+descriptionId + \
            '&annotationId='+itemAnnotation['id']
        itemAnnotation['enlaceOriginalRich'] = rt1
        itemAnnotation['enlaceRich'] = rt

        if(len(itemAnnotation['text']) > 70):
            itemAnnotation['shorttext'] = itemAnnotation['text'][:68]+'...'
        else:
            itemAnnotation['shorttext'] = itemAnnotation['text']

    context = {
        'dateReport': fechaActual,
        'description_title': description['title'],
        'shortDescription': description['description'],
        'detailslbl': _('DETAILS'),
        'replieslbl': _('REPLIES'),
        'noreplies': _('There is not replies for this annotation'),
        'noclosestatement': _('There is no final comment about this description'),
        'annotations': listAnnotationsApproved,
        'qent': 'false',
        'tent': 'false',
        'fent': 'false',
        'content_table_title': _('Content Table'),
        'annotation_on_page': _('Annotation on page'),
        'reportTitle': _('DESCRIPTION REPORT'),
        'shortDescriptionlbl': _('Short summary'),
        'term': _('TERM'),
        'question': _('QUESTION'),
        'feedback': _('FEEDBACK'),
        'posted_by': _('Posted by'),
        'websitepage': _('Website Page'),
        'openingtext': _('Opening Text'),
        'referencetext': _('Reference Text'),
        'closingstatement': _('CLOSING STATEMENT'),
        'date': _('Date')

    }
    doc.render(context)

    # Refresco la tabla de contenidos:

    def set_updatefields_true(doc):
        from lxml import etree
        namespace = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
        #doc = Document(docx_path)
        # add child to doc.settings element
        element_updatefields = etree.SubElement(
            doc.settings.element, f"{namespace}updateFields"
        )
        element_updatefields.set(f"{namespace}val", "true")
        return doc

    doc = set_updatefields_true(doc)

    name = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")+"_reportFilled.docx"
    root = txtRaiz+"Render/"+name

    #logging.info('The 1 root is:')
    logging.error(root)

    doc.save(root)

    # Fix the correct folder:
    root = "Render/"+name

    #logging.info('The 2 root is:')
    logging.error(root)

    # Borro el archivo generado despues de que hago la descarga.
    @after_this_request
    def delete(response):
        # logging.info('root:')
        logging.error(root)

        #logging.info('The 3 root is:')
        logging.error(txtRaiz+root)

        os.remove(txtRaiz+root)
        return response

    return send_file(root, name, as_attachment=True,
                     attachment_filename=os.path.basename(name))


@authInterlink.route('/description/<string:descriptionId>',)
@login_required
def description(descriptionId=None):

    description = Description._get_Descriptions_byId(id=descriptionId)[0]

    urlMainPage = [url['url']
                   for url in description['urls'] if url['ismain'] == True][0]

    categoria = request.args.get('category')

    page = request.args.get("page", 1)
    registroInicial = (int(page)-1)*10

    if(categoria == None or categoria == 'all'):
        categoria = ''

    stats = []
    # listUrlsPages = []
    # for itemUrl in description['urls']:
    #     url = itemUrl['url']
    #     listUrlsPages.append(url)

    # Cargo las replies de cada annotacion:
    stats = stats + \
        Annotation.annotationStats(Annotation, descriptionId=description['id'])

    res = []
    res = Annotation._get_by_multiple(Annotation, textoABuscar='', estados={
                                      'InProgress': True, 'Archived': False, 'Approved': True}, descriptionId=description['id'], category=categoria, notreply=True, page=page)

    numRes = 0
    numRes = res['numRes']
    res = res['annotations']

    dictStats = {}
    for itemStat in stats:
        clave = itemStat['key']
        val = itemStat['doc_count']
        dictStats[clave] = val

    for itemRes in res:
        if itemRes['id'] in dictStats.keys():
            itemRes['nroReplies'] = dictStats[itemRes['id']]
        else:
            itemRes['nroReplies'] = 0

    page = request.args.get("page", 1)
    pagesNumbers = math.ceil(numRes/10)

    paginacion = {'page': page, 'pagesNumbers': pagesNumbers,
                  'totalRegisters': numRes}

    # Cargo las Notificaciones
    listNotifications, numRes = cargarNotifications()

    #Es el usuario moderador?
    ismoderator = False
    for moderator in description['moderators']:
        if(current_user.email == moderator['email']):
            ismoderator=True

    return render_template("description.html", user=current_user, description=description, anotations=res, categoryLabel=categoria, paginacion=paginacion, urlMainPage=urlMainPage, notifications=listNotifications, notificationNum=numRes,ismoderator=ismoderator)
   # return 'la desc: '+category+'lauri is'+str(uri)


@authInterlink.route('/description/<string:descriptionId>/<string:option>',)
@login_required
def editDescription(descriptionId=None, option='Edit'):

    vectorPAs = Description._get_uniqueValues(campo="padministration")
    paList = []
    for pas in vectorPAs:
        key = pas["key"]

        if key == "":
            key = 'Unassigned'

        paList.append(key)
    if not ('Global' in paList):
        paList.insert(0, 'Global')
    # print(paList)

    description = Description._get_Descriptions_byId(id=descriptionId)[0]

    for itemUrl in description['urls']:
        if itemUrl['language'] != 'Undefined':
            itemUrl['langText'] = getLanguagesList()[itemUrl['language']]
        else:
            itemUrl['langText'] = "Undefined"

# Cargo las Notificaciones
    listNotifications, numRes = cargarNotifications()
    return render_template("descriptionDetail.html", user=current_user, description=description, option=option, publicsa=paList, notifications=listNotifications, notificationNum=numRes, noShowMenEmpty=True)


@authInterlink.route('/subjectPage/<string:descriptionId>/<string:annotatorId>',)
@login_required
def subjectPage(descriptionId=None, annotatorId=None):

    description = Description._get_Descriptions_byId(id=descriptionId)[0]

    urlMainPage = [url['url']
                   for url in description['urls'] if url['ismain'] == True][0]

    annotation = Annotation._get_Annotation_byId(id=annotatorId)[0]

    # Obtengo los replies de esta annotacion.

    res = Annotation._get_by_multiple(Annotation, textoABuscar='', estados={
                                      'InProgress': True, 'Archived': False, 'Approved': True}, descriptionId=descriptionId, category='reply', notreply=False, page='all')

    #nroReplies = res['numRes']
    replies = res['annotations']

    nroReplies = len(Annotation.getReplies(Annotation, annotationId=annotatorId,listChildrenRep=[]))

    # nroReplies = Annotation.count(
    #     query={'idReplyRoot': annotatorId, 'category': 'reply'})
    # replies = Annotation.search(
    #     query={'idReplyRoot': annotatorId, 'category': 'reply'}, limit=nroReplies)

    #nroRepliesOfAnnotation = nroReplies
    #nroRepliesOfAnnotation = Annotation.count(query={ '_id': description['id'] ,'category':'reply','idReplyRoot':annotatorId  })

    # Cargo las Notificaciones
    listNotifications, numRes = cargarNotifications()

    return render_template("subjectPage.html", user=current_user, annotation=annotation, description=description, categoryLabel=annotation['category'], replies=replies, nroReplies=nroReplies, urlMainPage=urlMainPage, notifications=listNotifications, notificationNum=numRes)
   # return 'la desc: '+category+'lauri is'+str(uri)


@authInterlink.route('/subjectPage/<string:descriptionId>/<string:annotatorId>/<string:option>', methods=["GET", "POST"])
@login_required
def changeAnnotation(descriptionId=None, annotatorId=None, option=None):

    if option == 'state':

        description = Description._get_Descriptions_byId(id=descriptionId)[0]

        #Es el usuario moderador?
        ismoderator = False
        for moderator in description['moderators']:
            if(current_user.email == moderator['email']):
                ismoderator=True
        
        if ismoderator == False:
            return jsonify({'ErrorInfo':'You need to be a moderator to change state of an annotation.'})

        argumentos = request.json
        newstate = argumentos.pop('stateToChange')
        commentsChangeState = argumentos.pop('commentsChangeState')
        objtype = argumentos.pop('objtype')

        annotationRootId = ''
        losvalores = argumentos.keys()
        if "annotationRootId" in losvalores:
            annotationRootId = argumentos.pop('annotationRootId')

        annotation = Annotation._get_Annotation_byId(id=annotatorId)[0]

        # Registro el cambio y quien lo hizo
        if(len(annotation['statechanges']) == 0):
            annotation['statechanges'] = []

        # Si el estado inicial es prohibido y el estado final es prohibido
        # Se resetea el estado a in progress.
        if(annotation['state'] == 3 & int(newstate) == 3):
            newstate = 0

        annotation['statechanges'].append({
            "initstate": annotation['state'],
            "endstate": int(newstate),
            "text": commentsChangeState,
            "objtype": objtype,
            "date": datetime.datetime.now().replace(microsecond=0).isoformat(),
            "user": current_user.email
        })

        # Actualizo el estado a todos los comentarios de la branch:
        # Pongo a todos los replies archivados (State=1)

        annotation._changeStateReplies(
            annotation=annotation, newstate=newstate)
        annotation['state'] = int(newstate)
        annotation.updateState()

        return jsonify(annotation)

    elif option == 'like':

        argumentos = request.json

        vote = int(argumentos.pop('stateToChange'))

        newstate = vote
        commentsChangeState = argumentos.pop('commentsChangeState')
        objtype = argumentos.pop('objtype')

        annotationRootId = ''
        losvalores = argumentos.keys()
        if "annotationRootId" in losvalores:
            annotationRootId = argumentos.pop('annotationRootId')

        # Verifico si  anteriormente este usuario ha realizado una anotacion
        annotation = Annotation._get_Annotation_byId(id=annotatorId)[0]
        nroLikes = annotation.userAlreadyLike(
            email=current_user.email, id=annotatorId)

        # Un usuario solo puede votar una vez
        if nroLikes == 0:

            # Registro el cambio y quien lo hizo
            if(len(annotation['statechanges']) == 0):
                annotation['statechanges'] = []

            # Registro el cambio y quien lo hizo
            initState = 0
            if(vote == 1):
                initState = int(annotation['like'])
                annotation['like'] = initState+1
                objtype = 'annotation_like'

            elif vote == -1:
                initState = int(annotation['dislike'])
                annotation['dislike'] = initState+1
                objtype = 'annotation_dislike'

            # Registro el cambio de estado
            annotation['statechanges'].append({
                "initstate": initState,
                "endstate": initState+1,
                "text": commentsChangeState,
                "objtype": objtype,
                "date": datetime.datetime.now().replace(microsecond=0).isoformat(),
                "user": current_user.email
            })

            annotation.updateLike()
            annotation.updateState()

        return jsonify(annotation)


@authInterlink.route("/descriptionDetail")
@login_required
def descriptionDetail():

    vectorPAs = Description._get_uniqueValues(campo="padministration")
    paList = []
    for pas in vectorPAs:
        key = pas["key"]

        if key == "":
            key = 'Unassigned'

        paList.append(key)

    if not ('Global' in paList):
        paList.insert(0, 'Global')
    # print(paList)

    #logging.info('Me dice si el usuario es anonimo:')
    # logging.info(current_user.is_anonymous)

    res = Annotation.search(query={'user': current_user.email})

    # Cargo las Notificaciones
    listNotifications, numRes = cargarNotifications()

    return render_template("descriptionDetail.html", user=current_user, anotations=res, publicsa=paList, notifications=listNotifications, notificationNum=numRes)


@authInterlink.route("/profile")
@login_required
def profile():

    # Cargo las Notificaciones
    listNotifications, numRes = cargarNotifications()

    return render_template("profile.html", user=current_user, notifications=listNotifications, notificationNum=numRes)


@authInterlink.route("/settingApp")
@login_required
def settingAppPage():

    results = []

    us_num = format_number(1099)
    results.append(us_num)

    us_num = format_currency(1099.98, 'USD')
    results.append(us_num)

    us_num = format_decimal(1.2346)
    results.append(us_num)

    # Cargo las Notificaciones
    listNotifications, numRes = cargarNotifications()

    return render_template("settings.html", user=current_user, results=results, notifications=listNotifications, notificationNum=numRes)


@authInterlink.route("/callback")
def callback():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    code = request.args.get("code")

    # la pagina que se pretende ingresar es:
    paginaNext = ''
    if 'next' in session.keys():
        paginaNext = session['next']

    if not code:
        return "The code was not returned or is not accessible", 403
    query_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': request.base_url
                    }
    query_params = requests.compat.urlencode(query_params)
    exchange = requests.post(
        current_app.config["TOKEN_URI"],
        headers=headers,
        data=query_params,
        auth=(current_app.config["CLIENT_ID"],
              current_app.config["CLIENT_SECRET"]),
    ).json()

    # Get tokens and validate
    if not exchange.get("token_type"):
        return "Unsupported token type. Should be 'Bearer'.", 403
    access_token = exchange["access_token"]
    id_token = exchange["id_token"]

    session['id_token'] = id_token

    # if not is_access_token_valid(access_token, config["issuer"], config["client_id"]):
    #    return "Access token is invalid", 403

    # if not is_id_token_valid(id_token, config["issuer"], config["client_id"], NONCE):
    #    return "ID token is invalid", 403

    # Authorization flow successful, get userinfo and login user
    userinfo_response = requests.get(current_app.config["USERINFO_URI"],
                                     headers={'Authorization': f'Bearer {access_token}'}).json()

    unique_id = userinfo_response["sub"]
    user_email = userinfo_response["email"]
    user_name = userinfo_response["given_name"]

    user = User(
        id_=unique_id, name=user_name, email=user_email
    )

    if not User.get(unique_id):
        User.create(unique_id, user_name, user_email)

    login_user(user)
   # g.user =user

    session.pop('_flashes', None)

    if paginaNext != "":
        return redirect(paginaNext)
    else:
        return redirect(url_for("authInterlink.dashboard"))


def cargarNotifications():
    # Cargo las Notificaciones
    listNotifications = Notification._get_Notification_byModerCategory(
        category="survey", user=current_user.email)

    numRes = listNotifications['numRes']
    listNotifications = listNotifications['notifications']
    return listNotifications, numRes
