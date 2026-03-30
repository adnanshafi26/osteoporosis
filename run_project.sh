#!/bin/bash

echo "Starting Osteoporosis Detection System"

cd backend
python model/train_model.py

python app.py