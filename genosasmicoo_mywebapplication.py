import streamlit as st

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "About"])

if page == "Home":
    st.title("Home Page")
    st.write("Main functionality goes here.")

elif page == "About":
    st.title("About This App")
    st.write("""
    *Use-case:* Example app for class project.
    *Target user:* Students learning Streamlit.
    *Inputs:* User text, numbers, selections.
    *Outputs:* Displayed results and visualizations.
    """)