import streamlit as st
import os
import json
from os.path import splitext
import SessionState
from plyer import notification
import psycopg2
from Levenshtein import distance
from nltk.translate.bleu_score import sentence_bleu
st.set_page_config(layout="wide")
state = SessionState.get(n = 0, file_list=os.listdir("./paintings/images/"))
name = st.sidebar.text_input("Input your name and press Enter please:","")
DATABASE_URL = os.environ['DATABASE_URL']
if (name!=''):
    con = psycopg2.connect(DATABASE_URL)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS annotations (id serial PRIMARY KEY, name varchar, file varchar, annotation varchar);")
    st.sidebar.markdown("** Attention! ** Before closing the app please close connection with database")
    work_dir = "./paintings/"+name+"/"
    if not os.path.exists(work_dir):
        os.mkdir(work_dir)  
    #download_data(name,work_dir,sec_key,sec_host,sec_user,sec_pas)
    try:
        image_name = state.file_list[state.n]
    except: 
        state.n = 0
        image_name = state.file_list[state.n]
    
    cur.execute("SELECT annotation FROM annotations WHERE name=%s AND file=%s",(name,image_name))
    record = cur.fetchall()
    print(record)
    if len(record)==0:
        provided_des = "None"
    else:
        provided_des = ""
        for i in record:
            provided_des=provided_des+i[0]+";"
    col1,col2 = st.beta_columns(2)
    col1.markdown('# Image')
    col1.markdown("** File name: **" + image_name)
    col1.image("./paintings/images/"+image_name)
    
    with open("./paintings/descriptions/"+os.path.splitext(image_name)[0]+'.json','r') as json_file:
        meta_data = json.load(json_file)
    
    col2.markdown('# Annotation')
    #col2.markdown("** Original caption: **"+meta_data["annot"])
    col2.markdown("** Provided caption: **"+provided_des)
    
    annotation = col2.text_input("Input annotation:")
    if annotation:
        col2.markdown(" ** BLEU Score: **"+str(sentence_bleu([meta_data["annot"].split(" ")],annotation.split(" "))))
        col2.markdown(" ** Levenshtein distance: **"+str(distance(meta_data["annot"],annotation)))
    if col2.button("I like it! Save! "):   
        print(image_name)
        print(annotation)
        
        annot = {"File":image_name}
        annot[name]=annotation
        cur.execute("INSERT INTO annotations (name, file, annotation) VALUES (%s, %s, %s)",(name, image_name, annotation))
        con.commit()
        #with open(work_dir+os.path.splitext(image_name)[0]+'.json', 'w') as json_file:
            #json.dump(annot, json_file)
        
    if col2.button("Next image",key = state.n):
        state.n=state.n+1
    if col2.button("Previous image",key = state.n):
        state.n=state.n-1
    #if st.sidebar.button("Close connection"):
        
        #st.sidebar.write("Connection is closed")
    col2.markdown('''<p style='text-align: justify;'>The BLEU score compares a sentence against one or more reference sentences and tells how well does the 
                    candidate sentence matched the list of reference sentences. It gives an output score between 0 and 1. A BLEU score of 1 means that the 
                    candidate sentence perfectly matches one of the reference sentences. <br><br>
                    The distance value describes the minimal number of deletions, insertions, or substitutions that are required to transform one string (the source) 
                    into another (the target).The greater the Levenshtein distance, the greater are the difference between the strings. 
                    <b> Please take into account that not of all images have original captions. It means that for some images BLEU score will be equal to 0 and Levenshtein distance will be relatively high</b</p>''',unsafe_allow_html=True)
    con.commit()
    cur.close()
    con.close()
