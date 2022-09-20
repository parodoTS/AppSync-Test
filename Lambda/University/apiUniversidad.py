import logging
import json
import boto3
import psycopg2
from psycopg2.extras import RealDictCursor

def getCredentials():
    credential = {}
    
    secret_name = "arn:aws:secretsmanager:us-west-2:YOUR_ACCOUNT:secret:rds-db-credentials/cluster-6K5UNEFWUTYRAQIYYCJHCTA5SU/admin2-8kt1kC"
    #region_name = "us-west-2"
    
    client = boto3.client(
      'secretsmanager'
      #region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
      SecretId=secret_name
    )

    secret = json.loads(get_secret_value_response['SecretString'])
    
    credential['username'] = secret['username']
    credential['password'] = secret['password']
    credential['host'] = "pcmt-25-cluster.cluster-ro-chnzk2wwqont.us-west-2.rds.amazonaws.com"
    credential['db'] = "db_test"
    
    return credential
    
    
def lambda_handler(event, context):
    # logger = logging.getLogger(__name__)
    # logging.getLogger().setLevel(logging.INFO)
    # logger.info('Event: %s' % json.dumps(event))
   
    arguments = event['arguments']
    
    info = event['info']
    tipo= info['fieldName']
    
    tabla=tipo.replace('get',"").replace('create',"").replace('delete',"").replace('update',"")
    
    credential = getCredentials()
    connection = psycopg2.connect(user=credential['username'], password=credential['password'], host=credential['host'], database=credential['db'])
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    
    query=" "
    if(tipo.startswith('get')):
        id=arguments['id']
        query = "SELECT * FROM "+tabla+" WHERE id="+id+" "
    elif (tipo.startswith('create')):
        mutations = arguments['input']
        query = "INSERT INTO "+tabla+" ("
        for a in mutations:
            query=query+" "+a+","
        query=query[:-1]+") VALUES ("
        for a in mutations:
            query=query+" '"+str(mutations[a])+"',"
        query=query[:-1]+")"
        cursor.execute(query)
        query = "SELECT * FROM "+tabla+" ORDER BY id DESC LIMIT 1;"
    elif (tipo.startswith('delete')):
        mutations = arguments['input']
        id=mutations['id']
        query = "DELETE FROM "+tabla+" WHERE id="+id+" "
        cursor.execute(query)
        cursor.close()
        connection.commit()
        resultado="eliminado"
        return resultado
    elif (tipo.startswith('update')):
        mutations = arguments['input']
        id=mutations['id']
        mutations.pop('id')
        query= "UPDATE "+tabla+" SET"
        for a in mutations:
            query=query+" "+a+"='"+str(mutations[a])+"',"
        query=query[:-1]+" WHERE id="+id+" "
        cursor.execute(query)
        query = "SELECT * FROM "+tabla+" WHERE id="+id+" "
    cursor.execute(query)
    results = cursor.fetchone()
    cursor.close()
    connection.commit()
    return results
