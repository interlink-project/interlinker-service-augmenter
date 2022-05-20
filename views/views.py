from locale import getlocale
import logging
import jwt
import datetime
from re import I
from flask import Blueprint, render_template, request, flash, jsonify, g, session, abort, after_this_request
import json
import requests
import math
import os
import iso8601
import asyncio

from asgiref.sync import async_to_sync

from werkzeug.utils import secure_filename
from api.notification import Notification
from authInterlink import authInterlink


from flask import redirect
from flask.helpers import url_for, make_response
from flask_mail import Mail, Message
from api import description
from tests.helpers import MockUser

from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from werkzeug.utils import redirect
from api.annotation import Annotation
from api.document import Document
from api.description import Description

from cryptography.fernet import Fernet

from datetime import date

from flask import current_app

import urllib.parse
from urllib.parse import unquote
from urllib import parse
import math
import uuid
import secrets

from app.config import settings

from app.languages import getLanguagesList

from app.messages import log, logapi


from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

import ssl


views = Blueprint('views', __name__, static_folder="./app/static",
                  template_folder="./app/templates")


# Integrations Roots:


@views.route('/assets/instantiate')
@login_required
def instantiateInterlinker():

    vectorPAs = Description._get_uniqueValues(campo="padministration")
    paList = []
    for pas in vectorPAs:
        key = pas["key"]

        if key == "":
            key = 'Unassigned'

        paList.append(key)
    # print(paList)
    if not ('Global' in paList):
        paList.insert(0, 'Global')

    return render_template("instantiate.html", user=current_user, publicsa=paList, servicepediaUrl=settings.REDIRECT_SERVICEPEDIA)


@views.route('/assets/<id>')
@login_required
def assetData(id):

    descriptiondata = Description._get_Descriptions_byId(id=id)[0]
    logging.info('La informacion del asset es:' + id)
    logging.info(descriptiondata)
    return jsonify(
        name=descriptiondata['title'],
        created_at=descriptiondata['created'],
        updated_at=descriptiondata['updated']
    )


@views.route('/assets/<id>/view')
@login_required
def assetView(id):
    description = Description._get_Descriptions_byId(id=id)[0]

    urlMainPage = [url['url']
                   for url in description['urls'] if url['ismain'] == True][0]

    return redirect(url_for("views.augment", rutaPagina=urlMainPage)+'?description='+id+"&integrationInterlinker=True")


@views.route('/assets/<id>', methods=["DELETE"])
@login_required
def assetDelete(id):

    description = Description._get_Descriptions_byId(id=id)[0]

    description.delete()

    return '', 204


@views.route('/assets/<id>/edit')
@login_required
def assetEdit(id):
    vectorPAs = Description._get_uniqueValues(campo="padministration")
    paList = []
    for pas in vectorPAs:
        key = pas["key"]

        if key == "":
            key = 'Unassigned'

        paList.append(key)
    # print(paList)
    if not ('Global' in paList):
        paList.insert(0, 'Global')

    description = Description._get_Descriptions_byId(id=id)[0]

    for itemUrl in description['urls']:
        if itemUrl['language'] != 'Undefined':
            itemUrl['langText'] = getLanguagesList()[itemUrl['language']]
        else:
            itemUrl['langText'] = "Undefined"

    return render_template("instantiate.html", user=current_user, description=description, option='edit', publicsa=paList)


@views.route('/assets/<id>/admin')
@login_required
def assetAdmin(id):
    description = Description._get_Descriptions_byId(id=id)[0]

    urlMainPage = [url['url']
                   for url in description['urls'] if url['ismain'] == True][0]

    categoria = request.args.get('category')

    page = request.args.get("page", 1)
    registroInicial = (int(page)-1)*10

    if(categoria == None or categoria == 'all'):
        categoria = ''

    res = []
    stats = []
    numRes = 0
    listUrlsPages = []
    for itemUrl in description['urls']:
        url = itemUrl['url']
        listUrlsPages.append(url)

        # Cargo las replies de cada annotacion:
        stats = stats + \
            Annotation.annotationStats(
                Annotation, descriptionId=description['id'])

    res = Annotation._get_by_multiple(Annotation, textoABuscar='', estados={
                                      'InProgress': True, 'Archived': False, 'Approved': True}, descriptionId=description['id'], category=categoria, notreply=True, page=page)
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

    return render_template("descriptionAsset.html", user=current_user, description=description, anotations=res, categoryLabel=categoria, paginacion=paginacion, urlMainPage=urlMainPage)
   # return 'la desc: '+category+'lauri is'+str(uri)


@views.route('/assets/<descriptionId>/<annotatorId>')
@login_required
def assetSubject(descriptionId, annotatorId):

    description = Description._get_Descriptions_byId(id=descriptionId)[0]

    urlMainPage = [url['url']
                   for url in description['urls'] if url['ismain'] == True][0]

    annotation = Annotation._get_Annotation_byId(id=annotatorId)[0]

    nroReplies = Annotation.count(
        query={'idReplyRoot': annotatorId, 'category': 'reply'})
    replies = Annotation.search(
        query={'idReplyRoot': annotatorId, 'category': 'reply'}, limit=nroReplies)

    nroRepliesOfAnnotation = nroReplies

    return render_template("subjectAsset.html", user=current_user, annotation=annotation, description=description, categoryLabel=annotation['category'], replies=replies, nroReplies=nroRepliesOfAnnotation, urlMainPage=urlMainPage)
   # return 'la desc: '+category+'lauri is'+str(uri)

# Builder:
# return redirect(url_for("authInterlink.description", descriptionId=id))


