# Authentication options:
In this section we are going to take a look at differents authentication methods allowed by AppSync.

## Cognito User Pools Set Up

>Amazon Cognito User Pools provide a fully managed user directory. Cognito User Pools also allows users to sign-in to your application using their social profile (e.g.: Google, Facebook, Amazon, or Apple). It’s also possible to federate a User Pool with existing SAML identity providers and OpenID Connect (OIDC) Identity providers.
>
>Cognito also allows for a secure way to exchange JWT tokens from User Pools with temporary AWS credentials using Cognito Identity Pools. It makes Cognito User Pools a good choice when your application must interact with an AppSync endpoint using JWT tokens as well as other AWS services using AWS credentials.

### Set up:
Those steps were completed using the AWS Management Console:
 1. First, we create a Cognito User Pool, we give it a name, and configure it by setting the mandatory atributtes for every user (email and birthdate for example), setting the password policy (min length, special keys...) and also we allow users to sign up. All other features are disabled or default.
 
 2. In the "Application Clients" section we create a new one, **unchecking the secret key option** (we are not going to use it). Here we can change some settings such as Tokens expiration or atributes read/write permissions. 
  ![Captura](https://user-images.githubusercontent.com/100789868/165334895-b876f91b-06d5-4b2f-b08a-e8e48a89161c.PNG)

  After create this App Client we can get its App Client id.
 
 ![Captura1](https://user-images.githubusercontent.com/100789868/165334912-9b9e9846-9264-4095-aa5d-137da485ecf8.PNG)

 3. Once we have created the App Client, under "App Integration" tab in "App Client settings", we enable the Cognito User Pool  as Identity Provider (the only one that appears because we have not configure anyone else yet). We also configure the Callback and Sign out URLs as follows:
 
 ![Captura2](https://user-images.githubusercontent.com/100789868/165335012-48a49818-96e8-43dd-8407-af927c503c1d.PNG)

Using "https://example.com" a domain which is maintained for documentation purposes.

We also have configured OAuth 2.0.

 4. In "Domain name" we configure a domain prefix:
 
 ![Captura3](https://user-images.githubusercontent.com/100789868/165335189-e298d970-82f5-4770-a080-3091fbd773c5.PNG)

 5. Back at the botton of "App Client settings", we can "Launch Hosted UI". We are using the default one because the main purpose of this project is to test its functionality, not developing a full application.
From the sign in form that appear we can also sign up a new user (since we allowed previously that users can sing up themselves):

![Captura4](https://user-images.githubusercontent.com/100789868/165335280-a9cca7bf-b51f-4c71-9bc4-f1921a4ca81a.PNG)


Link: https://pcmt25.auth.us-west-2.amazoncognito.com/signup?client_id=7vls2sq4j4tuc07cbbj37t2201&response_type=code&scope=email+openid&redirect_uri=https://example.com/callback

After complete all the initial information, we will receive a confirmation code through the mail indicated in order to confirm the account (you can change this configuration in the "MFA and verifications" tab ). 

![Captura5](https://user-images.githubusercontent.com/100789868/165335382-d7bdef65-7573-44b0-823e-a3739253e7ef.PNG)

If everything is okey you will be redirected to the callback url we have set up.

We can see all users registered under "Users and groups" tab.

## Appsync + Cognito configuration:
Under settings, we are going to set up the default authentication method as Cognito User Pool, we select the user group and ALLOW as default action (this default option will affect all operations in the schema for what we do not indicate any other directive, we will see it later)

![Captura6](https://user-images.githubusercontent.com/100789868/165335454-2f49e131-a581-4071-ba8a-70aeb3b6800d.PNG)

### Test:
After that we can test it using the "Queries" integrated in AppSync.
If we try to do any operation, for example a query without logging in: 

![Captura7](https://user-images.githubusercontent.com/100789868/165335511-0b9edc5c-2328-4e94-9a10-21c0ca5cdf84.PNG)

So we need to loggin:

![Captura8](https://user-images.githubusercontent.com/100789868/165335554-45c69c1f-2ec7-42da-89e8-882accba4ea0.PNG)

And now, we can query:

![Captura9](https://user-images.githubusercontent.com/100789868/165335579-f54fd119-b5d6-4255-a968-d80994ee60c3.PNG)

If we want to try it with Postman, we need to follow the next steps:

From the sign in form (in our Cognito User Pool at the botton of "App Client settings",  "Launch Hosted UI"), we need to **change the word "code" to "token"** in the URL:

Link: https://pcmt25.auth.us-west-2.amazoncognito.com/login?client_id=7vls2sq4j4tuc07cbbj37t2201&response_type=token&scope=email+openid&redirect_uri=https://example.com/callback

From this link (notice the "response_type=token"), after we sing in, we are redirected to our callback URL, **with the token as param inside the URL**, from where we extract our tokens. For example:

***id_token**=eyJraWQiOiI5TzR3YkRURkY2XC9OZjdcLzZJN3IwREQ0bTNKc0M4OFwvaTJBMG05MXFiSzVVPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiLUhGb0dFMG51TVl6b3NOYTAxc2lMZyIsInN1YiI6ImJiM2ZiYTEzLTg1YmItNDU4YS04MTEzLTliODAzMzdkY2E0NiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9SUUdxNndTTkkiLCJjb2duaXRvOnVzZXJuYW1lIjoidXNlcjEiLCJhdWQiOiI3dmxzMnNxNGo0dHVjMDdjYmJqMzd0MjIwMSIsImV2ZW50X2lkIjoiZTZjZDljZDktMDRhNi00N2M1LThlNWMtZDNiMTM3ODJjYjE0IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2NTA5ODQ3OTgsImV4cCI6MTY1MDk4ODM5OCwiaWF0IjoxNjUwOTg0Nzk4LCJqdGkiOiI5NDdiMGZhNC1kYzY2LTQyY2QtOGY3YS1kZjdmOWIxZDljM2IiLCJlbWFpbCI6InBhYmxvLnJvYXMtZG9taW5nb0B0LXN5c3RlbXMuY29tIn0.IHHXytdOb24uD0qh4IZvfPLuiYQYliAPMEe4LMSYd7j8eOs_TQOYrpmO2NNubJLGw6hecIT_vWB2C2ytsCmltRMVkmQXj6yUrI7lRMEQdrP8R9kZsOtuvoLUQk6JJav3kqgzBNPJc2f_h9UoNNo6vWjW7q8l8U1_7cckDOEG2c4aRu0IUwahEl1B4NAlM-_8XztmIT39RbF_TqMkvm2ccDghEOz8AGYd2TOIxLFWjWD8Ki82geS__bz6p7juJMbDeYvmTztmrdijivPuODPP_Akd0-0guC1CBzwOMZJhBDTDRkhrd0D-eJrLxxFa7ga5cmrt5YkyF4L5bi6KW_yNRw*

***access_token**=eyJraWQiOiJ5TnNVbTdrUFJKRTQ5amZkU2dPTDNhb0J1alo5MWlEbEZVN0d4TEdNSlBJPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJiYjNmYmExMy04NWJiLTQ1OGEtODExMy05YjgwMzM3ZGNhNDYiLCJldmVudF9pZCI6ImU2Y2Q5Y2Q5LTA0YTYtNDdjNS04ZTVjLWQzYjEzNzgyY2IxNCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoib3BlbmlkIGVtYWlsIiwiYXV0aF90aW1lIjoxNjUwOTg0Nzk4LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtd2VzdC0yLmFtYXpvbmF3cy5jb21cL3VzLXdlc3QtMl9SUUdxNndTTkkiLCJleHAiOjE2NTA5ODgzOTgsImlhdCI6MTY1MDk4NDc5OCwidmVyc2lvbiI6MiwianRpIjoiNTk4MWE5NmYtZTdkMi00YWMwLTljMzgtMjM2YzAxZGRmZmVjIiwiY2xpZW50X2lkIjoiN3ZsczJzcTRqNHR1YzA3Y2JiajM3dDIyMDEiLCJ1c2VybmFtZSI6InVzZXIxIn0.pExYkItwOns2nsNqsMTrPs5XXySev07Apkb3k65K2QtNAlPXZ0Hiiv9OUPm6BHL8JnTLRwlng0Ph9WGgGOLBc-_-UDpauu7gItjzE0hBxCStqRc--fzzKpETQykoVDmD540Cq_OxFuANPxQB34pcX5aRwdinowoSwd1u-KXX9e4h5j9nY9xC2rdoAiSYg1DfbccUIVFRfKB6J_RAMKMZoru21ybMc8COxhhDkiqe6legGaK8Wd3Kg_-r8PFJqFYcLGD7iSu65nrAOkI48K_84qoS-vQqYlkjtWRv9UV5xrMaFhM0eitcR-8DGURonVkdzSz0D2Xj9SPGj3u57yxkSg*

***expires_in**=3600
**token_type**=Bearer*

Those tokens are retrieve from Cognito for the user we have used to sign in. We save this info.

So now in Postman (in our previously created GraphQL API), we change the Authoritation Key  in the Header to "Authoritation" and in the value we copy the "access token" received (we can also use the "id token" and it will work too, the main difference between them it is that the id token also allows the backend to retrieve info about our Cognito User, so for this case we can use just the acces token. See differences [later](https://github.com/parodoTS/PCMT25/blob/main/Authentication/README.md#fined-grained-access-control)).

![Captura10](https://user-images.githubusercontent.com/100789868/165335648-9b089ef5-1b44-46c9-8713-df1b17676cbe.PNG)

>Alternatively we can configure Postman to request the token from its interface as follows:
>
>![Captura12](https://user-images.githubusercontent.com/100789868/165790371-8bbed38d-da42-4d89-baa0-752244982f15.PNG)
>
>It is a good practice to store all sensitive data in Postman variables instead of writing them directly

Now we can query the API:

![Captura11](https://user-images.githubusercontent.com/100789868/165335660-dff0dcbd-e3e0-4249-8e96-43636ee89fd1.PNG)


We can also use AppSync cognito directives in our schema to filter specific fields access to diferent cognito users. For that we have created a cognito user group called "admins" fro administrators users.
After that for example if we want the query "getDirector" restricted only for "admins" users:

     type Query {
    	getDirector(id: ID!): Director
		    @aws_auth(cognito_groups: ["admins"])

If we try to use this query with an user who is not in this group:

![Captura13](https://user-images.githubusercontent.com/100789868/165937524-bffc6543-6a41-4269-ada8-6d9daf7f6de9.PNG)

But if an admins user queries:

![Captura14](https://user-images.githubusercontent.com/100789868/165937548-f4075989-60b2-4b5f-a0c0-b101397164b3.PNG)

## Multiple authentication methods.

Appsync also allows to use multiple authentication methods. You can add more than one mechanism from its settings.

For example we are going to add API key authentication to our Appsync which was configured with Cognito authentications as default method. **The default authentication (primary method configurated) will acts for all those schema types in which we do not specify any directive.**

When we have set up more than one authentication method we can configure which method will be allowed per type or field in our schema.
For example if we want to allow both authenticated users (API key and Cognito) to perfom queries, we should add both directives at the Query type as follows:

    type Query @aws_api_key @aws_cognito_user_pools {
    	getDirector(id: ID!): Director
		    @aws_auth(cognito_groups: ["admins"])
    	getHospital(id: ID!): Hospital
    	...
All fields inside type Query (all queries) will be allowed for API key and Cognito users, except those fields (queries) for which we specify other directive, in the sample code before, only users authenticated using Cognito that are in the "admins" group will be able to perfom "getDirector" query. **Once we specify some directive in any type, all fields inside it will get the same directive unless we specify another directive in a field concrete.**

What happens if we now perfom a query athenticated using API key, for example:

![Captura15](https://user-images.githubusercontent.com/100789868/165937654-55a0bd9b-aa60-464b-acf6-ae5856a1c015.PNG)

We are getting an error, because the type "Hospital" (that should be retrieved) has not got any directive specified, so it is using just the default authentication (Cognito); so we need to add the following:

    type Hospital @aws_api_key {
    	id: ID!
    	ubicacion: String!
    	nombre: String!
    	director_id: Int!
    }

   After that, it will apply just that directive for that type, disallowing default method (Cognito).

> We can also apply directives for fields (as we have done for queries inside ype "Query") to allow access only to a subset of them, filtering the info an user can access. For example:
> 
    type Hospital {
        id: ID!
    	ubicacion: String!
    	nombre: String!
	        @aws_api_key
    	director_id: Int!
    }
> API key authenticated users will only be able to acces the "nombre " field.

## Fined-Grained access control:
With all these methods showed above, we can decide which kind of authentication will be needed to acces types and fields and even use Cognito groups. But what if we want to implement more restrictive access patterns, for example differents privileges for users inside a group?
In these cases we should configure authorization in our backend logic, for example in our resolvers. When Appsync calls a resolvers, it adds a field "identity" in the $context (data passed to the resolver) with information about identity of the user accessing the API.

If we check the "identity" field of some of our previous requests (from the CloudWatch logs of the Lambda resolver) while using the "id token":

    "identity": { 
	    "claims": { 
		    "sub":  "bb3fba13-85bb-458a-8113-9b80337dca46",
		    "email_verified":  true,
		    "birthdate":  "26/04/2022", 
		    "iss":  "https://cognito-idp.us-west-2.amazonaws.com/us-west-2_RQGq6wSNI", 
		    "cognito:username":  "user1", 
		    "origin_jti":  "a185e792-5602-41c0-87f3-decdcd10c71a", 
		    "aud":  "7vls2sq4j4tuc07cbbj37t2201", 
		    "event_id":  "6fa413c1-4a84-45bb-9ef2-c800540eaacc", 
		    "token_use":  "id", 
		    "auth_time":  1651227981, 
		    "exp":  1651231581, 
		    "iat":  1651227981, 
		    "jti":  "6f03807b-0d02-41ca-8a03-b77eb1560204", 
		    "email":  "mail@mail.com" 
	    }, 
	    "defaultAuthStrategy":  "ALLOW", 
	    "groups":  null, 
	    "issuer":  "https://cognito-idp.us-west-2.amazonaws.com/us-west-2_RQGq6wSNI", 
	    "sourceIp": [ "217.14.40.189" ], 
	    "sub":  "bb3fba13-85bb-458a-8113-9b80337dca46", 
	    "username":  "user1" 
    },


And if we compare it to the same field but using the "access token":

    "identity": { 
	    "claims": {
		     "sub":  "bb3fba13-85bb-458a-8113-9b80337dca46", 
		     "event_id":  "3fe2c13b-5944-448d-8908-1e34c5214a6c", 
		     "token_use":  "access", 
		     "scope":  "openid email", 
		     "auth_time":  1651241715, 
		     "iss":  "https://cognito-idp.us-west-2.amazonaws.com/us-west-2_RQGq6wSNI", 
		     "exp":  1651245315, 
		     "iat":  1651241715, 
		     "version":  2, 
		     "jti":  "ee7d1638-4417-4a73-a43b-9c868a7623f4", 
		     "client_id":  "7vls2sq4j4tuc07cbbj37t2201", 
		     "username":  "user1" 
	     },
	      "defaultAuthStrategy":  "ALLOW", 
	      "groups":  null, 
	      "issuer":  "https://cognito-idp.us-west-2.amazonaws.com/us-west-2_RQGq6wSNI", 
	      "sourceIp": [ "54.86.50.139" ], 
	      "sub":  "bb3fba13-85bb-458a-8113-9b80337dca46", 
	      "username":  "user1" 
      },

We can see how the firstone includes more identity information related to the user info from Cognito (like we have said before).

Using this info, we can implement some logic and checks to allow diferents users access only their data, or maybe to store user data in a database to log who is accessing/modifiying the data.
