# Para correr estas queries es necesario habilitar ElasticSearch entorno.


DELETE description
PUT description
{
    "mappings": {
        "description": {
            "properties": {
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
                        "email": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "created": {
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
                    "index": "not_analyzed"
                },
                "url": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "created": {
                    "type": "date",
                    "format": "dateOptionalTime"
                },
                "updated": {
                    "type": "date",
                    "format": "dateOptionalTime"
                }
            }
        }
    }
}

DELETE description/description/AXzB72JcW2WuxQVN8aJF

POST description/description/1
{
    "id":"1",
    "title":"la descripcion titulada",
    "description":"es el texto de la descripcion",
    "keywords":"ads,fads,fa,ds",
    "moderators": [
        {
           "email":"danyc@hotmail.com",
           "created":1635334650,
           "expire":1635334650
        },
        {
           "email":"d.silvad@hotmasil.com",
           "created":1635334650,
           "expire":1635334650 
        }
    ],
    "padministration":"",
    "url":"",
    "created":1635334650,
    "updated":1635334650
}


POST description/description/5
{
    "id":"5",
    "title":"la descripcion 5",
    "description":"es el texto de la 5",
    "keywords":"palabra, esta ,mostrando",
    "moderators": [
        {
           "email":"danyc@hotmail.com",
           "created":1635334650,
           "expire":1635334650
        },
        {
           "email":"d.silvad@hotmasil.com",
           "created":1635334650,
           "expire":1635334650 
        }
    ],
    "padministration":"Latvia",
    "url":"http://latvia.vl/x1.html",
    "created":1635334650,
    "updated":1635334650
}

GET description/description/AXzB72JcW2WuxQVN8aJF

DELETE description/description/AXzB72JcW2WuxQVN8aJF







POST description/description/_search
{
    "query": {
        "prefix":{
            "title": "titula"
            }
            
        }
    }
}




GET description/description/_search
{
    "query": {
        "filtered":{
            "filter":{
                "term":{
                    "title": "titulada"
                }
            }
        }
    }
}


GET description/description/_search
{
    "query": {
        "bool": {
            "filter": 
                {
                    "term": {
                        "url": "4"
                    }
                }
            
        }
    }
}
}


POST description/description/_search
{
    "sort": [
            {
            "updated": {
                "order": "desc",
                "ignore_unmapped": true
            }
            }
        ],
    "from": 0,
    "size": 20,
    "query": {
        "bool": {
        "must":[
        {
        "match":{
            "url": "http://exterior.es"
            }
        }
        ]
        }
    }
}




POST description/description/_search
{
    "query": {
        "bool": {
        "must":[
        {
        "prefix":{
            "title": "titulada1"
            }
        },
        {
        "match":{
            "padministration": "Zaragora"
            }

        }
        ]
        }
    }
}



POST description/description/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "prefix": {
                        "title": ""
                    }
                },
                {
                    "match": {
                        "padministration": "Zaragora"
                    }
                },
                {
                    "match": {
                        "url": "http://exterior.es"
                    }
                }
            ]
        }
    }
}


POST description/description/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "prefix": {
                        "title": "titulada"
                    }
                }
            ]
        }
    }
}


POST description/description/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "prefix": {
                        "title": "titulada"
                    }
                },
                {
                    "match": {
                        "padministration": "MEF"
                    }
                },
                {
                    "match": {
                        "domain": "http://interior.es/treinta/b.html"
                    }
                }
            ]
        }
    }
}


GET description/description/_search

#Agregacion de documentos
POST description/description/_search
{
    "aggs": {
        "group_by_url": {
            "terms": {
                "field": "url"
            }
        }
    },
     "size": 0
}





POST description/description/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "padministration": "Zaragora"
                    }
                }
            ]
        }
    }
}



POST description/description/_search
{
    "query": {
        "match":{
            "title": "titulad"
            }
        }
     
    }
}


POST description/description/_search
{
    "query": {
        "match_all":{}
        }
     
    }
}

#Busca las palabras que comiencen con la busqueda
POST description/description/_search
{
    "query": {
        "prefix":{
            "title": "titula"
            }
            
        }
    }
}



#Obtengo una description usando id:

GET description/description/4



GET description/description/_search
{
    "sort": [
        {
            "updated": {
                "order": "desc",
                "ignore_unmapped": true
            }
        }
    ],
    "from": 0,
    "size": 20,
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