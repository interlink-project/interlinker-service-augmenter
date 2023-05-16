# Respaldos de ElasticSearch:

#curl -X GET "elastic:elastic@localhost:9200/_cat/indices/my-index-*?v=true&s=index&pretty"

GET /_cat/indices   

#curl -X PUT "elastic:elastic@localhost:9200/_snapshot/my_repository?pretty" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "my_fs_backup_location"
  }
}
'

# curl -X POST "elastic:elastic@localhost:9200/_snapshot/my_repository/_verify?pretty"



PUT _snapshot/my_repository
{
  "type": "fs",
  "settings": {
    "location": "my_fs_backup_location"        
  }
}

curl -X PUT "elastic:elastic@localhost:9200/_snapshot/my_repository/my_snapshot_29_07_22?pretty"


PUT _snapshot/my_repository/my_snapshot?wait_for_completion=true

curl -X GET "elastic:elastic@localhost:9200/_snapshot/_status?pretty"


GET _snapshot/_status

curl -X GET "elastic:elastic@localhost:9200/_snapshot/my_repository/*?verbose=false"

GET _snapshot/my_repository/*?verbose=false

DELETE annotator

DELETE description


POST _snapshot/my_repository/my_snapshot/_restore
{
  "indices": "annotator,description"
}

GET /_cat/indices   

