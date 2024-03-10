import google.generativeai as genai


def load_model():

    genai.configure(api_key = "AIzaSyBvoBZV6Nk8UpHbRUe2tvx4bFz-CGOBT5E")

    return genai.GenerativeModel("gemini-pro")


def get_output(question):
    model = load_model()
    response = model.generate_content(contents=question)
    return response.text
