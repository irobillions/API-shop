# How use the project

## Install all requirement in the requirement.txt


## First step
 - create an virtual environment usinf python 3.7 with: 
       
       
       py -m venv env
 - run the virtual env and install all dependencies :
 
    
       env\Scripts\activate on windows
 - Check the config file to change config with appropriate configuration for you
 - You can check DataBaseUri and change it to start database
 - After if you have installed all requirement you can use migration to init database
 - But before the previous step you must create database (use mysql or sqlite but relationel database)
 - If you do all of this you can use migration
       
       python -m app-shared.manage db init // init database
       python -m app.shared.manage db migrate // start migration
       python -m app.shared.manage db upgrade  // upgrade database
  - After you can run seeders.py to populate database with:
        
        python -m app.seeders 
 - But if you don't want you can create your own data
 - I have used WAMP to launch databaseServer in port:3306
 
 
 ## Second step 
 
 - You can use the API with all the request
 - Before run all the test to see if something went to wrong
 - For that run the with the run.py file
       
        python run.py