import streamlit as st
from en_norm.__init__ import tts_norm
form = st.form(key = 'my_form')
text_input = form.text_input(label = 'input text here')
submit_button = form.form_submit_button(label = 'submit')
form2 = st.form(key = 'my_form2')
text_input2 = form2.text_input(label = 'keep punctuation? input \'True\' or \'False\'')
submit_button2 = form2.form_submit_button(label = 'submit')
if submit_button and submit_button2:
    st.write(tts_norm(text_input, bool(text_input2)))