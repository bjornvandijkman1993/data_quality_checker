import streamlit as st
import helpers
from Text import text_markdown
from pandas.api.types import infer_dtype
from pandas import concat


def preprocess(df):
    """
    Gives different preprocessing Suggestions based on the input dataframe
    """

    st.title(":newspaper: Additional Information")
    st.sidebar.title(":newspaper: Additional Information")

    st.subheader("Duplicates")
    st.markdown("You can check your data for duplicates. By default **all columns** are selected in the "
                "sidebar :point_left:, which implies "
                "that the tool will check for duplicate rows. However, you can also select individual columns "
                "(or multiple) to see whether duplicates are present. If duplicates are present, a dataset "
                "will be displayed containing the rows which are duplicates when only considering the selected columns.")

    st.sidebar.subheader("Duplicates")
    all_names = helpers.get_all_names(df)
    choice_duplicates = st.sidebar.multiselect("Select the column that you want to check for duplicates", all_names,
                                               all_names)

    if len(choice_duplicates) != 0:
        try:
            # returns dataframe that contains duplicates in a column/columns
            # duplicate_df = df[df[choice_duplicates].duplicated() == True].sort_values(choice_duplicates)
            duplicate_df = concat(g for _, g in df.groupby(choice_duplicates) if len(g) > 1)
            if len(duplicate_df) != 0:
                st.write(duplicate_df)
            else:
                st.success(":heavy_check_mark: There are no duplicate rows for the selected columns")
        except ValueError:
            st.success(":heavy_check_mark: There are no duplicate rows for the selected columns")


    st.subheader("Mixed datatypes")
    st.markdown("Shows the columns which contain a mix of data types. For example, a column with both "
                "numerical values and strings.")

    @st.cache
    def is_mixed(col):
        return infer_dtype(col) in ['mixed', 'mixed-integer']

    mixed_types = df.apply(is_mixed)
    mixed_types = mixed_types.loc[mixed_types == 1].reset_index()
    list_mixed_types = mixed_types['index'].tolist()
    mixed_string = ", ".join(list_mixed_types)

    if len(mixed_string) > 0:
        st.warning(
            ":warning: The column **{}** has mixed data types.".format(mixed_string)
        )
    elif len(mixed_string) == 0:
        st.success(":heavy_check_mark: There are no columns with mixed data types.")


    # Call function to see if any data is missing
    (
        missing_values,
        only_missings_df,
        percent_missing,
        missing_values_names,
    ) = helpers.get_missing_values(df)

    still_missing, messages, type = helpers.is_data_missing(df, percent_missing)

    st.subheader("Missing Values")
    st.markdown("Shows information on the missing values and how to deal with those.")
    # not sure about this
    if len(still_missing) != 0:

        # st.info(is_missing)
        for message, type in zip(messages, type):
            if type == "drop":
                st.warning(message)
            elif type == "impute":
                st.info(message)

        if st.checkbox("Show me different imputation options"):
            text_markdown.missings_recommendation()
    else:
        st.success(messages)




    return
