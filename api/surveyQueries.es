# Para correr estas queries es necesario habilitar ElasticSearch entorno.

POST survey/survey/_search

DELETE survey

POST survey
{
    "mappings": {
        "description": {
            "properties": {
                "id": {
                    "type": "string",
                    "index": "no"
                },
                "idAsset": {
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
                "isMandatory": {
                    "type": "boolean"
                },
                "created": {
                    "type": "date"
                },
                "updated": {
                    "type": "date"
                }
            }
        }
    }
}



POST survey/survey/_search
{
    "query": {
        "bool": {
            "should": [
                {
                    "term": {
                        "email": "d.silva@deusto.es"
                    }
                },
                {
                    "term": {
                        "email": "*"
                    }
                }
            ]
        }
    }
}