from flask import Blueprint, jsonify, flash
import requests, math
from urllib.parse import urljoin, urlparse
import datetime
import uuid
from flask import current_app, g

from flask_babel import format_number,gettext,format_decimal, format_currency, format_percent


from flask import Flask, render_template, redirect, request, url_for, session
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from annotator.survey import Survey


from authInterlink.user import User

from annotator.annotation import Annotation
from annotator.description import Description
from annotator.notification import Notification
from website.languages import getLanguagesList

authInterlink = Blueprint('authInterlink', __name__,template_folder="./gui/templates")

#Genero Secretos para los estados:
tok1 = uuid.uuid4()
tok2 = uuid.uuid4()

APP_STATE = tok1.hex
NONCE = tok2.hex

@authInterlink.route("/login")
def login():
    # get request params
    query_params = {'client_id': current_app.config["CLIENT_ID"],
                    'redirect_uri': current_app.config["REDIRECT_URI"],
                    'scope': "openid email profile",
                    'state': APP_STATE,
                    'nonce': NONCE,
                    'response_type': 'code',
                    'response_mode': 'query'}

    # build request_uri
    request_uri = "{base_url}?{query_params}".format(
        base_url=current_app.config["AUTH_URI"],
        query_params=requests.compat.urlencode(query_params)
    )

    return redirect(request_uri)


@authInterlink.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    #response = redirect(config["end_session_endpoint"])
    payload = {'id_token_hint': session['id_token'],
                    'post_logout_redirect_uri': "http://127.0.0.1:5000/home",
                    'state': APP_STATE}
    #headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.get(
        current_app.config["END_SESSION_ENDPOINT"],
        params=payload,
    )
    r.url
    r.text
    session.clear()
    #return response
    #return render_template("home.html")
    return redirect(current_app.config["END_SESSION_ENDPOINT"]) #Por ahora queda asi.


@authInterlink.route("/about")
def about():
    return render_template("about.html")
    


