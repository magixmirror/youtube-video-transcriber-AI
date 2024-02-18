import google.generativeai as genai
from langchain_openai import OpenAI
from langchain_community.llms import HuggingFaceHub
import streamlit as st

def generate_text(prompt:str, model_, api_key)->str:
    genai.configure(api_key=api_key)
    try:
        if model_ == "Gemini Pro":
            model = genai.GenerativeModel('gemini-pro')
            text = model.generate_content(prompt)
            return text.text
        elif model_=="OpenAI":
            llm = OpenAI(model_name="gpt-3.5-turbo-instruct")
            return llm.invoke(prompt)
    except Exception as e:
        st.warning(e)
        st.stop()


