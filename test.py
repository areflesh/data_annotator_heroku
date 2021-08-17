import streamlit as st
import datetime
import random
st.set_page_config(layout="wide")
key_list=random.sample(range(10, 30), 3)
while len(set(key_list))!=3:
    key_list=random.sample(range(10, 30), 3)
st.write(key_list)
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.datetime.now().time().strftime('%H:%M:%S')
if st.button("Show time"):
    end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    total_time=(datetime.datetime.strptime(end_time,'%H:%M:%S') - datetime.datetime.strptime(st.session_state.start_time,'%H:%M:%S'))
    st.write(st.session_state.start_time)
    st.write(end_time)
    st.write(total_time)
    st.session_state.start_time = datetime.datetime.now().time().strftime('%H:%M:%S')