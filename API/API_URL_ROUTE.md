api_url = http://127.0.0.1:5000/

##Auth route:
    #register route : to register new user with sessionToken with json web token
    note: when user registering it receives sessionToken such as accessToken, refreshToken
     - POST: /users/register

    #login: to authenticate an existing user
     - POST: /users/login-client

    #refresh: to refresh accessToken if expired to reauthenticate user automatically if he does not logout himself
    but may out of application
     - POST: /users/refresh

    #infosUser : get user infos use this when user is login or register
     - GET: /users/auth/info

    #logout: logout user with revoking sessionToken
     - POST: /users/logout

##Order route
//coming
##Product route
//coming
##Message route
//coming
##WishList route
##Addresse route
