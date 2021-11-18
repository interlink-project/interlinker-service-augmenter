

DELETE annotator


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