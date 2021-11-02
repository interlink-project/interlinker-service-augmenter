from flask import Blueprint
import requests, math
from urllib.parse import urljoin, urlparse

from flask import Flask, render_template, redirect, request, url_for, session
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from authInterlink.helpers import  config
from authInterlink.user import User

from annotator.annotation import Annotation
from annotator.description import Description

authInterlink = Blueprint('authInterlink', __name__,template_folder="./website/templates")

APP_STATE = 'ApplicationState'
NONCE = 'SampleNonce'

@authInterlink.route("/login")
def login():
    # get request params
    query_params = {'client_id': config["client_id"],
                    'redirect_uri': config["redirect_uri"],
                    'scope': "openid email profile",
                    'state': APP_STATE,
                    'nonce': NONCE,
                    'response_type': 'code',
                    'response_mode': 'query'}

    # build request_uri
    request_uri = "{base_url}?{query_params}".format(
        base_url=config["auth_uri"],
        query_params=requests.compat.urlencode(query_params)
    )

    return redirect(request_uri)



""" @authInterlink.route("/dashboard")
@login_required
def dashboard():

    res = Annotation.search(query={'user': current_user.email})
    

    return render_template("dashboard.html", user=current_user, anotations=res) """
@authInterlink.route("/dashboard")
@login_required
def dashboard():

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


    return render_template("dashboard.html",descriptions=res,urls=urlList,publicsa=paList,paginacion=paginacion)


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
        

    pagesNumbers=math.ceil(totalRegistros/10)
    
    paginacion={'page':page,'pagesNumbers':pagesNumbers,'totalRegisters':totalRegistros,'searchBox':textoABuscar,'padministration':padministration,'url':domain}


    return render_template("moderate.html",descriptions=res,urls=urlList,publicsa=paList,paginacion=paginacion)



@authInterlink.route('/advanceSearch',)
def advanceSearch():


    res = Annotation.search(query={'user': current_user.email})
    


    return render_template("advanceSearch.html", user=current_user, anotations=res)

@authInterlink.route('/description/<string:descriptionId>',)
def description(descriptionId=None):

    description = Description._get_Descriptions_byId(id=descriptionId)

    categoria=request.args.get('category')

    if(categoria == None or categoria=='all' ):
        categoria='all'
        res = Annotation.search(query={ 'uri': description[0]['url']   })
    else:
        res = Annotation.search(query={ 'uri': description[0]['url'] ,'category':categoria  })


  
    
    return render_template("description.html", user=current_user, description=description[0],anotations=res,categoryLabel=categoria)
   # return 'la desc: '+category+'lauri is'+str(uri) 

@authInterlink.route('/subjectPage/<string:descriptionId>/<string:annotatorId>',)
def subjectPage(descriptionId=None,annotatorId=None):

    description = Description._get_Descriptions_byId(id=descriptionId)[0]

    anotation = Annotation._get_Annotation_byId(id=annotatorId)[0]

    replies = Annotation.search(query={ 'uri': description['url'] ,'category':'reply'  })
    
    return render_template("subjectPage.html", user=current_user, anotation=anotation,description=description,categoryLabel=anotation['category'],replies=replies)
   # return 'la desc: '+category+'lauri is'+str(uri) 


@authInterlink.route("/annotateIt")
@login_required
def annotateIt():

    vectorPAs=Description._get_uniqueValues(campo="padministration")
    paList=[]
    for pas in vectorPAs:
        key=pas["key"]

        if key=="":
            key='Unassigned'

        paList.append(key)
    print(paList)

    res = Annotation.search(query={'user': current_user.email})
    

    return render_template("annotateIt.html", user=current_user, anotations=res,publicsa=paList)


@authInterlink.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@authInterlink.route("/oidc_callback")
def callback():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    code = request.args.get("code")
    if not code:
        return "The code was not returned or is not accessible", 403
    query_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': request.base_url
                    }
    query_params = requests.compat.urlencode(query_params)
    exchange = requests.post(
        config["token_uri"],
        headers=headers,
        data=query_params,
        auth=(config["client_id"], config["client_secret"]),
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
    userinfo_response = requests.get(config["userinfo_uri"],
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

    return redirect(url_for("authInterlink.dashboard"))


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
        config["end_session_endpoint"],
        params=payload,
    )

    r.url

    r.text

    


    #return response
    #return render_template("home.html")
    return redirect(config["end_session_endpoint"]) #Por ahora queda asi.