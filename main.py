import streamlit as st
import os
import json
from os.path import splitext
#import SessionState
from plyer import notification
import psycopg2
from Levenshtein import distance
from nltk.translate.bleu_score import sentence_bleu
import datetime

st.set_page_config(layout="wide")
@st.cache
def get_file_list():
    my_file = open("paintings/images/file_list.txt", "r")
    content = my_file.read()
    fl = content.split("\n")    
    return fl
def rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))
#state = SessionState.get(n = 0,start_time = datetime.datetime.now().time().strftime('%H:%M:%S'))
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.datetime.now().time().strftime('%H:%M:%S')
if 'n' not in st.session_state:
    st.session_state.n=0
if 'annotation_key' not in st.session_state:
    st.session_state.annotation_key=1
name = st.sidebar.text_input("Input your name and press Enter please:","")
DATABASE_URL = os.environ['DATABASE_URL']
if (name!=''):
    con = psycopg2.connect(DATABASE_URL)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS annotations (id serial PRIMARY KEY, name varchar, file varchar, annotation text, track_time interval);")
    #st.sidebar.markdown("** Attention! ** Before closing the app please close connection with database")
    #work_dir = "./paintings/"+name+"/"
    #if not os.path.exists(work_dir):
     #   os.mkdir(work_dir)  
    #download_data(name,work_dir,sec_key,sec_host,sec_user,sec_pas)
    file_list = get_file_list()
    try:
        image_name = file_list[st.session_state.n]
    except: 
        st.session_state.n = 0
        image_name = file_list[st.session_state.n]
    
    cur.execute("SELECT annotation FROM annotations WHERE name=%s AND file=%s",(name,image_name))
    record = cur.fetchall()
    if len(record)==0:
        f_n = "** File name: **" + image_name
    else:
        f_n = "** File name: **" + image_name + ";* Already annotated *"
    col1,col2 = st.columns(2)
    col1.markdown('# Image')
    col1.markdown(f_n)
    col1.image("./paintings/images/"+image_name)
    with open("./paintings/descriptions/"+os.path.splitext(image_name)[0]+'.json','r') as json_file:
        meta_data = json.load(json_file)
    col2.markdown('# Annotation')
    #col2.markdown("** Original caption: **"+meta_data["annot"])
    #col2.markdown("** Provided caption: **"+provided_des)
    anno_place = col2.empty()
    #value = " "
    annotation = anno_place.text_area("Input annotation:", height=100, key=chr(st.session_state.annotation_key))
    if annotation:
        #if meta_data["annot"]!="nan":
        #    col2.markdown(" ** BLEU Score: **"+str(sentence_bleu([meta_data["annot"].split(" ")],annotation.split(" "))))
        #    col2.markdown(" ** Levenshtein distance: **"+str(distance(meta_data["annot"],annotation)))
        anno_place.empty()
        col2.markdown("** Saved caption: **"+annotation)
    if col2.button("I like it! Save! "):   
        #print(image_name)
        #print(annotation)
        #value = " "
        end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        total_time=(datetime.datetime.strptime(end_time,'%H:%M:%S') - datetime.datetime.strptime(st.session_state.start_time,'%H:%M:%S'))
        annot = {"File":image_name}
        annot[name]=annotation
        cur.execute("INSERT INTO annotations (name, file, annotation, track_time) VALUES (%s, %s, %s, %s)",(name, image_name, annotation,total_time))
        con.commit()
        #with open(work_dir+os.path.splitext(image_name)[0]+'.json', 'w') as json_file:
            #json.dump(annot, json_file)
        st.session_state.start_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    if col2.button("Next image"):
        st.session_state.annotation_key=st.session_state.annotation_key+1
        st.session_state.n=st.session_state.n+1
        if st.session_state.n == 92:
            st.session_state.n = 0
        rerun() 
    if col2.button("Previous image"):
        st.session_state.annotation_key=st.session_state.annotation_key+1
        st.session_state.n=st.session_state.n-1
        if st.session_state.n == -1:
            st.session_state.n = 91
        rerun()
    #if st.sidebar.button("Close connection"):
        
        #st.sidebar.write("Connection is closed")
    #col2.markdown('''<p style='text-align: justify;'>The BLEU score compares a sentence against one or more reference sentences and tells how well does the 
    #                candidate sentence matched the list of reference sentences. It gives an output score between 0 and 1. A BLEU score of 1 means that the 
    #                candidate sentence perfectly matches one of the reference sentences. <br><br>
    #                The distance value describes the minimal number of deletions, insertions, or substitutions that are required to transform one string (the source) 
    #                into another (the target).The greater the Levenshtein distance, the greater is the difference between the strings. 
    #                </p>''',unsafe_allow_html=True)
    con.commit()
    cur.close()
    con.close()
