import streamlit as st
import datetime
import SessionState
st.set_page_config(layout="wide")
state = SessionState.get(start_time = datetime.datetime.now().time().strftime('%H:%M:%S'))
if st.button("Show time"):
    end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    total_time=(datetime.datetime.strptime(end_time,'%H:%M:%S') - datetime.datetime.strptime(state.start_time,'%H:%M:%S'))
    st.write(state.start_time)
    st.write(end_time)
    st.write(total_time)
    state.start_time = datetime.datetime.now().time().strftime('%H:%M:%S')