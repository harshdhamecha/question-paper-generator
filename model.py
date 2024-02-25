from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai


def load_model():

    genai.configure(api_key = "AIzaSyBvteFupAmebDnz5ZacjeQcZzVLKzlgDXk")

    return genai.GenerativeModel("gemini-pro")


def get_output(question):
    model = load_model()
    response = model.generate_content(contents=question)
    return response.text
