# Respaldos de ElasticSearch:

GET /_cat/indices   

PUT _snapshot/my_fs_backup
{
  "type": "fs",
  "settings": {
    "location": "my_fs_backup_location"        
  }
}

PUT _snapshot/my_fs_backup/my_snapshot?wait_for_completion=true

GET _snapshot/_status

GET _snapshot/my_fs_backup/*?verbose=false

DELETE annotator

DELETE description


POST _snapshot/my_fs_backup/my_snapshot/_restore
{
  "indices": "annotator,description"
}

GET /_cat/indices   

