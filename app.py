# Crop Recommendation System - Streamlit App
import numpy as np
import pickle
from sklearn import svm
import streamlit as st
import os
import time

# Basic Streamlit configuration for Cloud Run
st.set_page_config(
    page_title="Crop Recommendation System",
    page_icon="🌱",
    layout="wide"
)

# Path to the pre-trained model
MODEL_PATH = 'models/pickle_model.pkl'

# Function to make predictions with the model
def model_prediction(x_in, model):
    x = np.asarray(x_in).reshape(1,-1)
    preds = model.predict(x)
    return preds

# Health check endpoint using query parameters
def check_health():
    # If there's a healthz parameter, return simple response
    if st.experimental_get_query_params().get("healthz"):
        st.write("ok")
        st.stop()

def main():
    # Check health first
    check_health()
    
    model = ''

    # Load the model
    if model == '':
        with open(MODEL_PATH, 'rb') as file:
            model = pickle.load(file)
    
    # Title
    html_temp = """
    <h1 style="color:#181082;text-align:center;">CROP RECOMMENDATION SYSTEM</h1>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)

    # Data input
    N = st.text_input("Nitrogen:")
    P = st.text_input("Phosphorus:")
    K = st.text_input("Potassium:")
    Temp = st.text_input("Temperature:")
    Hum = st.text_input("Humidity:")
    pH = st.text_input("pH:")
    rain = st.text_input("Rainfall:")
    
    # Prediction button to start processing
    if st.button("Predict:"): 
        x_in = [np.float_(N.title()),
                np.float_(P.title()),
                np.float_(K.title()),
                np.float_(Temp.title()),
                np.float_(Hum.title()),
                np.float_(pH.title()),
                np.float_(rain.title())]
        predictS = model_prediction(x_in, model)
        st.success('RECOMMENDED CROP: {}'.format(predictS[0]).upper())

if __name__ == '__main__':
    main()
