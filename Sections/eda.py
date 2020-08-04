import helpers
import streamlit as st
from pandas import concat
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set(style="darkgrid")
sns.set(rc={"figure.figsize": (11.7, 9.27)})


def first_inspection(df):
    """
    :param df: The loaded dataframe
    :return:
    - Contains first look at the dataframe
    - Shows the number of rows and columns of the dataset
    - Shows the data characteristics (unique, missing, percent missing, zero, variable type)
    - Summary of numerical data (mean, std, min, max etc.)
    """

    # Preparation for EDA
    unique_values = helpers.get_unique_values(df)
    data_types = helpers.get_type_variables(df)
    zero_values = helpers.get_zero_values(df)
    missing_values, percent_missing = helpers.get_missings(df)

    # Create table and highlight missing values
    summary_table = concat(
        [unique_values, missing_values, percent_missing, zero_values, data_types],
        axis=1,
    )

    # Gets the names of missing values, a dataframe with the missings, the number of rows/columns
    # of the original df, and two tables with summary statistics
    data_characteristics = helpers.describe_table(df)

    st.title(":mag_right: First Inspection")

    # Show dataframe and a title in streamlit
    st.subheader("Your dataframe")
    st.dataframe(df)

    # space within sections
    helpers.innersection_space()

    # Show Number
    helpers.all_cards(df)

    helpers.innersection_space()

    st.subheader("Data Characteristics")
    st.markdown(
        "Shows the number of **unique values**, the number of **missing values** and the **variable "
        "type** in Python for each variable in the dataset."
    )
    st.write(summary_table)

    helpers.innersection_space()

    st.subheader("Summary of Numerical Data")
    st.markdown(
        "Shows the **count**, the **average** value, **lowest** and **highest** value for each variable"
    )
    st.write(data_characteristics)

    helpers.innersection_space()

    st.sidebar.title(":mag_right: First Inspection")
    all_names = helpers.get_all_names(df)
    choice_duplicates = st.sidebar.multiselect("Select the column that you want to check for duplicates", all_names,
                                               all_names)

    st.subheader("Duplicates")
    st.markdown("You can check your data for duplicates. By default **all columns** are selected in the "
                "sidebar :point_left:, which implies "
                "that the tool will check for duplicate rows. However, you can also select individual columns "
                "to see whether duplicates are present.")

    if len(choice_duplicates) != 0:
        try:
            # returns dataframe that contains duplicates in a column/columns
            # duplicate_df = df[df[choice_duplicates].duplicated() == True].sort_values(choice_duplicates)
            duplicate_df = concat(g for _, g in df.groupby(choice_duplicates) if len(g) > 1)
            if len(duplicate_df) != 0:
                st.write(duplicate_df)
            else:
                st.success("There are no duplicate rows for the selected columns")
        except ValueError:
            st.success("There are no duplicate rows for the selected columns")

    helpers.sidebar_space()
    float_names = helpers.get_numerical_names(df)
    int_names = helpers.get_int_names(df)
    num_names = float_names + int_names

    st.sidebar.subheader(":scissors: Filter the data")
    column = st.sidebar.selectbox("Select a column to filder between a specific range", num_names)
    min_value = float(df[column].min())
    max_value = float(df[column].max())
    values = st.sidebar.slider("Select a range of values", min_value, max_value, (min_value, max_value))

    choice_range = st.sidebar.radio("Select rows inside or outside a specified range", ['Inside', 'Outside'])
    helpers.innersection_space()
    st.subheader(":scissors: Data Filtered")
    if choice_range == 'Inside':
        st.write(df[df[column].between(values[0], values[1])])
    elif choice_range == 'Outside':
        st.write(df[~df[column].between(values[0], values[1])])

    st.sidebar.markdown("---")
    helpers.betweensection_space()


def visuals(df):
    # create lists of column names
    cat_names = helpers.get_categorical_names(df)
    num_names = helpers.get_numerical_names(df)

    # Create list of options for visualizations
    options = []
    if len(num_names) > 0:
        options.append("Histogram")
    if len(cat_names) > 0 and len(num_names) > 0:
        options.append("Boxplot")
    if len(cat_names) > 0:
        options.append("Barplot")
    if len(num_names) > 1:
        options.append("Scatterplot")

    st.title(":chart_with_upwards_trend: Visualizations")
    st.sidebar.title(":chart_with_upwards_trend: Visualizations")

    choice_options = st.sidebar.multiselect(
        "Which visualizations do you want to display", default=options, options=options
    )
    st.sidebar.subheader("Column")

    num_column = st.sidebar.selectbox(
        "Select a numerical column for the histogram, boxplot " "and scatterplot",
        num_names,
    )
    cat_column = st.sidebar.selectbox("Select a grouping variable", cat_names)

    # remove the first numerical choice from the list with numerical columns,
    # as we do not to include it when choosing a second numerical column
    if len(num_names) > 1:
        num_names.remove(num_column)

    fig = plt.figure()
    fig.subplots_adjust(hspace=0.3, wspace=0.3)

    if "Histogram" in choice_options:
        fig.add_subplot(2, 2, 1)
        sns.distplot(df[num_column].dropna())

    if "Boxplot" in choice_options:
        if "Histogram" in choice_options:
            fig.add_subplot(2, 2, 2)
        else:
            fig.add_subplot(2, 2, 1)
        sns.boxplot(cat_column, num_column, data=df)

    if "Barplot" in choice_options:
        if "Histogram" in choice_options and "Boxplot" in choice_options:
            fig.add_subplot(2, 2, 3)
        elif len(choice_options) == 2 and "Boxplot" in choice_options:
            fig.add_subplot(2, 2, 2)
        elif len(choice_options) == 2 and "Histogram" in choice_options:
            fig.add_subplot(2, 2, 2)
        elif len(choice_options) == 3:
            fig.add_subplot(2, 2, 2)
        else:
            fig.add_subplot(2, 2, 1)
        sns.countplot(x=cat_column, data=df)

    if "Scatterplot" in choice_options:
        num_column2 = st.sidebar.selectbox(
            "Select a second numerical column for the scatterplot", num_names
        )
        # Position for scatterplot is always last
        # so it just depends on the length of the chosen options
        for i in range(1, 4):
            if len(choice_options) == i + 1:
                fig.add_subplot(2, 2, i + 1)

        if len(cat_names) > 0:
            sns.scatterplot(x=num_column, y=num_column2, hue=cat_column, data=df)
        else:
            sns.scatterplot(x=num_column, y=num_column2, data=df)
    st.pyplot()



    return
