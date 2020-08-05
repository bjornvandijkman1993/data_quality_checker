import streamlit as st
import pandas as pd

# import functions from external python scripts
from Text import text_markdown

# helper functions
import helpers

# The different sections
from Sections import eda
from Sections import preprocessing


def main():
    st.set_option('deprecation.showfileUploaderEncoding', False)

    def _max_width_():
        max_width_str = f"max-width: 1000px;"
        st.markdown(
            f"""
        <style>
        .reportview-container .main .block-container{{
            {max_width_str}
        }}
        </style>
        """,
            unsafe_allow_html=True,
        )

    # Hide the Streamlit header and footer
    def hide_header_footer():
        hide_streamlit_style = """
                    <style>
                    footer {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)


    # increases the width of the text and tables/figures
    _max_width_()

    # hide the footer and optionally the streamlit menu in the topright corner which is unrelated to our app
    hide_header_footer()

    # show the intro page
    text_markdown.intro_page()

    # load the data, currently allows for csv and excel imports
    st.sidebar.title(":floppy_disk: Upload Your File")
    filename = st.sidebar.file_uploader("Choose a file", type=["xlsx", "csv"])

    delim = st.sidebar.selectbox(
        "In case of a CSV file, pick the delimiter.", [",", ";", "|"]
    )

    if filename:

        df = helpers.load_file(filename, delim)

    else:
        df = pd.read_excel("titanic.xlsx")

    # space between sections
    helpers.betweensection_space()
    helpers.sidebar_space()


    # Ensures navigation between pages
    df = eda.first_inspection(df)
    eda.visuals(df)
    helpers.betweensection_space()
    helpers.sidebar_space()
    preprocessing.preprocess(df)

    # bottom line and github logo
    st.markdown("---")


if __name__ == "__main__":
    main()