@views.route('/')
def inicio():

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
    # print(paList)

    if not ('Global' in paList):
        paList.insert(0, 'Global')

    textoABuscar = request.args.get("searchText")
    padministration = request.args.get("padministration")
    domain = request.args.get("domain")

    page = request.args.get("page", 1)
    registroInicial = (int(page)-1)*10

    totalRegistros = 0
    if(textoABuscar == None or textoABuscar == ''):
        res = Description.search(offset=registroInicial)
        totalRegistros = Description.count()
    else:
        res = Description._get_Descriptions(
            textoABuscar=textoABuscar, padministration=padministration, url=domain, offset=registroInicial)
        totalRegistros = Description._get_DescriptionsCounts(
            textoABuscar=textoABuscar, padministration=padministration, url=domain)

    for itemDesc in res:
        urlMainPage = [url['url']
                       for url in itemDesc['urls'] if url['ismain'] == True][0]
        itemDesc['mainUrl'] = urlMainPage

    pagesNumbers = math.ceil(totalRegistros/10)

    paginacion = {'page': page, 'pagesNumbers': pagesNumbers, 'totalRegisters': totalRegistros,
                  'searchBox': textoABuscar, 'padministration': padministration, 'url': domain}

    if not current_user.is_anonymous:
        # Cargo las Notificaciones
        listNotifications = Notification._get_Notification_byModerCategory(
            category="survey", user=current_user.email)

        numRes = listNotifications['numRes']
        listNotifications = listNotifications['notifications']
    else:
        numRes = 0
        listNotifications = []

    return render_template("home.html", descriptions=res, urls=urlList, publicsa=paList, paginacion=paginacion, notifications=listNotifications, notificationNum=numRes)


# Formulatio de carga de Pagina
@views.route("/buscar", methods=["POST"])
def buscar():
    sitio = request.form["nm"]
    userNombre = request.form["usr"]
    return redirect(url_for("views.augment", rutaPagina=sitio))


# Formulatio de carga de Pagina
@views.route("/registrar", methods=["POST"])
def saveDescription():
    logging.info('Los datos a guardar son:')
    logging.info(request.form)
    itemsDict = request.form.to_dict()

    title = itemsDict.pop("createTitle")
    description = itemsDict.pop("createDescription")
    keywords = itemsDict.pop("createKeywords")
    userNombre = itemsDict.pop("usr")
    descriptionId = itemsDict.pop("descriptionId")

    # Obtengo la opcion de tipo de Description
    is_portal = False
    if 'is_portal' in itemsDict.keys():
        is_portal = itemsDict.pop("is_portal")
        if is_portal == 'true':
            is_portal = True

    interlinkIntegration = False
    if 'interlinkerPlataform' in itemsDict.keys():
        interlinkIntegration = True

    # Obtengo el valor de la administracion publica
    try:
        publicAdmin = itemsDict.pop("createPA")
    except:
        publicAdmin = ""
    try:
        newPA = itemsDict.pop("addNewPA")
    except:
        newPA = ""
    if newPA != "":
        publicAdmin = newPA

    todayDateTime = datetime.datetime.now().replace(microsecond=0).isoformat()

    # Obtengo el listado de urls nuevo

    if 'MainUrlRadio' in itemsDict.keys():
        mainPageItem = itemsDict['MainUrlRadio']
    else:
        mainPageItem = 'url_1'

    listadoUrlNuevo = {}
    for key in itemsDict:
        if(key.startswith('url_')):

            ismain = False
            if(key == mainPageItem):
                ismain = True

            webAdress = itemsDict[key]
            langCode = itemsDict['langCode_'+key.split('_')[1]]
            langCodeSel = itemsDict['sel_'+key.split('_')[1]]

            if langCode == '':
                langCode = langCodeSel

            if len(langCode) > 2:
                langCode = 'Undefined'
            listadoUrlNuevo[webAdress] = [langCode, ismain]

    if(len(listadoUrlNuevo) == 0):
        # Si el campo de lista esta vacio miro el campo url
        flash("It is needed to add at least one URL of description.", "info")
        return jsonify({"error": "It is needed to add at least one URL of description"})

    # Busco si alguno de los URLS ya ha sido incluido en existe:

    if descriptionId == '':

        # ---------------------------------------------------------------------
        # Create:
        # ---------------------------------------------------------------------

        perms = {'read': ['group:__world__']}
        moderat = []

        # Creo listados de Urls:
        urls = []
        for itemUrlFormat in listadoUrlNuevo:
            newUrl = {
                'createdate': todayDateTime,
                'url': itemUrlFormat,
                'language': listadoUrlNuevo[itemUrlFormat][0],
                'ismain': listadoUrlNuevo[itemUrlFormat][1],
                'email': current_user.email
            }
            urls.append(newUrl)

        newdescription = Description(title=title, description=description,
                                     keywords=keywords, moderators=moderat,
                                     padministration=publicAdmin,
                                     permissions=perms, urls=urls, is_portal=is_portal
                                     )

        if(title == "" or description == "" or publicAdmin == ""):
            description = editDescripcion
            flash("Algunos campos de la descripción no son correctos.", "info")
            return redirect('/descriptionDetail')

        else:

            # Agrego al usuario creador como moderador.
            # Le permito ser moderador por 30 dias.
            from datetime import timedelta
            initDate = datetime.datetime.now(iso8601.iso8601.UTC).isoformat()
            endDate = (datetime.datetime.now(iso8601.iso8601.UTC) +
                       timedelta(days=30)).isoformat()

            newdescription['moderators'].append({
                "created": initDate,
                "expire": endDate,
                "email": current_user.email
            })

            # Guardo el tipo de portal
            newdescription['is_portal'] = is_portal

            # Actualizo la description
            newdescription.save(index="description")
            description = newdescription

            # Guardo los logs:
            # Create a new description

            logapi(
                {"action": "new_description", "object_id": description['id'], "model": "description", 'description_data': description})

            # Redirecciono a la descripcion creada:
            if interlinkIntegration:
                return jsonify({'id': description['id']})
            else:
                return redirect(url_for('authInterlink.description', descriptionId=description['id']))

    else:
        # ---------------------------------------------------------------------
        # Update:
        # ---------------------------------------------------------------------
        editDescripcion = Description._get_Descriptions_byId(id=descriptionId)[
            0]

        editDescripcion.title = title
        editDescripcion.description = description
        editDescripcion.keywords = keywords
        editDescripcion.padministration = publicAdmin
        editDescripcion.updated = todayDateTime
        editDescripcion.is_portal = is_portal

        listUrlUpdate = editDescripcion['urls']
        listModificado = editDescripcion['urls']

        # Busco Url a borrar:
        contador = 0
        for itemUrl in listUrlUpdate:
            if itemUrl['url'] not in listadoUrlNuevo.keys():
                listModificado.pop(contador)
            contador = contador+1

        # Actualizo el listado de links:
        for key in listadoUrlNuevo:

            webAdress = key
            langCode = listadoUrlNuevo[key][0]

            # Reviso que todos esten y los que no estan los agrego:

            existe = False
            for itemUrl in listModificado:
                if (itemUrl['url'] == webAdress):
                    # Ya existe
                    itemUrl['language'] = langCode
                    itemUrl['ismain'] = listadoUrlNuevo[key][1]
                    existe = True
                    break

            if existe == False:
                # Es nuevo y Agrego
                newUrl = {
                    'createdate': todayDateTime,
                    'url': webAdress,
                    'language': langCode,
                    'ismain': listadoUrlNuevo[key][1],
                    'email': current_user.email
                }
                listModificado.append(newUrl)

        editDescripcion['urls'] = listModificado

        # Comprobar los permisos de edicion del usuario:
        nroEnc = editDescripcion._get_checkPermisos_byId(
            email=userNombre, id=descriptionId)

        if(nroEnc != 0):
            editDescripcion.updateFields(index="description")
            description = editDescripcion
            flash("Registro editado correctamente.", "info")

            # Guardo los logs:
            # Create a new description

            logapi(
                {"action": "update_description", "object_id": description['id'], "model": "description", 'description_data': editDescripcion})

        else:
            description = editDescripcion
            flash("No tienes permisos de moderador para editar esta descripción.", "info")

    if interlinkIntegration:
        return jsonify({'id': description['id']})
    else:
        return redirect(url_for('authInterlink.editDescription', descriptionId=description['id'], option='edit'))


