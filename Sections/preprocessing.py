import streamlit as st
import helpers


def preprocess(df):
    """
    Gives different preprocessing Suggestions based on the input dataframe
    """

    # Call function to see if any data is missing
    missing_values, only_missings_df, percent_missing, missing_values_names = helpers.get_missing_values(df)

    still_missing, messages, type = helpers.is_data_missing(df, percent_missing)

    st.title("Missing Value Considerations")

    # not sure about this
    if len(still_missing) != 0:
        # st.info(is_missing)
        for message, type in zip(messages, type):
            if type == 'drop':
                st.warning(message)
            elif type == 'impute':
                st.info(message)
    else:
        st.info(messages)

    if st.checkbox("Show me different imputation options"):
        st.markdown("""    
        ### **Complete Case Analysis**
        The simplest thing to do is to ignore the missing values. This approach is known as 
        complete case analysis where we only consider observations where all variables are observed.

        In general, this method **should not be used** unless the proportion of missing values is very small (<5%). 
        Complete case analysis has the cost of having less data and the result is highly likely to be biased if the 
        missing mechanism is not MCAR.

        ### **Mean, median, mode imputation**
        A simple guess of a missing value is the mean, median, or mode (most frequently appeared value) of that 
        variable.



        ### **Regression Imputation**
        Mean, median or mode imputation only look at the distribution of the values of the variable with missing 
        entries. 
        If we know there is a correlation between the missing value and other variables, we can often get better 
        guesses by 
        regressing the missing variable on other variables.

        ### **KNN imputation**
        Besides model-based imputation like regression imputation, neighbour-based imputation can also be used. 
        K-nearest 
        neighbour (KNN) imputation is an example of neighbour-based imputation. For a discrete variable, 
        KNN imputer uses 
        the most frequent value among the k nearest neighbours and, for a continuous variable, use the mean or mode.
        To use KNN for imputation, first, a KNN model is trained using complete data. For continuous data, commonly used 
        distance metric include Euclidean, Mahapolnis, and Manhattan distance and, for discrete data, hamming distance is a 
        frequent choice. 


        ### **Last observation carried forward**
        For example, for longitudinal data, such as patients’ weights over a period of visits, it might make sense to use 
        last valid observation to fill the NA’s. This is known as Last observation carried forward (LOCF).

        In other cases, for instance, if we are dealing with time-series data, it might make senes to use interpolation 
        of observed values before and after a timestamp for missing values

        ### **Multiple Imputations**
        There are a variety of MI algorithms and implementations available. One of the most popular ones is MICE 
        (multivariate imputation by chained equations) and a python implementation is available in the 
        fancyimpute package.

        """)

    return
