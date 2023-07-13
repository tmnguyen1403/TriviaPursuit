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
1. Sign up for MongoDB using gmail with [this link](https://account.mongodb.com/account/login?signedOut=true). I will try to grant you access to the database.

2. Download my branch and navigate to the backend file using Linux command in your VS code terminal. The frontend is not ready yet so you can ignore it.

3. You will need to install some packages to run the backend. They are "body-parser", "express", "express-validator", "mongoose", "nodemon" and "mongoose-unique-validator". Run the following commands to install:
    ```npm install --save express body-parser```

    ```npm install --save-dev nodemon```

    ```git status```
