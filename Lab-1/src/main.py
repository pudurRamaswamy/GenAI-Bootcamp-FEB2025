import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
# Load environment variables
load_dotenv()

# Streamlit app main function
def main():

    col1, col2, col3, col4 = st.columns((1, 3, 3.5, 2.5))
    c1, c2, c3 = st.columns((1, 6.5, 2.5))

    with col2:
        st.write('# ')
        st.write("# ")
        st.markdown(
            "<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>File Upload</span></p>", 
            unsafe_allow_html=True
        )

    with col3:
        st.write("### ")
        vAR_fileinput = st.file_uploader("Upload a CSV or Excel file", type=['csv', 'xlsx'])

    if vAR_fileinput:
        try:
            # Determine file type and read the data
            if vAR_fileinput.name.endswith('.csv'):
                data = pd.read_csv(vAR_fileinput)
            elif vAR_fileinput.name.endswith('.xlsx'):
                data = pd.read_excel(vAR_fileinput, engine='openpyxl')
            else:
                st.error("Unsupported file format. Please upload a CSV or Excel file.")
                return

            with col3:
                if st.button("Preview Data"):
                    with c2:
                        st.dataframe(data)

        except Exception as e:
            st.error(f"Error reading file: {e}")


        