from api import es,authz
import datetime

from api.annotation import Annotation

TYPE = 'description'
MAPPING = {

    "id": {
        "type": "string",
        "index": "no"
    },

    "title": {
        "type": "string",
        "analyzer": "standard"
    },

    "description": {
        "type": "string",
        "analyzer": "standard"
    },

    "keywords": {
        "type": "string",
        "analyzer": "standard"
    },

    "moderators": {
        "type": "nested",
        "properties": {
            "email": {"type": "string"},
            "createdat": {
                    "type": "date",
                    "format": "dateOptionalTime"
                },
            "expire": {
                    "type": "date",
                    "format": "dateOptionalTime"
                }
        }
    },

    
    "padministration": {
        "type": "string",
        "analyzer": "standard"
    },

    "url": {
        "type": "string",
        "index": "not_analyzed"
    },
    
     "urls": {
        "type": "nested",
        "properties": {
            "createdate": {
                    "type": "date",
                    "format": "dateOptionalTime"
                },
            "ismain": {
                        "type" : "boolean"},
            "url": {
                    "type": "string",
                    "index": "not_analyzed"
                },
            "language": {
                    "type": "string",
                    "index": "not_analyzed"
                },
            "email": {"type": "string"},
        }
    },

    'created': {'type': 'date'},
    'updated': {'type': 'date'},
    
    'permissions': {
        'index_name': 'permission',
        'properties': {
            'read': {'type': 'string'},
            'update': {'type': 'string'},
            'delete': {'type': 'string'},
            'admin': {'type': 'string'}
        }
    }


}
MAX_ITERATIONS = 5
PAGGINATION_SIZE = 10


