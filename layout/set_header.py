import streamlit as st

def header():
    st.write('<style>body { margin: 0; font-family: Arial, Helvetica, sans-serif;} '
             '.header{padding: 10px 16px; background: lightblue; color: black; position:fixed;top:0;} '
             '.sticky { position: fixed; top: 0; width: 100%;} </style><div class="header" id="myHeader">' +
             str("This is the header") + '</div>', unsafe_allow_html=True)