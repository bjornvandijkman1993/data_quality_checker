import pandas as pd
import streamlit as st
import io
from pandas.io.parsers import ParserError


def load_file(filename):
    """
    :param filename: a filename selected by the user using the uploader widget, see main.py
    :return: df: a dataframe with the loaded data
    """

    # Caching function for panda dataframes
    # see https://github.com/streamlit/streamlit/issues/1180

    def hash_io(input_io):
        return input_io.getvalue(), input_io.tell()

    # Function decorator to improve speed of the app using caching
    @st.cache(
        hash_funcs={io.BytesIO: hash_io, io.StringIO: hash_io},
        allow_output_mutation=True,
    )
    # Function that tries to read file as a csv
    # if selected file is not a csv file then it will load as an excel file
    def try_read_df(filename):
        try:
            comma_sep = pd.read_csv(filename, sep=",")
            number_columns = comma_sep.shape[1]
            if number_columns != 1:
                return comma_sep
            else:
                other_sep = pd.read_csv(filename, sep=";")
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


# Function that creates a list of all column names, just the numerical names and categorical names
def get_float_names(df):
    df_float = df.loc[:, df.dtypes == "float64"]
    float_names = df_float.columns.tolist()
    return float_names


@st.cache
def get_predictor_names(df):
    # Check the number of unique values per column
    unique_values = df.apply(pd.Series.nunique).to_frame("Unique Values").iloc[:, 0]
    df_predictors = df.loc[:, unique_values == 2]

    # convert these names to a list
    predictor_names = df_predictors.columns.tolist()
    return predictor_names


@st.cache
def get_int_names(df):
    df_int = df.loc[:, df.dtypes == "int64"]
    int_names = df_int.columns.tolist()
    return int_names


@st.cache
def get_numerical_names(df):
    # Only the numerical columns
    df_int = df.loc[:, df.dtypes == "int64"]
    df_float = df.loc[:, df.dtypes == "float64"]
    int_names = df_int.columns.tolist()
    float_names = df_float.columns.tolist()
    num_names = int_names + float_names
    return num_names


@st.cache
def get_categorical_names(df):
    # Check the number of unique values per column
    unique_values = df.apply(pd.Series.nunique).to_frame("Unique Values").iloc[:, 0]

    # If the number is lower than 5, I classify it as a categorical variable, this is subjective.
    df_factors = df.loc[:, unique_values < 10]

    # Ensure that these are of type: object
    for col in df_factors:
        df[col] = df[col].astype("object")

    # convert these names to a list
    factor_names = df_factors.columns.tolist()
    return factor_names


#
@st.cache
def get_text_names(df):
    unique_values = df.apply(pd.Series.nunique).to_frame("Unique Values").iloc[:, 0]
    df_obj = df.loc[:, df.dtypes == "object"]
    nr_rows = df.shape[0]
    # if more than 10% of the data is unique the column is marked as a potential text feature.
    df_text = df_obj.loc[:, unique_values / nr_rows >= 0.10]
    return df_text.columns.tolist()


@st.cache
def get_uniqueID_names(df):
    """
    Return column names that use have unique values
    """
    nr_rows = df.shape[0]
    unique_values = df.apply(pd.Series.nunique).to_frame("Unique Values").iloc[:, 0]
    uniqueID_col = df.loc[:, unique_values == nr_rows]
    uniqueID_names = uniqueID_col.columns.tolist()
    # if there is no colomn with unique values, create one called 'identifier'
    if len(uniqueID_names) == 0:
        df["identifier"] = range(1, len(df) + 1)
        uniqueID_names.append("identifier")
    return uniqueID_names


@st.cache
def get_all_names(df):
    """
    :return: all the column names
    """
    all_names = df.columns.tolist()
    return all_names


@st.cache
def highlight_outliers(df):
    dfcopy = pd.DataFrame("", index=df.index, columns=df.columns)
    yellow = "background-color: #FEF4D5"
    blue = "background-color: #E5F0F9"
    for row in df.index:
        # goes wrong if colomns contain , in col name
        for value in df.loc[row, "outliers_above"].split(", "):
            if value == "":
                pass
            else:
                dfcopy.loc[row, value] = yellow
                dfcopy.loc[row, "outliers_above"] = yellow
        for value in df.loc[row, "outliers_below"].split(", "):
            if value == "":
                pass
            else:
                dfcopy.loc[row, value] = blue

                dfcopy.loc[row, "outliers_below"] = blue
    return dfcopy


def highlight_missing(c):
    """
    Highlight the cells with missing value more than 10%
    """
    missing = c >= 10
    return ["background-color: #FFD5D5" if v else "" for v in missing]


