import streamlit as st

# import functions from external python scripts
from Layout import hide_header_footer
from Layout import max_width
from Layout import utils
from Text import text_markdown

# helper functions
import helpers

# The different sections
from Sections import eda
from Sections import preprocessing
from Sections import ml


def main():

    # increases the width of the text and tables/figures
    max_width._max_width_()

    # hide the footer and optionally the streamlit menu in the topright corner which is unrelated to our app
    hide_header_footer.hide_header_footer()

    # show the intro page
    text_markdown.intro_page()

    # load the data, currently allows for csv and excel imports
    st.sidebar.title(":floppy_disk: Upload Your File")
    filename = st.sidebar.file_uploader("Choose a file", type=["xlsx", "csv"])

    if filename:

        df = helpers.load_file(filename)

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
            eda.exploratory_data_analysis(df)
        elif choice_page == "Preprocessing Suggestions":
            preprocessing.preprocess(df)
        elif choice_page == "ML":
            ml.classification(df)

    # bottom line and github logo
    st.markdown("---")

    # insert github logo
    utils.insert_github_logo()


if __name__ == "__main__":
    main()
