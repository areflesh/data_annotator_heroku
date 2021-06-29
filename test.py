import streamlit as st
st.set_page_config(layout="wide")
col1,col2 = st.beta_columns(2)
place = col2.empty()
col1.text("sign")
place.text("sign")