@st.cache
def is_data_missing(df, percent_missing):
    """
    :param df: original dataframe
    :param percent_missing: df with percentage of missing values for each variable
    :return: list of columns that are still missing, list of messages to return to the user, and the type
    of message that is return to the user
    """

    still_missing = df.columns[df.isna().any()].tolist()

    message = []
    type = []
    drop_columns = []
    impute_columns = []
    for index, row in percent_missing.iterrows():
        if row[0] >= 10:
            drop_columns.append(index)
        elif 0.000 < row[0] < 10.000:
            impute_columns.append(index)
    if drop_columns is not None:
        drop_string = ", ".join(drop_columns)
        if len(drop_columns) > 1:
            message.append(
                " The columns **{}** contain more than 10% of missing values, you should consider "
                "**dropping** these "
                "columns if the columns do not contain valuable information.".format(
                    drop_string
                )
            )
            type.append("drop")
        elif len(drop_columns) == 1:
            message.append(
                "**{}** contains more than 10% of missing values, you should consider **dropping** this "
                "column if the column does not contain valuable information.".format(
                    drop_string
                )
            )
            type.append("drop")
    if impute_columns is not None:
        impute_string = ", ".join(impute_columns)
        if len(impute_columns) > 1:
            message.append(
                "**{}** contain between 0 and 10% of missing values, you should "
                "consider **imputing** the values.".format(impute_string)
            )
        elif len(impute_columns) == 1:
            message.append(
                "**{}** contains between 0 and 10% of missing values, you should "
                "consider **imputing** the values for this column.".format(
                    impute_string
                )
            )
        type.append("impute")

    if len(still_missing) == 0:
        message = "There are no missing values in your data."
    # message_missing = "Your original data contains missing values, imputation is necessary."
    # not_missing = "Your data does not contain any missing values. No imputation is necessary."
    # is_missing = message_missing if len(still_missing) != 0 else not_missing
    return still_missing, message, type


@st.cache
def get_head_df(df, choice_size):
    """
    :param choice_size: A parameter that the user determines
    Returns either the full dataset or the first 100 rows
    """
    if choice_size == "Full":
        head_df = df
    elif choice_size == "First 100":
        head_df = df.head(100)
    return head_df


@st.cache(show_spinner=False)
def get_unique_values(df):
    """
    show number of unique values for each variable
    """
    unique_values = df.apply(pd.Series.nunique).to_frame("Unique Values").iloc[:, 0]
    return unique_values


@st.cache(show_spinner=False)
def get_type_variables(df):
    """
    Gets the type of each variable in the df
    """
    data_types = df.dtypes.to_frame("Variable Type")
    return data_types


@st.cache(show_spinner=False)
def get_zero_values(df):
    """
    Gets the number of values with 0
    """
    zero_values = df.isin([0]).sum()
    zero_values = zero_values.to_frame()
    zero_values.columns = ["Zero Values"]
    return zero_values


@st.cache(show_spinner=False)
def get_missings(df):
    """
    Gets the percentage and absolute number of missing vlaues
    """
    # get number of missing values for each variable
    missing_values = df.isnull().sum().to_frame("Missing Values").iloc[:, 0]

    # compute percentage of missing values
    percent_missing = (missing_values * 100 / len(df)).to_frame("Percent Missing")

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
    missing_values = df.isnull().sum().to_frame("Missing Values").iloc[:, 0]

    # reset the index
    missing_values_df = missing_values.reset_index()

    # get the columns with more than 0 missing values
    only_missings_df = missing_values_df[missing_values_df["Missing Values"] > 0]

    # assign column names to dataframe
    only_missings_df.columns = ["Variable", "Missing Values"]

    # get the names of the  columns that contain missing values
    missing_values_names = only_missings_df["Variable"].tolist()

    # compute percentage of missing values
    percent_missing = (missing_values * 100 / len(df)).to_frame("Percent Missing")

    return missing_values, only_missings_df, percent_missing, missing_values_names


@st.cache(show_spinner=False)
def summary_table(df):
    """Summary table of the data
    :param df: the input data
    :return: summary statistics table, including the unique values, missing values and data types
    """

    # show number of unique values for each variable
    unique_values = df.apply(pd.Series.nunique).to_frame("Unique Values").iloc[:, 0]

    # show the number of missing values for each variable
    missing_values = df.isnull().sum().to_frame("Missing Values").iloc[:, 0]
    missing_values_df = missing_values.reset_index()
    only_missings_df = missing_values_df[missing_values_df["Missing Values"] > 0]
    only_missings_df.columns = ["Variable", "Missing Values"]

    # get the names of the  columns that contain missing values
    missing_values_names = only_missings_df["Variable"].tolist()

    # compute percentage of missing values
    percent_missing = (missing_values * 100 / len(df)).to_frame("Percent Missing")

    # the type for each variable
    data_types = df.dtypes.to_frame("Variable Type")

    # merge the different values
    table = pd.concat(
        [unique_values, missing_values, percent_missing, data_types], axis=1
    )
    zero_values = df.isin([0]).sum()
    table["0 values"] = zero_values
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
    """
    Get statistics on numerical data
    """

    data_characteristics = df.describe().loc[
        ["mean", "std", "min", "25%", "50%", "75%", "max"]
    ]
    return data_characteristics


def innersection_space():
    """
    Some visual space to separate tables/graphs within a section
    """
    st.write(" ")
    st.write(" ")
    st.write(" ")


def betweensection_space():
    """
    A larger space and a horizontal line for between sections
    """

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.markdown("---")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")


def sidebar_space():
    """
    Creates some space and a horizontal line in the sidebar
    """
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("---")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
    st.sidebar.markdown("")
