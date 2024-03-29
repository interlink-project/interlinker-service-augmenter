

DELETE annotator

GET annotator/_search

POST annotator/_search
{
    "sort": [
        {
            "created": {
                "format": "strict_date_optional_time_nanos",
                "order": "desc"
            }
        }
    ],
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "descriptionId": "VcAoM4gBaQZSsIEWHVwi"
                    }
                }
            ]
        }
    }
}

GET annotator/OcAsL4gBaQZSsIEWS1wG

PUT annotator/_doc/OcAsL4gBaQZSsIEWS1wG
{
    "text": "<p>the last of us</p>"
}


POST annotator/_search
{
    "sort" : [
    { "created" : {"format": "strict_date_optional_time_nanos","order" : "desc"}}
  ],
    "query": {
        "range": {
            "data_creacio":  {
                        "gte": "1684394792800"
                    }
               
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

POST annotator/_search
{
    "sort": [
        {
            "created": {
                "format": "strict_date_optional_time_nanos",
                "order": "desc"
            }
        }
    ],
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
                                    "state": 2
                                }
                            }
                        ]
                    }
                },
                {
                    "match": {
                        "descriptionId": "VcAoM4gBaQZSsIEWHVwi"
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
                        "_id": "1653465716079"
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

POST annotator/_search
{
    "sort": [
        {
            "updated": {
                "order": "desc",
                "unmapped_type": "date"
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
                                        "url": "https://elpais.com/espana/2023-05-17/el-cis-da-ganador-al-psoe-con-19-puntos-de-ventaja-y-situa-a-sumar-como-tercera-fuerza-tras-adelantar-a-vox.html",
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



POST annotator/annotation/_search


POST annotator/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "match": {
                        "user": "d.silva@deusto.es"
                    }
                }
            ]
        }
    },
    "aggs": {
        "group_by_uri": {
            "terms": {
                "field": "uri"
            }
        }
    },
    "size": 0
}