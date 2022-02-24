# Para correr estas queries es necesario habilitar ElasticSearch entorno.

POST notification/notification/_search

DELETE notification

POST notification
{
    "mappings": {
        "description": {
            "properties": {
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
        }
    }
}



POST notification/notification/_search
{
    "query": {
        "bool": {
            "must": [
                {
                    "term": {
                        "resolved": false
                    }
                },
                {
                    "term": {
                        "category": "survey"
                    }
                }
            ]
        }
    }
}