from annotator import authz, document, es
import datetime

TYPE = 'annotation'
MAPPING = {
    'id': {'type': 'string', 'index': 'no'},
    'annotator_schema_version': {'type': 'string'},
    'created': {'type': 'date'},
    'updated': {'type': 'date'},
    'quote': {'type': 'string', 'analyzer': 'standard'},
    'tags': {'type': 'string', 'index_name': 'tag'},
    'text': {'type': 'string', 'analyzer': 'standard'},
    'category': {'type': 'string'},
    'uri': {'type': 'string'},
    'user': {'type': 'string'},
    'consumer': {'type': 'string'},
    'ranges': {
        'index_name': 'range',
        'properties': {
            'start': {'type': 'string'},
            'end': {'type': 'string'},
            'startOffset': {'type': 'integer'},
            'endOffset': {'type': 'integer'},
        }
    },
    'permissions': {
        'index_name': 'permission',
        'properties': {
            'read': {'type': 'string'},
            'update': {'type': 'string'},
            'delete': {'type': 'string'},
            'admin': {'type': 'string'}
        }
    },

    "statechanges": {
        "type": "nested",
        "properties": {
            "initstate": {"type": "byte"},
            "endstate": {"type": "byte"},
            "objtype": {"type":"string"},
            "text": {"type": "string"},
            "date": {"type": "date","format": "dateOptionalTime"},
            "user": {"type": "string"}
        }
    },

    

    "state": {
        "type": "byte",
        "index": "not_analyzed"
    },



    "likes": {
        "type": "integer",
        "index": "not_analyzed"
    },

    "dislikes": {
        "type": "integer",
        "index": "not_analyzed"
    },

    "replies": {
        "type": "integer",
        "index": "not_analyzed"
    },


    'document': {
        'properties': document.MAPPING
    },
    'idAnotationReply': {
        'type': 'string'
    },
    'idReplyRoot': {
        'type': 'string'
    }
}


MAX_ITERATIONS = 5
PAGGINATION_SIZE = 10

