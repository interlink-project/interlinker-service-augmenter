

DELETE annotator

POST annotator/annotation/_search


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