class Description(es.Model):
    __type__ = TYPE
    __mapping__ = MAPPING


    @classmethod
    def _get_all(cls):
        """
        Returns a list of all descriptions 
        """
        q= {
        "sort": [
            {
            "updated": {
                "order": "desc",
                "ignore_unmapped": True
            }
            }
        ],
        "from": 0,
        "size": PAGGINATION_SIZE,
        "query": {
            "bool": {
            "must": [
                {
                "match_all": {}
                }
            ]
            }
        }
        }
        res = cls.es.conn.search(index="description",
                                 doc_type=cls.__type__,
                                 body=q)
        return [cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]

    @classmethod
    def _get_by_title(cls,searchText="",padministration='',domain=''):
        


        q= {
        "query": {
            "prefix":{
                "title":searchText
                }
            }
        }

        

        res = cls.es.conn.search(index="description",
                                 doc_type=cls.__type__,
                                 body=q)
        return [cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]


    @classmethod
    def _get_uniqueValues(cls,campo=""):
        


        q= {
                "aggs": {
                    "group_by_url": {
                        "terms": {
                            "field": campo
                        }
                    }
                },
                "size": 0
        }

        

        res = cls.es.conn.search(index="description",
                                 doc_type=cls.__type__,
                                 body=q)

        resultadosDistintos=res["aggregations"]["group_by_url"]["buckets"]
        

        print(resultadosDistintos)

        return resultadosDistintos


    #Get users that has participated as Moderator of a Description
    @classmethod
    def currentActiveUsersModerators(cls,**kwargs):
        q={
            "aggs" : {
                    "moderators" : {
                        "nested" : {
                            "path" : "moderators"
                        },
                        "aggs" : {
                            "group_by_user": {
                                "terms": {
                                    "field": "moderators.email"
                                }
                            }

                        }
                    }
                },
            "size": 0
        }
        
        print(q)

    
        res = cls.es.conn.search(index="description",
                                 doc_type=cls.__type__,
                                 body=q)


        if(len(res['aggregations']['moderators']['group_by_user']['buckets'])>0):
            res=res['aggregations']['moderators']['group_by_user']['buckets']
        else:
            res=[]
        
        return res


    @classmethod
    def _get_uniqueValuesUrl(cls):
        
        q= {
            "aggs" : {
                        "urls" : {
                            "nested" : {
                                "path" : "urls"
                            },
                            "aggs" : {
                                "group_by_url": {
                                    "terms": {
                                        "field": "urls.url"
                                    }
                                }

                            }
                        }
                    },
            "size": 0
        }

        

        res = cls.es.conn.search(index="description",
                                 doc_type=cls.__type__,
                                 body=q)

        resultadosDistintos=res["aggregations"]["urls"]["group_by_url"]["buckets"]
        

        print(resultadosDistintos)

        return resultadosDistintos


    


    @classmethod
    def _get_Descriptions_byId(cls,**kwargs):
        
        q= {
            
            "query": {
            "terms": {
            "_id":[kwargs.pop("id")]
            }
        }
        }

        print(q)


        res = cls.es.conn.search(index="description",
                                 doc_type=cls.__type__,
                                 body=q)

        return [cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]




    """
    totalRegistros = 0
    if(textoABuscar == None or textoABuscar == ''):
        res = Description.search(offset=registroInicial)
        totalRegistros = Description.count()
    else:
        res = Description._get_Descriptions(
            textoABuscar=textoABuscar, padministration=padministration, url=domain, offset=registroInicial)
        totalRegistros = Description._get_DescriptionsCounts(
            textoABuscar=textoABuscar, padministration=padministration, url=domain)
    """


    @classmethod
    def _getDescriptionsUser_Stats_onSearch(cls,**kwargs):

        user=kwargs.pop("user")

        #Obtengo todas las anotaciones del usuario
        listAnnotations=Annotation._get_Annotations_by_User(user=user)

        textoABuscar=kwargs.pop("textoABuscar")
        padministration=kwargs.pop("padministration")
        domain=kwargs.pop("domain")

        # Now I obtain all descriptions related with this annotations
        listDescription=[]
        for urlItem in listAnnotations:
            url=urlItem['key']

            #Apply filters and the search options
            descriptions = Description._get_by_multiple(textoABuscar=textoABuscar, padministration=padministration, urlPrefix=domain, page="all",urlFixed=url)

            nroRegistros = descriptions['numRes']
            
            if(nroRegistros>0):
                descriptionFound = descriptions['descriptions'][0]

                #Si la descripcion ya ha sido agregada entonces no debe agregarse :
                existsDescr=False
                for itemDescript in listDescription:
                    if(itemDescript['id']==descriptionFound['id']):
                        existsDescr=True
                        break
                if not existsDescr:
                    listDescription.append(descriptionFound)

        # Now I obtain all descriptions where I am moderator

        #Apply filters and the search options
        descriptionsModerator = Description._get_by_multiple(textoABuscar=textoABuscar, padministration=padministration, urlPrefix=domain,isModerator=True, page="all",user=user)

        nroRegistros = descriptionsModerator['numRes']
        
        if(nroRegistros>0):
            descriptionFound = descriptionsModerator['descriptions'][0]

            #Si la descripcion ya ha sido agregada entonces no debe agregarse :
            existsDescr=False
            for itemDescript in listDescription:
                if(itemDescript['id']==descriptionFound['id']):
                    existsDescr=True
                    break
            if not existsDescr:
                listDescription.append(descriptionFound)
        

        registroInicial=kwargs.pop("registroInicial")
        listDescription[registroInicial:registroInicial+10]


        #Guardo el numero total de descriptions found:
        numTotalOfDescFound=len(listDescription)

        res=listDescription

        #Include Stats to show in the dashboard:
        # Cargo los números de anotaciones por categoria
        for itemDesc in res:

            # Obtengo los Urls:
            listUrl = []
            for url in itemDesc['urls']:
                listUrl.append(url['url'])

            # Cargo datos estadisticos de las descripciones
            resCategory = Annotation.descriptionStats(Annotation, uris=listUrl)

            nroFeedbacks = 0
            nroQuestions = 0
            nroTerms = 0

            nroFeedProgress = 0
            nroFeedApproved = 0
            nroQuesProgress = 0
            nroQuesApproved = 0
            nroTermProgress = 0
            nroTermApproved = 0

            # Obtengo la informacion estadistica:
            if(len(resCategory) > 0):

                for itemCategory in resCategory:

                    cateGroup = itemCategory['key']

                    if(cateGroup == 'feedback'):
                        nroFeedbacks = itemCategory['doc_count']
                        listStates = itemCategory['group_state']['buckets']

                        for itemState in listStates:
                            cateState = itemState['key']
                            nroState = itemState['doc_count']
                            if(cateState == 0):  # In Progress
                                nroFeedProgress = nroState
                            if(cateState == 2):  # In Approved
                                nroFeedApproved = nroState

                    if(cateGroup == 'question'):
                        nroQuestions = itemCategory['doc_count']
                        listStates = itemCategory['group_state']['buckets']

                        for itemState in listStates:
                            cateState = itemState['key']
                            nroState = itemState['doc_count']
                            if(cateState == 0):  # In Progress
                                nroQuesProgress = nroState
                            if(cateState == 2):  # In Approved
                                nroQuesApproved = nroState

                    if(cateGroup == 'term'):
                        nroTerms = itemCategory['doc_count']
                        listStates = itemCategory['group_state']['buckets']

                        for itemState in listStates:
                            cateState = itemState['key']
                            nroState = itemState['doc_count']
                            if(cateState == 0):  # In Progress
                                nroTermProgress = nroState
                            if(cateState == 2):  # In Approved
                                nroTermApproved = nroState

            # Cargo los valores totales
            itemDesc['nroTerms'] = nroTerms
            itemDesc['nroQuest'] = nroQuestions
            itemDesc['nroFeeds'] = nroFeedbacks

            # Cargo los progressBar con valores por estados.
            # Progreso Total (%) = Approved * 100 / (InProgress + Approved)
            # Feedback Progress:

            # Incluyo validacion de la division  x / 0 (if statement)

            progressFeed = ((nroFeedApproved * 100) / (nroFeedProgress +
                            nroFeedApproved)) if (nroFeedProgress + nroFeedApproved) != 0 else 0
            progressTerm = ((nroTermApproved * 100) / (nroTermProgress +
                            nroTermApproved)) if (nroTermProgress + nroTermApproved) != 0 else 0
            progressQues = ((nroQuesApproved * 100) / (nroQuesProgress +
                            nroQuesApproved)) if (nroQuesProgress + nroQuesApproved) != 0 else 0

            itemDesc['progressFeed'] = progressFeed
            itemDesc['progressTerm'] = progressTerm
            itemDesc['progressQues'] = progressQues

            textoStats = ("<b>Feedback ("+str(nroFeedApproved)+"/"+str(nroFeedApproved+nroFeedProgress)+")</b> : "+str(round(progressFeed))+"% <br>" +
                        "<b>Terms ("+str(nroTermApproved)+"/"+str(nroTermApproved+nroTermProgress)+")</b>: "+str(round(progressTerm))+"% <br>" +
                        "<b>Questions ("+str(nroQuesApproved)+"/"+str(nroQuesApproved+nroQuesProgress)+")</b>: "+str(round(progressQues))+"% <br>")

            itemDesc['textoStats'] = textoStats

            progressTotalApproved = nroFeedApproved + nroTermApproved + nroQuesApproved
            progressTotalInProgress = nroFeedProgress + nroTermProgress + nroQuesProgress
            progressTotal = ((progressTotalApproved * 100) / (progressTotalInProgress +
                            progressTotalApproved)) if (progressTotalInProgress + progressTotalApproved) != 0 else 0

            itemDesc['progressTotal'] = round(progressTotal)

        resultado={'descriptions':res,'numRes':numTotalOfDescFound}

        return resultado




  

    @classmethod
    def _get_Descriptions_byURI(cls,**kwargs):
        #Search for the description that include this url in the urls set.
   
  
        q= {
        
            "query": {
                "nested": {
                    "path": "urls",
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "match": {
                                        "urls.url": kwargs.pop("url")
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }

       

        print(q)


        res = cls.es.conn.search(index="description",
                                 doc_type=cls.__type__,
                                 body=q)

        return [cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]


    def _get_checkPermisos_byURI(cls,**kwargs):

        q= {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "url":kwargs.pop("url")
                            }
                        },
                        {
                            "nested": {
                                "path": "moderators",
                                "query": {
                                    "bool": {
                                        "must": [
                                            {
                                                "match": {
                                                    "moderators.email": kwargs.pop("email")
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

        print(q)

    
        res = cls.es.conn.count(index="description",
                                 doc_type=cls.__type__,
                                 body=q)
    
        return res['count']

    def _get_checkPermisos_byId(cls,**kwargs):

        q= {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "_id":kwargs.pop("id")
                            }
                        },
                        {
                            "nested": {
                                "path": "moderators",
                                "query": {
                                    "bool": {
                                        "must": [
                                            {
                                                "match": {
                                                    "moderators.email": kwargs.pop("email")
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    ]
                }
            }
        }

        print(q)

    
        res = cls.es.conn.count(index="description",
                                 doc_type=cls.__type__,
                                 body=q)
    
        return res['count']


    @classmethod
    def _get_Descript_byModerEmail(cls,**kwargs):
       

        q= {
                
                "query": {
                    "nested": {
                        "path": "moderators",
                        "query": {
                            "bool": {
                                "must": [
                                    {
                                        "match": {
                                            
                                            "moderators.email": kwargs.pop("email") 
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }

        #Parametros de busqueda:

       
        print(q)

    
        res = cls.es.conn.search(index="description",
                                 doc_type=cls.__type__,
                                 body=q)
        return [cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]

       
    @classmethod
    def _get_Descript_byModerEmailCounts(cls,**kwargs):
       

        q= {
                
                "query": {
                    "nested": {
                        "path": "moderators",
                        "query": {
                            "bool": {
                                "must": [
                                    {
                                        "match": {
                                            
                                            "moderators.email": kwargs.pop("email") 
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            }

        #Parametros de busqueda:

       
        print(q)

    
        res = cls.es.conn.count(index="description",
                                 doc_type=cls.__type__,
                                 body=q)
    
        return res['count']

    @classmethod
    def _get_DescriptionsCounts(cls,**kwargs):
        

        q= {
            "query": {
                "bool": {
                "must":[
                {
                "prefix":{
                    "title":kwargs.pop("textoABuscar")
                    }
                },
                {
                "prefix":{
                    "url":kwargs.pop("url")
                    }
                }
                ]
                }
            }
        }

        #Parametros de busqueda:

        i = 0
      
        for key, value in kwargs.items():
            i += 1

            
            seccion =  {
                "match":{
                    key: value
                    }

                }

         
            q['query']['bool']['must'].append(seccion)

        print('_get_DescriptionsCounts')   
        print(q)

        

        

        res = cls.es.conn.count(index="description",
                                 doc_type=cls.__type__,
                                 body=q)
        return [cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]

    @classmethod
    def _get_by_multiple(cls,**kwargs):

        #Base filter parameters
        page=kwargs.get("page")
        
        if page=='all':
            initReg=0
            numRegxConsulta=10000
        else:    
            initReg=(int(page)-1)*10
            numRegxConsulta=PAGGINATION_SIZE

        
        q= {
            "sort": [
                    {
                    "updated": {
                        "order": "desc",
                        "ignore_unmapped": True
                    }
                }
            ],
            "from": initReg,
            "size": numRegxConsulta
        }


        #Filter by searchBox
        textoBusqueda=kwargs.pop("textoABuscar")
        if textoBusqueda=='' or textoBusqueda==None :
            searchScope={
                       
                        "bool": {
                            "must":[
                            
                            ]
                        }
                       
                        }
        else:
            searchScope={
                       
                        "bool": {
                            "must":[
                                {
                                "match":{
                                    "title":textoBusqueda
                                    }
                                }
                            ]
                        }
                       
                        }

        q['query']=searchScope

        #Filter by Public administration:
        padminitration=kwargs.pop("padministration")

        #Filter by Public administration:
        if padminitration!='' and padminitration!=None:
            q['query']['bool']['must'].append({
                                                "match":{
                                                    "padministration":padminitration
                                                    }
                                                })
        
        #Filter by URl:
        if 'urlFixed' in kwargs:
            urlFixed=kwargs.pop("urlFixed")

            if urlFixed!='' and urlFixed!=None:
                q['query']['bool']['must'].append(
                {
                    "nested": {
                        "path": "urls",
                        "query": {
                            "bool": {
                                "must": [
                                    {
                                        "match": {
                                            "urls.url": urlFixed
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            )
            
            

        #Filter by Domain
        urlPrefix=kwargs.pop("urlPrefix")
        if urlPrefix!=''  and urlPrefix!=None:
            q['query']['bool']['must'].append(
                {
                    "nested": {
                        "path": "urls",
                        "query": {
                            "bool": {
                                "should": [
                                    {
                                        "prefix": {
                                            "urls.url": "https://"+urlPrefix
                                        }
                                    },
                                    {
                                        "prefix": {
                                            "url": "http://"+urlPrefix
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            )

        #Filter by Moderator
        if 'isModerator' in kwargs:
            ismoderator=kwargs.pop("isModerator")
            if ismoderator != None:
                if ismoderator==True:
                    userEmail=kwargs.pop("user")
                    q['query']['bool']['must'].append(
                    {
                        "nested": {
                            "path": "moderators",
                            "query": {
                                "bool": {
                                    "must": [
                                        {
                                            "match": {
                                                "moderators.email": userEmail
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
                )

    

        print('_get_by_multiple')
        print(q)

        res = cls.es.conn.search(index="description",
                                 doc_type=cls.__type__,
                                 body=q)


        descriptions=[cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]
        numRes=res['hits']['total']

        resultado={'descriptions':descriptions,'numRes':numRes}
        return resultado


        
    @classmethod
    def _get_by_multipleCounts(cls,**kwargs):
        
    
      
        q= {
            "query": {
            "bool": {
            "must":[
            {
            "prefix":{
                "title":kwargs.get("textoABuscar")
                }
            }
            ]
            }
        }
        }

        #Parametros de busqueda:

        i = 0
      
        for key, value in kwargs.items():
            i += 1

            if(key=='url'):

                preUrl={"bool": {
                "should":[
                ]
                }}

                seccion1 =  {
                    "prefix":{
                        key: 'http://'+value
                        }

                    }
                preUrl['bool']['should'].append(seccion1)
                seccion2 =  {
                    "prefix":{
                        key: 'https://'+value
                        }

                    }
                preUrl['bool']['should'].append(seccion2)
                q['query']['bool']['must'].append(preUrl)

            else:    
                if value=='Unassigned':
                    value=''

                    seccion =  {
                        "match":{
                            key: value
                            }

                        }

                    if(key!='textoABuscar' and key!='page'):
                        q['query']['bool']['must'].append(seccion)
                else:
                    seccion =  {
                        "match":{
                            key: value
                            }

                        }

                    if(key!='textoABuscar' and key!='page'and value!=''):
                        q['query']['bool']['must'].append(seccion)

        print('_get_by_multipleCounts')
        print(q)

        res = cls.es.conn.count(index="description",
                                 doc_type=cls.__type__,
                                 body=q)
    
        return res['count']


    @classmethod
    def _searchAndFilters(cls,**kwargs):
        
        page=kwargs.get("page")
        initReg=(int(page)-1)*10
        q= {
            "sort": [
                {
                "updated": {
                    "order": "desc",
                    "ignore_unmapped": True
                }
                }
            ],
            "from": initReg,
            "size": PAGGINATION_SIZE,
            "query": {
            "bool": {
            "must":[
            {
            "prefix":{
                "title":kwargs.get("textoABuscar")
                }
            }
            ]
            }
        }
        }

        #Parametros de busqueda:

        i = 0


        """ "query": {
                "query_string":{
                    "query": "*http*",
                    "fields": ["url"]
                    
                    }
                }
        } """

      
        for key, value in kwargs.items():
            i += 1

            
            seccion =  {
                "match":{
                    key: value
                    }

                }

            if(key!='textoABuscar' and key!='page' and value!=''):
                q['query']['bool']['must'].append(seccion)

        print('_searchAndFilters')   
        print(q)
        

        res = cls.es.conn.search(index="description",
                                 doc_type=cls.__type__,
                                 body=q)
        return [cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]


    def save(self, *args, **kwargs):
        _add_default_permissions(self)

        # If the annotation includes document metadata look to see if we have
        # the document modeled already. If we don't we'll create a new one
        # If we do then we'll merge the supplied links into it.

        

        super(Description, self).save(*args, **kwargs)




 


    def updateFields(self, *args, **kwargs):
        #_add_default_permissions(self)

        # If the annotation includes document metadata look to see if we have
        # the document modeled already. If we don't we'll create a new one
        # If we do then we'll merge the supplied links into it.

        
        q = {
                "doc" : {
                "title":self.title,
                "description":self.description,
                "keywords":self.keywords,
                "padministration":self.padministration,
                "urls":self['urls'],
                "updated":datetime.datetime.now().replace(microsecond=0).isoformat()
                }
            } 

        super(Description, self).updateFields(body=q,*args, **kwargs)


    def updateModerators(self, *args, **kwargs):
        #_add_default_permissions(self)

        # If the annotation includes document metadata look to see if we have
        # the document modeled already. If we don't we'll create a new one
        # If we do then we'll merge the supplied links into it.

        
        q = {
                "doc" : {
                "moderators":self['moderators'],
                "updated":datetime.datetime.now().replace(microsecond=0).isoformat()
                }
            } 

        super(Description, self).updateFields(body=q,*args, **kwargs)

    @classmethod
    def search_raw(cls, query=None, params=None, raw_result=False,
                   user=None, authorization_enabled=None,index='description'):
        """Perform a raw Elasticsearch query

        Any ElasticsearchExceptions are to be caught by the caller.

        Keyword arguments:
        query -- Query to send to Elasticsearch
        params -- Extra keyword arguments to pass to Elasticsearch.search
        raw_result -- Return Elasticsearch's response as is
        user -- The user to filter the results for according to permissions
        authorization_enabled -- Overrides Description.es.authorization_enabled
        """
        if query is None:
            query = {}
        if authorization_enabled is None:
            authorization_enabled = es.authorization_enabled
        if authorization_enabled:
            f = authz.permissions_filter(user)
            if not f:
                raise RuntimeError("Authorization filter creation failed")
            filtered_query = {
                'filtered': {
                    'filter': f
                }
            }
            # Insert original query (if present)
            if 'query' in query:
                filtered_query['filtered']['query'] = query['query']
            # Use the filtered query instead of the original
            query['query'] = filtered_query

        res = super(Description, cls).search_raw(index=index,query=query, params=params,
                                                raw_result=raw_result)
        return res

    @classmethod
    def _build_query(cls, query=None, offset=None, limit=None, sort=None, order=None):
        if query is None:
            query = {}
        else:
            query = dict(query)  # shallow copy

        # Pop 'before' and 'after' parameters out of the query
        after = query.pop('after', None)
        before = query.pop('before', None)

        q = super(Description, cls)._build_query(query, offset, limit, sort, order)
        
        print(str(q))
        
        # Create range query from before and/or after
        if before is not None or after is not None:
            clauses = q['query']['bool']['must']

            # Remove match_all conjunction, because
            # a range clause is added
            if clauses[0] == {'match_all': {}}:
                clauses.pop(0)

            created_range = {'range': {'created': {}}}
            if after is not None:
                created_range['range']['created']['gte'] = after
            if before is not None:
                created_range['range']['created']['lt'] = before
            clauses.append(created_range)

        

        return q


def _add_default_permissions(ann):
    if 'permissions' not in ann:
        ann['permissions'] = {'read': [authz.GROUP_CONSUMER]}