# return redirect(url_for("views.augment",rutaPagina=sitio,userId=userNombre))
""" def generar_clave():
    clave= Fernet.generate_key()
    session["claveCript"]=clave
    # with open("clave.key","wb") as archivo_clave:
    #     archivo_clave.write(clave)

def cargar_clave():
    return session["claveCript"]
    # try:
    #     return open("clave.key","rb").read()
    # except:
    #     return None """


@views.route("/claimModeration", methods=["POST"])
def claimModeration():

    itemsDict = request.form.to_dict()

    firstName = itemsDict.pop("firstName").title()
    lastName = itemsDict.pop("lastName").title()
    userPosition = itemsDict.pop("userPosition").title()
    oneUrl = itemsDict.pop("oneUrl")
    userMotivations = itemsDict.pop("userMotivations")

    userMotivations = userMotivations[0].upper()+userMotivations[1:]

    # This are the URI's
    urlList = []
    for key in itemsDict:
        if(key.startswith("id_")):
            urlList.append(itemsDict[key])

    if(len(urlList) == 0):
        flash("It is needed to add at least one URL of description.", "danger")
        return authInterlink.moderate()

    # Check if the urls of descriptions are valid:
    allUrlValid = True
    listMsgError = []
    for key in itemsDict:
        if(key.startswith("id_")):
            encontrado = Description._get_Descriptions_byId(id=itemsDict[key])
            if (len(encontrado) == 0):
                allUrlValid = False
                listMsgError.append('The description for ' +
                                    itemsDict[key]+' do not exist.')

    if(not allUrlValid):
        for itemError in listMsgError:
            flash(itemError)
        flash('Before requesting moderation privileges the descriptions must be created.')
        return authInterlink.moderate()
    else:

        itemsDict['email'] = current_user.email

        dataClaimEncoded = urllib.parse.urlencode(itemsDict)

        # Now will send the email:
        msg = Message('The user '+firstName+' '+lastName+' ha realizado un claim to be a moderator.',
                      sender='support@interlink-project.eu', recipients=['interlinkdeusto@gmail.com'])

        sites = " ".join(str(x) for x in urlList)
        claimInfo = "The user {} {} who is a {} ".format(
            firstName, lastName, userPosition)+"send a request to be a moderator of the following descriptions identifiers: "

        # Encripto los datos del Claim:

        message = dataClaimEncoded

        key = settings.CRYPT_KEY

        # cargar_clave()
        # if key ==None:
        #     generar_clave()
        #     key =cargar_clave()

        fernet = Fernet(key)
        encMessage = fernet.encrypt(message.encode())
        #print("original string: ", message)
        #print("encrypted string: ", encMessage)

        textHref = settings.REDIRECT_SERVICEPEDIA+'/aproveModerator?datos=' + \
            encMessage.decode('ascii')

        msg.html = """<td width='700' class='esd-container-frame' align='center' valign='top'> 
        <table cellpadding='0' cellspacing='0' width='100%' style='background-color: #515151; border-radius: 30px 36
        333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
        30px 30px 30px; border-collapse: separate;' bgcolor='#515151'>
            <tbody>
                <tr>
                    <td align='center' class='esd-block-text es-p20t'>
                        <h1 style='color: #ffffff;'>Description moderation request</h1>
                    </td>
                </tr>
                <tr>
                    <td align='center' style='padding-right: 140px; padding-left: 140px;' class='esd-block-text es-m-p20l es-m-p20r es-p30t'>
                        <p style='font-size: 16px; letter-spacing: 1px; color: #ffffff;'>"""+claimInfo+"""</p>
                        <p style='font-size: 16px; letter-spacing: 1px; color: #ffffff; color: white;
    padding: 14px 25px;
    text-align: center;
    text-decoration: none;'>"""+sites+"""</p>
                    </td>
                </tr>
                <tr>
                    <td align='center' style='padding-right: 110px; padding-left: 110px;' class='esd-block-text es-m-p20l es-m-p20r es-p30t es-p40b'>
                        <p style='font-size: 16px; letter-spacing: 1px; color: #ffffff;'>The motivations are:</p>
                        <p  style='font-size: 16px; letter-spacing: 1px; color: #ffffff;'>"""+userMotivations+"""</p>
                    </td>
                </tr>
                <tr>
                    <td align='center'  style='padding-bottom: 50px; font-size: 20px; color: #ffffff;'><a target='_blank' style='background-color: #f44336;
    color: white;
    padding: 14px 25px;
    text-align: center;
    text-decoration: none;
    display: inline-block;  border-radius: 5px;' href='"""+textHref + """'>Aproved the request.</a></td>
                </tr>
            </tbody>
        </table>
    </td>"""

        # Agrego los archivos

        uploaded_file = request.files['archivoIdentificacion']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':

            file_ext = os.path.splitext(filename)[1]
            if file_ext not in settings.UPLOAD_EXTENSIONS:
                abort(400)
            # Guardo Archivo
            filepathTemp = "app/Render/"+filename
            uploaded_file.save(filepathTemp)

            filepathTemp = "Render/"+filename
            # Lo adjunto al email
            with current_app.open_resource(filepathTemp) as fp:
                msg.attach(filename, 'application/pdf', fp.read())

            # Lo borro del disco

            # os.remove(filepathTemp)

            # Borro el archivo generado despues de que hago la descarga.
            @after_this_request
            def delete(response):
                # logging.info('root:')
                logging.error(filepathTemp)

                os.remove('app/'+filepathTemp)
                return response

        mail = Mail(current_app)
        mail.send(msg)

        flash("The moderation request has been send.", "info")

        return authInterlink.moderate()

    # return render_template("moderate.html",descriptions=res,urls=urlList,publicsa=paList,paginacion=paginacion)


