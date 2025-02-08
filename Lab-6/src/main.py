import streamlit as st
from streamlit_chat import message
from src.validate import validate_openai_key
from src.chat_interface import text_based
from src.model import vectorstore
import pandas as pd
import openai
import os

# Streamlit app main function
def main_ui():
    col1, col2, col3, col4 = st.columns((1, 3, 3.5, 2.5))
    c1, c2, c3 = st.columns((1, 6.5, 2.5))

    with col2:
        st.write('## ')
        st.write("### ")
        st.markdown(
            "<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Enter OpenAI API Key</span></p>", 
            unsafe_allow_html=True
        )
    with col3:
        st.write("### ")
        vAR_api_key = st.text_input(" ", type="password")

    if vAR_api_key:
        with col4:
            message = validate_openai_key(vAR_api_key)
            if "Invalid" in message:
                st.write("### ")
                st.write("### ")
                st.warning(message)
            else:
                st.write("### ")
                st.write("### ")
                st.success(message)
        if message == "Valid API Key!":
            with col2:
                st.write('## ')
                st.write("### ")
                st.markdown(
                    "<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Upload KnowledgeBase</span></p>", 
                    unsafe_allow_html=True
                )
            with col3:
                st.write("### ")
                uploaded_file  = st.file_uploader("", type='csv', key="fileupload")
            if uploaded_file:
                vAR_DB=vectorstore(uploaded_file, vAR_api_key)
                text_based(vAR_api_key, vAR_DB)
           
        
