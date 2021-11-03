# Para correr estas queries es necesario habilitar ElasticSearch entorno.


DELETE description
POST description
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
                    "analyzer": "simple"
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

                "permissions": {
                    "index_name": "permission",
                    "properties": {
                        "read": {
                            "type": "string"
                        },
                        "update": {
                            "type": "string"
                        },
                        "delete": {
                            "type": "string"
                        },
                        "admin": {
                            "type": "string"
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

POST description/description/_search
{
"query": {
        "prefix": {
            "title": ""
        }

    }
}

DELETE description/description/AXzB72JcW2WuxQVN8aJF

POST description/description/9
{
    "id":"9",
    "title":"la descripcion titulada9",
    "description":"es el texto de la descripcion",
    "keywords":"ads fads fa ds",
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
    "padministration":"Zaragoza",
    "url":"http://interior.es",
    "created":1635334650,
    "updated":1635334650
}


POST description/description/
{
    "title":"la demanda12 mucho demas gusto",
    "description":"es el texto de la 12",
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
    "permissions":[{"read": ["group:__world__"]}],
    "padministration":"Latvia",
    "url":"http://latvia.vl/x1.html",
    "created":1635334650,
    "updated":1635334650
}

POST description/description/_search?search_type=count

GET description/description/AXzB72JcW2WuxQVN8aJF

DELETE description/description/AXzB72JcW2WuxQVN8aJF

POST description/description/_search?search_type=count
{
    "query": {
        "bool": {
            "must": [
                {
                    "prefix": {
                        "title": "t"
                    }
                }
            ]
        }
    }
}




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
        "query_string": {
        "query": "*la descripcion titulada1*",
        "default_field": "title"
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
                    "prefix": {
                        "url": "http://interior.es/treinta/b.html"
                    }
                }
            ]
        }
    }
}


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


GET description/description/_search
{
    "from":1,"size":1
}

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

POST description/description/_search
{
    
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

#Busca las palabras que comiencen con la busqueda
POST description/description/_search
{
    "query": {
        "query_string":{
            "default_field": "title",
             "query": "*Form3*"
             

            }
            
        }
    }
}




POST description/description/_search




#Obtengo una description usando id:

POST description/description/_search



GET description/description/_search
{

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


POST description/description/_search
{
  "query": {
    "terms": {
      "_id": [ "AXzf9asNW2WuxQVN8aJo" ] 
    }
  }
}


POST annotator/annotation/_search
{
    "query": {
        "terms": {
            "_id": [
                "1635863824727"
            ]
        }
    }
}


POST annotator/annotation/_search


POST annotator/annotation/_search
{
    "sort": [
        {
            "updated": {
                "order": "desc"
            }
        }
    ],
    "from": 0,
    "size": 10,
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "uri": "http://www.interior.gob.es/web/servicios-al-ciudadano/extranjeria/regimen-general/tarjeta-de-identidad-de-extranjero"
                    }
                },
                {
                    "match": {
                        "category": "reply"
                    }
                }
            ]
        }
    }
}