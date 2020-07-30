from Layout import html_injections
import helpers
import streamlit as st
from pandas import concat
import seaborn as sns
import matplotlib.pyplot as plt

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
    ).style.apply(helpers.highlight_missing, subset=["Percent Missing"])

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
    html_injections.all_cards(df)

    helpers.innersection_space()

    st.subheader("Data Characteristics")
    st.markdown(
        "Shows the number of **unique values**, the number of **missing values** and the **variable "
        "type** in Python for each variable in the dataset."
    )
    st.dataframe(summary_table)

    helpers.innersection_space()

    st.subheader("Summary of Numerical Data")
    st.markdown(
        "Shows the **count**, the **average** value, **lowest** and **highest** value for each variable"
    )
    st.write(data_characteristics)

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