@authInterlink.route("/dashboard")
@login_required
def dashboard():

     #Cargo los combos:

    vectorUrls=Description._get_uniqueValuesUrl()
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

    #Cargo los números de anotaciones por categoria
    for itemDesc in res:
        
        #Obtengo los Urls:
        listUrl=[]
        for url in itemDesc['urls']:
            listUrl.append(url['url'])

        #Cargo datos estadisticos de las descripciones
        resCategory=Annotation.descriptionStats(Annotation,uris=listUrl)
        
        nroFeedbacks=0
        nroQuestions=0
        nroTerms=0

        nroFeedProgress=0
        nroFeedApproved=0
        nroQuesProgress=0
        nroQuesApproved=0
        nroTermProgress=0
        nroTermApproved=0
        
        #Obtengo la informacion estadistica:
        if(len(resCategory)>0):
            
            for itemCategory in resCategory:
                
                cateGroup=itemCategory['key']
             
                
                if(cateGroup=='feedback'):
                    nroFeedbacks=itemCategory['doc_count']
                    listStates=itemCategory['group_state']['buckets']
                    
                    for itemState in listStates:
                        cateState=itemState['key']
                        nroState=itemState['doc_count']
                        if(cateState==0):#In Progress
                            nroFeedProgress=nroState
                        if(cateState==2):#In Approved
                            nroFeedApproved=nroState    

                if(cateGroup=='question'):
                    nroQuestions=itemCategory['doc_count']
                    listStates=itemCategory['group_state']['buckets']
                    
                    for itemState in listStates:
                        cateState=itemState['key']
                        nroState=itemState['doc_count']
                        if(cateState==0):#In Progress
                            nroQuesProgress=nroState
                        if(cateState==2):#In Approved
                            nroQuesApproved=nroState   

                if(cateGroup=='term'):
                    nroTerms=itemCategory['doc_count']
                    listStates=itemCategory['group_state']['buckets']
                    
                    for itemState in listStates:
                        cateState=itemState['key']
                        nroState=itemState['doc_count']
                        if(cateState==0):#In Progress
                            nroTermProgress=nroState
                        if(cateState==2):#In Approved
                            nroTermApproved=nroState 

        #Cargo los valores totales
        itemDesc['nroTerms']=nroTerms
        itemDesc['nroQuest']=nroQuestions
        itemDesc['nroFeeds']=nroFeedbacks  

        #Cargo los progressBar con valores por estados.
        # Progreso Total (%) = Approved * 100 / (InProgress + Approved)
        #Feedback Progress:

        #Incluyo validacion de la division  x / 0 (if statement) 
       
        progressFeed= ( (nroFeedApproved * 100) /  ( nroFeedProgress + nroFeedApproved ) )  if ( nroFeedProgress + nroFeedApproved ) != 0 else 0
        progressTerm= ( (nroTermApproved * 100) /  ( nroTermProgress + nroTermApproved ) )  if ( nroTermProgress + nroTermApproved ) != 0 else 0
        progressQues= ( (nroQuesApproved * 100) /  ( nroQuesProgress + nroQuesApproved ) )  if ( nroQuesProgress + nroQuesApproved ) != 0 else 0

        itemDesc['progressFeed']=progressFeed
        itemDesc['progressTerm']=progressTerm
        itemDesc['progressQues']=progressQues


        textoStats=("<b>Feedback ("+str(nroFeedApproved)+"/"+str(nroFeedApproved+nroFeedProgress)+")</b> : "+str(round(progressFeed))+"% <br>"+
                   "<b>Terms ("+str(nroTermApproved)+"/"+str(nroTermApproved+nroTermProgress)+")</b>: "+str(round(progressTerm))+"% <br>"+
                   "<b>Questions ("+str(nroQuesApproved)+"/"+str(nroQuesApproved+nroQuesProgress)+")</b>: "+str(round(progressQues))+"% <br>")
               
        
        itemDesc['textoStats']=textoStats

        progressTotalApproved =  nroFeedApproved + nroTermApproved + nroQuesApproved
        progressTotalInProgress = nroFeedProgress + nroTermProgress + nroQuesProgress
        progressTotal= ( (progressTotalApproved * 100) /  ( progressTotalInProgress + progressTotalApproved ) ) if ( progressTotalInProgress + progressTotalApproved ) != 0 else 0

        itemDesc['progressTotal']=round(progressTotal)


    pagesNumbers=math.ceil(totalRegistros/10)
    
    paginacion={'page':page,'pagesNumbers':pagesNumbers,'totalRegisters':totalRegistros,'searchBox':textoABuscar,'padministration':padministration,'url':domain}

    listNotifications,numRes=cargarNotifications()

    return render_template("dashboard.html",descriptions=res,urls=urlList,publicsa=paList,paginacion=paginacion,notifications=listNotifications,notificationNum=numRes)


@authInterlink.route("/moderate")
@login_required
def moderate():

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
        
    res=Description._get_Descript_byModerEmail(email=current_user.email)
    totalRegistros= Description._get_Descript_byModerEmailCounts(email=current_user.email)


    pagesNumbers=math.ceil(totalRegistros/10)
    
    paginacion={'page':page,'pagesNumbers':pagesNumbers,'totalRegisters':totalRegistros,'searchBox':textoABuscar,'padministration':padministration,'url':domain}


    #Cargo las Notificaciones
    listNotifications,numRes=cargarNotifications()

    return render_template("moderate.html",descriptions=res,urls=urlList,publicsa=paList,paginacion=paginacion,notifications=listNotifications,notificationNum=numRes)


@authInterlink.route("/survey")
@login_required
def survey():

    textoABuscar=request.args.get("searchText")
    
    page=request.args.get("page",1)
    registroInicial=(int(page)-1)*10
    
    totalRegistros=0

    #Searchs:
    """ if(textoABuscar==None or textoABuscar==''):
        res= Survey.search(offset=registroInicial)
        totalRegistros= Survey.count()
    else:
        res= Survey._get_Surveys(textoABuscar=textoABuscar,offset=registroInicial) """
        
    resTemp=Survey._get_all()
    res=resTemp['surveys']
    totalRegistros= resTemp['numRes']


    pagesNumbers=math.ceil(totalRegistros/10)
    
    paginacion={'page':page,'pagesNumbers':pagesNumbers,'totalRegisters':totalRegistros,'searchBox':textoABuscar}

    #Cargo las Notificaciones
    listNotifications,numRes=cargarNotifications()

    #Defino la direccion del SurveyHost
    surveyHost=current_app.config['SURVEYINTERLINK_URL']
    surveyApiVersion=current_app.config['SURVEYAPI_VERSION']

    return render_template("surveys.html",surveys=res,paginacion=paginacion,notifications=listNotifications,notificationNum=numRes,surveyHost=surveyHost,surveyApiVersion=surveyApiVersion)