@views.route("/aproveModerator", methods=["GET", "POST"])
@login_required
def aproveModerator():

    argumentos = request.args.to_dict()

    # Obtain Datos datos
    datosBin = argumentos.pop('datos').encode('ascii')

    # key = cargar_clave()
    # if key ==None:
    #     generar_clave()
    #     key =cargar_clave()

    key = settings.CRYPT_KEY

    fernet = Fernet(key)

    if unquote(datosBin) != '':

        argumentos = fernet.decrypt(datosBin).decode()
        argumentos = unquote(argumentos)

        listArgs2 = parse.parse_qsl(argumentos)
        argumentos = dict(listArgs2)

        argKeys = argumentos.keys()
        email = argumentos.pop('email')

        existUrl = any(list(map(lambda x: x.startswith('url_'), argKeys)))

        urlList = []
        lisDescriptions = {}
        if existUrl:
            for key in argumentos:
                if(key.startswith('id_')):
                    # urlList.append(argumentos[key])
                    encontrado = Description._get_Descriptions_byId(
                        id=argumentos[key])
                    if (len(encontrado) != 0):
                        urlList.append(encontrado[0])
                        # lisDescriptions[argumentos[key]]=Description._get_Descriptions_byURI(url=argumentos[key])[0]

        today = date.today()
        endDate = today.replace(today.year + 1)
    else:
        email = ''
        urlList = []
        today = date.today()
        endDate = today.replace(today.year + 1)
        # endDate=today.strftime("%Y-%m-%d")

    return render_template("approveClaim.html", email=email, argumentos=urlList, now=today.strftime("%Y-%m-%d"), endDate=endDate.strftime("%Y-%m/%d"))


@views.route("/aprovarClaimsList", methods=["POST"])
def aprovarClaimsList():

    argumentos = request.form.to_dict()
    usuarioModerator = argumentos.pop('email')
    adminComment = argumentos.pop('commentBox')

    argumentosList = list(argumentos.values())

    contador = 0
    nroActualizaciones = 0
    listMsg = []
    for i in range(math.ceil(len(argumentosList)/4)):
        if(i != 0):
            contador = i*4
        estado = argumentosList[contador]
        descriptionId = argumentosList[contador+1]
        initDate = argumentosList[contador+2]
        endDate = argumentosList[contador+3]

        # Agrego como moderador en la descripcion:
        descriptions = Description._get_Descriptions_byId(id=descriptionId)

        if len(descriptions) == 1:
            if estado == "on":
                descripcionAct = descriptions[0]

                if(len(descripcionAct['moderators']) == 0):
                    descripcionAct['moderators'] = []

                descripcionAct['moderators'].append({
                    "created": initDate,
                    "expire": endDate,
                    "email": usuarioModerator
                })
                descripcionAct.updateModerators(index="description")
                nroActualizaciones = nroActualizaciones+1
                listMsg.append("The moderation of " +
                               descriptions[0]['title']+" has been assigned.")
        elif len(descriptions) == 0:
            listMsg.append(
                "The description could not be found (Most be created first) !.")

    listActionsBody = ""
    for msnItem in listMsg:
        listActionsBody = listActionsBody + \
            """<p style='font-size: 16px; letter-spacing: 1px; color: #ffffff;'>"""+msnItem+"""</p>"""

    msg = Message('Your claim has been resolved.',
                  sender='support@interlink-project.eu', recipients=[usuarioModerator])

    msg.html = """<td width='700' class='esd-container-frame' align='center' valign='top'> 
    <table cellpadding='0' cellspacing='0' width='100%' style='background-color: #515151; border-radius: 30px 36
    333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
    30px 30px 30px; border-collapse: separate;' bgcolor='#515151'>
        <tbody>
            <tr>
                <td align='center' class='esd-block-text es-p20t'>
                    <h2 style='color: #ffffff;'>Your claim to be a moderator     has been resolved.</h2>
                    
                </td>
            </tr>

            <tr>
                <td align='center' style='padding-right: 110px; padding-left: 110px;' class='esd-block-text es-m-p20l es-m-p20r es-p30t es-p40b'>
                    """+listActionsBody+"""
                </td>
            </tr>

             <tr>
                <td align='center' style='padding-right: 110px; padding-left: 110px;' class='esd-block-text es-m-p20l es-m-p20r es-p30t es-p40b'>
                    <p style='font-size: 16px; letter-spacing: 1px; color: #ffffff;'>The admin comments are:</p>
                    <p  style='font-size: 16px; letter-spacing: 1px; color: #ffffff;'>"""+adminComment+"""</p>
                </td>
            </tr>

           
            
        </tbody>
    </table>
    </td>"""

    mail = Mail(current_app)
    mail.send(msg)

    for msnItem in listMsg:
        flash(msnItem, "info")

    return redirect(url_for("views.aproveModerator", datos='', argumentos=argumentosList))


