# 🌱 AI-Powered-Crop-Monitoring-System

## Overview
AI-Powered-Crop-Monitoring-System is a machine learning-based web application that helps analyze soil conditions and provide smart agricultural insights. It uses Python, Streamlit, and a trained ML model to convert soil data into meaningful predictions.

---

## What This Project Does
The system takes soil parameters like Nitrogen, Phosphorus, Potassium, pH, and Moisture as input, processes them using a trained machine learning model, and predicts the soil condition. The result is displayed in a simple and interactive dashboard.

---

## Features
- Soil condition prediction (Good / Moderate / Poor)
- Machine learning-based analysis
- Interactive Streamlit dashboard
- Login and admin panel system
- Fast real-time prediction
- Clean and simple UI

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

### 4. Run the application
streamlit run app.py

---

## How It Works
1. User enters soil parameters (N, P, K, pH, moisture)
2. ML model processes the input
3. System predicts soil condition
4. Result is shown in dashboard

---

## Future Improvements
- Weather API integration
- Crop disease detection using CNN
- IoT sensor integration
- Fertilizer recommendation system
- Mobile app version

---

## Author
Thangalakshmi A  
B.E CSE (Artificial Intelligence & Machine Learning)  
GitHub: thangalakshmi-18

---

## License
This project is for educational purposes only.
