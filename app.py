import streamlit as st
import pandas as pd

# Backend logic
def process_excel(file, threshold):
    df_yoga = pd.read_excel(file)
    df_yoga = df_yoga[['Name', 'No of months attended']]
    df_yoga['Call_Flag'] = df_yoga['No of months attended'].apply(lambda x: 'Call' if x > threshold else 'No Call')
    to_call = df_yoga[df_yoga['Call_Flag'] == 'Call'].sort_values('No of months attended')
    no_call = df_yoga[df_yoga['Call_Flag'] == 'No Call'].sort_values('No of months attended')
    return to_call[['Name', 'No of months attended']], no_call[['Name', 'No of months attended']]

# Streamlit app
st.title("Yoga Attendance Analyzer")

# File upload
uploaded_file = st.file_uploader("Upload Excel File (Return to Yoga-2.xlsx)", type=["xlsx"])

# Threshold input
threshold = st.number_input("Threshold (Months)", min_value=0.0, step=0.1, value=3.0)

if uploaded_file is not None:
    try:
        # Process the file
        to_call, no_call = process_excel(uploaded_file, threshold)
        
        # Display results
        st.subheader(f"Results (Threshold: {threshold} months)")
        
        # To Call list
        st.write(f"**To Call (>{threshold} months):** {len(to_call)} individuals")
        if not to_call.empty:
            st.dataframe(to_call)
        else:
            st.write("No one to call.")
        
        # Not to Call list
        st.write(f"**Not to Call (≤{threshold} months):** {len(no_call)} individuals")
        if not no_call.empty:
            st.dataframe(no_call)
        else:
            st.write("No one not to call.")
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.info("Please upload an Excel file to proceed.")
