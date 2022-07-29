

#MOdificando los tipos de:
PUT /my-index-000001
{
  "mappings" : {
    "properties": {
      "user_id": {
        "type": "long"
      }
    }
  }
}


PUT /description
{
    "mappings": {
        "properties": {
            "id": {
                "type": "text",
                "index": "false"
            },
            "title": {
                "type": "text",
                "analyzer": "standard"
            },
            "description": {
                "type": "text",
                "analyzer": "standard"
            },
            "keywords": {
                "type": "text",
                "analyzer": "standard"
            },
            "moderators": {
                "type": "nested",
                "properties": {
                    "email": {
                        "type": "keyword"
                    },
                    "createdat": {
                        "type": "date"
                    },
                    "expire": {
                        "type": "date"
                    }
                }
            },
            "padministration": {
                "type": "keyword",
                "index": "false"
            },
            "is_portal": {
                "type": "boolean",
                "index": "false"
            },
            "url": {
                "type": "text",
                "index": "false"
            },
            "urls": {
                "type": "nested",
                "properties": {
                    "createdate": {
                        "type": "date"
                    },
                    "ismain": {
                        "type": "boolean"
                    },
                    "url": {
                        "type": "keyword",
                        "index": "false"
                    },
                    "language": {
                        "type": "text",
                        "index": "false"
                    },
                    "email": {
                        "type": "keyword"
                    }
                }
            },
            "created": {
                "type": "date"
            },
            "updated": {
                "type": "date"
            },
            "permissions": {
                "properties": {
                    "read": {
                        "type": "text"
                    },
                    "update": {
                        "type": "text"
                    },
                    "delete": {
                        "type": "text"
                    },
                    "admin": {
                        "type": "text"
                    }
                }
            }
        }
    }
}



#Creo un nuevo indice con el nuevo mapping:

PUT /my-index-000001
{
  "mappings" : {
    "properties": {
      "user_id": {
        "type": "keyword"
      }
    }
  }
}

#Copio la informacion del indice anterior

POST /_reindex
{
  "source": {
    "index": "description"
  },
  "dest": {
    "index": "newdescription"
  }
}

Borro el indice inicial
Lo vuelvo a crear

POST /_reindex
{
  "source": {
    "index": "newdescription"
  },
  "dest": {
    "index": "description"
  }
}