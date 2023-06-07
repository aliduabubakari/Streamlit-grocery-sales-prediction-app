import pandas as pd
import streamlit as st
import numpy as np
from matplotlib import pyplot as plt
import pickle
import sklearn
import joblib
from PIL import Image
import base64


num_imputer = joblib.load('numerical_imputer.joblib')
cat_imputer = joblib.load('categorical_imputer.joblib')
encoder = joblib.load('encoder.joblib')
scaler = joblib.load('scaler.joblib')
dt_model = joblib.load('Final_model.joblib')

# Add a title and subtitle
st.write("<center><h1>Sales Prediction App</h1></center>", unsafe_allow_html=True)

#image = Image.open("grocery_shopping_woman.png")

# Display the image
#st.image(image, width=600)

# Load the image
image = Image.open("grocery_shopping_woman.png")

# Set up the layout
col1, col2, col3 = st.columns([1, 3, 3])
col2.image(image, width=600)


#st.image("https://www.example.com/logo.png", width=200)
# Add a subtitle or description
st.write("This app uses machine learning to predict sales based on certain input parameters. Simply enter the required information and click 'Predict' to get a sales prediction!")

st.subheader("Enter the details to predict sales")

# Add some text
#st.write("Enter some data for Prediction.")

 # Create the input fields
input_data = {}
col1,col2 = st.columns(2)
with col1:
    input_data['store_nbr'] = st.slider("store_nbr",0,54)
    input_data['products'] = st.selectbox("products", ['AUTOMOTIVE', 'CLEANING', 'BEAUTY', 'FOODS', 'STATIONERY',
       'CELEBRATION', 'GROCERY', 'HARDWARE', 'HOME', 'LADIESWEAR',
       'LAWN AND GARDEN', 'CLOTHING', 'LIQUOR,WINE,BEER', 'PET SUPPLIES'])
    input_data['onpromotion'] =st.number_input("onpromotion",step=1)
    input_data['state'] = st.selectbox("state", ['Pichincha', 'Cotopaxi', 'Chimborazo', 'Imbabura',
       'Santo Domingo de los Tsachilas', 'Bolivar', 'Pastaza',
       'Tungurahua', 'Guayas', 'Santa Elena', 'Los Rios', 'Azuay', 'Loja',
       'El Oro', 'Esmeraldas', 'Manabi'])
    input_data['store_type'] = st.selectbox("store_type",['D', 'C', 'B', 'E', 'A'])
    input_data['cluster'] = st.number_input("cluster",step=1)

with col2:
    input_data['dcoilwtico'] = st.number_input("dcoilwtico",step=1)
    input_data['year'] = st.number_input("year",step=1)
    input_data['month'] = st.slider("month",1,12)
    input_data['day'] = st.slider("day",1,31)
    input_data['dayofweek'] = st.number_input("dayofweek,0=Sun and 6=Sat",step=1)
    input_data['end_month'] = st.selectbox("end_month",['True','False'])


# Define CSS style for the download button
# Define the custom CSS
predict_button_css = """
    <style>
    .predict-button {
        background-color: #C4C4C4;
        color: gray;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        border: none;
        font-size: 1.1rem;
        font-weight: bold;
        text-align: center;
        margin-top: 2rem;
    }
    </style>
"""

download_button_css = """
    <style>
    .download-button {
        background-color: #C4C4C4;
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        border: none;
        font-size: 1.1rem;
        font-weight: bold;
        text-align: center;
        margin-top: 1rem;
    }
    </style>
"""

# Display the custom CSS
st.markdown(predict_button_css + download_button_css, unsafe_allow_html=True)


  # Create a button to make a prediction

if st.button("Predict", key="predict_button", help="Click to make a prediction."):
    # Convert the input data to a pandas DataFrame
        input_df = pd.DataFrame([input_data])


# Selecting categorical and numerical columns separately
        cat_columns = [col for col in input_df.columns if input_df[col].dtype == 'object']
        num_columns = [col for col in input_df.columns if input_df[col].dtype != 'object']


# Apply the imputers
        input_df_imputed_cat = cat_imputer.transform(input_df[cat_columns])
        input_df_imputed_num = num_imputer.transform(input_df[num_columns])


 # Encode the categorical columns
        input_encoded_df = pd.DataFrame(encoder.transform(input_df_imputed_cat).toarray(),
                                   columns=encoder.get_feature_names(cat_columns))

# Scale the numerical columns
        input_df_scaled = scaler.transform(input_df_imputed_num)
        input_scaled_df = pd.DataFrame(input_df_scaled , columns = num_columns)

#joining the cat encoded and num scaled
        final_df = pd.concat([input_encoded_df, input_scaled_df], axis=1)

# Make a prediction
        prediction = dt_model.predict(final_df)[0]


# Display the prediction
        st.write(f"The predicted sales are: {prediction}.")
        input_df.to_csv("data.csv", index=False)
        st.table(input_df)

# Define custom CSS
css = """
table {
    background-color: #f2f2f2;
    color: #333333;
}
"""

# Set custom CSS
st.write(f'<style>{css}</style>', unsafe_allow_html=True)


# Add the download button
def download_csv():
    with open("data.csv", "r") as f:
        csv = f.read()
    b64 = base64.b64encode(csv.encode()).decode()
    button = f'<button class="download-button"><a href="data:file/csv;base64,{b64}" download="data.csv">Download Data CSV</a></button>'
    return button

st.markdown(
    f'<div style="text-align: center">{download_csv()}</div>',
    unsafe_allow_html=True
)
