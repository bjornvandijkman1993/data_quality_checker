import streamlit as st

# import functions from external python scripts
from Text import text_markdown

# helper functions
import helpers

# The different sections
from Sections import eda
from Sections import preprocessing
from Sections import ml

st.set_option('deprecation.showfileUploaderEncoding', False)


def main():
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

        # space between sections
        helpers.betweensection_space()
        helpers.sidebar_space()

        st.sidebar.title(":car: Navigation")

        options = ["EDA", "Preprocessing Suggestions", "ML"]
        choice_page = st.sidebar.radio(
            "Which page do you want to navigate to?", options
        )

        helpers.sidebar_space()

        # Ensures navigation between pages
        if choice_page == "EDA":
            eda.first_inspection(df)
            eda.visuals(df)
        elif choice_page == "Preprocessing Suggestions":
            preprocessing.preprocess(df)

    # bottom line and github logo
    st.markdown("---")


if __name__ == "__main__":
    main()
