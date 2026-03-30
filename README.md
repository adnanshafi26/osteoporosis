# AI-Based Osteoporosis Detection System

This project predicts the risk of osteoporosis using
clinical bone density data and machine learning.

Technologies used:

- Python
- Flask
- TensorFlow / Scikit-Learn
- HTML
- CSS
- JavaScript
- Java
- SQL

Project Structure:

backend → AI model and Flask API  
frontend → Web user interface  
java-module → Clinical report analyzer  
database → SQL schema and records  

------------------------------------------------

## Installation

1 Install Python libraries

pip install -r backend/requirements.txt


2 Train the AI model

cd backend
python model/train_model.py


3 Run Flask server

python app.py


4 Open frontend

Open frontend/index.html in browser


------------------------------------------------

## API Endpoint

POST /predict

Example request:

{
 "features":[65,0,22,0.55,800,20]
}


Response:

{
 "prediction":"High Risk of Osteoporosis"
}

------------------------------------------------

## Authors

AI Osteoporosis Detection Project