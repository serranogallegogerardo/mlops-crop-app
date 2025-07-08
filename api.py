#!/usr/bin/env python3
"""
API endpoint for Crop Recommendation Model
This file provides a REST API interface for the ML model
"""

import numpy as np
import pickle
import json
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Path to the pre-trained model
MODEL_PATH = 'models/pickle_model.pkl'

# Load the model globally
try:
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
    print(f"✅ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

def model_prediction(x_in, model):
    """Make predictions with the model"""
    x = np.asarray(x_in).reshape(1,-1)
    preds = model.predict(x)
    return preds

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "model_loaded": model is not None})

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Prediction endpoint"""
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
    
    try:
        # Get parameters from query string (GET) or JSON body (POST)
        if request.method == 'GET':
            N = float(request.args.get('n', 0))
            P = float(request.args.get('p', 0))
            K = float(request.args.get('k', 0))
            Temp = float(request.args.get('temp', 0))
            Hum = float(request.args.get('hum', 0))
            pH = float(request.args.get('ph', 0))
            rain = float(request.args.get('rain', 0))
        else:  # POST
            data = request.get_json()
            N = float(data.get('n', 0))
            P = float(data.get('p', 0))
            K = float(data.get('k', 0))
            Temp = float(data.get('temp', 0))
            Hum = float(data.get('hum', 0))
            pH = float(data.get('ph', 0))
            rain = float(data.get('rain', 0))
        
        # Validate input parameters
        if any(val == 0 for val in [N, P, K, Temp, Hum, pH, rain]):
            return jsonify({
                "error": "Missing or invalid parameters",
                "required_params": ["n", "p", "k", "temp", "hum", "ph", "rain"],
                "example": "?n=90&p=45&k=60&temp=20&hum=80&ph=6.5&rain=120"
            }), 400
        
        # Make prediction
        x_in = [N, P, K, Temp, Hum, pH, rain]
        prediction = model_prediction(x_in, model)[0]
        
        # Return JSON response
        return jsonify({
            "status": "success",
            "recommended_crop": prediction.upper(),
            "input_parameters": {
                "nitrogen": N,
                "phosphorus": P,
                "potassium": K,
                "temperature": Temp,
                "humidity": Hum,
                "ph": pH,
                "rainfall": rain
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Invalid input parameters"
        }), 400

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API documentation"""
    return jsonify({
        "message": "Crop Recommendation API",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "documentation": {
                "GET /predict": "Use query parameters: n, p, k, temp, hum, ph, rain",
                "POST /predict": "Send JSON body with parameters: n, p, k, temp, hum, ph, rain",
                "example": "GET /predict?n=90&p=45&k=60&temp=20&hum=80&ph=6.5&rain=120"
            }
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False) 