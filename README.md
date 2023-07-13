# TriviaPursuit
TriviaPursuit is the game project for Foundation of SWE class 

# Development setup
1. Require git to be installed on machine   
    https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
2. Set up ssh key on github
    https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
3. Clone the project to your prefer working directory  
   On Mac/Windows, open terminal  
    ```git clone git@github.com:tmnguyen1403/TriviaPursuit.git```  
4. Create your own branch  
    ```git checkout -b <branch_name> ```

# Development flow
1. Whenever your code changes are ready for reviewed

    ```git status``` #This shows the files that you modified

    ```git diff``` #This displays your changes, verify the changes
    
    ```git add <files_that_change>```

    ```git commit -m " <message_about_your_changes> " ```

    ```git push ``` # Push/upload your changes to the remote git repository () 

You can now start developing 

# How to run backend
1. Install Node.js to your computer using [this link](https://nodejs.org/en). Download the version recommended for most users and install it.

2. Download Postman App using [this link](https://www.postman.com/downloads/) and sign up for free.

3. Sign up for MongoDB using gmail with [this link](https://account.mongodb.com/account/login?signedOut=true). Let me know your email you used to create the account once you register successfully. I will try to grant you access to the database. I have configured the network access to allow all the IP addresses to access the database so you should be able to connect to the database sufccessfully with the conncetion link in the code. It is possible that you will only be able to interact with database by sending requests, meaning you can't directly see the database from MongoDB website. Again, you don't need the database access for this step. Continue to the following steps to set up the environment.

4. Download LinBranch and navigate to the backend file using Linux command in your VS code terminal. The frontend is not ready yet so you can ignore it.

5. You will need to install some packages to run the backend. They are "body-parser", "express", "express-validator", "mongoose", "nodemon" and "mongoose-unique-validator". Run the following commands to install:
   
   ```npm install --save express body-parser```

   ```npm install --save-dev nodemon```

   ```npm install --save express-validator```

   ```npm install --save mongoose```

   ```npm install --save mongoose-unique-validator```

6. To run the backend, run the following command. Your terminal should show this message "Connected to MongoDB successfully." If it reports error, it means that you haven't had access to database. Let me know if it reports errors.

   ```npm start```
