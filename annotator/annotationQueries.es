

DELETE annotator

POST annotator/annotation/_search

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
    "size":0,
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
    },
    "aggs": {
        "group_by_uri": {
            "terms": {
                "field": "uri"
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