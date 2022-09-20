# AppSync Test
Test GraphQL+AWS Serverless backend (Appsync+Lambda+Aurora Postgres Serverless)

The main purpose of this project is to test AppSync, the AWS service that allows us deploy GraphQL APIs.

GraphQL is a data language with some features, for example it allows API clients to ask the server for specific data, avoiding overfetching data, or Subscriptions operations to implement real-time apps.

To test this service, we are going to deploy the following architecture:

![165063565-ed36b36d-345c-40f5-ba24-e6471d2ad6b4](https://user-images.githubusercontent.com/100789868/165940664-e6baef32-cc9f-4d17-bff7-2c27f6eb0bb8.png)

It is made up of two AppSync APIs. The first one uses an RDS Aurora PostgreSQL instance as database and it contains data about an University app. The second one uses an Aurora PostgreSQL **Serverless** instance as database an its data is about an Hospital app.

Both of them use Lambda functions as data source (using direct Lambda resolvers), each one connects to Secret Manager in order to get access to the database. 

The Hospital API also connects to the University API, so we ilustrate how to connect GraphQL APIs.

# APIs

In this section we are going to describe the steps followed to set up the architecture above mentioned. For each step we are going to differentiate bettween both APIs. 

 1. Creating an Aurora PostgreSQL database.
 2. Building AWS Appsync with GraphQL schema
 3. Set Lambda functions as datasource to connect AppSync with the database.

## Creating an Aurora PostgreSQL database.

> Amazon Aurora is a fully managed relational database engine with
> support for MySQL and PostgreSQL. Aurora includes a high performance
> storage subsystem. Its MySQL and PostgreSQL compatible database
> engines are customized to take advantage of its rapidly distributed
> storage. The underlying storage automatically grows as needed.
> 
> Reference: 
> https://docs.aws.amazon.com/es_es/AmazonRDS/latest/AuroraUserGuide/CHAP_SettingUp_Aurora.html

Both databases store their credentials using a secret in **Secret Manager**. 

### University:
In this case we have set up an Aurora PostgreSQL instance.
We have designed the following data schema just for test:

![dbeaver](https://user-images.githubusercontent.com/100789868/166444633-a608224f-d0ab-4775-a5a9-b7e6328890cf.PNG)

To define the tables and insert the data, we have connected to the instance using DBeaver from our computer. The code used is available [here](https://github.com/parodoTS/PCMT25/tree/main/PostgreSQL).

### Hospital:
In this case the database selected is an Aurora PostgreSQL **Serverless** with the HTTPS endpoint enabled (this allows us to connect to the database directly using this endpoint).

The data schema is similar to the University one, just changing the types and fields names.

To connect to the database, in this case we can use the Query Editor embedded in the RDS console.
We have also set up some PLSQL methods to performs more complex queries. 

## Creation of AWS AppSync

Then we will create an API in AppSync, for that we need to define the Graphql schema for our data and also the operations allowed with them, for example the queries or mutations.

### University
The schema can be found [here](https://github.com/parodoTS/PCMT25/blob/main/AppSync/Schemas/UniversitySchema.graphql).

### Hospital
The [schema](https://github.com/parodoTS/PCMT25/blob/main/AppSync/Schemas/HospitalSchema.graphql)


## Lambda Function

The next step is to asociate the operations in our schema to resolvers and datasources. In our case we are going to use Lambda functions that will receive data directly from the AppSync and perform the connection to the database. To accomplish this, we used [direct Lambda resolvers](https://docs.aws.amazon.com/es_es/appsync/latest/devguide/resolver-mapping-template-reference-lambda.html#direct-lambda-resolvers), setting up the Lambda fuctions as the datasource and leaving blank the resolvers template.


### University
In this case we are using only [one fuction](https://github.com/parodoTS/PCMT25/blob/main/Lambda/University/apiUniversidad.py) for all queries. In this case in order to connect to the database we are going to use the psycorpg2 library (PostgreSQL client for Python), which is not included in the default packages of Lambda, so we firstly need to create a Layer with all necessary packages (you can check steps [here](https://github.com/parodoTS/SkillProfile/blob/main/Lambda/LayerOpenpyxl.md) for a similar Layer creation).

The function code starts getting the credential from Secret Manager (using boto3), then using the info inside it, connects to the database (using psycopg2). By checking the info passed to the function from AppSync, the function puts together the statement that will send to the database (get--> Select, create--> Insert, update--> Update, delete-->Delete), and returns the results back.

### Hospital
For this API we are going to use differents functions ([available here](https://github.com/parodoTS/PCMT25/tree/main/Lambda/Hospital)) and in order to connect to the database we can use boto3 (AWS SDK for Python) directly due to the HTTPS endpoint set up.

For this API we have defined a fuction for a "List" operations to retrieve more than one element of our database. To accomplish that, the fuction performs a Select all and then it re-organizes the data before sending them back to AppSync.

Another fuction developed uses some PLSQL methods implemented in the database. These methods perform the queries that allows us to retrieve departments inside patients data type with just one query to the database.

 
# Testing with Postman
 We can test all the implementation directly from the AppSync console using the Queries tab. Alternatively we can use Postman to test the API, following the same steps as described [here](https://github.com/parodoTS/SkillProfile#testing-the-api-with-postman).

# Subscriptions
[Subscription link](https://github.com/parodoTS/PCMT25/tree/main/AppSync/Subscriptions)
# Authentication and Authorization
[Authentication link](https://github.com/parodoTS/PCMT25/tree/main/AppSync/Authentication)

# References
[Usefull links](https://github.com/parodoTS/PCMT25/tree/main/References)
