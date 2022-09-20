import json
import boto3
import logging

rds_client = boto3.client('rds-data')

database_name = "db_serverless"
db_cluster_arn = "arn:aws:rds:us-west-2:YOUR_ACCOUNT:cluster:pcmt-25-serverless"
db_credentials_secrets_arn = "arn:aws:secretsmanager:us-west-2:YOUR_ACCOUNT:secret:rds-db-credentials/cluster-RV3Y7OJVZRC5XYJBOYI2CY7CJ4/admin2-MQASTx"

def ejecutaQuery(query):
    response = rds_client.execute_statement(
        secretArn=db_credentials_secrets_arn,
        database=database_name,
        resourceArn=db_cluster_arn,
        sql=query
        #includeResultMetadata=True
    )
    return response
    
def get(tabla, id):
    query=" "
    if(tabla=='Paciente'):
        query = "SELECT getPaJson("+id+")"
    elif(tabla=='Departamento'):
        query = "SELECT getDeJson("+id+")"
    resultado=ejecutaQuery(query)
    resultado1=json.loads(resultado['records'][0][0]["stringValue"])
    return resultado1[0]
    
def lambda_handler(event, context):
    logger = logging.getLogger(__name__)
    logging.getLogger().setLevel(logging.INFO)
    logger.info('Event: %s' % json.dumps(event))
    
    arguments = event['arguments']
    
    info = event['info']
    tipo= info['fieldName']
    
    tabla=tipo.replace('get',"").replace('create',"").replace('delete',"").replace('update',"")

    resultado=" "
    resultado = get(tabla, arguments['id'])

    return resultado
