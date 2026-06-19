# 🌱 CropSense AI — Smart Crop Monitoring System

## Overview
CropSense AI is a machine learning-based web application that helps analyze soil conditions and provide intelligent farming insights. It uses Python, Streamlit, and a trained ML model to convert soil data into meaningful predictions for better agricultural decisions.

---

## What This Project Does
This system takes soil inputs like Nitrogen, Phosphorus, Potassium, pH, and Moisture, processes them using a trained model, and predicts the soil condition. The results are shown in a simple dashboard for easy understanding.

---

## Features
- Soil condition prediction (Good / Moderate / Poor)
- Machine learning-based analysis
- Interactive Streamlit dashboard
- Simple login and admin panel
- Clean and structured UI
- Fast real-time prediction

---

## Tech Stack
- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Pickle

---

## Project Structure
AI-Powered-Crop-Monitoring-System/
│
├── app.py
├── admin_panel.py
├── pages/
│   ├── login.py
│   ├── dashboard.py
│   └── admin_panel.py
│
├── datasets/
│   └── soil_data.csv
│
├── models/
│   └── trained_model.pkl
│
├── assets/
├── requirements.txt
└── README.md

---

## How to Run

### 1. Clone the repository
git clone https://github.com/your-username/AI-Powered-Crop-Monitoring-System.git
cd AI-Powered-Crop-Monitoring-System

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   (Windows)

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run the app
streamlit run app.py

---

## How It Works
- User enters soil values
- ML model processes input
- System predicts soil condition
- Result is displayed in dashboard

---

## Future Improvements
- Weather API integration
- Crop disease detection using CNN
- IoT sensor integration
- Fertilizer recommendation system
- Mobile version

---

## Author
Thangalakshmi A  
B.E CSE (AI & ML)  
GitHub: thangalakshmi-18