@authInterlink.route("/surveyInstantiator",methods=["POST"])
def surveyInstantiator():

    #Redirecciono al editor:
    return redirect(current_app.config['SURVEYINTERLINK_URL']+"/assets/"+"instantiate")

def obtainUsersEmail(listItemsBucket=[]):
    listUsers=[]
    for itemBucket in listItemsBucket:
        userEmail=itemBucket['key']
        if userEmail!='Anonymous' and userEmail!='Annonymous' :
            listUsers.append(userEmail)
    return listUsers



@authInterlink.route("/lauchSurvey",methods=["POST"])
def surveyLauchProcess():

    #Obtengo los valores del Survey:
    selTargetUsers=request.form.get("selTargetList")
    listUsersArea=request.form.get("listUsersArea")
    is_optional=request.form.get("is_optional")
    ini_date=request.form.get("ini_date")
    fin_date=request.form.get("fin_date")
    selEvent=request.form.get("selEvent")

    mandatory=True
    if is_optional =='on':
        mandatory=False


    #Creo la notification:
    idAsset=request.form.get('assetId')
    title=request.form.get('surveyTitle')
    description= request.form.get('surveyDesc')

    #Defino the users:
    listUsersEmails=[]
    if selTargetUsers=="everybody":

        listUsersWhoAnnotated=obtainUsersEmail(Annotation.currentActiveUsers())
        listUsersWhoModerate= obtainUsersEmail(Description.currentActiveUsersModerators())
        listUsersEmails=list(set(listUsersWhoAnnotated+listUsersWhoModerate))
        
    else:
        listUsersEmails= listUsersArea.split(";")
    


    for userEmail in listUsersEmails:

        email=userEmail
        target_url=current_app.config['SURVEYINTERLINK_URL']+ "/assets/"+idAsset+"/view/"

        newNotification=Notification(
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


    #Se ha lanzado exitosamente el suvey:
    flash("The survey has been lauched.","info")
       
    #Redirecciono al editor:
    return redirect("/survey")


@authInterlink.route('/advanceSearch',)
def advanceSearch():


    res = Annotation.search(query={'user': current_user.email})
    


    return render_template("advanceSearch.html", user=current_user, anotations=res)

@authInterlink.route('/description/<string:descriptionId>',)
@login_required
def description(descriptionId=None):

    description = Description._get_Descriptions_byId(id=descriptionId)[0]
    
    urlMainPage = [url['url'] for url in description['urls'] if url['isMain'] == True][0]

    categoria=request.args.get('category')

    page=request.args.get("page",1)
    registroInicial=(int(page)-1)*10

    


    if(categoria == None or categoria=='all' ):
        categoria=''
    
    res=[]
    stats=[]
    numRes=0
    listUrlsPages=[]
    for itemUrl in description['urls']:
        url=itemUrl['url']
        listUrlsPages.append(url)

        # Cargo las replies de cada annotacion:
        stats=stats+Annotation.annotationStats(Annotation,uri=itemUrl['url'])

    res= Annotation._get_by_multiple(Annotation,textoABuscar='',estados={'InProgress':True,'Archived':True,'Approved':True},urls=listUrlsPages,category=categoria,notreply=True,page=page)
    numRes= res['numRes']
    res=res['annotations']


    dictStats={}
    for itemStat in stats:
        clave=itemStat['key']
        val=itemStat['doc_count']
        dictStats[clave]=val

    for itemRes in res:
        if itemRes['id'] in dictStats.keys():
            itemRes['nroReplies']=dictStats[itemRes['id']]
        else:
            itemRes['nroReplies']=0
    
    page=request.args.get("page",1)
    pagesNumbers=math.ceil(numRes/10)
    
    paginacion={'page':page,'pagesNumbers':pagesNumbers,'totalRegisters':numRes}

    #Cargo las Notificaciones
    listNotifications,numRes=cargarNotifications()

    return render_template("description.html", user=current_user, description=description,anotations=res,categoryLabel=categoria,paginacion=paginacion,urlMainPage=urlMainPage,notifications=listNotifications,notificationNum=numRes)
   # return 'la desc: '+category+'lauri is'+str(uri) 

@authInterlink.route('/description/<string:descriptionId>/<string:option>',)
@login_required
def editDescription(descriptionId=None,option='Edit'):

    vectorPAs=Description._get_uniqueValues(campo="padministration")
    paList=[]
    for pas in vectorPAs:
        key=pas["key"]

        if key=="":
            key='Unassigned'

        paList.append(key)
    print(paList)

    description = Description._get_Descriptions_byId(id=descriptionId)[0]   
    
    for itemUrl in description['urls']:
        if itemUrl['language']!='Undefined':
            itemUrl['langText']=getLanguagesList()[itemUrl['language']]
        else:
            itemUrl['langText']="Undefined"

#Cargo las Notificaciones
    listNotifications,numRes=cargarNotifications()  
    return render_template("descriptionDetail.html", user=current_user, description=description,option=option,publicsa=paList,notifications=listNotifications,notificationNum=numRes)



@authInterlink.route('/subjectPage/<string:descriptionId>/<string:annotatorId>',)
@login_required
def subjectPage(descriptionId=None,annotatorId=None):

    description = Description._get_Descriptions_byId(id=descriptionId)[0]

    urlMainPage = [url['url'] for url in description['urls'] if url['isMain'] == True][0]

    annotation = Annotation._get_Annotation_byId(id=annotatorId)[0]

    nroReplies = Annotation.count(query={ 'idReplyRoot': annotatorId ,'category':'reply' })
    replies = Annotation.search(query={ 'idReplyRoot': annotatorId ,'category':'reply'  },limit=nroReplies)

    nroRepliesOfAnnotation=nroReplies
    #nroRepliesOfAnnotation = Annotation.count(query={ '_id': description['id'] ,'category':'reply','idReplyRoot':annotatorId  })
    
    #Cargo las Notificaciones
    listNotifications,numRes=cargarNotifications()

    return render_template("subjectPage.html", user=current_user, annotation=annotation,description=description,categoryLabel=annotation['category'],replies=replies,nroReplies=nroRepliesOfAnnotation,urlMainPage=urlMainPage,notifications=listNotifications,notificationNum=numRes)
   # return 'la desc: '+category+'lauri is'+str(uri) 

@authInterlink.route('/subjectPage/<string:descriptionId>/<string:annotatorId>/<string:option>', methods=["GET", "POST"])
@login_required
def changeAnnotation(descriptionId=None,annotatorId=None,option=None):

    
    if option == 'state':
        
        argumentos=request.json
        newstate=argumentos.pop('stateToChange')
        commentsChangeState=argumentos.pop('commentsChangeState')
        objtype=argumentos.pop('objtype')

        annotationRootId=''
        losvalores=argumentos.keys()
        if "annotationRootId" in losvalores:
            annotationRootId=argumentos.pop('annotationRootId')
        

        annotation = Annotation._get_Annotation_byId(id=annotatorId)[0]
        

        #Registro el cambio y quien lo hizo
        if(len(annotation['statechanges'])==0):
            annotation['statechanges']=[]  

        #Si el estado inicial es prohibido y el estado final es prohibido
        #Se resetea el estado a in progress.
        if(annotation['state']==3 & int(newstate)==3):
            newstate=0
        

        annotation['statechanges'].append({
                        "initstate": annotation['state'],
                        "endstate": int(newstate),
                        "text": commentsChangeState,
                        "objtype" : objtype,
                        "date": datetime.datetime.now().replace(microsecond=0).isoformat(),
                        "user": current_user.email
                    })

        annotation['state']=int(newstate)
        annotation.updateState()

        return jsonify(annotation)
        
        

    elif option=='like':

        argumentos=request.json


        vote=int(argumentos.pop('stateToChange'))

        newstate=vote
        commentsChangeState=argumentos.pop('commentsChangeState')
        objtype=argumentos.pop('objtype')

        annotationRootId=''
        losvalores=argumentos.keys()
        if "annotationRootId" in losvalores:
            annotationRootId=argumentos.pop('annotationRootId')

        #Verifico si  anteriormente este usuario ha realizado una anotacion
        annotation = Annotation._get_Annotation_byId(id=annotatorId)[0]
        nroLikes=annotation.userAlreadyLike(email=current_user.email,id=annotatorId)

        #Un usuario solo puede votar una vez
        if nroLikes==0:

            

            #Registro el cambio y quien lo hizo
            if(len(annotation['statechanges'])==0):
                annotation['statechanges']=[] 
            
            #Registro el cambio y quien lo hizo
            initState=0
            if(vote==1):
                initState=int(annotation['like'])
                annotation['like']=initState+1
                objtype='annotation_like'
                    
            elif vote==-1:
                initState=int(annotation['dislike'])
                annotation['dislike']=initState+1
                objtype='annotation_like'

            #Registro el cambio de estado
            annotation['statechanges'].append({
                            "initstate": initState,
                            "endstate": initState+1,
                            "text": commentsChangeState,
                            "objtype" : objtype,
                            "date": datetime.datetime.now().replace(microsecond=0).isoformat(),
                            "user": current_user.email
                        })


            annotation.updateLike()
            annotation.updateState()

        return jsonify(annotation)




@authInterlink.route("/descriptionDetail")
@login_required
def descriptionDetail():

    vectorPAs=Description._get_uniqueValues(campo="padministration")
    paList=[]
    for pas in vectorPAs:
        key=pas["key"]

        if key=="":
            key='Unassigned'

        paList.append(key)
    print(paList)

    res = Annotation.search(query={'user': current_user.email})
    

    return render_template("descriptionDetail.html", user=current_user, anotations=res,publicsa=paList)


@authInterlink.route("/profile")
@login_required
def profile():

    #Cargo las Notificaciones
    listNotifications,numRes=cargarNotifications()

    return render_template("profile.html", user=current_user,notifications=listNotifications,notificationNum=numRes)

@authInterlink.route("/settings")
@login_required
def settings():    

    results=[]
    
    anthony =gettext('Anthony')

    us_num=format_number(1099)
    results.append(us_num)
  
    us_num=format_currency(1099.98, 'USD')
    results.append(us_num)
  
    us_num=format_decimal(1.2346)
    results.append(us_num)
    
    #Cargo las Notificaciones
    listNotifications,numRes=cargarNotifications()

    return render_template("settings.html", user=current_user,results=results,anthony=anthony,notifications=listNotifications,notificationNum=numRes)


@authInterlink.route("/oidc_callback")
def callback():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    code = request.args.get("code")

    #la pagina que se pretende ingresar es:
    paginaNext=''
    if 'next' in session.keys():
        paginaNext=session['next']

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
        auth=(current_app.config["CLIENT_ID"], current_app.config["CLIENT_SECRET"]),
    ).json()

    # Get tokens and validate
    if not exchange.get("token_type"):
        return "Unsupported token type. Should be 'Bearer'.", 403
    access_token = exchange["access_token"]
    id_token = exchange["id_token"]

    session['id_token']=id_token

    #if not is_access_token_valid(access_token, config["issuer"], config["client_id"]):
    #    return "Access token is invalid", 403

    #if not is_id_token_valid(id_token, config["issuer"], config["client_id"], NONCE):
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

    if paginaNext!="":
        return redirect(paginaNext)
    else:
        return redirect(url_for("authInterlink.dashboard"))

def cargarNotifications():
    #Cargo las Notificaciones
    listNotifications=Notification._get_Notification_byModerCategory(category="survey")
    #listNotifications.append(Notification._get_Notification_byModerCategory(category="survey"))
    numRes=listNotifications['numRes']
    listNotifications=listNotifications['notifications']
    return listNotifications,numRes

