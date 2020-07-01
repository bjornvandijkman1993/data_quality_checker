import pandas as pd
import streamlit as st

@st.cache(show_spinner=False)
def get_unique_values(df):
    # show number of unique values for each variable
    unique_values = df.apply(pd.Series.nunique).to_frame('Unique Values').iloc[:, 0]
    return unique_values

@st.cache(show_spinner = False)
def get_type_variables(df):
    # the type for each variable
    data_types = df.dtypes.to_frame('Variable Type')
    return data_types

@st.cache(show_spinner = False)
def get_zero_values(df):
    zero_values = df.isin([0]).sum()
    zero_values = zero_values.to_frame()
    zero_values.columns = ['Zero Values']
    return zero_values

@st.cache(show_spinner=False)
def get_missings(df):

    # get number of missing values for each variable
    missing_values = df.isnull().sum().to_frame('Missing Values').iloc[:, 0]

    # compute percentage of missing values
    percent_missing = (missing_values * 100 / len(df)).to_frame('Percent Missing')

    return missing_values, percent_missing

@st.cache(show_spinner=False)
def get_missing_values(df):
    """

    :param df:
    :return:

    - df with number of missing values per variable
    - a df with only the missing value columns
    - a df with the percentage of missing values
    - the names of the missing value columns

    """

    # get number of missing values for each variable
    missing_values = df.isnull().sum().to_frame('Missing Values').iloc[:, 0]

    # reset the index
    missing_values_df = missing_values.reset_index()

    # get the columns with more than 0 missing values
    only_missings_df = missing_values_df[missing_values_df['Missing Values'] > 0]

    # assign column names to dataframe
    only_missings_df.columns = ['Variable', 'Missing Values']

    # get the names of the  columns that contain missing values
    missing_values_names = only_missings_df['Variable'].tolist()

    # compute percentage of missing values
    percent_missing = (missing_values * 100 / len(df)).to_frame('Percent Missing')
    only_percent_missing = percent_missing[percent_missing['Percent Missing'] > 0.0000]

    return missing_values, only_missings_df, percent_missing, missing_values_names


@st.cache(show_spinner=False)
def summary_table(df):
    """Summary table of the data
    :param df: the input data
    :return: summary statistics table, including the unique values, missing values and data types
    """

    # show number of unique values for each variable
    unique_values = df.apply(pd.Series.nunique).to_frame('Unique Values').iloc[:, 0]

    # show the number of missing values for each variable
    missing_values = df.isnull().sum().to_frame('Missing Values').iloc[:, 0]
    missing_values_df = missing_values.reset_index()
    only_missings_df = missing_values_df[missing_values_df['Missing Values'] > 0]
    only_missings_df.columns = ['Variable', 'Missing Values']

    # get the names of the  columns that contain missing values
    missing_values_names = only_missings_df['Variable'].tolist()

    # compute percentage of missing values
    percent_missing = (missing_values*100 / len(df)).to_frame('Percent Missing')
    only_percent_missing = percent_missing[percent_missing['Percent Missing'] > 0.0000]

    # the type for each variable
    data_types = df.dtypes.to_frame('Variable Type')

    # merge the different values
    table = pd.concat([unique_values, missing_values, percent_missing, data_types], axis=1)
    zero_values = df.isin([0]).sum()
    table['0 values'] = zero_values
    table = table.round(2)
    return table, missing_values_names, only_missings_df, percent_missing

@st.cache(show_spinner=False)
def number_rows_columns(df):
    """
    :param df:
    :return: number of rows and columns of dataframe
    """
    number_rows = df.shape[0]
    number_columns = df.shape[1]
    return number_rows, number_columns

@st.cache(show_spinner=False)
def describe_table(df):
    data_characteristics = df.describe().loc[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
    return data_characteristics
