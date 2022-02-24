from api import authz, es
import datetime

TYPE = 'notification'
MAPPING = {

            "id": {
                "type": "string",
                "index": "no"
            },
            "email": {
                "type": "string"
            },

            "resolved": {
                "type": "boolean"
            },
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            },

            "category": {
                "type": "string"
            },
            "title": {
                "type": "string",
                "analyzer": "standard"
            },
            "description": {
                "type": "string",
                "analyzer": "standard"
            },
            "target_url": {
                "type": "string"
            },

            
            "isMandatory":{
                "type": "boolean"
            },

            "idAsset": {
                "type": "string"
            },
            "triggerEvent": {
                "type": "string"
            },
            "triggerDate": {
                "type": "string"
            }
}


MAX_ITERATIONS = 5
PAGGINATION_SIZE = 10



class Notification(es.Model):
    __type__ = TYPE
    __mapping__ = MAPPING


    def save(self, *args, **kwargs):
        _add_default_permissions(self)
        super(Notification, self).save(*args, **kwargs)




    @classmethod
    def _get_all(cls):
        """
        Returns a list of all notifications 
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
        res = cls.es.conn.search(index="notification",
                                 doc_type=cls.__type__,
                                 body=q)
        return [cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]


    @classmethod
    def _get_Notifications_byId(cls,**kwargs):
        
        q= {
            
            "query": {
            "terms": {
            "_id":[kwargs.pop("id")]
            }
        }
        }

        print(q)


        res = cls.es.conn.search(index="notification",
                                 doc_type=cls.__type__,
                                 body=q)


        notifications=[cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]
        numRes=res['hits']['total']

        resultado={'notifications':notifications,'numRes':numRes}

        return resultado
    
    @classmethod
    def _get_Notification_byModerEmail(cls,**kwargs):
       

        q= {
            
            "query": {
                "terms": {
                    "email":[kwargs.pop("email")]
                }
            }
        }

        print(q)

    
        res = cls.es.conn.search(index="notification",
                                 doc_type=cls.__type__,
                                 body=q)
       

        notifications=[cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]
        numRes=res['hits']['total']

        resultado={'notifications':notifications,'numRes':numRes}

        return resultado

    @classmethod
    def _get_Notification_byAssetId(cls,**kwargs):
       

        q= {
            
            "query": {
                "terms": {
                    "idAsset":[kwargs.pop("assetId")]
                }
            }
        }

        print(q)

    
        res = cls.es.conn.search(index="notification",
                                 doc_type=cls.__type__,
                                 body=q)
       

        notifications=[cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]
        numRes=res['hits']['total']

        resultado={'notifications':notifications,'numRes':numRes}

        return resultado

    @classmethod
    def _get_Notification_byModerCategory(cls,**kwargs):
       

        q= {
            
            "query": {

                "bool": {
                    "must": [
                        {
                            "term": {
                                "resolved": False
                            }
                        },
                        {
                            "term": {
                                "category": kwargs.pop("category")
                            }
                        }
                    ]
                }

            }
        }

        print(q)

    
        res = cls.es.conn.search(index="notification",
                                 doc_type=cls.__type__,
                                 body=q)


        notifications=[cls(d['_source'], id=d['_id']) for d in res['hits']['hits']]
        numRes=res['hits']['total']

        resultado={'notifications':notifications,'numRes':numRes}

        return resultado


    def updateFieldResolve(self, *args, **kwargs):
        #_add_default_permissions(self)

        # If the annotation includes document metadata look to see if we have
        # the document modeled already. If we don't we'll create a new one
        # If we do then we'll merge the supplied links into it.

        
        q = {
                "doc" : {
                "resolved":self['resolved'],
                "updated":datetime.datetime.now().replace(microsecond=0).isoformat()
                }
            } 

        super(Notification, self).updateFields(body=q,*args, **kwargs)

    @classmethod
    def search_raw(cls, query=None, params=None, raw_result=False,
                   user=None, authorization_enabled=None,index='notification'):
        """Perform a raw Elasticsearch query

        Any ElasticsearchExceptions are to be caught by the caller.

        Keyword arguments:
        query -- Query to send to Elasticsearch
        params -- Extra keyword arguments to pass to Elasticsearch.search
        raw_result -- Return Elasticsearch's response as is
        user -- The user to filter the results for according to permissions
        authorization_enabled -- Overrides Notification.es.authorization_enabled
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

        res = super(Notification, cls).search_raw(index=index,query=query, params=params,
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

        q = super(Notification, cls)._build_query(query, offset, limit, sort, order)
        
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

    def updateFields(self, *args, **kwargs):
        #_add_default_permissions(self)

        # If the annotation includes document metadata look to see if we have
        # the document modeled already. If we don't we'll create a new one
        # If we do then we'll merge the supplied links into it.

        for argItem in args:
            self['resolved']=argItem['resolved']
            
        q = {
                "doc" : {
                "title":self['title'],
                "description":self['description'],
                "resolved":self['resolved'],
                "updated":datetime.datetime.now().replace(microsecond=0).isoformat()
                }
            } 

        super(Notification, self).updateFields(body=q,*args, **kwargs)


    
def _add_default_permissions(ann):
    if 'permissions' not in ann:
        ann['permissions'] = {'read': [authz.GROUP_CONSUMER]}
