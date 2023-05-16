from api import es, annotation, document, notification, store, description, survey, feedback
from api.description import Description

lines = []

with open('_varam-interlink-project-eu-logging_logs_07_12_h_12_15.txt', encoding='utf8') as f:
    lines = f.readlines()


count = 0
countDescriptions= 0
countAnnotations= 0
for line in lines:
    #line=lines[39]
    count += 1
    #print(f'line {count}: {line}')

    #Obtengo la fecha Hora
    listinfo=line.split(' ',1)
    fechaHora=listinfo[0]

    #print(fechaHora)
    restodeData=listinfo[1]

    #Creacion de Descripciones:

    if 'new_description' in restodeData:
        countDescriptions +=1
	    #print(f'line {count}: {fechaHora} {restodeData}')
        print(f'line {countDescriptions}: {fechaHora} {restodeData}')

        import json

        dataDescription = json.loads(restodeData)

        print(dataDescription)

        dataDescription['description_data']['id']=dataDescription['object_id']

        json_formatted_str = json.dumps(dataDescription['description_data'], indent=2)

        print(json_formatted_str)

        Description.guardar(dataDescription['description_data'],index='description')


    if 'new_annotation' in restodeData:
        countAnnotations +=1
	    #print(f'line {count}: {fechaHora} {restodeData}')
        print(f'line {countAnnotations}: {fechaHora} {restodeData}')

        import json

        dataDescription = json.loads(restodeData)

        print(dataDescription)

        dataDescription['annotation_data']['id']=dataDescription['object_id']

        json_formatted_str = json.dumps(dataDescription['annotation_data'], indent=2)

        print(json_formatted_str)

        Description.guardar(dataDescription['annotation_data'],index='annotator')






    
