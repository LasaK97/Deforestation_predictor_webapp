import streamlit as st
import base64
import pickle
import numpy as np 
import pandas as pd

st.set_page_config(page_title= 'Deforestation Predictor ', layout="wide")

with open('./static/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("<h1 class = 'title'>DETECTION OF DEFORESTATION USING SATELLITE IMAGES IN SRI LANKA</h1>",unsafe_allow_html=True)
st.markdown("<hr style = 'color:red;'>",unsafe_allow_html=True) 

# set background
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64('./background/back.jpg')
page_bg_img = f"""
    <style> 
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
    }}
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0)
    }}
    [data-testid="stToolbar"] {{
        right: 2rem;
    }}
    
"""

# loading model
st.markdown(page_bg_img, unsafe_allow_html=True)

with open('./model/model.pickle', 'rb') as file:
    loaded_model = pickle.load(file)


box = st.container()
with box:
    c1, c2 = st.columns([2, 1])

    with c1:
        st.header("Information")
        st.write("Horowpathana National Park, located in Sri Lanka, is a critical natural habitat that plays a vital role in preserving the country's biodiversity. Identifying the deforestation percentage within this national park is crucial for understanding the level of ecological damage and the potential effects for its ecosystem. Through  satellite imagery analysis and Normalized Difference Vegetation Index(NDVI) Calculation, Here we are working  to determine the exact percentage of deforestation in Horowpathana National Park. ")
    with c2:
        st.markdown('<p style="font-size:30px; color: #90EE90; font-weight:bold;">Predicted Future Deforestation</p>', unsafe_allow_html=True)
        # Accept user input for a specific date
        specific_date_str = st.date_input("Enter the specific date (YYYY-MM-DD): ", max_value = pd.to_datetime("2100-01-01"))
        specific_date = pd.to_datetime(specific_date_str)

        # Extract the day of the year for the specific date
        day_of_year = specific_date.dayofyear

        # Predict deforestation percentage for the specific date using Random Forest
        new_data_rf = pd.DataFrame({'day_of_year': [day_of_year]})
        new_deforestation_percentage = loaded_model.predict(new_data_rf)[0]


      
        st.write("Predicted deforestation percentage for "+str(specific_date)[:11]+" is ")
        st.header(str(np.round(new_deforestation_percentage, 2)) + " %")
