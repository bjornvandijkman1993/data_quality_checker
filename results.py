import streamlit as st

# import external functions
from helper_functions import export_results
from helper_functions import graphing
from helper_functions import create_lists
from helper_functions import highlighting


# layout
from layout import create_space, elements

# text
from text_app import text_markdown


def results_section(results, counts, outlier_choice, name_project):
    st.title(":bar_chart: The Results")
    # shows the number of outliers and non-outliers
    elements.outliers_vs_non_outliers(counts[1], counts[0])
    # text from text_markdown.py
    text_markdown.results_text()

    st.write(results.sort_values(by='Score', ascending=False).head(100).style.apply(highlighting.highlight_outliers, axis=None))
    # export the results, see export_results.py
    export_results.export_results(results, name_project, outlier_choice)


    if len(results) < 100000:
        create_space.innersection_space()

        # visualize the results
        if outlier_choice == "All of the above":
            value_count = results['Total outlier prediction'].value_counts().reset_index()
            value_count = value_count.iloc[1:]
            value_count.columns = ["Number of agreeing algorithms", "Count"]

            altair_bar = graphing.altair_bar(value_count)
            st.subheader("Counts for the number of predictions for an observation")
            st.write(altair_bar)

            create_space.innersection_space()

        # if st.checkbox("Show Visualizations"):
        all_names = create_lists.get_all_names(results)
        factor_names = create_lists.get_categorical_names(results)
        float_names = create_lists.get_float_names(results)
        integer_names = create_lists.get_int_names(results)
        numerical_names = float_names + integer_names
        # Create lists of column names, necessary for dropdown menus
        st.sidebar.title(":bar_chart: Visualizations")
        var1 = st.sidebar.selectbox("Select a numerical variable", numerical_names)
        # Remove variable that is already chosen from list
        numerical_names_var2 = [x for x in numerical_names if x != var1]
        var2 = st.sidebar.selectbox("Select a second numerical variable "
                                    "for the scatterplot.", numerical_names_var2)
        var_cat = st.sidebar.selectbox("Select a grouping variable", factor_names)
        index_name = st.sidebar.selectbox("Select a unique ID of your data to "
                                          "inspect when hovering over the data", all_names)


        altair_interactive_scatter = graphing.interactive_scatterplot(results, var1, var2, var_cat, index_name)
        altair_density = graphing.density_plot(results, var1, var_cat)

        st.subheader("Interactive Scatterplot")
        st.write(altair_interactive_scatter)

        create_space.innersection_space()
    # st.subheader("Density Plot")
    # st.write(altair_density)




    return