class Annotation(es.Model):

    __type__ = TYPE
    __mapping__ = MAPPING

    def save(self, *args, **kwargs):
        _add_default_permissions(self)
        
        #The initial state of the annotation is 0.
        #the 0 state: on discussion.
        #the 1 state: archived
        #the 2 state: approved
        #the 3 state: banned
        #en statechages register the states changes.
        self['state']=0
        self['statechanges']={}

        self['like']=0
        self['dislike']=0

       


        # If the annotation includes document metadata look to see if we have
        # the document modeled already. If we don't we'll create a new one
        # If we do then we'll merge the supplied links into it.

        if 'document' in self:
            d = document.Document(self['document'])
            d.save()

        super(Annotation, self).save(*args, **kwargs)



    def updateState(self, *args, **kwargs):
        #_add_default_permissions(self)

        # If the annotation includes document metadata look to see if we have
        # the document modeled already. If we don't we'll create a new one
        # If we do then we'll merge the supplied links into it.

        
        q = {
                "doc" : {
                "state": self['state'],   
                "statechanges":self['statechanges']
                }
            } 

        super(Annotation, self).updateFields(body=q,*args, **kwargs)

    def updateLike(self, *args, **kwargs):
        #_add_default_permissions(self)

        # If the annotation includes document metadata look to see if we have
        # the document modeled already. If we don't we'll create a new one
        # If we do then we'll merge the supplied links into it.

        
        q = {
                "doc" : {
                "like": self['like'],   
                "dislike":self['dislike']
                }
            } 

        super(Annotation, self).updateFields(body=q,*args, **kwargs)    

    #Return the number of terms, questions and feedbacks
    def descriptionStats(cls,**kwargs):
        q = {
                "query": {
                    "bool": {
                        "must": []
                    }
                },
                "aggs": {
                    "group_category": {
                        "terms": {
                            "field": "category"
                        },
                        "aggs": {
                            "group_state": {
                                "terms": {
                                    "field": "state"
                                }
                            }
                        }
                    }
                }
            }

        
        #Parametros de busqueda URI:
        urls=kwargs.pop("uris")

        filtroUriSection={
            "bool": {
                "should": []
                }
        }

        existenUris=False
        
        for url in urls:  
            existenUris=True
            seccionState =  {
                "match":{
                    "uri": url
                    }
                }

            filtroUriSection['bool']['should'].append(seccionState)
        
        if existenUris:    
            q['query']['bool']['must'].append(filtroUriSection)
                   

        print(q)

    
        res = cls.es.conn.search(index="annotator",
                                 doc_type=cls.__type__,
                                 body=q)


        if(len(res['aggregations']['group_category']['buckets'])>0):
            res=res['aggregations']['group_category']['buckets']
        else:
            res=[]
                                 
    
        return res



    #Return the number of terms, questions and feedbacks
    def annotationStats(cls,**kwargs):
        q={
            "size":0,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "uri": kwargs.pop("uri")
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "group_by_uri": {
                    "terms": {
                        "field": "idReplyRoot"
                    }
                }
            }
        }
        
        print(q)

    
        res = cls.es.conn.search(index="annotator",
                                 doc_type=cls.__type__,
                                 body=q)


        if(len(res['aggregations']['group_by_uri']['buckets'])>0):
            res=res['aggregations']['group_by_uri']['buckets']
        else:
            res=[]
                                 
    
        return res



    #Return the number of time a user register a like over an annotation
    def userAlreadyLike(cls,**kwargs):
        q= {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "_id": kwargs.pop("id")
                            }
                        },
                        {
                            "nested": {
                                "path": "statechanges",
                                "query": {
                                    "bool": {
                                        "must": [
                                            {
                                                "match": {
                                                    "statechanges.user": kwargs.pop("email")
                                                }
                                            },
                                            {
                                                "match": {
                                                    "objtype": "annotation_like"
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

    
        res = cls.es.conn.count(index="annotator",
                                 doc_type=cls.__type__,
                                 body=q)
    
        return res['count']


    def _get_by_multiple0(cls,**kwargs):
        
        page=kwargs.pop("page")
        estados=kwargs.pop("estados")
        url=kwargs.pop("url")
        textoForSearch=kwargs.pop("textoABuscar")
        category=kwargs.pop("category")
        notreply=kwargs.pop("notreply")

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
                        "match": {
                            "uri": url
                        }
                    }
                    ]
                }
            }
        }

        #Parametro de busqueda por texto Box:
        if textoForSearch != "":
            sectSearchByText={
                    "match":{
                        "text": textoForSearch
                        }
                    }
            q['query']['bool']['must'].append(sectSearchByText)

        #Parametro de busqueda por category:

        if category != "":
            sectCategory={
                    "match":{
                        "category": category
                        }
                    }
            q['query']['bool']['must'].append(sectCategory)

        #Obtenemos solo los reply
        if notreply:

            seccionJR=  {
                        "match":{
                            "category": "reply"
                            }
                        }

            q['query']['bool']['must_not']=[seccionJR]



        #Parametros de busqueda:
        #Estados:

        filtroEstadosSection={
            "bool": {
                "should": []
                }
        }

        existenStates=False
        
        for keyItem in estados.keys():
            if estados[keyItem]:
                existenStates=True
                if(keyItem=="Approved"):
                    
                    valueState=2   
                if(keyItem=="Archived"):
                    valueState=1   
                if(keyItem=="InProgress"):
                    valueState=0   
                
                seccionState =  {
                    "match":{
                        "state": valueState
                        }
                    }

                filtroEstadosSection['bool']['should'].append(seccionState)
        
        if existenStates:    
            q['query']['bool']['must'].append(filtroEstadosSection)
                   

                    

        print('_get_by_multiple')
        print(q)

        res = cls.es.conn.search(index="annotator",
                                 doc_type=cls.__type__,
                                 body=q)
        annotations=[cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]
        numRes=res['hits']['total']

        resultado={'annotations':annotations,'numRes':numRes}
        return resultado



    def _get_by_multiple(cls,**kwargs):
        
        page=kwargs.pop("page")
        estados=kwargs.pop("estados")
        urls=kwargs.pop("urls")
        textoForSearch=kwargs.pop("textoABuscar")
        category=kwargs.pop("category")
        notreply=kwargs.pop("notreply")

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
                "must":[]
                }
            }
        }

        #Parametros de busqueda URI:
        filtroUriSection={
            "bool": {
                "should": []
                }
        }

        existenUris=False
        
        for url in urls:  
            existenUris=True    
            seccionState =  {
                "match":{
                    "uri": url
                    }
                }

            filtroUriSection['bool']['should'].append(seccionState)
        
        if existenUris:    
            q['query']['bool']['must'].append(filtroUriSection)
                   


        #Parametro de busqueda por texto Box:
        if textoForSearch != "":
            sectSearchByText={
                    "match":{
                        "text": textoForSearch
                        }
                    }
            q['query']['bool']['must'].append(sectSearchByText)

        #Parametro de busqueda por category:

        if category != "":
            sectCategory={
                    "match":{
                        "category": category
                        }
                    }
            q['query']['bool']['must'].append(sectCategory)

        #Obtenemos solo los reply
        if notreply:

            seccionJR=  {
                        "match":{
                            "category": "reply"
                            }
                        }

            q['query']['bool']['must_not']=[seccionJR]



        #Parametros de busqueda:
        #Estados:

        filtroEstadosSection={
            "bool": {
                "should": []
                }
        }

        existenStates=False
        
        for keyItem in estados.keys():
            if estados[keyItem]:
                existenStates=True
                if(keyItem=="Approved"):
                    
                    valueState=2   
                if(keyItem=="Archived"):
                    valueState=1   
                if(keyItem=="InProgress"):
                    valueState=0   
                
                seccionState =  {
                    "match":{
                        "state": valueState
                        }
                    }

                filtroEstadosSection['bool']['should'].append(seccionState)
        
        if existenStates:    
            q['query']['bool']['must'].append(filtroEstadosSection)
                   

                    

        print('_get_by_multiple')
        print(q)

        res = cls.es.conn.search(index="annotator",
                                 doc_type=cls.__type__,
                                 body=q)
        annotations=[cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]
        numRes=res['hits']['total']

        resultado={'annotations':annotations,'numRes':numRes}
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
    def search_raw(cls, query=None, params=None, raw_result=False,
                   user=None, authorization_enabled=None):
        """Perform a raw Elasticsearch query

        Any ElasticsearchExceptions are to be caught by the caller.

        Keyword arguments:
        query -- Query to send to Elasticsearch
        params -- Extra keyword arguments to pass to Elasticsearch.search
        raw_result -- Return Elasticsearch's response as is
        user -- The user to filter the results for according to permissions
        authorization_enabled -- Overrides Annotation.es.authorization_enabled
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
        
        print(query)


        res = super(Annotation, cls).search_raw(query=query, params=params,
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

        q = super(Annotation, cls)._build_query(query, offset, limit, sort, order)

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

        # attempt to expand query to include uris for other representations
        # using information we may have on hand about the Document
        if 'uri' in query:
            clauses = q['query']['bool']
            doc = document.Document.get_by_uri(query['uri'])
            if doc:
                for clause in clauses['must']:
                    # Rewrite the 'uri' clause to match any of the document URIs
                    if 'match' in clause and 'uri' in clause['match']:
                        uri_matchers = []
                        for uri in doc.uris():
                            uri_matchers.append({'match': {'uri': uri}})
                        del clause['match']
                        clause['bool'] = {
                            'should': uri_matchers,
                            'minimum_should_match': 1
                        }

        return q


    @classmethod
    def _get_Annotation_byId(cls,**kwargs):
        
        q= {
            
            "query": {
            "terms": {
            "_id":[kwargs.pop("id")]
            }
        }
        }

        print(q)


        res = cls.es.conn.search(index="annotator",
                                 doc_type=cls.__type__,
                                 body=q)

        return [cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]



    @classmethod
    def _get_Annotation_byCategory(cls,**kwargs):
        
        q= {
            
            "query": {
            "terms": {
            "category":[kwargs.pop("category")]
            }
        }
        }

        print(q)


        res = cls.es.conn.search(index="annotator",
                                 doc_type=cls.__type__,
                                 body=q)

        return [cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]


def _add_default_permissions(ann):
    if 'permissions' not in ann:
        ann['permissions'] = {'read': [authz.GROUP_CONSUMER]}
