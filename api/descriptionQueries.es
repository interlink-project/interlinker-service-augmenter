# Para correr estas queries es necesario habilitar ElasticSearch entorno.

DELETE description

POST description/_search

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

                "urls": {
                    "type": "nested",
                    "properties": {
                        "url": {
                            "type": "string",
                            "index": "not_analyzed"
                        },
                        "ismain": {
                            "type" : "boolean"
                        },
                        "created": {
                            "type": "date",
                            "format": "dateOptionalTime"
                        },
                        "language": {
                            "type": "string",
                            "index": "not_analyzed"
                        }
                    }
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




POST description/_search
{
"query": {
        "prefix": {
            "title": ""
        }

    }
}

DELETE description/AXzB72JcW2WuxQVN8aJF

POST description/9
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


POST description/
{
    "title":"la demanda12 mucho demas gusto",
    "description":"es el texto de la 12",
    "keywords":"palabra, esta ,mostrando",
    "moderators": [
        {
           "email":"d.silva@deusto.es",
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

PUT description/
{
    "title":"la demanda12 mucho demas gusto",
    "description":"es el texto de la 12",
    "keywords":"palabra, esta ,mostrando",
    "moderators": [
        {
           "email":"d.silva@deusto.es",
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

PUT description/AX0ljS0D8dyVuOp-TDl4
{
  "url" : "la demanda12 mucho demas gusto1"
}


POST description/AX0ljS0D8dyVuOp-TDl4/_update
{
 "doc" : {
 "url" : "http://www.riga.lv/en/services/burial-riga-municipal-cemeteries"
 }
}

POST description/AXzvKf1iW2WuxQVN8aKY/_update
{
    "doc": {
        "moderators": [
            {
                "email": "danyche2005@deusto.es",
                "created": "2022-11-05T08:14:20.359310+00:00",
                "expire": "2022-11-05T08:14:20.359310+00:00"
              
            },
        {
           "email":"dipina@deusto.es",
           "created": "2022-11-05T08:14:20.359310+00:00",
           "expire": "2022-11-05T08:14:20.359310+00:00"
        }
        ]
    }
}


POST description/AXzvKf1iW2WuxQVN8aKY/_update
{
  "script": {
    "source": "ctx._source.moderators.add(params.moderator)",
    "params": {
      "moderator": {
        "email": "danyche2014@gmail.com",
        "created": "2021-11-05T08:14:20.359310+00:00",
        "expire": "2021-11-05T08:14:20.359310+00:00"
      }
    }
  }
}


DELETE description/AX0Kg2vFCEacbMWTC_E2

GET description/u5gbKogBXZJ6KRd3nVxx


GET description/_search


POST description/_search


POST description/_search
{
 
    "query": {
        "nested": {
            "path": "moderators",
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "moderators.email": "d.silvad@deusto.es"
                            }
                        }
                    ]
                }
            }
        }
    }
}


POST description/_search
{
 
    "query": {
        "nested": {
            "path": "urls",
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "urls.url": "https://latvija.lv/ppk/dzives-situacija/apakssituacija/p5551/procesaapraksts2"
                            }
                        }
                    ]
                }
            }
        }
    }
}


POST description/_search
{

    "query": {
        "nested": {
            "path": "moderators",
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "moderators.email": "d.silva@deusto.es"
                            }
                        }
                    ]
                }
            }
        }
    }
}


POST description/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "url": "http://extranjeros.inclusion.gob.es/es/informacioninteres/informacionprocedimientos/ciudadanosnocomunitarios/hoja001/index.html"
                    }
                }]
        }
    }
}


POST description/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "url": "http://extranjeros.inclusion.gob.es/es/informacioninteres/informacionprocedimientos/ciudadanosnocomunitarios/hoja001/index.html"
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
                                            "moderators.email": "d.silva@deusto.es"
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


POST description/_search?search_type=count
,
                "inner_hits": {
                    "_source": {
                        "includes": [
                            "moderators.created",
                            "moderators.expire"
                        ]
                    },
                    "highlight": {
                        "fields": {
                            "timedTextLines.textLine": {}
                        }
                    }
                }

POST description/_search?search_type=count

GET description/AXzB72JcW2WuxQVN8aJF

DELETE description/AXzB72JcW2WuxQVN8aJF

POST description/_search?search_type=count
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




POST description/_search
{
    "query": {
        "prefix":{
            "title": "titula"
            }
            
        }
    }
}

POST description/_search

