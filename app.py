# This is a test comment to trigger the CI/CD pipeline (English)

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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS to block external emoji loading and reduce spam
def load_custom_css():
    with open('assets/custom.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load custom CSS
load_custom_css()

# Additional inline CSS for immediate effect
st.markdown("""
<style>
    /* Block external emoji CDN requests immediately */
    img[src*="twemoji.maxcdn.com"] { display: none !important; }
    img[src*="emoji-cdn"] { display: none !important; }
    .stEmoji { display: none !important; }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
</style>
""", unsafe_allow_html=True)

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
