from re import I
from flask import Blueprint, render_template, request, flash, jsonify, g,session
import json, requests, math

from authInterlink import authInterlink


from flask import redirect
from flask.helpers import url_for,make_response
from flask_mail import Mail, Message
from annotator import description
from tests.helpers import MockUser

from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from werkzeug.utils import redirect
from annotator.annotation import Annotation
from annotator.document import Document
from annotator.description import Description

from datetime import date

from flask import current_app

import urllib.parse
import math


from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)



views = Blueprint('views',__name__,static_folder="static",template_folder="templates")


""" @views.route('/',methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        anotacion = request.form.get('anotacion')

        if len(anotacion) < 1:
            flash('Anotation is too short!', category='error')
        else:
            new_anotacion = Annotation(texto=anotacion,uri='http://127.0.0.1:8000', user_id=1)
            db.session.add(new_anotacion)
            db.session.commit()
            flash('Annotation added!', category='success')

    return render_template("home.html")
 """

@views.route('/')
def inicio():
 
    #Cargo los combos:

    vectorUrls=Description._get_uniqueValues(campo="url")
    urlList=[]
    for urls in vectorUrls:
        key=urls["key"]
        if(key!=""):
            domain = urlparse(key).netloc
            if not (domain in urlList):
                urlList.append(domain)
    print(urlList)





    vectorPAs=Description._get_uniqueValues(campo="padministration")
    paList=[]
    for pas in vectorPAs:
        key=pas["key"]

        if key=="":
            key='Unassigned'

        paList.append(key)
    print(paList)


    textoABuscar=request.args.get("searchText")
    padministration=request.args.get("padministration")
    domain=request.args.get("domain")

    page=request.args.get("page",1)
    registroInicial=(int(page)-1)*10
    
    

    totalRegistros=0
    if(textoABuscar==None or textoABuscar==''):
        res= Description.search(offset=registroInicial)
        totalRegistros= Description.count()
    else:
        res= Description._get_Descriptions(textoABuscar=textoABuscar,padministration=padministration,url=domain,offset=registroInicial)
        totalRegistros= Description._get_DescriptionsCounts(textoABuscar=textoABuscar,padministration=padministration,url=domain)
        

    pagesNumbers=math.ceil(totalRegistros/10)
    
    paginacion={'page':page,'pagesNumbers':pagesNumbers,'totalRegisters':totalRegistros,'searchBox':textoABuscar,'padministration':padministration,'url':domain}


    return render_template("home.html",descriptions=res,urls=urlList,publicsa=paList,paginacion=paginacion)





#Formulatio de carga de Pagina
@views.route("/buscar",methods=["POST"])
def buscar():
    sitio = request.form["nm"]
    userNombre=request.form["usr"]
    return redirect(url_for("views.modifica",rutaPagina=sitio,userId=userNombre))







#Formulatio de carga de Pagina
@views.route("/registrar",methods=["POST"])
def saveDescription():
    
    site = request.form["createUrl"]
    title = request.form["createTitle"]
    description = request.form["createDescription"]
    keywords = request.form["createKeywords"]
    userNombre=request.form["usr"]

    try:
        publicAdmin=request.form["createPA"]
    except:
        publicAdmin=""

    try:
        newPA=request.form["addNewPA"]
    except:
        newPA=""

    if newPA!="":
        publicAdmin=newPA


    todayDateTime=datetime.datetime.now().replace(microsecond=0).isoformat()


    #Example of vector register:
    #perms = {'read': ['group:__world__']}

    

    #Busco si esta la descripcion funciona:

    editDescripcion =Description._get_Descriptions_byURI(url=site)
    
    
    if len(editDescripcion)==0:
        #Create:

        perms = {'read': ['group:__world__']}
  
        moderat = {}

        newdescription=Description(title=title,description=description,
                                keywords=keywords,moderators=moderat,
                                padministration=publicAdmin,url=site,
                                permissions=perms
                                )
    
    
        if(title=="" or description==""  or publicAdmin=="" or site=="" ):
            description=editDescripcion 
            flash("Algunos campos de la descripción no son correctos.","info")
            return redirect('/descriptionDetail')

        else:
            newdescription.save(index="description")
            description=newdescription
            flash("Registro creado correctamente.","info")

    else:
        #Update: 
        editDescripcion=editDescripcion[0]

        editDescripcion.title=title
        editDescripcion.description=description
        editDescripcion.keywords=keywords
        editDescripcion.padministration=publicAdmin
        editDescripcion.updated=todayDateTime


        #Comprobar los permisos de edicion del usuario:
        nroEnc=editDescripcion._get_checkPermisos_byURI(email=userNombre,url=site)

        if(nroEnc!=0):
            editDescripcion.updateFields(index="description")   
            description=editDescripcion 
            flash("Registro editado correctamente.","info")

            

        else:
            description=editDescripcion 
            flash("No tienes permisos de moderador para editar esta descripción.","info")


        


    
    
    return redirect('/description/'+description['id']+'/edit')

