import streamlit as st
from __init__ import tts_norm
title = st.text_input('text normalizer', 'input text')
st.write(tts_norm(title))