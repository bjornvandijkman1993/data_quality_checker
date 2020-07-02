import streamlit as st
from Layout import utils

def intro_page():
    # Uploader widget

    TRELLO_LINK = (
        "https://trello.com/b/Gh80k24M/outlier-detection"
    )

    BITBUCKET_LINK = (
        "https://bitbucket.org/bvandijkman/data_quality_checker/src/master/"
    )

    ### introductory text

    st.markdown(
        body=utils.generate_html(text=f"Data Quality Checker", bold=True, tag="h1"),
        unsafe_allow_html=True,
    )
    st.markdown(
        body=utils.generate_html(
            tag="h2",
            text="A tool that checks the quality of your dataset.<br>",
        ),
        unsafe_allow_html=True,
    )


    st.markdown(
        body=utils.generate_html(
            tag="h4",
            text=f"<u><a href=\"{BITBUCKET_LINK}\" target=\"_blank\" style=color:{utils.COLOR_MAP['pink']};>"
                 "Source Code</a></u> <span> &nbsp;&nbsp;&nbsp;&nbsp</span>"
                 f"<u><a href=\"{TRELLO_LINK}\" target=\"_blank\" style=color:{utils.COLOR_MAP['pink']};>"
                 "Trello Board</a></u> <span> &nbsp;&nbsp;&nbsp;&nbsp</span>"
                 "<hr>",
        ),
        unsafe_allow_html=True,
    )

    st.markdown("""
    This tool checks and visualizes any excel or csv file that you upload, which makes it a great way to get 
    quickly get a sense of the data that you are dealing with. 
    
    👈 **Please _upload a csv or excel file_ in the sidebar to start.**
    """)

    return