""" 
    
    "title": {"type": "string","analyzer": "standard"},
    "description": {"type": "string","analyzer": "standard"},
    "keywords": {"type": "string","analyzer": "standard"},
    "moderators": {"type": "nested",
        "properties": {
            "email": {"type": "string"},
            "createdat": {"type": "date","format": "dateOptionalTime"},
            "expire": { "type": "date","format": "dateOptionalTime"},
        }
    },
    "padministration": {"type": "string","analyzer": "standard"},
    "url": {"type": "string","index": "not_analyzed"},
    'created': {'type': 'date'},
    'updated': {'type': 'date'}


 """



    
    #return redirect(url_for("views.modifica",rutaPagina=sitio,userId=userNombre))



@views.route("/claimModeration",methods=["POST"])
def claimModeration():
    
    itemsDict  = request.form.to_dict()

    firstName=itemsDict.pop("firstName").title()
    lastName=itemsDict.pop("lastName").title()
    userPosition=itemsDict.pop("userPosition").title()
    oneUrl=itemsDict.pop("oneUrl")
    userMotivations=itemsDict.pop("userMotivations")

    userMotivations=userMotivations[0].upper()+userMotivations[1:]
 

    #This is the file
    archivoIdentificacion=itemsDict.pop("archivoIdentificacion")


    #This are the URI's
    urlList=[]
    for key in itemsDict:
        urlList.append(itemsDict[key])

    if(len(urlList)==0):
        #Si el campo de lista esta vacio miro el campo url
        if oneUrl != "":
            urlList.append(oneUrl)
        else:
            flash("It is needed to add at least one URL of description.","info")
            return authInterlink.moderate()
        

    itemsDict['email'] = current_user.email

    dataClaimEncoded=urllib.parse.urlencode(itemsDict)

    #Now will send the email:
    msg = Message('The user '+firstName+' '+lastName+' ha realizado un claim to be a moderator.', sender = 'interlinkdeusto@gmail.com', recipients = [current_user.email])

    sites =" ".join(str(x) for x in urlList)
    claimInfo= "The user {} {} who is a {} ".format(firstName,lastName,userPosition)+"send a request to be a moderator of the following sites: "
    

    textHref='http://127.0.0.1:5000/website/aproveModerator?'+dataClaimEncoded

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
  display: inline-block;  border-radius: 5px;' href='"""+textHref+ """'>Aproved the request.</a></td>
            </tr>
        </tbody>
    </table>
