import streamlit as st
from en_norm.__init__ import tts_norm
form = st.form(key = 'my_form')
text_input = form.text_input(label = 'input text here')
submit_button = form.form_submit_button(label = 'submit')
st.write(tts_norm(text_input, True))