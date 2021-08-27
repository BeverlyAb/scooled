import psycopg2
import csv
import streamlit as st
import os

# conn = psycopg2.connect(database = st.secrets["name_of_db"],user = st.secrets["username"] ,host = st.secrets["hostname"], port=st.secrets["port_number"] ,password = st.secrets["user_password"])
conn = psycopg2.connect(database = os.environ["db"],user = os.environ["user"] ,host = os.environ["hostname"] ,password = os.environ["password"], port = os.environ["port"])
st.write("HELLO")
cur = conn.cursor()
cur.execute("USE test;")
cur.execute("SELECT * FROM test.courses WHERE name in ('ENGLISH_0');")
for i in cur:
    st.write("HI",i)
st.write(cur.execute("SHOW TABLES"))

st.stop()
