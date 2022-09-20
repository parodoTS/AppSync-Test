
# Subscriptions:

GraphQL subscriptions allows user to subscribe on topics, so every time this topic is hit the users subscribed will receive a notifications. This feature is usefull for example for real-time based websites.

We have defined the allowed supscriptions in our schema as follows:

    type Subscription { 
	     onCreatePaciente(id: ID, apellido: String, nombre: String): Paciente
	     @aws_subscribe(mutations: ["createPaciente"]) 
	     onUpdatePaciente(id: ID, apellido: String, nombre: String): Paciente 
	     @aws_subscribe(mutations: ["updatePaciente"]) 
	     onDeletePaciente(id: ID, apellido: String, nombre: String): String 
	     @aws_subscribe(mutations: ["deletePaciente"]) 
	     
	     #Subscription to multiple mutations
	     onChangesPaciente(id: ID, apellido: String, nombre: String): Paciente 
	     @aws_subscribe(mutations: ["createPaciente","updatePaciente"]) }
	     
Suscriptions for the "Paciente" type. We have defined one for each mutation type: the creation, the update and the deletion. We have also defined another subscription to show that we can use mutliple mutations in the same one.

Subscriptions in AppSync work over Web Sockets (instead of HTTPS requests as the Mutations/Queries).


> We can test them using AppSync Queries portal in two browser tabs (one for the suscription and other to execute the mutations)

## Testing with Postman:

 1. **Collection** 

In Postman we should create a WebSocket collection (from the desktop app, at this time not available through the browser app).
 
 2. **URL**

From the AppSync GraphQL endpoint:

    https://w47n2fpinvdqtkdpp2zghturii.appsync-api.us-west-2.amazonaws.com/graphql

we obtain the  AppSync Real Time endpoint changing the protocol to **wss** and adding "**-realtime-**":

    wss://w47n2fpinvdqtkdpp2zghturii.appsync-realtime-api.us-west-2.amazonaws.com/graphql

 3. **Params**

We should add two params (both values encoded base64):

 - **header**: with host and authentication info (in this example just API key). 
 To get the header we first build a Json as follows:

       {
            "host":"w47n2fpinvdqtkdpp2zghturii.appsync-api.us-east-1.amazonaws.com",
            "x-api-key":"da2-cqbr3x37j5dploeucfcifu5xgi"
        }
Then we need to encode base64 this Json (for example using [this](https://www.base64encode.org/)) and we get:

    eyJob3N0IjoidzQ3bjJmcGludmRxdGtkcHAyemdodHVyaWkuYXBwc3luYy1hcGkudXMtZWFzdC0xLmFtYXpvbmF3cy5jb20iLCJ4LWFwaS1rZXkiOiJkYTItY3FicjN4MzdqNWRwbG9ldWNmY2lmdTV4Z2kifQ==

 - **payload**: as Json to. For this example just:

	    {}

  Which encoded is:

	e30=
So the final URL looks like:

    wss://w47n2fpinvdqtkdpp2zghturii.appsync-realtime-api.us-west-2.amazonaws.com/graphql?header=eyJob3N0IjoidzQ3bjJmcGludmRxdGtkcHAyemdodHVyaWkuYXBwc3luYy1hcGkudXMtZWFzdC0xLmFtYXpvbmF3cy5jb20iLCJ4LWFwaS1rZXkiOiJkYTItY3FicjN4MzdqNWRwbG9ldWNmY2lmdTV4Z2kifQ==&payload=e30=
In Postman:

![Captura16](https://user-images.githubusercontent.com/100789868/166417697-6b993570-cb83-4d42-94fe-b085b272330f.PNG)

With all these configured we can **Connect**.

4. **Sequence messages**:
The communication proccess is described in the following schema:

![realtime-client-flow](https://user-images.githubusercontent.com/100789868/166417975-a90aaa67-bccc-473e-ad99-33ac6c6d2284.png)

The first message is "Connection init" message which contains the following:

    { "type": "connection_init" }

Then we can subscribe using the "Start subscription" message, which contains the following:

    {
      "id": "1",
      "payload": {
        "data": "{\"query\":\"subscription MySubscription {\\n onCreatePaciente {\\n apellido\\n }\\n }\",\"variables\":{}}",
          "extensions": {
            "authorization": {
              "x-api-key": "da2-cqbr3x37j5dploeucfcifu5xgi",
              "host": "w47n2fpinvdqtkdpp2zghturii.appsync-api.us-west-2.amazonaws.com"
             }
          }
      },
      "type": "start"
    }

In the data field we need to specify the Subscription, in this example we are subscribing to the "onCretePaciente" subscriptions and requesting only the "apellido " field. The id is used to identify uniquely the subscription.

In Postman we can see the messages interchange:
 
![Captura17](https://user-images.githubusercontent.com/100789868/166417854-88f2b457-474a-41e1-bc75-97cc35af505e.PNG)

We can see the message received with the "apellido" field corresponding to a new "Paciente" created.

If we want to unsubscribe we can send a "Stop subscription" message, which contains the following:

    {
      "type":"stop",
      "id":"1"
    }
    
    
Reference: https://docs.aws.amazon.com/appsync/latest/devguide/real-time-websocket-client.html


## Considerations:

Subscription messages will return only fields requested back in the Mutation that activate the Subscription; other fields will appear as null.

Also: 

![image](https://user-images.githubusercontent.com/100789868/166723187-018e3cfe-fa68-4cc5-a707-08019430327c.png)
