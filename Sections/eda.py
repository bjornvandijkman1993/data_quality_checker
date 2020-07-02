import streamlit as st
from pandas import concat
import seaborn as sns
sns.set(style="darkgrid")

import helpers


def exploratory_data_analysis(df):
    """
    :param df: The loaded dataframe
    :return:
    - Contains first look at the dataframe
    - Shows the number of rows and columns of the dataset
    - Shows the data characteristics (unique, missing, percent missing, zero, variable type)
    - Summary of numerical data (mean, std, min, max etc.)
    """

    ##### Preparation for EDA
    unique_values = helpers.get_unique_values(df)
    data_types = helpers.get_type_variables(df)
    zero_values = helpers.get_zero_values(df)
    missing_values, percent_missing = helpers.get_missings(df)

    # Create table and highlight missing values
    summary_table = concat([unique_values, missing_values, percent_missing, zero_values, data_types], axis=1).\
        style.apply(helpers.highlight_missing, subset=['Percent Missing'])

    # Gets the names of missing values, a dataframe with the missings, the number of rows/columns
    # of the original df, and two tables with summary statistics
    data_characteristics = helpers.describe_table(df)

    # create lists of column names
    cat_names = helpers.get_categorical_names(df)
    float_names = helpers.get_float_names(df)

    # Create list of options for visualizations
    options = []
    if len(float_names) > 0:
        options.append('Histogram')
    if len(cat_names) > 0 and len(float_names) > 0:
        options.append('Boxplot')
    if len(cat_names) > 0:
        options.append('Barplot')
    if len(float_names) > 1:
        options.append('Scatterplot')

    # get number of rows and columns
    number_rows, number_columns = helpers.number_rows_columns(df)


    st.title(":mag_right: First Look at the data")

    # Show dataframe and a title in streamlit
    st.subheader("Your dataframe")
    st.dataframe(df)

    # space within sections
    helpers.innersection_space()

    # Show Shape in streamlit
    st.subheader("Number of Rows, Columns")

    st.write("The data has {} rows and {} columns.".format(number_rows, number_columns))

    helpers.innersection_space()

    st.subheader("Data Characteristics")
    st.markdown("Shows the number of **unique values**, the number of **missing values** and the **variable "
                "type** in Python for each variable in the dataset.")
    st.write(summary_table)

    helpers.innersection_space()

    st.subheader("Summary of Numerical Data")
    st.markdown("Shows the **count**, the **average** value, **lowest** and **highest** value for each variable")
    st.write(data_characteristics)

    helpers.betweensection_space()

    st.title(":chart_with_upwards_trend: Visualizations")
    st.sidebar.title(":chart_with_upwards_trend: Visualizations")

    choice_options = st.sidebar.multiselect("Which visualizations do you want to display", default = options,
                                            options = options)

    st.sidebar.subheader("Column")

    num_column = st.sidebar.selectbox("Select a numerical column for the histogram, boxplot "
                                      "and scatterplot", float_names)
    cat_column = st.sidebar.selectbox("Select a grouping variable", cat_names)

    # remove the first numerical choice from the list with numerical columns,
    # as we do not to include it when choosing a second numerical column
    if len(float_names) > 1:
        float_names.remove(num_column)

    if "Histogram" in choice_options:
        ax = sns.distplot(df[num_column].dropna())
        st.pyplot()
    if "Boxplot" in choice_options:
        boxplot = sns.boxplot(cat_column, num_column, data=df)
        st.pyplot()
    if "Barplot" in choice_options:
        ax = sns.countplot(x=cat_column, data=df)
        st.pyplot()
    if "Scatterplot" in choice_options:
        num_column2 = st.sidebar.selectbox("Select a second numerical column for the scatterplot", float_names)
        if len(cat_names) > 0:
            ax = sns.scatterplot(x=num_column, y=num_column2, hue = cat_column,
                             data=df)
        else:
            ax = sns.scatterplot(x=num_column, y=num_column2,
                             data=df)
        st.pyplot()

    return
