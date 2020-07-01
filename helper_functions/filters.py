import streamlit as st

@st.cache(show_spinner=False)
def delete_row(df, column, value):
    """
    :return: completely drops the rows, cannot be retrieved without reloading orginal data
    """
    df.drop(df.loc[df[column] == value].index, inplace=True)
    return df

@st.cache
def delete_str_contains(df, column, value):
    new_df = df[~df[column].str.contains(value, na=False)]
    filtered_out = len(df) - len(new_df)
    return new_df, filtered_out

