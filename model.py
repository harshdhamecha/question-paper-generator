import google.generativeai as genai
import streamlit as st

def load_model():

    genai.configure(api_key = st.secrets['google_cloud_api_key'])

    return genai.GenerativeModel("gemini-pro")


def get_output(question):
    model = load_model()
    response = model.generate_content(contents=question)
    return response.text