POST description/_search
{
    "query": {
        "match":{
            "url": "http://extranjeros.inclusion.gob.es/es/informacioninteres/informacionprocedimientos/ciudadanosnocomunitarios/hoja001/index.html"
            }
            
        }
    }
}

POST description/_search
{
    "query": {
        "match": {
            "url": [
                "http://latvia.vl/x1.html"
            ]
        }
    }
}


POST description/_search
{
    "query": {
        "prefix":{
            "_id": "AXzqK2S3W2WuxQVN8aJ8"
            }
            
        }
    }
}




GET description/_search
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


GET description/_search
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


POST description/_search
{
    "sort": [
            {
            "updated": {
                "order": "desc",
                "unmapped_type": "date"
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




POST description/_search
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


POST description/_search


POST description/_search
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


POST description/_search
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


POST description/_search
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


GET description/_search
{
    "from":1,"size":1
}

#Agregacion de documentos
POST description/_search
{
    "aggs": {
        "group_by_url": {
            "terms": {
                "field": "id"
            }
        }
    },
    "size": 0
}


POST description/_search
{
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
    }
}


POST description/_search
{
    "aggs" : {
        "moderators" : {
            "nested" : {
                "path" : "moderators"
            },
            "aggs" : {
                "group_by_url": {
                    "terms": {
                        "field": "moderators.email"
                    }
                }

            }
        }
    },
    "size": 0
}




POST description/_search
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



POST description/_search
{
    "query": {
        "match":{
            "title": "titulad"
            }
        }
     
    }
}


POST description/_search
{
    "query": {
        "match_all":{}
        }
     
    }
}

POST description/_search
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
POST description/_search
{
    "query": {
        "query_string":{
            "default_field": "title",
             "query": "*Form3*"
             

            }
            
        }
    }
}




POST description/_search




#Obtengo una description usando id:

POST description/_search



GET description/_search
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


POST description/_search
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


POST annotator/_search


POST annotator/_search
{
    "sort": [
        {
            "updated": {
                "order": "desc"
            }
        }
    ],
    "from": 0,
    "size": 10000,
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "uri": "http://www.interior.gob.es/web/servicios-al-ciudadano/extranjeria/regimen-general/tarjeta-de-identidad-de-extranjero"
                    }
                }
            ]
        }
    }
}

GET annotator/_search 
{
    "query": {
        "bool": {
            "must": [
                {
                    "prefix": {
                        "uri": "http://www.interior.gob.es/web/servicios-al-ciudadano/extranjeria/regimen-general/tarjeta-de-identidad-de-extranjero"
                    }
                },
                {
                    "match": {
                        "_id": "1636002050378"
                    }
                }
            ]
        }
    }
}



GET annotator/_search 
{
    "query": {
        "bool": {
            "must": [
                {
                    "prefix": {
                        "uri": "http://www.interior.gob.es/web/servicios-al-ciudadano/extranjeria/regimen-general/tarjeta-de-identidad-de-extranjero"
                    }
                }
            ]
        }
    }
}

/search?uri=http%3A%2F%2Fwww.interior.gob.es%2Fweb%2Fservicios-al-ciudadano%2Fextranjeria%2Fregime


GET description/_search
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


POST description/_search


POST description/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "_id": "AX2fOijeQQ_0OCFdQwHD"
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
                                            "moderators.email": "d.silva@deusto.es"
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



POST description/_search
{
    "sort": [
        {
            "updated": {
                "order": "desc",
                "ignore_unmapped": "True"
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
                        "title": "burial"
                    }
                },
                {
                    "match": {
                        "padministration": "Latvija Goverment"
                    }
                },
                {
                    "nested": {
                        "path": "urls",
                        "query": {
                            "bool": {
                                "should": [
                                    {
                                        "prefix": {
                                            "urls.url": "https://"
                                        }
                                    },
                                    {
                                        "prefix": {
                                            "url": "http://"
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


POST description/_search
{
  
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "url": "https://latvija.lv/en/ppk/izglitiba/augstaka-izglitiba/p11899/procesaapraksts"
                    }
                }
            ]
        }
    }
}

POST description/_search
{
    "from": 0,
    "query": {
        "nested": {
            "path": "moderators",
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "moderators.email": "d.silva@deusto.es"
                            }
                        }
                    ]
                }
            },
            "score_mode": "sum"
        }
    }
}

PUT /description/_mapping
{
  "properties": {
    "moderators": {
        "type": "nested",
        "properties": {
            "email": {"type": "keyword"},
            "createdat": {
                "type": "date"
            },
            "expire": {
                "type": "date"
            }
        }
    }
  }
}

