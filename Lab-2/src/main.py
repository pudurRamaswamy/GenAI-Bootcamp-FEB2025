import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Streamlit app main function
def main():
    global accuracy,model,label_encoders, scaler
    
    # Initialize only three session state variables for button clicks
    if 'train_button_clicked' not in st.session_state:
        st.session_state.train_button_clicked = False
    if 'test_button_clicked' not in st.session_state:
        st.session_state.test_button_clicked = False
    if 'predict_button_clicked' not in st.session_state:
        st.session_state.predict_button_clicked = False

    # Define column layout
    col1, col2, col3, col4 = st.columns((1, 3, 3.5, 2.5))
    c1, c2, c3 = st.columns((1, 6.5, 2.5))
    w1, col4, col5, w2 = st.columns((1, 3, 3.5, 2.5))
    w1, n1, n2, w2 = st.columns((1, 3, 3.5, 2.5))
    c1, c4, c3 = st.columns((1, 6.5, 2.5))
    w1, col6, col7, w2 = st.columns((1, 3, 3.5, 2.5))
    c1, c6, c3 = st.columns((1, 6.5, 2.5))

    # Step 1: Upload Training Data
    with col2:
        st.write("### ")
        st.write("### ")
        st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Upload Training Data</span></p>", unsafe_allow_html=True)
    
    with col3:
        train_file = st.file_uploader("", type=["csv"], key="train")

    if train_file:
        train_data = pd.read_csv(train_file)
        with c2:
            st.dataframe(train_data)
  
        with col4:
            st.write("## ")
            # st.write("### ")
            st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Select Model</span></p>", unsafe_allow_html=True)
        
        with col5:
            model_option = st.selectbox("", ["Select", "Random Forest", "Logistic Regression"], key="model_select")
            if model_option != "Select":
                st.write("")
                if st.button("Train the Model", key="train_button"):
                    train_data.fillna(train_data.median(numeric_only=True), inplace=True)
                    train_data.fillna(train_data.mode().iloc[0], inplace=True)
                    # Encode categorical variables
                    label_encoders = {}
                    for column in train_data.select_dtypes(include=['object']).columns:
                        le = LabelEncoder()
                        train_data[column] = le.fit_transform(train_data[column])
                        label_encoders[column] = le 
                    
                    # Split into features and target
                    X = train_data.drop(columns=[' loan_status'])  
                    y = train_data[' loan_status']

                    # Standardize numerical features
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)

                    # Split into training and validation sets
                    X_train, X_valid, y_train, y_valid = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

                    # Train a Random Forest Classifier
                    model = RandomForestClassifier(n_estimators=100, random_state=42)
                    model.fit(X_train, y_train)

                    # Predictions on validation set
                    y_pred = model.predict(X_valid)
                    st.success("Model Trained Successfully")
                    accuracy = accuracy_score(y_valid, y_pred)
                    st.session_state.train_button_clicked = True

    # Step 3: Upload Test Data (only appears after model training)
    if st.session_state.train_button_clicked:
        with n1:
            st.write("### ")
            st.write("### ")
            # st.write("### ")
            # st.write("### ")
            st.markdown("<p style='text-align: left; color: black; font-size:20px;'><span style='font-weight: bold'>Upload Test Data</span></p>", unsafe_allow_html=True)

        with n2:
            test_file = st.file_uploader("Upload CSV", type=["csv"], key="test")
        if test_file:
            test_data = pd.read_csv(test_file)
            with c4:
                st.subheader("Preview of Test Data")
                st.write(test_data.head())
            with col7:
                if st.button("Test the Model", key="test_button"):
                   st.session_state.test_button_clicked = True
                   st.success("Model Accuracy:"+ str(accuracy))
    
    if st.session_state.test_button_clicked:
        with col7:
            if st.button("Predict on Test Data", key="predict_button"):
                st.session_state.predict_button_clicked = True

            if st.session_state.predict_button_clicked:
                # Display predictions
                with c6:
                    for column in test_data.select_dtypes(include=['object']).columns:
                        if column in label_encoders:
                            test_data[column] = label_encoders[column].transform(test_data[column])
                    # Standardize test data
                    X_test_scaled = scaler.transform(test_data)

                    # Predict on test data
                    test_predictions = model.predict(X_test_scaled)

                    # Add predictions to the original test dataset
                    test_data['Predicted_Loan_Status'] = test_predictions

                    # Map the predictions (assuming 1 = Approved, 0 = Rejected)
                    test_data['Predicted_Loan_Status'] = test_data['Predicted_Loan_Status'].map({1: 'Approved', 0: 'Rejected'})

                    test_data.drop(columns=['loan_id'])
                    # Display the final output
                    st.dataframe(test_data)