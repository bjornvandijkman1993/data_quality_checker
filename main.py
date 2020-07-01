import streamlit as st
import pandas as pd

# import functions from external python scripts
from layout import hide_header_footer
from layout import max_width
from layout import create_space
from layout import utils

# helper functions
from helper_functions import load_file

import first_look_data
from text_app import text_markdown


def main():

    # increases the width of the text and tables/figures
    max_width._max_width_()

    # hide the footer and optionally the streamlit menu in the topright corner which is unrelated to our app
    hide_header_footer.hide_header_footer()

    # show the intro page
    text_markdown.intro_page()

    # load the data, currently allows for csv and excel imports
    filename = []
    if not filename:
        st.sidebar.title(":floppy_disk: Upload Your File")
        filename = st.sidebar.file_uploader("Choose a file", type=['xlsx', 'csv'])
        df = pd.read_excel("data/titanic.xlsx")
    if filename:

        # Load File:
        # - Loads excel and csv files.
        # - Automatically detects which delimiter is used
        # - Ignores columns that contain more than 80% of missing values

        df = load_file.load_file(filename)
        # if a df has been loaded, meaning it has more than 1 row

    if len(df) != 0:

        # space between sections
        create_space.betweensection_space()

        options = ['EDA', 'ML']
        st.sidebar.title(":car: Navigation")
        choice_page = st.sidebar.radio('Which page do you want to navigate to?', options)

        st.sidebar.markdown(" ")
        st.sidebar.markdown(" ")
        st.sidebar.markdown(" ")
        st.sidebar.markdown("---")
        st.sidebar.markdown(" ")

        if choice_page == 'EDA':
            first_look_data.exploratory_data_analysis(df)
        elif choice_page == 'ML':
            st.title("Hello World")




            # if st.checkbox("Continue to preprocessing"):
            #     create_space.betweensection_space()
            #
            #     preprocessed_df = preprocessing.preprocess(df)
            #
            #     if st.checkbox("Continue to log transformations"):
            #         create_space.betweensection_space()
            #         st.title(":twisted_rightwards_arrows: Log Transformations")
            #         transformed_df = data_transformations.data_transformations(preprocessed_df)
            #         st.success("**If you are ready to do the outlier detection then click on the checkbox below.**")
            #
            #         if len(transformed_df) != 0 and st.checkbox("Continue to modelling"):
            #             create_space.betweensection_space()
            #             try:
            #                 outcome, outlier_choice, counts = quick_detection.outlier_detection(raw_df, transformed_df)
            #
            #                 create_space.betweensection_space()
            #
            #                 # show the results of the analysis if they have been done
            #                 if len(outcome) != 0:
            #                     results.results_section(outcome, counts, outlier_choice, name_project)
            #             except ValueError as e:
            #                 st.error(e)
            #                 # st.error("The data contains **missing values**, you can impute them during "
            #                 #          "the preprocessing step or exclude the column from the analysis.")

    # bottom line and github logo
    st.markdown("---")

    # insert github logo
    utils.insert_github_logo()

# Run the script
if __name__ == "__main__":
    main()