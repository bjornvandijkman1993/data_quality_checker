import streamlit as st
import pandas as pd

# Don't remove, necessary to include the enable iterative imputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer


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
        drop_string = ', '.join(drop_columns)
        if len(drop_columns) > 1:
            message.append(" The columns **{}** contain more than 10% of missing values, you should consider "
                           "**dropping** these "
                           "columns if the columns do not contain valuable information.".format(drop_string))
            type.append('drop')
        elif len(drop_columns) == 1:
            message.append("**{}** contains more than 10% of missing values, you should consider **dropping** this "
                           "column if the column does not contain valuable information.".format(drop_string))
            type.append('drop')
    if impute_columns is not None:
        impute_string = ', '.join(impute_columns)
        if len(impute_columns) > 1:
            message.append("**{}** contain between 0 and 10% of missing values, you should "
                           "consider **imputing** the values.".format(impute_string))
        elif len(impute_columns) == 1:
            message.append("**{}** contains between 0 and 10% of missing values, you should "
                           "consider **imputing** the values for this column.".format(impute_string))
        type.append('impute')

    if len(still_missing) == 0:
        message = "There are no missing values in your data."
    # message_missing = "Your original data contains missing values, imputation is necessary."
    # not_missing = "Your data does not contain any missing values. No imputation is necessary."
    # is_missing = message_missing if len(still_missing) != 0 else not_missing
    return still_missing, message, type

@st.cache(allow_output_mutation=True)
def new_bool_list(df, col_name):
    bool_list = []
    for index, row in df.iterrows():
        value = row[col_name]
        value_out = 1
        if pd.isna(value):
            value_out = 0
        bool_list.append(value_out)
    return bool_list


@st.cache(allow_output_mutation=True)
def imputation(df, columns_to_impute_with, impute_method):
    """

    :param df: original dataframe
    :param columns_to_impute_with: the columns that the user has selected to impute the missing values in one or
    more of the selected columns with
    :param impute_method: choice is KNN or MICE imputation.
    :return:
    """

    data = df[columns_to_impute_with]
    not_imputed_data = df[df.columns.difference(columns_to_impute_with)]
    data_cols = list(data)

    # KNN and mice model
    knn = KNNImputer(n_neighbors=5, weights="uniform")
    mice = IterativeImputer(max_iter=100, random_state=0)

    imputer = knn if impute_method == "KNN" else mice

    imputed_data = pd.DataFrame(imputer.fit_transform(data))
    imputed_data.columns = data_cols
    imputed_df = pd.concat([imputed_data, not_imputed_data], axis=1)

    return imputed_df, imputed_data