</td>"""
    
    
    mail = Mail(current_app)
    mail.send(msg)


    flash("The moderation request has been send.","info")

    return authInterlink.moderate()

    #return render_template("moderate.html",descriptions=res,urls=urlList,publicsa=paList,paginacion=paginacion)


@views.route("/aproveModerator",methods=["GET","POST"])
def aproveModerator():

    argumentos=request.args.to_dict()
    argKeys=argumentos.keys()
    email=argumentos.pop('email')


    existUrl=any(list(map(lambda x: x.startswith('url_'), argKeys))) 

    urlList=[]
    if existUrl:
        for key in argumentos:
            urlList.append(argumentos[key])
        
    today = date.today()
    endDate = today.replace(today.year + 1)

    return render_template("approveClaim.html",email=email,argumentos=urlList, now=today.strftime("%Y-%m-%d"),endDate=endDate.strftime("%Y-%m/%d"))

@views.route("/aprovarClaimsList",methods=["POST"])
def aprovarClaimsList():

    argumentos=request.form.to_dict()
    usuarioModerator=argumentos.pop('email')
    adminComment=argumentos.pop('commentBox')

    argumentosList=list(argumentos.values())
    
    contador=0
    nroActualizaciones=0
    listMsg=[]
    for i in range(math.ceil(len(argumentosList)/4)):
        if(i!=0):
            contador=i*4
        estado=argumentosList[contador]
        url=argumentosList[contador+1]
        initDate=argumentosList[contador+2]
        endDate=argumentosList[contador+3]
        

        #Agrego como moderador en la descripcion:
        descriptions=Description._get_Descriptions_byURI(url=url)
        
        if len(descriptions)==1:
            if estado=="on":
                descripcionAct=descriptions[0]

                if(len(descripcionAct['moderators'])==0):
                    descripcionAct['moderators']=[]    

                descripcionAct['moderators'].append({
                                "created": initDate,
                                "expire": endDate,
                                "email": usuarioModerator
                            })
                descripcionAct.updateModerators(index="description")
                nroActualizaciones=nroActualizaciones+1
            listMsg.append("The moderation of "+url+" has been assigned.")
        elif len(descriptions)==0:
            listMsg.append("The description of "+url+" could not be found (Most be created first) !.")

    listActionsBody=""
    for msnItem in listMsg:
        listActionsBody=listActionsBody+"""<p style='font-size: 16px; letter-spacing: 1px; color: #ffffff;'>"""+msnItem+"""</p>""" 
    

    msg = Message('Your claim has been resolved.', sender = 'interlinkdeusto@gmail.com', recipients = [usuarioModerator])

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
        flash(msnItem,"info")


    return redirect(url_for("views.aproveModerator",email=usuarioModerator,argumentos=argumentosList))
 


#Formulatio de carga de Pagina
@views.route("/visor",methods=["GET"])
def visor():
    return render_template("prototipo.html")
  



#Cargo la pagina desde beautifulSoup y la muestro en pantalla
@views.route("/modifica/<userId>/<path:rutaPagina>",methods=["GET","POST"])
def modifica(rutaPagina,userId):

    print("La ruta de la Pagina es: "+rutaPagina)
    print("El nombre de usuario es: "+userId)
    
    session['username'] = userId

    headersUserAgent={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }


    #Obtengo el codigo:
    response=requests.get(rutaPagina,headers=headersUserAgent)
    resp_Contenido=response.content
    #print(resp_Contenido.decode())
    soup = BeautifulSoup(resp_Contenido,'html.parser')


    #Codigo para Latvia:
    if rutaPagina.startswith("https://latvija.lv/ppk/"):
        arrayUrl=['DokumentiUnVeidlapas','PakalpojumaMaksajumi','CitaInformacija']
        #Obtengo seccion doc
        contador=0
        for newUrl in arrayUrl:
            contador=contador+1

            rutaTemp=rutaPagina.split("/")
            rutaTemp[7]=newUrl
            newUrl="/".join(rutaTemp)

            responseAdd=requests.get(newUrl,headers=headersUserAgent)
            resp_ContenidoAdd=responseAdd.content
            #print(resp_Contenido.decode())
            soupAdd = BeautifulSoup(resp_ContenidoAdd,'html.parser')

            contenidoAdd= soupAdd.find(id='content_0_contentsimplecontentph_1_uxTabPage')
           
            contenidoHeader= soupAdd.find("table",class_="dxtcControl_LatvijaLv service-tab-control")
           

         
            contenidoOriginal=soup.find(id='content_0_contentsimplecontentph_1_uxTabPage')
            contenidoOriginal.append(contenidoHeader)
            contenidoOriginal.append(contenidoAdd)

    #Quitamos los scripts:
    for data in soup(['script','pre','noscript']):
        # Remove tags
        data.decompose()

    #print(soup.decode)

    try:
        headTag =soup.html.head
    except:
        headTag =soup.html
     #Inserto las librerias de css de la pagina:
    
    #1 Obtengo los archivos css
    css_files = []


    count = 0
    for css in soup.find_all("link"):
        if css.attrs.get("href"):
            # if the link tag has the 'href' attribute
            css_url = urljoin(rutaPagina, css.attrs.get("href"))
            if "css" in css_url:
                count += 1
                css_files.append(css_url)
                anotationTemp = soup.new_tag('link', href=css_url,rel="stylesheet")
                headTag.append(anotationTemp)
                print("Line{}: {}".format(count, css_url))

                
    print("Total CSS insertados en the page:", len(css_files))

    #Inserto las librerias del AnnotationJS
    #Creo los tags necesarios:
    
    anotationcss1 = soup.new_tag('link', href="/website/static/lib/annotator-full.1.2.9/annotator.min.css",rel="stylesheet")
    anotationcss2 = soup.new_tag('link', href="/website/static/src/css/style.css",rel="stylesheet")
    anotationcss3 = soup.new_tag('link', href="/website/static/lib/css/annotator.touch.css",rel="stylesheet")

    fontAwesome3 = soup.new_tag('link', href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",rel="stylesheet")

 
    try:
        headTag.append(anotationcss1)
    except:
        print("Excepcion en ccs1")

    try:
        headTag.append(anotationcss2)
    except:
        print("Excepcion en ccs1")
    

    try:
        headTag.append(anotationcss3)
    except:
        print("Excepcion en ccs1")
    
    try:
        headTag.append(fontAwesome3)
    except:
        print("Excepcion en ccs1")
    

    try:
        soup.html.head=headTag
    except:
        print("Excepcion en ccs1")

    soup = obtenerReemplazarImagenes(rutaPagina,soup)

    #Ingreso el script para iniciar Aplicacion Annotation
    try:
        bodyTag=soup.html.body
    except:
        print("Excepcion en ccs1")
    
    jqueryScript1 = soup.new_tag('script', src="/website/static/lib/jquery-1.9.1.js")
    jqueryScript2 = soup.new_tag('script', src="/website/static/lib/annotator-full.1.2.9/annotator-full.min.js")
    jqueryScript3 = soup.new_tag('script', src="/website/static/lib/jquery-i18n-master/jquery.i18n.min.js")
    jqueryScript4 = soup.new_tag('script', src="/website/static/lib/jquery.dateFormat.js")
    jqueryScript5 = soup.new_tag('script', src="/website/static/lib/jquery.slimscroll.js")

    jqueryScript12 = soup.new_tag('script', src="/website/static/locale/en/annotator.js")
    jqueryScript13 = soup.new_tag('script', src="/website/static/lib/tinymce/tinymce.min.js")
    jqueryScript14 = soup.new_tag('script', src="/website/static/src/richEditor.js")



    jqueryScript6 = soup.new_tag('script', src="/website/static/lib/lunr.js-0.5.7/lunr.min.js")
    jqueryScript7 = soup.new_tag('script', src="/website/static/locale/en/annotator.js")
    jqueryScript8 = soup.new_tag('script', src="/website/static/lib/annotator.touch.js")
    jqueryScript9 = soup.new_tag('script', src="/website/static/src/view_annotator.js")
    jqueryScript10 = soup.new_tag('script', src="/website/static/src/categories.js")
    jqueryScript11 = soup.new_tag('script', src="/website/static/src/search.js")

    try:
        bodyTag.append(jqueryScript1)
        bodyTag.append(jqueryScript2)
        bodyTag.append(jqueryScript3)
        bodyTag.append(jqueryScript4)
        bodyTag.append(jqueryScript5)
        bodyTag.append(jqueryScript6)
        bodyTag.append(jqueryScript7)
        bodyTag.append(jqueryScript8)
        bodyTag.append(jqueryScript9)
        bodyTag.append(jqueryScript10)
        bodyTag.append(jqueryScript11)

        bodyTag.append(jqueryScript12)
        bodyTag.append(jqueryScript13)
        bodyTag.append(jqueryScript14)
    except:
        print("Excepcion en ccs1")
    

    #Anotation Init Version Anterior
    """
     jQuery(function ($) {
        $("#contenidoAnotar").annotator().annotator("setupPlugins", {tokenUrl: 'http://127.0.0.1:8000/token'});
        
      });


    """




    anotationIniScript = soup.new_tag('script')
    anotationInitScriptTemp= """ 
     
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
            $('body').annotator().annotator("addPlugin", "Touch");


 
            //let uriAdress =$(location).attr('href');
            //const uriAdressBase = uriAdress.split('#')[0];

            //Dejo unicamente la primera parte del uri
            uriAdressBase = '"""+rutaPagina+"""';     

            console.log(uriAdressBase)
            $('body').annotator().annotator('addPlugin', 'Store',{
                        annotationData: {uri:uriAdressBase},
                        loadFromSearch: {uri:uriAdressBase}
                        }
            );

           
            
            //noinspection JSJQueryEfficiency
            $('body').annotator().annotator('addPlugin', 'Search');

            //Annotation scroll
            $('#anotacions-uoc-panel').slimscroll({height: '100%'});

            //$('body').annotator().annotator("setupPlugins");

        });

    """

    anotationIniScript.string =anotationInitScriptTemp

    #anotationIniScript.string.replace('demoUser',str(current_user.id))
    try:   
        bodyTag.append(anotationIniScript)

        #Inserto
        # Es como poner una emvoltura sobre un Tag
        bodyTag.wrap(soup.new_tag("div",id="contenidoAnotar"))
        soup.html.body=bodyTag
    except:
        print("Excepcion en ccs1")
      

    

    headers = {'Content-Type': 'text/html',
                'x-annotator-auth-token':generate_token()}

    return make_response(soup.prettify(), 200,headers)  

def generate_token():
    return jwt.encode({
      'consumerKey': CONSUMER_KEY,
      'userId': current_user.id,
      'issuedAt': _now().isoformat() + 'Z',
      'ttl': CONSUMER_TTL
    }, CONSUMER_SECRET)



def obtenerReemplazarImagenes(rutaPagina,soup):
    #De la misma forma busco todas las imagenes:
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            # if img does not contain src attribute, just skip
            continue
        
        # make the URL absolute by joining domain with the URL that is just extracted
        img_url = urljoin(rutaPagina, img_url)

        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        
        # finally, if the url is valid
        if is_valid(img_url):
            urls.append(img_url)
    #print(urls)

    #Reemplazo las fuentes de las imagenes
    for img in soup.findAll('img'):
        for img_urlLine in urls:
            if img['src'] in img_urlLine:
                print("Cambia "+img['src']+" por: "+img_urlLine)
                img['src']=img_urlLine
                break

    return soup



def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)



import datetime
import jwt

# Replace these with your details
CONSUMER_KEY = '***REMOVED***'
CONSUMER_SECRET = 'yourconsumersecret'

# Only change this if you're sure you know what you're doing
CONSUMER_TTL = 86400

@views.route("/token")
def generate_token():
    return jwt.encode({
      'consumerKey': CONSUMER_KEY,
      'userId': 1,
      'issuedAt': _now().isoformat() + 'Z',
      'ttl': CONSUMER_TTL
    }, CONSUMER_SECRET)

def _now():
    return datetime.datetime.utcnow().replace(microsecond=0)