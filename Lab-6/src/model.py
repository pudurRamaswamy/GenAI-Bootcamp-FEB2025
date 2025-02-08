import streamlit as st
import os
from io import StringIO
from langchain_experimental.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
import pandas as pd

def vectorstore(uploaded_file, vAR_api_key):   
    uploaded_file.seek(0)  # Reset pointer before reading
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8")  # Read for display only
    except Exception:
        df = pd.read_csv(uploaded_file, encoding="ISO-8859-1")  # Fallback encoding

    if df.empty:
        st.error("The uploaded CSV file is empty or improperly formatted.")
    else:
        pass
        # st.dataframe(df.head())  # Show first few rows

        # Reset file pointer AGAIN before passing to agent
        uploaded_file.seek(0)
        # Create CSV Agent
        agent = create_csv_agent(
            ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=vAR_api_key),
            uploaded_file,  # Pass the in-memory file object
            verbose=True,
            allow_dangerous_code=True
        )    
        return agent

    # Chat Interface
def get_response(query, agent):
    response = agent.run(query)
    return response