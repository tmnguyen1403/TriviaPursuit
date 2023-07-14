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

2. If you want to merge the features of another branch to your branch:  

    ```git fetch -p```  
    ```git merge origin/<branch_name>```    
For example, if I want to merge branch **drewf**:
    ```git fetch -p```  
    ```git merge origin/drewf```  
If merge successfully in the terminal, an editor will popup with message. If it is a vim editor, you can type ```:wq``` to write and save the merge commit.  
If there is a merge conflict, please Google or contact me to learn how to resolve the conflicts.  

You can now start developing 

# How to run backend
1. Install Node.js to your computer using [this link](https://nodejs.org/en). Download the version recommended for most users and install it.

2. Download Postman App using [this link](https://www.postman.com/downloads/) and sign up for free. I created a team workspace called "Trivial Compute" in Postman. Click [this link](https://app.getpostman.com/join-team?invite_code=1a9d64a74e6f67652ce43fd7b19e9c91&target_code=6e99ce5265d2a7031e7fa67a03dd5be4) to join the team. I created a copy of all the requests in the team workspace.

3. Sign up for MongoDB using gmail with [this link](https://account.mongodb.com/account/login?signedOut=true). Let me know your email you used to create the account once you register successfully. I will try to grant you access to the database. I have configured the network access to allow all the IP addresses to access the database so you should be able to connect to the database sufccessfully with the conncetion link in the code. It is possible that you will only be able to interact with database by sending requests, meaning you can't directly see the database from MongoDB website. Again, you don't need the database access for this step. Continue to the following steps to set up the environment.

4. Download LinBranch and navigate to the backend file using Linux command in your VS code terminal. The frontend is not ready yet so you can ignore it.  
```Navigate to your TriviaPursuit folder, open the terminal```   
```git fetch -p```  
```git checkout ```  

5. Install backend dependency packages:  
   ```cd backend ```  
   ```npm install --save-dev```  

6. At the backend, run the below command to start the backend server. Your terminal should show this message "Connected to MongoDB successfully."  
   ```npm start```

You can use the following APIs on Postman to test the running servers
# API
1. User sign up: ```http://localhost:9000/api/users/signup```
2. User login: ```http://localhost:9000/api/users/login```
3. Get all users: ```http://localhost:9000/api/users```
4. Create a question: ```http://localhost:9000/api/questions```
5. Update a question: ```http://localhost:9000/api/questions/{question id}```
6. Delete a question: ```http://localhost:9000/api/questions/{question id}```
7. Get a question by id: ```http://localhost:9000/api/questions/{question id}```
8. Get questions by user id: ```http://localhost:9000/api/questions/user/{user id}```
9. Get questions by category: ```http://localhost:9000/api/questions/category/{category}```

For more details, join the postman team.
