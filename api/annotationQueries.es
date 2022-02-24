

DELETE annotator

POST annotator/annotation/_search

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
                },
                {
                    "match": {
                        "text": "relevant"
                    }
                },
                {
                    "match": {
                        "uri": "http://www.interior.gob.es/web/servicios-al-ciudadano/extranjeria/regimen-general/tarjeta-de-identidad-de-extranjero"
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
            ],
            "must_not": [
                {
                    "match": {
                        "category": "reply"
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
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "uri": {
                                        "createdate": "2021-12-10T10:01:06",
                                        "language": "lv",
                                        "url": "https://latvija.lv/PPK/dzives-situacija/apakssituacija/p5551/ProcesaApraksts",
                                        "email": "d.silva@deusto.es"
                                    }
                                }
                            },
                            {
                                "match": {
                                    "uri": {
                                        "createdate": "2021-12-10T10:01:06",
                                        "language": "lv",
                                        "url": "https://latvija.lv/PPK/dzives-situacija/apakssituacija/p5551/DokumentiUnVeidlapas",
                                        "email": "d.silva@deusto.es"
                                    }
                                }
                            },
                            {
                                "match": {
                                    "uri": {
                                        "createdate": "2021-12-10T10:01:06",
                                        "language": "lv",
                                        "url": "https://latvija.lv/PPK/dzives-situacija/apakssituacija/p5551/PakalpojumaMaksajumi",
                                        "email": "d.silva@deusto.es"
                                    }
                                }
                            },
                            {
                                "match": {
                                    "uri": {
                                        "createdate": "2021-12-10T10:01:06",
                                        "language": "lv",
                                        "url": "https://latvija.lv/PPK/dzives-situacija/apakssituacija/p5551/CitaInformacija",
                                        "email": "d.silva@deusto.es"
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
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

POST annotator/annotation/_search
{

    "aggs" : {
        "group_by_user": {
            "terms": {
                "field": "user"
            }
        }

    },
        
   
    "size": 0
}



POST annotator/annotation/_search

POST annotator/annotation/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "bool": {
                        "should": [
                            {
                                "match": {
                                    "uri": "https://latvija.lv/ppk/dzives-situacija/apakssituacija/p5551/procesaapraksts"
                                }
                            },
                            {
                                "match": {
                                    "uri": "https://latvija.lv/PPK/dzives-situacija/apakssituacija/p5551/DokumentiUnVeidlapas"
                                }
                            },
                            {
                                "match": {
                                    "uri": "https://latvija.lv/PPK/dzives-situacija/apakssituacija/p5551/PakalpojumaMaksajumi"
                                }
                            }
                        ]
                    }
                }
            ]
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