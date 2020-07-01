import streamlit as st
import pandas as pd
from layout import custom_css
from helper_functions import create_lists

def preprocessing(df, choice_preprocessing):


    if "Convert data types" in choice_preprocessing:

        all_columns_names = create_lists.get_all_names(df)

        st.subheader("Original data types")
        orig_unique_values = df.apply(pd.Series.nunique).to_frame('Unique Values').iloc[:, 0]
        orig_missing_values = df.isnull().sum().to_frame('Missing Values').iloc[:, 0]
        orig_data_types = df.dtypes.to_frame('Original Variable Type')
        orig_table = pd.concat([orig_unique_values, orig_missing_values, orig_data_types], axis=1)
        st.write(orig_table)

        st.sidebar.subheader("Feature transformations")

        type_of_dtconversion = st.sidebar.selectbox("Select type of conversion",
                                            ["Numeric", "String", "Datetime_EU", "Datetime_US", "Categorical Dates"])
        feature_to_convert = st.sidebar.multiselect("Select the feature to convert", all_columns_names)
        failed_conversions = []


        def check_data_type(org_data_type):
            if str(org_data_type) == 'int64':
                return 'numeric'
            if str(org_data_type) == 'float64':
                return 'numeric'
            if str(org_data_type) == 'object':
                return 'object'
            if str(org_data_type) == 'datetime64[ns]':
                return 'datetime'


        def error_message(type, i):
            if type == 'Categorical Dates':
                errormessage = 'The feature ' + i + ' could not be transformed to seperate categorical features.'
            if type == 'Numeric':
                errormessage = 'The feature ' + i + ' could not be transformed to a numeric datatype.'
            if type == 'String':
                errormessage = 'The feature ' + i + ' could not be transformed to a string datatype.'
            if type == 'Datetime_US' or type == 'Datetime_EU':
                errormessage = 'The feature ' + i + ' could not be transformed to a datetime datatype.'
            return errormessage

        def apply_conversion(type, i):
            newfeatures = []
            if type == "Categorical Dates":
                df['temp'] = df[i].apply(lambda x: x.strftime("Y%YyM%mmD%dd") if pd.notnull(x) else pd.NaT)
                temp1 = df['temp'].str.split('[a-z]', n=3, expand=True)
                df["year_" + i] = temp1[0]
                df["month_" + i] = temp1[1]
                df["day_" + i] = temp1[2]
                newfeatures.append(str("year_" + i))
                newfeatures.append(str("month_" + i))
                newfeatures.append(str("day_" + i))
                df.drop(columns=['temp'], inplace=True)
                successmessage = 'The feature ' + i + ' is converted from a ' + check_data_type(
                    (orig_data_types.loc[i, 'Original Variable Type'])) + ' datatype to seperate categorical features'
            if type == 'Numeric':
                df[i] = pd.to_numeric(df[i], errors='raise')
                successmessage = 'The feature ' + i + ' is converted from a ' + check_data_type(
                    (orig_data_types.loc[i, 'Original Variable Type'])) + ' datatype to a numeric datatype'
            if type == 'String':
                df[i] = list(map(str, df[i]))
                successmessage = 'The feature ' + i + ' is converted from a ' + check_data_type(
                            (orig_data_types.loc[i, 'Original Variable Type'])) + ' datatype to a string datatype'
            if type == 'Datetime_EU':
                df[i] = pd.to_datetime(df[i], dayfirst=True, errors='raise', infer_datetime_format=True)
                successmessage = 'The feature ' + i + ' is converted from a ' + check_data_type(
                                (orig_data_types.loc[i, 'Original Variable Type'])) + ' datatype to a datetime datatype'
            if type == 'Datetime_US':
                df[i] = pd.to_datetime(df[i], dayfirst=False, errors='raise', infer_datetime_format=True)
                successmessage = 'The feature ' + i + ' is converted from a ' + check_data_type(
                                (orig_data_types.loc[i, 'Original Variable Type'])) + ' datatype to a datetime datatype'
            return newfeatures, successmessage


        #feature_to_convert = st.sidebar.multiselect("Select the feature to convert", all_columns_names)
        if st.sidebar.checkbox('Apply conversion to data'):
            if len(feature_to_convert) == 0:
                st.warning('**Please select the features you want to convert**')
            else:
                for i in feature_to_convert:
                    try:
                        newfeatures, successmessage = apply_conversion(type_of_dtconversion, i)
                        conv_unique_values = df.apply(pd.Series.nunique).to_frame('Unique Values').iloc[:, 0]
                        conv_missing_values = df.isnull().sum().to_frame('Missing Values').iloc[:, 0]
                        conv_data_types = df.dtypes.to_frame('Converted Variable Type')
                        conv_table = pd.concat([conv_unique_values, conv_missing_values, orig_data_types, conv_data_types], axis=1)
                        st.success(successmessage)
                    except (ValueError, AttributeError, TypeError):
                        errormessage = error_message(type_of_dtconversion, i)
                        st.error(errormessage)
                        failed_conversions.append(i)
                        continue
                if  len(feature_to_convert) == len(failed_conversions):
                    return
                else:
                    #st.write(df)
                    st.subheader("Converted Features")
                    st.dataframe(conv_table.style.apply(
                        lambda x: ['background: #CEEED8' if x.name in newfeatures or x.name in feature_to_convert and x.name not in failed_conversions else '' for y in x],
                        axis=1))


    # export preprocessed data

    # if st.checkbox("Export the preprocessed data"):
    #     # current date and time
    #     timestamp = time.time()
    #     stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H%M%S')
    #     preprocess_export = "Processed Data/" + stamp + "_" + name_project + "_preprocessed.xlsx"
    #
    #     df.to_excel(preprocess_export)
    #     st.success("The results have been exported to " + preprocess_export)


    return df