import streamlit as st
import pandas as pd
import io

from pandas.io.parsers import ParserError


def load_file(filename):
    """
    :param filename: a filename selected by the user using the uploader widget, see main.py
    :return: df: a dataframe with the loaded data

    Deletes columns that have more than 80% of missing values

    """

    # Caching function for panda dataframes
    # see https://github.com/streamlit/streamlit/issues/1180

    def hash_io(input_io):
        return input_io.getvalue(), input_io.tell()

    # Function decorator to improve speed of the app using caching
    @st.cache(hash_funcs={io.BytesIO: hash_io, io.StringIO: hash_io},
              allow_output_mutation=True)
    # Function that tries to read file as a csv
    # if selected file is not a csv file then it will load as an excel file
    def try_read_df(filename):
        try:
            comma_sep = pd.read_csv(filename, sep=',')
            number_columns = comma_sep.shape[1]
            if number_columns != 1:
                return comma_sep
            else:
                other_sep = pd.read_csv(filename, sep=';')
                st.write(other_sep)
                return other_sep

        except (UnicodeDecodeError, ParserError):
            return pd.read_excel(filename)

    # if a filename is found, then read it using the function above
    if filename:
        # df = try_read_df(filename)
        df = try_read_df(filename)
        if len(df) != 0:
            st.sidebar.success("**The file has been loaded.**")


    return df