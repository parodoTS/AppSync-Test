import json
import boto3
import logging

rds_client = boto3.client('rds-data')

database_name = "db_serverless"
db_cluster_arn = "arn:aws:rds:us-west-2:YOUR_ACCOUNT:cluster:pcmt-25-serverless"
db_credentials_secrets_arn = "arn:aws:secretsmanager:us-west-2:YOUR_ACCOUNT:secret:rds-db-credentials/cluster-RV3Y7OJVZRC5XYJBOYI2CY7CJ4/admin2-MQASTx"

def parse_data_service_response(res):
    columns = [column['name'] for column in res['columnMetadata']]
    
    items={}
    items["items"]=[]

    for record in res['records']:
        parsed_record = {}
        for i, cell in enumerate(record):
            key = columns[i]
            value = list(cell.values())[0]
            parsed_record[key] = value
        items["items"].append(parsed_record)

    return items

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
    query = "SELECT * FROM "+tabla+" " 
    resultado=parse_data_service_response(ejecutaQuery(query))
    return resultado
    
def lambda_handler(event, context):
    logger = logging.getLogger(__name__)
    logging.getLogger().setLevel(logging.INFO)
    logger.info('Event: %s' % json.dumps(event))
    
    arguments = event['arguments']
    info = event['info']
    tipo= info['fieldName']
    
    tabla=(tipo.replace('list',''))[:-1]

    query=" "
    resultado=" "
    
    if(tipo.startswith('list')):
        resultado = get(tabla,1)
    
    return resultado
