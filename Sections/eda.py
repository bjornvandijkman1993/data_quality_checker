import helpers
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from pandas import concat

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

    st.title(":mag_right: First Inspection")
    st.markdown("""
    You can use the filter functionality to inspect the part of the dataframe that you are interested.
    This filter applies to all the :page_facing_up: dataframes and graphs :bar_chart:  in the application. Follow these steps to filter the data:

    1. :walking: Select a **column** to filter on
    2. :open_hands: Select a **range of values** for the selected column 
    3. :question: Indicate whether you want to return the dataframe that falls **inside** or **outside** of the specified range
    4. Hit the checkbox :point_left: to filter the data 
    """)
    st.sidebar.title(":scissors: Filters")
    st.sidebar.warning(":warning: Applies to the full application")
    st.sidebar.subheader("By Numerical Values")

    # Show dataframe and a title in streamlit
    float_names = helpers.get_numerical_names(df)
    int_names = helpers.get_int_names(df)
    num_names = float_names + int_names

    column = st.sidebar.selectbox("Select a column to filter between a specific range", num_names)
    min_value = float(df[column].min())
    max_value = float(df[column].max())

    choice_range = st.sidebar.radio("Select rows inside or outside a specified range", ['Inside', 'Outside'])
    helpers.innersection_space()

    values = st.sidebar.slider("Select a range of values", min_value, max_value, (min_value, max_value))

    if st.sidebar.checkbox("Filter Data"):
        if choice_range == 'Inside':
            df = df[df[column].between(values[0], values[1])]
            st.warning(":warning: **NA's** are filtered out as well.")
        elif choice_range == 'Outside':
            df = df[~df[column].between(values[0], values[1])]

        st.info(
            ":scissors: You are currently filtering on **{}**, where data is retained that is **{}** of the following range: "
            "`{}` and `{}`".format(column, choice_range.lower(), values[0], values[1]))

    cat_names = helpers.get_categorical_names(df)
    if len(cat_names) != 0:
        st.sidebar.markdown("")
        st.sidebar.subheader("By Category")
        choice_column = st.sidebar.selectbox("Select a categorical column to filter on", cat_names)
        categories = df[choice_column].unique()
        choice_category = st.sidebar.multiselect("Choose on or more categories from the selected variable", categories)
        if choice_category:
            # Filters by category
            df = df[df[choice_column].isin(choice_category)]


    st.write(df)
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

    # Preparation for EDA
    unique_values = helpers.get_unique_values(df)
    data_types = helpers.get_type_variables(df)
    zero_values = helpers.get_zero_values(df)
    missing_values, percent_missing = helpers.get_missings(df)

    # Create table and highlight missing values
    @st.cache
    def get_summary_table(unique_values, missing_values, percent_missing, zero_values, data_types):
        table = concat([unique_values, missing_values, percent_missing, zero_values, data_types],
        axis=1,)
        return table


    summary_table = get_summary_table(unique_values, missing_values, percent_missing, zero_values, data_types)

    # Gets the names of missing values, a dataframe with the missings, the number of rows/columns
    # of the original df, and two tables with summary statistics
    data_characteristics = helpers.describe_table(df)

    st.write(summary_table)

    helpers.innersection_space()

    st.subheader("Summary of Numerical Data")
    st.markdown(
        "Shows the **count**, the **average** value, **lowest** and **highest** value for each variable"
    )
    st.write(data_characteristics)

    helpers.innersection_space()

    st.sidebar.markdown("")


    helpers.betweensection_space()

    helpers.sidebar_space()

    return df

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
