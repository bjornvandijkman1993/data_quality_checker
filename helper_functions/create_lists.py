import pandas as pd
import streamlit as st
# Function that creates a list of all column names, just the numerical names and categorical names
@st.cache
def get_float_names(df):
    df_float = df.loc[:, df.dtypes == 'float64']
    float_names = df_float.columns.tolist()
    return float_names

@st.cache
def get_int_names(df):
    df_int = df.loc[:, df.dtypes == 'int64']
    int_names = df_int.columns.tolist()
    return int_names

@st.cache
def get_numerical_names(df):
    # Only the numerical columns
    df_int = df.loc[:, df.dtypes == 'int64']
    df_float = df.loc[:, df.dtypes == 'float64']
    int_names = df_int.columns.tolist()
    float_names = df_float.columns.tolist()
    num_names = int_names + float_names
    return num_names

@st.cache
def get_categorical_names(df):
    # Check the number of unique values per column
    unique_values = df.apply(pd.Series.nunique).to_frame('Unique Values').iloc[:, 0]

    # If the number is lower than 5, I classify it as a categorical variable, this is subjective.
    df_factors = df.loc[:, unique_values < 100]

    # Ensure that these are of type: object
    for col in df_factors:
        df[col] = df[col].astype('object')

    # convert these names to a list
    factor_names = df_factors.columns.tolist()
    return factor_names
#
@st.cache
def get_text_names(df):
     unique_values = df.apply(pd.Series.nunique).to_frame('Unique Values').iloc[:, 0]
     df_obj = df.loc[:, df.dtypes == 'object']
     nr_rows = df.shape[0]
     #if more than 10% of the data is unique the column is marked as a potential text feature.
     df_text = df_obj.loc[:, unique_values/nr_rows >= 0.10]
     return df_text.columns.tolist()



@st.cache
def get_uniqueID_names(df):
    nr_rows = df.shape[0]
    unique_values = df.apply(pd.Series.nunique).to_frame('Unique Values').iloc[:, 0]
    uniqueID_col = df.loc[:, unique_values == nr_rows]
    uniqueID_names = uniqueID_col.columns.tolist()
    #if there is no colomn with unique values, create one called 'identifier'
    if len(uniqueID_names) == 0:
        df['identifier'] = range(1, len(df) + 1)
        uniqueID_names.append('identifier')
    return uniqueID_names



@st.cache
def get_all_names(df):
    all_names = df.columns.tolist()
    return all_names

@st.cache
def get_letter_number_names(df):
    bool(re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', 'hasAlphanum123'))



