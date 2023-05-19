#This code is used for Testing the Page Load!!.
#This code is used to load the page and show the annotations.

from bs4 import BeautifulSoup
import ssl
import requests
import codecs
from urllib.parse import urljoin


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


# This function is used to write the file.

def writeToFile(content, fileName):
    # Open a file in write mode
    with open(fileName, 'w') as file:
        # Write the response content to the file
        file.write(content)
        #print("File saved successfully.")

# This function is used to load the page.

def loadPage(rutaPagina):
    
    #print('Enter the method load page')
    #print('the path is: '+rutaPagina)
   

    # In case is important one annotation:

    descriptionRef = ''
  

    # Set the headers:
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
    resp_Contenido=''
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(rutaPagina, headers=headersUserAgent, verify=False)
        resp_Contenido = response.content

        #Write the file:
        writeToFile(response.text, 'output.html')

    except requests.exceptions.RequestException as err:
        return 'TimeoutError'
       


    # Validate if the site is case sensitive.
    isCaseSensitive = False
    if('latvija' in rutaPagina):
        isCaseSensitive = True

    # Decodifico el contenido:
    try:
        resp_Contenido = codecs.decode(resp_Contenido, 'utf-8')
    except:
        print('Error al cargar con utf-8')

    writeToFile(resp_Contenido, 'output.html')

    # print(resp_Contenido.decode())
    #soup = BeautifulSoup(resp_Contenido, 'html5lib')
    #soup = BeautifulSoup(resp_Contenido, 'lxml')
    soup = BeautifulSoup(resp_Contenido, 'html.parser')

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
    
    ###
    # DEFINE THE JAVASCRIPT LIBRARIES OF THE PAGE:
    ###
    # Keep the javascript libraries that are important to mantain the style of the page:

    listScript = soup.find_all('script')
    listScriptRelatedEstilos = []
    #logging.info('Los script son:')

    for itemScript in listScript:
        if itemScript.attrs.get("src"):
            if 'bootstrap' in itemScript.attrs.get("src"):
                completeSrc = urljoin(rutaPagina, itemScript.attrs.get("src"))
                listScriptRelatedEstilos.append(completeSrc)
                #logging.info(completeSrc)
            if 'moment' in itemScript.attrs.get("src"):
                completeSrc = urljoin(rutaPagina, itemScript.attrs.get("src"))
                listScriptRelatedEstilos.append(completeSrc)
                #logging.info(completeSrc)
            if 'jquery' in itemScript.attrs.get("src"):
                completeSrc = urljoin(rutaPagina, itemScript.attrs.get("src"))
                listScriptRelatedEstilos.append(completeSrc)
                #logging.info(completeSrc)


    #logging.info('Los script Seleccionados:')
    #logging.info(listScriptRelatedEstilos)
    #logging.info('')

   
    # Remove all other scripts that are not user in the page:

    for data in soup(['script', 'pre', 'noscript']):
        data.decompose()

    ###
    # REMOVE PARTS OF THE PAGE THAT ARE NOT IMPORTANT:
    ###
    # Remove parts of the page:
    


    #  Remove advertising from the page:
    #  Remove div components by class identifier:
    listDiv = soup.find_all("div")
    for div in listDiv:
        if div.attrs != None:
            if div.attrs.get("class"):
                classesStr = div.attrs['class']

                for itemClass in classesStr:

                    if 'header-ad' in itemClass:
                        div.decompose()
                        break
                    if 'cookieBackground' in itemClass:
                        div.decompose()
                        break
                    if 'ad-' in itemClass:
                        div.decompose()
                        break
                    if 'advertising' in itemClass:
                        div.decompose()
                        break
                    if 'notification-global' in itemClass:#latvia.lv
                        div.decompose()     
                        break
                    if 'fc-consent-root' in itemClass:#bbc
                        div.decompose()
                        break
                    if 'bbc-n7zdg2' in itemClass:#bbc
                        div.decompose()
                        break
                    if 'bbc-p3fogx' in itemClass:#bbc
                        div.decompose()
                        break

    # Remove div components by id identifier:
    listDiv = soup.find_all("div")
    for div in listDiv:
        if div.attrs != None:
            if div.attrs.get("id"):
                idStr = div.attrs['id']
                if 'onetrust-consent-sdk' in idStr: #cnn español
                    div.decompose()
                    break
                    
    #Remove section components that is not important:
    listDiv = soup.find_all("section")
    for div in listDiv:
        if div.attrs != None:
            if div.attrs.get("class"):
                classesStr = div.attrs['class']

                for itemClass in classesStr:

                    if 'bbc-p3fogx' in itemClass:#bbc
                        div.decompose()
                        break

    #Reset the scroll of the body (to visualize the scroll bar)
    listDiv = soup.find_all("body")
    for body in listDiv:
        if body.attrs != None:
            if body.attrs.get("style"):
                classesStr = body.attrs['style']
                body.attrs['style']=classesStr.replace("overflow: hidden", "overflow: auto")
    

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

    # Replace que SRC of the pictures:
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

    ###
    # DEFINE THE CSS STYLES OF THE PAGE:
    ###

    # Keep the css styles that are important to mantain the style of the page:
    
    css_files = []
    count = 0


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

    
    for a_Link in soup.find_all("a"):
        if a_Link.attrs.get("href"):
            hrefVal = a_Link.attrs.get("href")
            
            # Pongo los enlaces

            if hrefVal.startswith('/'):
                newURLVal = urljoin(rutaPagina, hrefVal)

                if isCaseSensitive:
                    newURLVal = newURLVal.lower()

                urlLink = newURLVal
                a_Link.attrs['href'] = urlLink
                
                a_Link.attrs['onclick'] = "navegatetoPage(event)"

            if hrefVal.startswith('https://') or hrefVal.startswith('http://'):

                urlLink = hrefVal
                a_Link.attrs['href'] = urlLink
                a_Link.attrs['onclick'] = "navegatetoPage(event)"

    #print("Total CSS insertados en the page:", len(css_files))

    # Inserto las librerias del AnnotationJS
    # Creo los tags necesarios:

    # anotationcss1 = soup.new_tag(
    #     'link', href='/lib/annotator-full.1.2.9/annotator.min.css')
    anotationcss2 = soup.new_tag(
        'link', href='/src/css/style.css')
    anotationcss3 = soup.new_tag(
        'link', href='/lib/css/annotator.touch.css')

    fontAwesome3 = soup.new_tag(
        'link', href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", rel="stylesheet")

   
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
        'script', src='lib/jquery-1.9.1.js')
    jqueryScript3 = soup.new_tag(
        'script', src='lib/jquery-i18n-master/jquery.i18n.min.js')
    """ jqueryScript2 = soup.new_tag(
        'script', src='lib/annotator-full.1.2.9/annotator-full.min.js') """

    jqueryScript4 = soup.new_tag(
        'script', src='lib/jquery.dateFormat.js')
    jqueryScript5 = soup.new_tag(
        'script', src='lib/jquery.slimscroll.js')

    jqueryScript6 = soup.new_tag(
        'script', src='lib/lunr.js-0.5.7/lunr.min.js')

    jqueryScript8 = soup.new_tag(
        'script', src='lib/annotator.touch.js')
    jqueryScript9 = soup.new_tag('script', src='src/view_annotator.js')
    jqueryScript10 = soup.new_tag('script', src='src/categories.js')
    jqueryScript11 = soup.new_tag('src/search.js')

    jqueryScript13 = soup.new_tag(
        'script', src='lib/tinymce/tinymce.min.js')
    jqueryScript14 = soup.new_tag('script', src='src/richEditor.js')

    internacii18nScript = soup.new_tag(
        'script', src='lib/gettext.js')

    socketioLibScript = soup.new_tag(
        'script', src='lib/socketio/socket.io.min.js')

    timermeLibScript = soup.new_tag(
        'script', src='lib/timeme.min.js')

    fontawsomeLibScript = soup.new_tag(
        'script', src='https://kit.fontawesome.com/edd7ce77d1.js',crossorigin="anonymous")


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
    """ for itemScript in listScriptRelatedEstilos:
        #logging.info('El estilo que trato de cargar es:')
        #logging.info(itemScript)
        jsEstilosPage = soup.new_tag('script', src=itemScript)
        bodyTag.append(jsEstilosPage)

    try:
        bodyTag.append(jqueryScript1)
        bodyTag.append(jqueryScript3)

        bodyTag.append(internacii18nScript)

        #bodyTag.append(jqueryScript2)

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
        bodyTag.append(timermeLibScript)
        bodyTag.append(fontawsomeLibScript)

    except:
        #print("Excepcion en ccs1")
        pass """

    anotationIniScript = soup.new_tag('script')
    anotationInitScriptTemp = """ 
     
    jQuery(function ($) {

              
        
            $.i18n.load(i18n_dict);
            // Customise the default plugin options with the third argument.
            var annotator = $('body').annotator().annotator().data('annotator');
            var propietary = 'danyche2014@gmail.com';
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

            sessionStorage.setItem('user', 'danyche2014@gmail.com');   

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
        #bodyTag.append(anotationIniScript)

        # Inserto
        # Es como poner una emvoltura sobre un Tag
        bodyTag.wrap(soup.new_tag("div", id="contenidoAnotar"))
        soup.html.body = bodyTag
    except:
        #print("Excepcion en ccs1")
        pass


    writeToFile(soup.prettify(), 'output.html')

    return soup


# Function to load the page
loadPage('https://www.varam.gov.lv/en')