import json
import boto3
import logging

rds_client = boto3.client('rds-data')

database_name = "db_serverless"
db_cluster_arn = "arn:aws:rds:us-west-2:YOUR_ACCOUNT:cluster:pcmt-25-serverless"
db_credentials_secrets_arn = "arn:aws:secretsmanager:us-west-2:YOUR_ACCOUNT:secret:rds-db-credentials/cluster-RV3Y7OJVZRC5XYJBOYI2CY7CJ4/admin2-MQASTx"

def parse_data_service_response(res):
    columns = [column['name'] for column in res['columnMetadata']]

    parsed_records = []
    for record in res['records']:
        parsed_record = {}
        for i, cell in enumerate(record):
            key = columns[i]
            value = list(cell.values())[0]
            parsed_record[key] = value
        parsed_records.append(parsed_record)

    return parsed_records

def ejecutaQuery(query):
    response = rds_client.execute_statement(
        secretArn=db_credentials_secrets_arn,
        database=database_name,
        resourceArn=db_cluster_arn,
        sql=query,
        includeResultMetadata=True
    )
    return response
    
def get(tabla, id):
    query = "SELECT * FROM "+tabla+" WHERE id="+id+" "
    resultado=parse_data_service_response(ejecutaQuery(query))[0]
    return resultado
    
def create(tabla, mutations):
    query = "INSERT INTO "+tabla+" ("
    query1 = " "
    query2 = " "
    for a in mutations:
        query1 = query1+" "+a+","
        query2 = query2+" '"+str(mutations[a])+"',"
    query = query+query1[:-1]+") VALUES ("+query2[:-1]+")"
    resultado = ejecutaQuery(query)
    return resultado

def delete(tabla, id):
    query = "DELETE FROM "+tabla+" WHERE id="+id+" "
    resultado = ejecutaQuery(query)
    return resultado

def update(tabla, id , mutations):
    query= "UPDATE "+tabla+" SET"
    for a in mutations:
        query=query+" "+a+"='"+str(mutations[a])+"',"
    query=query[:-1]+" WHERE id="+id+" "
    resultado = ejecutaQuery(query)
    return resultado
    
def lambda_handler(event, context):
    logger = logging.getLogger(__name__)
    logging.getLogger().setLevel(logging.INFO)
    logger.info('Event: %s' % json.dumps(event))
    
    arguments = event['arguments']
    #return "hello"
    info = event['info']
    tipo= info['fieldName']
    
    tabla=tipo.replace('get',"").replace('create',"").replace('delete',"").replace('update',"")

    query=" "
    resultado=" "
    
    if(tipo.startswith('get')):
        resultado = get(tabla, arguments['id'])
    elif (tipo.startswith('create')):
        mutations = arguments['input']
        query = create(tabla, mutations)
        resultado = parse_data_service_response(ejecutaQuery("SELECT * FROM "+tabla+" ORDER BY id DESC LIMIT 1"))[0]
    elif (tipo.startswith('delete')):
        mutations = arguments['input']
        id = mutations['id']
        query = delete(tabla,id)
        resultado = "eliminado"
    elif (tipo.startswith('update')):
        mutations = arguments['input']
        id = mutations['id']
        mutations.pop('id')
        query = update(tabla,id,mutations)
        resultado = get(tabla,id)
    
    return resultado
