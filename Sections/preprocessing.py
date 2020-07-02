import streamlit as st
import helpers
from Text import text_markdown


def preprocess(df):
    """
    Gives different preprocessing Suggestions based on the input dataframe
    """

    # Call function to see if any data is missing
    (
        missing_values,
        only_missings_df,
        percent_missing,
        missing_values_names,
    ) = helpers.get_missing_values(df)

    still_missing, messages, type = helpers.is_data_missing(df, percent_missing)

    st.title("Missing Value Considerations")

    # not sure about this
    if len(still_missing) != 0:
        # st.info(is_missing)
        for message, type in zip(messages, type):
            if type == "drop":
                st.warning(message)
            elif type == "impute":
                st.info(message)
    else:
        st.info(messages)

    if st.checkbox("Show me different imputation options"):
        text_markdown.missings_recommendation()

    return
