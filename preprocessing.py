import numpy as np
import pandas as pd
import streamlit as st

from helper_functions import create_lists
from helper_functions import doc2vec
from helper_functions import impute_missing_values
from helper_functions import summary_stats
from helper_functions import export_results
from layout import create_space
from pages import preprocessing
from text_app import text_markdown


def preprocess(df):

    st.sidebar.title(":pencil: Preprocessing")

    # import the app text
    text_markdown.preprocess_text()

    # Call function to see if any data is missing
    missing_values, only_missings_df, percent_missing, missing_values_names  = summary_stats.get_missing_values(df)

    still_missing, messages, type = impute_missing_values.is_data_missing(df, percent_missing)

    all_names = create_lists.get_all_names(df)

    # not sure about this
    if len(still_missing) != 0:
        # st.info(is_missing)
        for message, type in zip(messages, type):
            if type =='drop':
                st.warning(message)
            elif type == 'impute':
                st.info(message)
    else:
        st.info(messages)

    preprocessing_options = ["Convert data types", "Slice column", "Doc2Vec", "Exclude Columns",
                             "Filter Columns"]

    # if the message equals the is missing message, then append it to the preprocessing options
    # the idea is that that option is not necessary if there are no missing values in the data
    if len(still_missing) != 0:
        preprocessing_options.append("Impute missing values")


    choice_preprocessing = st.sidebar.radio("Do you want to preprocess your data", ("no", "yes"))

    if choice_preprocessing == "yes":

        preprocessed_df = df.copy()

        choice_preprocessing = st.sidebar.multiselect("How do you want to preprocess the data?",
                                                      (preprocessing_options))

        if "Filter Columns" in choice_preprocessing:
            all_names = create_lists.get_all_names(preprocessed_df)
            filter_columns = st.sidebar.multiselect("Filter on Column names", all_names)
            preprocessed_df = preprocessed_df[filter_columns]

        if "Exclude Columns" in choice_preprocessing:
            numerical_names = create_lists.get_all_names(preprocessed_df)
            excluded_columns = st.sidebar.multiselect("Exclude Columns", all_names)

            if excluded_columns and st.sidebar.checkbox("Exclude this column"):
                preprocessed_df.drop(excluded_columns, axis=1, inplace=True)
                numerical_names = preprocessed_df.columns.tolist()



        if "Slice column" in choice_preprocessing:
            all_names = create_lists.get_all_names(df)
            feature_to_slice = st.sidebar.selectbox("Select the feature to slice", all_names)
            if df[feature_to_slice].dtype != np.float64 or df[feature_to_slice].dtype != np.int64:
                if st.sidebar.button("Execute slicing data"):
                    try:
                        df[feature_to_slice] = df[feature_to_slice].str[1:]
                        preprocessed_df[feature_to_slice] = pd.to_numeric(df[feature_to_slice])
                    except AttributeError:
                        st.error("Slicing failed. You can only slice columns of type object.")


        create_space.innersection_space()

        # if preprocessing is yes, then preprocess the data
        if "Convert data types" in choice_preprocessing:
            preprocessed_df = preprocessing.preprocessing(df, choice_preprocessing)
        # else:
        #     preprocessed_df = df

        create_space.innersection_space()

        # impute missing values if chosen and if present
        if "Impute missing values" in choice_preprocessing:

            # include boolean value for missings
            st.sidebar.subheader("Get boolean missing vs non-missing")
            choose_boolean = st.sidebar.multiselect(
                "Choose a column with missing values that you want to include "
                "as a boolean", still_missing)

            if choose_boolean is not None and st.sidebar.checkbox('Convert to boolean'):

                for name in choose_boolean:
                    bool_list = impute_missing_values.new_bool_list(preprocessed_df, name)
                    boolean_name = name + '_boolean'
                    preprocessed_df[boolean_name] = bool_list

            st.sidebar.subheader("Impute Numerical Missing Values")

            imputation_methods = ['KNN', 'MICE']

            impute_method = st.sidebar.selectbox('Which missing value method do you want to select?',
                                                               imputation_methods)

            all_names = create_lists.get_all_names(df)
            columns_to_impute_with = st.sidebar.multiselect("Select the variables that you want to use "
                                                            "for the imputation", all_names)



            if st.sidebar.checkbox("Execute imputation"):
                try:
                    preprocessed_df, imputed_data = impute_missing_values.imputation(df, columns_to_impute_with,
                                                                                     impute_method)
                except ValueError:
                    st.error("Select numerical variables that you want to use for the imputation.")

            st.sidebar.subheader("Impute Categorical Missing Values")
            cat_names = create_lists.get_categorical_names(preprocessed_df)
            cat_missing = preprocessed_df.columns[preprocessed_df.isna().any()].tolist()

            cat_missing = st.sidebar.multiselect("Select the variables that you want to use "
                                                            "for the imputation", cat_missing)

            if st.sidebar.checkbox("Impute categorical missings"):
                for col in cat_missing:
                    preprocessed_df[col] = preprocessed_df[col].fillna('Missing')
                st.write(preprocessed_df)

            still_missing = preprocessed_df.columns[preprocessed_df.isna().any()].tolist()
            st.subheader("After imputation")
            if len(still_missing) != 0:
                for i in still_missing:
                    st.warning("**{}** still contains missing values".format(i))
            else:
                st.success("The data does not contain any missing values anymore.")

        create_space.innersection_space()

        if "Doc2Vec" in choice_preprocessing:
            uniqueID_names = create_lists.get_uniqueID_names(df)
            if 'identifier' in df.columns:
                st.warning('The dataset did not contain a column to serve as an unique ID. Therefore a column **identifier** was added to the set.')
            text_names = create_lists.get_text_names(df)
            st.sidebar.subheader("Doc2Vec")
            feature_to_vectorize = st.sidebar.multiselect('Select the text features', text_names)
            other_column = st.sidebar.selectbox('Select a column containing an unique ID', uniqueID_names)

            if st.sidebar.checkbox("Execture vectorization"):
                if len(df) > 1000:
                    vec_df = preprocessed_df.head(1000)
                    st.info("Your analysis will be tested on the first 1000 rows. If you want to do it on a bigger dataset "
                            "than the code should be adapted.")
                else:
                    vec_df = preprocessed_df

                for feature in feature_to_vectorize:
                    output = doc2vec.doc2vec(vec_df, feature, other_column)
                    preprocessed_df = pd.merge(vec_df, output, on=other_column)

                create_space.innersection_space()
                st.subheader("Dataframe including doc2vec scores for {}".format(feature))
                st.markdown("A low scores indicates a more unique text field.")
                st.write(preprocessed_df)
                create_space.innersection_space()

    elif choice_preprocessing == "no":
        preprocessed_df = df
    #st.write(preprocessed_df)
    create_space.innersection_space()

    if st.checkbox("Export preprocessed dataframe"):
        export_results.export_preprocessing(preprocessed_df)

    st.success("**If you are done with preprocessing and ready to transform the data then click "
               "on the checkbox below.**")

    return preprocessed_df
