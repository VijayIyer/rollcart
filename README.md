Note : This is a copy of the repository from Fall 2022 semester during a Master's Degree course. Edits need to be made to make this app functioning again.

# Welcome to the rollcart app wiki

## What is our product?
### How many times do we actually search different retailer websites to compare prices?  
Every single time.  
Worry no more. Given an item you want to buy our application compares prices across different retailers and recommends the best product based on your preferences. 

## Setup Instructions. 
* Make sure you clone the project. 
```
git clone https://github.iu.edu/P532-OOSD/f22-grocery-budget
```
### Backend.
1. Go to the backend folder. 
```
cd backend/
```
2. Install all the requirements. 
```
pip install -r requirements.txt
```
3. Copy the .env file by requesting from one of the collaborators. 
4. Start the application. 
```
flask --debug run
```

### Frontend.
1. Go the frontend folder. 
```
cd frontend/
```
2. Install all the requirements. 
```
npm i
```
3. Start the react application. 
```
npm start
```

###CI-CD
* We setup the entire backend and frontend on Azure. 
* We also setup our ci-cd pipeline on Azure. On every update to main branch, we will run the test cases and deploy the latest code. 