# Formulatio de carga de Pagina
@views.route("/visor", methods=["GET"])
def visor():
    return render_template("prototipo.html")


@views.route("/survey", methods=["GET"])
def survey():
    return render_template("survey.html")


def mostrarPagina(rutaPagina, integrationInterlinker='False'):
    # En el caso que se tiene interes en una anotacion en particular
    argumentos = request.args.to_dict()
    anotationSel = ''
    descriptionRef = ''
    descripcionSel = None

    scriptToFocusParragraph = ''
    if('annotationSel' in argumentos.keys()):
        anotationSel = argumentos.pop('annotationSel')
        session['anotationSel'] = anotationSel

    if('description' in argumentos.keys()):
        descriptionRef = argumentos.pop('description')
        descripcionSel = Description._get_Descriptions_byId(id=descriptionRef)[
            0]
    if('integrated' in argumentos.keys()):
        integrationInterlinker = argumentos.pop('integrated')

    if('integrationInterlinker' in argumentos.keys()):
        integrationInterlinker = argumentos.pop('integrationInterlinker')

    # Obtengo el usuario de session
    # Lo pongo en la session de cookie local:
    if not current_user.is_anonymous:
        session['userId'] = current_user.email  # setting session date
        session['username'] = current_user.email
        userId = current_user.email
    else:
        userId = 'Anonymous'

    headersUserAgent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    }

    # Fix ssl issues:
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context

    # Obtengo el codigo:
    response = requests.get(rutaPagina, headers=headersUserAgent, verify=False)
    resp_Contenido = response.content

    # Valido si el sitio es sensible al Mayusculas y Minusculas.
    isCaseSensitive = False
    if('latvija' in rutaPagina):
        isCaseSensitive = True

    import codecs

    try:
        resp_Contenido = codecs.decode(resp_Contenido, 'utf-8')
    except:
        print('Trato de cargar con utf-8')

    # If the page is a single page try to load code:
    # Working with React Pages.
    if False:
        from selenium.webdriver.chrome.options import Options
        from selenium import webdriver
        import time

        DRIVER_PATH = "/chromedriver/chromedriver"

        options = Options()
        options.headless = True
        # overcome limited resource problems
        options.accept_insecure_certs = True
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("start-maximized")

        driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

        driver.delete_all_cookies()
        driver.implicitly_wait(15)
        driver.maximize_window()

        url = rutaPagina

        driver.get(url)
        time.sleep(5)  # Let the user actually see something!

        pageSource = driver.find_element_by_xpath(
            "//*").get_attribute("outerHTML")

        resp_Contenido = pageSource

    # print(resp_Contenido.decode())
    #soup = BeautifulSoup(resp_Contenido, 'html5lib')
    #soup = BeautifulSoup(resp_Contenido, 'lxml')
    soup = BeautifulSoup(resp_Contenido, 'html.parser')

    # Quitamos los scripts:
    # for data in soup(['script', 'pre', 'noscript']):
    #     # Remove tags
    #     data.decompose()

    # print(soup.decode)

    try:
        headTag = soup.html.head
    except:
        headTag = soup.html
     # Inserto las librerias de css de la pagina:

    # Nuevamente valido la codificacion:
    # If html.parse no funciona trato con la lib html5lib:
    if headTag == None:
        # I try another codec:
        soup = BeautifulSoup(resp_Contenido, 'html5lib')
        # print(soup.decode)
        try:
            headTag = soup.html.head
        except:
            headTag = soup.html

    listScript = soup.find_all('script')
    listScriptRelatedEstilos = []
    logging.info('Los script son:')

    for itemScript in listScript:
        if itemScript.attrs.get("src"):
            if 'bootstrap' in itemScript.attrs.get("src"):
                completeSrc = urljoin(rutaPagina, itemScript.attrs.get("src"))
                listScriptRelatedEstilos.append(completeSrc)
                logging.info(completeSrc)
            if 'moment' in itemScript.attrs.get("src"):
                completeSrc = urljoin(rutaPagina, itemScript.attrs.get("src"))
                listScriptRelatedEstilos.append(completeSrc)
                logging.info(completeSrc)
            if 'jquery' in itemScript.attrs.get("src"):
                completeSrc = urljoin(rutaPagina, itemScript.attrs.get("src"))
                listScriptRelatedEstilos.append(completeSrc)
                logging.info(completeSrc)

    logging.info('Los script Seleccionados:')
    logging.info(listScriptRelatedEstilos)
    logging.info('')

    # Quitamos los scripts:
    for data in soup(['script', 'pre', 'noscript']):
        data.decompose()

    # 1 Obtengo los archivos css
    css_files = []

    count = 0

    # Quito las propagandas de la pagina:

    listDiv = soup.find_all("div")
    for div in listDiv:
        if div.attrs != None:
            if div.attrs.get("class"):
                classesStr = div.attrs['class']

                for itemClass in classesStr:

                    if 'header-ad' in itemClass:
                        div.decompose()
                        break
                    if 'ad-' in itemClass:
                        div.decompose()
                        break
                    if 'advertising' in itemClass:
                        div.decompose()
                        break

    # Special configuration for a page:
    # -------------------------------------------------
    listCssToAvoid = []
    # The guardian:
    listCssToAvoid.append('print.css')
    listCssToAvoid.append('.js')

    # Lista de atributos que deben cambiar de nombre:
    # Reemplazo del tag video el attributo data-src por src
    REPLACEMENTS = [('video', 'src', 'data-src'),  # video.data-src -> src
                    ('video', 'autoplay', ''),
                    ('figure', 'src', 'data-bg'),
                    ('img', 'src', 'data-src'),
                    ('img', 'src', 'data-lazy-src')
                    ]

    # Busca y reemplaza
    def replace_tags(soup, replacements=REPLACEMENTS):
        for tag, new_attribs, old_attibute in replacements:
            for node in soup.find_all(tag):
                if old_attibute == '':
                    node[new_attribs] = None
                if old_attibute in node.attrs:
                    node[new_attribs] = node[old_attibute]
                    del node[old_attibute]
        return soup

    soup = replace_tags(soup, REPLACEMENTS)

    # Reemplazo la fuente del picture
    listPictures = soup.find_all('picture')

    contado = 0
    for node in listPictures:
        try:
            if node.img['src'] != None:
                if node.img['src'].startswith('data:image'):
                    if node.source != None:
                        if 'srcset' in node.source.attrs:
                            del node.img['src']
                            node.img['src'] = node.source.attrs['srcset']
                            contado = contado+1
                            # print(''+str(contado))
                            # print(node)
        except:
            continue

    # Reemplazo la fuente del picture
    listFigures = soup.find_all('figure')

    for node in listFigures:
        if 'data-bg' in node.attrs:
            node['src'] = node.attrs['data-bg']
            del node['data-bg']
        node.name = 'img'

    listCss = soup.find_all("link")

    # Quito las referencias viejas al css

    for a in soup.findAll('link', href=True):
        a.extract()

    for css in listCss:

        if css.attrs.get("href"):

            if css.attrs.get("rel"):
                # print(css.attrs.get("rel"))
                # or "dns-prefetch" in css.attrs.get("rel") or "preconnect" in css.attrs.get("rel"):
                if "shortcut" in css.attrs.get("rel") or "apple-touch-icon" in css.attrs.get("rel") or "alternate" in css.attrs.get("rel"):
                    css.decompose()
                    continue
            if css.attrs.get("as"):
                if css.attrs.get("as") == "script" or css.attrs.get("as") == "font":
                    css.decompose()
                    continue

            # if the link tag has the 'href' attribute
            css_url = urljoin(rutaPagina, css.attrs.get("href"))
            if "css" in css_url:

                # Busco una coincidencia:
                esIndeseable = False
                for terminacionCss in listCssToAvoid:
                    if terminacionCss in css_url:

                        esIndeseable = True
                        break

                if not(esIndeseable):
                    count += 1
                    css_files.append(css_url)
                    anotationTemp = soup.new_tag(
                        'link', href=css_url, rel="stylesheet")
                    headTag.append(anotationTemp)
                    #print("Line{}: {}".format(count, css_url))
            else:
                headTag.append(css)

    # Obtengo el usuario Logueado o pongo anonimo:

    usuarioActivo = current_user.email if not current_user.is_anonymous else 'Anonymous'

    for a_Link in soup.find_all("a"):
        if a_Link.attrs.get("href"):
            hrefVal = a_Link.attrs.get("href")
            if descripcionSel['is_portal'] == 'false':
                # Quito los enlaces

                newURLVal = rutaPagina

                if isCaseSensitive:
                    newURLVal = newURLVal.lower()

                urlLink = url_for(
                    'views.augment', rutaPagina=newURLVal)+'?description='+descriptionRef+'&integrated='+integrationInterlinker
                a_Link.attrs['href'] = urlLink
                a_Link.attrs['integrated'] = integrationInterlinker
                a_Link.attrs['is_portal'] = 'false'
                a_Link.attrs['onclick'] = "navegatetoPage(event)"

            else:

                # Pongo los enlaces

                if hrefVal.startswith('/'):
                    newURLVal = urljoin(rutaPagina, hrefVal)

                    if isCaseSensitive:
                        newURLVal = newURLVal.lower()

                    urlLink = url_for(
                        'views.augment', rutaPagina=newURLVal)+'?description='+descriptionRef+'&integrated='+integrationInterlinker
                    a_Link.attrs['href'] = urlLink
                    a_Link.attrs['integrated'] = integrationInterlinker
                    a_Link.attrs['is_portal'] = 'true'
                    a_Link.attrs['onclick'] = "navegatetoPage(event)"

                if hrefVal.startswith('https://') or hrefVal.startswith('http://'):

                    # If the external link is http I change them to https to visualited well
                    if settings.DOMAIN != 'localhost':
                        hrefVal.replace("http://", "https://")

                    # Pregunto si el enlace esta dentro del mismo dominio de la pagina
                    if settings.DOMAIN in hrefVal:

                        urlLink = url_for(
                            'views.augment', rutaPagina=hrefVal)+'?description='+descriptionRef+'&integrated='+integrationInterlinker
                        a_Link.attrs['href'] = urlLink
                        a_Link.attrs['integrated'] = integrationInterlinker
                        a_Link.attrs['is_portal'] = 'true'
                        a_Link.attrs['onclick'] = "navegatetoPage(event)"
                    else:

                        urlLink = hrefVal
                        a_Link.attrs['href'] = urlLink
                        a_Link.attrs['integrated'] = integrationInterlinker
                        a_Link.attrs['isexternal'] = 'true'
                        a_Link.attrs['is_portal'] = 'true'
                        a_Link.attrs['onclick'] = "navegatetoPage(event)"

    #print("Total CSS insertados en the page:", len(css_files))

    # Inserto las librerias del AnnotationJS
    # Creo los tags necesarios:

    anotationcss1 = soup.new_tag(
        'link', href=url_for('static', filename='/lib/annotator-full.1.2.9/annotator.min.css'), rel="stylesheet")
    anotationcss2 = soup.new_tag(
        'link', href=url_for('static', filename='/src/css/style.css'), rel="stylesheet")
    anotationcss3 = soup.new_tag(
        'link', href=url_for('static', filename='/lib/css/annotator.touch.css'), rel="stylesheet")

    fontAwesome3 = soup.new_tag(
        'link', href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", rel="stylesheet")

    import flask_babel
    idiomaBabel = flask_babel.get_locale().language

    # Para la internacionalizacion:
    internacii18nLink = soup.new_tag(
        'link', href=url_for('static', filename='/locale/'+idiomaBabel+'/annotator.po'), type="application/x-po",  rel="gettext")

    servicepediaPath = settings.REDIRECT_SERVICEPEDIA

    if not (settings.DOMAIN == "localhost"):
        servicepediaPath = servicepediaPath.replace(
            "http://", "https://")

    descriptionRedirect = ''
    metauserName = soup.new_tag(
        'meta', id='databackend', basepath=settings.BASE_PATH, servicepediapath=servicepediaPath, descriptionRef=descriptionRef, currentuser=usuarioActivo, integrationInterlinker=integrationInterlinker, is_portal=descripcionSel['is_portal'])

    # Agrego codificacion a la pagina:

    metatag = soup.new_tag('meta')
    metatag.attrs['charset'] = 'utf-8'
    headTag.append(metatag)

    try:
        headTag.append(metauserName)
    except:
        #print("Excepcion en Username")
        #logging.error("Da una excepcion en esta linea")
        pass

    try:
        headTag.append(anotationcss1)
    except:
        #print("Excepcion en ccs1")
        pass

    try:
        headTag.append(anotationcss2)
    except:
        #print("Excepcion en ccs1")
        pass

    try:
        headTag.append(anotationcss3)
    except:
        #print("Excepcion en ccs1")
        pass

    try:
        headTag.append(fontAwesome3)
    except:
        #print("Excepcion en ccs1")
        pass

    try:
        headTag.append(internacii18nLink)
    except:
        #print("Excepcion en ccs1")
        pass

    try:
        soup.html.head = headTag
    except:
        #print("Excepcion en ccs1")
        pass

    soup = obtenerReemplazarImagenes(rutaPagina, soup)

    # Ingreso el script para iniciar Aplicacion Annotation
    try:
        bodyTag = soup.html.body
    except:
        #print("Excepcion en ccs1")
        pass

    jqueryScript1 = soup.new_tag(
        'script', src=url_for('static', filename='lib/jquery-1.9.1.js'))
    jqueryScript3 = soup.new_tag(
        'script', src=url_for('static', filename='lib/jquery-i18n-master/jquery.i18n.min.js'))
    jqueryScript7 = soup.new_tag(
        'script', src=url_for('static', filename='locale/'+idiomaBabel+'/annotator.js'))
    jqueryScript2 = soup.new_tag(
        'script', src=url_for('static', filename='lib/annotator-full.1.2.9/annotator-full.min.js'))

    jqueryScript4 = soup.new_tag(
        'script', src=url_for('static', filename='lib/jquery.dateFormat.js'))
    jqueryScript5 = soup.new_tag(
        'script', src=url_for('static', filename='lib/jquery.slimscroll.js'))

    jqueryScript6 = soup.new_tag(
        'script', src=url_for('static', filename='lib/lunr.js-0.5.7/lunr.min.js'))

    jqueryScript8 = soup.new_tag(
        'script', src=url_for('static', filename='lib/annotator.touch.js'))
    jqueryScript9 = soup.new_tag('script', src=url_for(
        'static', filename='src/view_annotator.js'))
    jqueryScript10 = soup.new_tag('script', src=url_for(
        'static', filename='src/categories.js'))
    jqueryScript11 = soup.new_tag(
        'script', src=url_for('static', filename='src/search.js'))

    jqueryScript13 = soup.new_tag(
        'script', src=url_for('static', filename='lib/tinymce/tinymce.min.js'))
    jqueryScript14 = soup.new_tag('script', src=url_for(
        'static', filename='src/richEditor.js'))

    internacii18nScript = soup.new_tag(
        'script', src=url_for('static', filename='lib/gettext.js'))

    socketioLibScript = soup.new_tag(
        'script', src=url_for('static', filename='lib/socketio/socket.io.min.js'))

    # Agrego las librerias personalizadas:

    # Defino la funcion de navegacion entre enlaces:
    #  Muestro un mensaje que es una pagina única
    onclickLinkScript = soup.new_tag('script')
    onclickLinkTemp = """ 
    function navegatetoPage(event) {
        if(event.type=='click'){
        event.preventDefault();
        
        integrated = event.target.getAttribute('integrated');
        is_portal = event.target.getAttribute('is_portal');
        
        
        var href = event.currentTarget.href;
        
        if (is_portal == 'false'){
            alert('This description is a single page, can´t navegate to other pages.');
            return false;
        }else{
            
            try {
                is_external = event.target.getAttribute('isexternal');
                if(is_external=='true'){
                    alert('You are about to navigate out of the portal pages. You will not be able to make annotations on these pages.');    
                }
            } catch (error) {
            }
            
            
        }
        
        sessionStorage.setItem("integrated",integrated);
        window.location = href;
        }
    }

    """

    onclickLinkScript.string = onclickLinkTemp
    bodyTag.append(onclickLinkScript)

    # Agrego librerias de estilos para funcionalidad (bootstrap)
    for itemScript in listScriptRelatedEstilos:
        logging.info('El estilo que trato de cargar es:')
        logging.info(itemScript)
        jsEstilosPage = soup.new_tag('script', src=itemScript)
        bodyTag.append(jsEstilosPage)

    try:
        bodyTag.append(jqueryScript1)
        bodyTag.append(jqueryScript3)

        bodyTag.append(internacii18nScript)
        bodyTag.append(jqueryScript7)
        bodyTag.append(jqueryScript2)

        bodyTag.append(jqueryScript4)
        bodyTag.append(jqueryScript5)
        bodyTag.append(jqueryScript6)

        bodyTag.append(jqueryScript8)
        bodyTag.append(jqueryScript9)
        bodyTag.append(jqueryScript10)
        bodyTag.append(jqueryScript11)

        # bodyTag.append(jqueryScript12)
        bodyTag.append(jqueryScript13)
        bodyTag.append(jqueryScript14)

        bodyTag.append(socketioLibScript)

    except:
        #print("Excepcion en ccs1")
        pass

    anotationIniScript = soup.new_tag('script')
    anotationInitScriptTemp = """ 
     
    jQuery(function ($) {

              
        
            $.i18n.load(i18n_dict);
            // Customise the default plugin options with the third argument.
            var annotator = $('body').annotator().annotator().data('annotator');
            var propietary = '"""+userId+"""';
            annotator.addPlugin('Permissions', {
                user: propietary,
                permissions: {
                    'read': [propietary],
                    'update': [propietary],
                    'delete': [propietary],
                    'admin': [propietary]
                },
                showViewPermissionsCheckbox: true,
                showEditPermissionsCheckbox: false
            });

            sessionStorage.setItem('user', '"""+userId+"""');   

            $('body').annotator().annotator('addPlugin', 'RichEditor');
            $('body').annotator().annotator('addPlugin', 'Categories', {
                        feedback: 'annotator-hl-destacat',
                        question: 'annotator-hl-subratllat',
                        term: 'annotator-hl-term'
                        }
            );
            $('body').annotator().annotator('addPlugin', 'AnnotatorViewer');
            


 
            //let uriAdress =$(location).attr('href');
            //const uriAdressBase = uriAdress.split('#')[0];

            //Dejo unicamente la primera parte del uri
            uriAdressBase = '"""+rutaPagina+"""'; 
            descriptionId = '"""+descriptionRef+"""';
            state = 1;   //No mostrar los archivados

            console.log(uriAdressBase)
            $('body').annotator().annotator('addPlugin', 'Store',{
                        annotationData: {uri:uriAdressBase,descriptionId:descriptionId,not_state:state},
                        loadFromSearch: {uri:uriAdressBase,descriptionId:descriptionId,not_state:state}
                        }
            );

           
            
            //noinspection JSJQueryEfficiency
            $('body').annotator().annotator('addPlugin', 'Search');

            //Annotation scroll
            $('#anotacions-uoc-panel').slimscroll({height: '100%'});

            //$('body').annotator().annotator("setupPlugins");

        });

    """

    anotationIniScript.string = anotationInitScriptTemp

    try:
        bodyTag.append(anotationIniScript)

        # Inserto
        # Es como poner una emvoltura sobre un Tag
        bodyTag.wrap(soup.new_tag("div", id="contenidoAnotar"))
        soup.html.body = bodyTag
    except:
        #print("Excepcion en ccs1")
        pass
    return soup

# Cargo la pagina desde beautifulSoup y la muestro en pantalla


@views.route("/augment/<path:rutaPagina>", methods=["GET", "POST"])
def augment(rutaPagina, integrationInterlinker='False'):

    soup = mostrarPagina(rutaPagina, integrationInterlinker)

    headers = {'Content-Type': 'text/html',
               'x-annotator-auth-token': generate_token()}

    return make_response(soup.prettify(), 200, headers)

# Cargo la pagina desde beautifulSoup y la muestro en pantalla


@views.route("/augments/<path:rutaPagina>", methods=["GET", "POST"])
@login_required
def augments(rutaPagina, integrationInterlinker='False'):

    soup = mostrarPagina(rutaPagina, integrationInterlinker)

    headers = {'Content-Type': 'text/html',
               'x-annotator-auth-token': generate_token()}

    return make_response(soup.prettify(), 200, headers)


def generate_token():
    return jwt.encode({
        'consumerKey': settings.CONSUMER_KEY,
        'userId': current_user.id,
        'issuedAt': _now().isoformat() + 'Z',
        'ttl': CONSUMER_TTL
    }, CONSUMER_SECRET)


def obtenerReemplazarImagenes(rutaPagina, soup):
    # De la misma forma busco todas las imagenes:
    urls = []
    for img in soup.find_all("img"):

        img_url = img.attrs.get("src")
        img_url_datOr = img.attrs.get("data-original")

        if img_url_datOr:
            img_url = img.attrs.get("data-original")
            del img["data-original"]

        else:
            if not img_url:
                # if img does not contain src attribute, just skip
                continue

        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(rutaPagina, img_url)

        # try:
        #     pos = img_url.index("?")
        #     img_url = img_url[:pos]
        # except ValueError:
        #     pass

        # finally, if the url is valid
        # if is_valid(img_url):
        img.attrs['src'] = img_url
        # urls.append(img_url)
    # #print(urls)

    # Reemplazo las fuentes de las imagenes
    # for img in soup.findAll('img'):
    #     for img_urlLine in urls:
    #         if img['src'] in img_urlLine:
    #             #print("Cambia "+img['src']+" por: "+img_urlLine)
    #             img['src'] = img_urlLine
    #             break

    return soup


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


# Replace these with your details
CONSUMER_SECRET = secrets.token_urlsafe(16)

# Only change this if you're sure you know what you're doing
CONSUMER_TTL = settings.CONSUMER_TTL


@views.route("/token")
def generate_token():
    return jwt.encode({
        'consumerKey': settings.CRYPT_KEY,
        'userId': 1,
        'issuedAt': _now().isoformat() + 'Z',
        'ttl': CONSUMER_TTL
    }, CONSUMER_SECRET)


def _now():
    return datetime.datetime.utcnow().replace(microsecond=0)
