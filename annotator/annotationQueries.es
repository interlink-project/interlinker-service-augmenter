

DELETE annotator

POST annotator/annotation/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "text": "relevant"
                    }
                }
            ]
        }
    }
    
}


POST annotator/annotation/_search
{
  "size": 0,
  "aggs": {
    "uri": {
      "terms": {
        "field": "uri"
        
      }
    }
  }
}

POST annotator/annotation/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "text": "relevant"
                    }
                },
                {
                    "match": {
                        "uri": "http://www.interior.gob.es/web/servicios-al-ciudadano/extranjeria/regimen-general/tarjeta-de-identidad-de-extranjero"
                    }
                },
                {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "state": 0
                                }
                            },
                            {
                                "match": {
                                    "state": 1
                                }
                            },
                            {
                                "match": {
                                    "state": 2
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
}

POST annotator/annotation/_search
{
  
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "uri": "http://www.interior.gob.es/web/servicios-al-ciudadano/extranjeria/regimen-general/tarjeta-de-identidad-de-extranjero"
                    }
                },
                {
                    "prefix": {
                        "text": "Este es mi termino"
                    }
                },
                {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "state": 0
                                }
                            },
                            {
                                "match": {
                                    "state": 1
                                }
                            },
                            {
                                "match": {
                                    "state": 2
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }
}



POST annotator/annotation/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "_id": "1637225312399"
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
                                            "statechanges.user": "d.silva@deusto.es"
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



POST annotator/annotation/_search
{
    "query": {
        "bool": {
        "must": [
            {
                "match":{
                "uri":"https://latvija.lv/ppk/dzives-situacija/apakssituacija/p5551/procesaapraksts"
                }
            },
            {
                "match":{
                "category":"reply"
                }
            }
            ,
            {
                "match":{
                "idAnotationReply":"annotation-1636726292600"
                }
            }
            
        ]
        }
    }
}

POST annotator/annotation/_search