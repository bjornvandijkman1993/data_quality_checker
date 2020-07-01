import streamlit as st
from pandas import concat
import seaborn as sns
sns.set(style="darkgrid")

import helpers
import visuals

def exploratory_data_analysis(df):
    """

    :param df: The loaded dataframe
    :return:
    first_look_data:
    - Contains first look at the dataframe
    - Shows the number of rows and columns of the dataset
    - Shows the data characteristics (unique, missing, percent missing, zero, variable type)
    - Summary of numerical data (mean, std, min, max etc.)
    """

    st.title(":mag_right: First Look at the data")
    st.sidebar.title(":mag_right: First Look at the data")

    helpers.innersection_space()

    # Show dataframe and a title in streamlit
    st.subheader("Your dataframe")

    # NUMBER_OF_ROWS is a constant
    choice_size = st.sidebar.radio("Do you want to see the full dataset or the first 100 rows?", ("First 100", "Full"))


    st.dataframe(helpers.get_head_df(df, choice_size))

    # create lists of column names
    num_names = helpers.get_numerical_names(df)
    cat_names = helpers.get_categorical_names(df)
    all_names = helpers.get_all_names(df)

    # space within sections
    helpers.innersection_space()

    # Show Shape in streamlit
    st.subheader("Number of Rows, Columns")

    # get number of rows and columns
    number_rows, number_columns = helpers.number_rows_columns(df)
    st.write("The data has {} rows and {} columns.".format(number_rows, number_columns))

    helpers.innersection_space()

    st.subheader("Data Characteristics")
    st.markdown("Shows the number of **unique values**, the number of **missing values** and the **variable "
                "type** in Python for each variable in the dataset.")

    unique_values = helpers.get_unique_values(df)
    data_types = helpers.get_type_variables(df)
    zero_values = helpers.get_zero_values(df)
    missing_values, percent_missing = helpers.get_missings(df)

    summary_table = concat([unique_values, missing_values, percent_missing, zero_values, data_types], axis=1).\
        style.apply(helpers.highlight_missing, subset=['Percent Missing'])

    st.write(summary_table)

    helpers.innersection_space()

    st.subheader("Summary of Numerical Data")
    st.markdown("Shows the **count**, the **average** value, **lowest** and **highest** value for each variable")

    # Gets the names of missing values, a dataframe with the missings, the number of rows/columns
    # of the original df, and two tables with summary statistics
    data_characteristics = helpers.describe_table(df)
    st.write(data_characteristics)

    helpers.betweensection_space()


    float_names = helpers.get_float_names(df)

    st.sidebar.markdown("---")

    st.title(":chart_with_upwards_trend: Visualizations")
    st.sidebar.title(":chart_with_upwards_trend: Visualizations")

    options = []
    if len(float_names) > 0:
        options.append('Histogram')
    if len(cat_names) > 0 and len(float_names) > 0:
        options.append('Boxplot')
    if len(cat_names) > 0:
        options.append('Barplot')
    if len(float_names) > 1:
        options.append('Scatterplot')

    choice_options = st.sidebar.multiselect("Which visualizations do you want to display", default = options,
                                            options = options)

    st.sidebar.subheader("Columns")

    num_column = st.sidebar.selectbox("Select a numerical column for the histogram, boxplot "
                                      "and scatterplot", float_names)
    cat_column = st.sidebar.selectbox("Select a grouping variable", cat_names)

    if len(float_names) > 1:
        float_names.remove(num_column)


    if "Histogram" in choice_options:
        ax = sns.distplot(df[num_column])
        st.pyplot()
    if "Boxplot" in choice_options:
        boxplot = visuals.boxplot(df, cat_column, num_column)
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

    helpers.betweensection_space()
    st.sidebar.markdown("---")

    st.title("Missing Value Considerations")
    # Call function to see if any data is missing
    missing_values, only_missings_df, percent_missing, missing_values_names = helpers.get_missing_values(df)

    still_missing, messages, type = helpers.is_data_missing(df, percent_missing)
    # not sure about this
    if len(still_missing) != 0:
        # st.info(is_missing)
        for message, type in zip(messages, type):
            if type == 'drop':
                st.warning(message)
            elif type == 'impute':
                st.info(message)

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
    else:
        st.info(messages)








    # choice_explore = st.sidebar.multiselect("How do you want to explore the data?",
    #                                         ("Visualizations", "Inconsistency Check",
    #                                          "Filter Data"))
    # if "Visualizations" in choice_explore:
    #
    #     # visualizations are computationally expensive, limit input data to 10000 rows
    #     if len(df) > 10000:
    #         vis_data = df.head(10000)
    #     else:
    #         vis_data = df
    #
    #     st.sidebar.subheader("Visualizations")
    #     choice_vis = st.sidebar.multiselect("Which visualizations do you want to use?",
    #                                         ("Grouped Boxplot", "Scatterplot",
    #                                          "Barplot", "Boxplot numerical",
    #                                          "Line Chart"))
    #
    #     if "Grouped Boxplot" in choice_vis:
    #         st.sidebar.subheader("Grouped boxplots")
    #         choice_numerical = st.sidebar.selectbox("Choose a numerical variable", num_names)
    #         choice_factor = st.sidebar.selectbox("Choose a grouping variable", cat_names)
    #         choice_hoover = st.sidebar.multiselect("Choose data you want to see for individual points", all_names)
    #
    #         if st.sidebar.button("Show Boxplots"):
    #             plot = graphing.boxplot(vis_data, choice_numerical, choice_factor, choice_hoover)
    #             plot.show()
    #
    #     if "Scatterplot" in choice_vis:
    #
    #         def data_scatter(df):
    #             num_names = create_lists.get_numerical_names(vis_data)
    #             cat_names = create_lists.get_categorical_names(vis_data)
    #             all_names = create_lists.get_all_names(vis_data)
    #
    #             st.sidebar.subheader("Grouped scatterplot")
    #             num1 = st.sidebar.selectbox("Choose a num variable", num_names)
    #             num2 = st.sidebar.selectbox("Choose a second num variable", num_names)
    #             choice_factor = st.sidebar.selectbox("Choose a group variable", cat_names)
    #             choice_hoover = st.sidebar.multiselect("Hover Data", all_names)
    #             return num1, num2, choice_factor, choice_hoover
    #
    #         num1, num2, choice_factor, choice_hoover = data_scatter(vis_data)
    #
    #         if st.sidebar.button("Scatterplot"):
    #             fig = graphing.scatter(vis_data, num1, num2, choice_factor, choice_hoover)
    #             fig.show()
    #
    #
    #
        # if "Barplot" in choice_vis:
        #     st.sidebar.subheader("Barplot")
        #     choice_factor = st.sidebar.selectbox("Choose a categorical variable", cat_names)
        #     if st.sidebar.checkbox("Barplot"):
        #         dfg = vis_data[choice_factor].value_counts().reset_index().rename(columns={'index': choice_factor,
        #                                                                              choice_factor: 'Count'})
        #         fig = px.bar(dfg, x=choice_factor, y='Count')
        #         fig.show()
    #
    #     if "Boxplot numerical" in choice_vis:
    #         st.sidebar.subheader("Boxplots")
    #         num_data = vis_data
    #         # num_data.dropna(inplace=True)  # drop all rows that have any NaN values
    #
    #         norm_data = pd.DataFrame()
    #         for column in num_data.columns:
    #             ser = num_data[column]
    #             norm_data[column] = (ser.values - ser.values.min()) / (ser.values.max() - ser.values.min())
    #
    #         num_data = num_data.unstack().reset_index()
    #         norm_data = norm_data.unstack().reset_index()
    #         num_data.columns = ['Variable', 'ID', 'Value']
    #         norm_data.columns = ['Variable', 'ID', 'Norm Value']
    #         norm_data['Value'] = num_data['Value']
    #
    #         choice_numerical = 'Norm Value'
    #         choice_factor = 'Variable'
    #
    #         # choice_factor = st.sidebar.selectbox("Choose a grouping variable", num_data.columns)
    #         choice_hoover = st.sidebar.multiselect("Choose data you want to see for individual points",
    #                                                norm_data.columns)
    #
    #         if st.sidebar.button("Show Boxplots"):
    #             plot = graphing.boxplot(norm_data, choice_numerical, choice_factor, choice_hoover)
    #             plot.show()
    #
    #     if "Line Chart" in choice_vis:
    #         time_df = pd.DataFrame()
    #         st.sidebar.markdown("---")
    #         st.sidebar.subheader("Time Series")
    #         date_column = st.sidebar.selectbox("Choose a date variable", all_names)
    #         value_column = st.sidebar.selectbox("Choose a numerical variable", num_names)
    #         time_df[value_column] = vis_data[value_column]
    #         time_df[date_column] = pd.to_datetime(vis_data[date_column])
    #         time_df['year'] = pd.DatetimeIndex(time_df[date_column]).year
    #         time_df['month'] = pd.DatetimeIndex(time_df[date_column]).month
    #
    #         month_values = st.sidebar.slider("Month Range", int(time_df.month.min()), int(time_df.month.max()),
    #                                          (int(time_df.month.min()), int(time_df.month.max())))
    #         year_values = st.sidebar.slider("Year Range", int(time_df.year.min()), int(time_df.year.max()),
    #                                         (int(time_df.year.min()), int(time_df.year.max())))
    #
    #         time_df = time_df.query(f"month.between{month_values}")
    #         time_df = time_df.query(f"year.between{year_values}")
    #
    #         # year_to_filter = st.sidebar.selectbox("Filter on a month", time_df['year'].unique())
    #
    #         # time_df = time_df.loc[time_df['month']==month_to_filter]
    #         # if st.sidebar.checkbox("Filter on year"):
    #         #     time_df = time_df.loc[time_df['year']==year_to_filter]
    #         helpers.innersection_space()
    #         st.subheader("Time Series Data")
    #         st.write(time_df)
    #         if st.sidebar.checkbox("Line Chart"):
    #             fig = graphing.line_chart(time_df, date_column, value_column)
    #             fig.show()
    #
    #         if st.checkbox("Use the filtered Time Series Data for further analysis"):
    #             df = time_df
    #
    #
    # if "Inconsistency Check" in choice_explore:
    #     helpers.innersection_space()
    #     st.sidebar.subheader("Look for inconsistencies")
    #     col1 = st.sidebar.selectbox("Choose a first column", all_names)
    #     col2 = st.sidebar.selectbox("Choose a second column", all_names)
    #
    #     if st.sidebar.checkbox('Check for inconsistencies'):
    #         @st.cache
    #         def difference_frame(df):
    #
    #             difference_table = df[(df.groupby([col1])[col2].transform(lambda x: x.nunique() != 1))]
    #             return difference_table
    #
    #         difference_table = difference_frame(df)
    #         difference_table = difference_table[[col1, col2]].sort_values(col1)
    #         final_table = difference_table.drop_duplicates(keep='first')
    #
    #         if len(difference_table) != 0:
    #             st.subheader("Inconsistencies")
    #             st.dataframe(final_table)
    #             st.write(len(final_table))
    #         else:
    #             st.info("There are no incosistencies between the columns **{}** and **{}**.".format(col1, col2))
    #
    #         if st.checkbox("Export inconsistencies"):
    #             export_results.export_consistency(final_table, col1, col2)

    # if "Filter Data" in choice_explore:
    #     st.sidebar.subheader("Filter Data")
    #     feature_to_filter = st.sidebar.selectbox("Select a column out of which you want to delete a "
    #                                              "value", all_names)
    #     value_to_filter = st.sidebar.text_input("Write down the exact value of the column...", )
    #     df = filters.delete_row(df, feature_to_filter, value_to_filter)
    #
    #     substring_to_filter = st.sidebar.text_input("or write down the substring that you want to exclude", )
    #     if st.sidebar.checkbox("Filter your data"):
    #         df, filtered_out = filters.delete_str_contains(df, feature_to_filter, substring_to_filter)
    #         st.info("{} values of the dataframe have been filtered out".format(filtered_out))
    #         st.subheader("Data after Filtering")
    #         st.dataframe(df.head(100))


    return df
