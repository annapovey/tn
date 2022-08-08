import streamlit as st
import logging
from en_norm.__init__ import tts_norm

logging.basicConfig(filename = 'maininfo.log', level = logging.INFO, format = '%(asctime)s:%(levelname)s:%(message)s')
st.header("Text Normalization for ASR")
st.caption("Mimicks LibriSpeech text normalization \n - numbers to words \n - CNN -> C N N \n - removes punctuation \n -  smimicks speech for dates")
form = st.form(key = 'my_form')
text_input = form.text_input(label = 'input text here')
form.caption("example: $3.9 billion -> three point nine billion dollars")
cb1 = form.checkbox("keep punctuation")
cb2 = form.checkbox("make text uppercase")
cb3 = form.checkbox("remove non-asci characters")
submit_button = form.form_submit_button(label = 'submit')
# form2 = st.form(key = 'my_form2')
# text_input2 = form2.text_input(label = 'keep punctuation? input \'True\' or \'False\'')
# submit_button2 = form2.form_submit_button(label = 'submit')
# if submit_button and submit_button2:
try:
    st.write(tts_norm(text_input, cb1, cb2))
except:
    logging.info(text_input)
# container = st.container()
# container.caption("Mimicks libri speech text normalization")