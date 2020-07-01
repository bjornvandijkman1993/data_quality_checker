# -*- coding: utf-8 -*-
"""
Created on Fri 17 Jan 2020

@author: anschipper

### Description of the purpose

"""
import numpy as np
import pandas as pd
import streamlit as st

from helper_functions import create_lists


def data_transformations(preprocessed_df):
    st.markdown("Based on the outcome of the descriptive statistics, you can decide to apply data transformations "
                "to reduce skewness of your features. You can apply the **Log transformation** to numerical data.")
    st.markdown("""
    👈 **Select the _feature to transform_ in the sidebar under the Log Transformations 
    header. Select the checkbox to apply a transformations. Log transformations on multiple variables is possible.**
    """)

    numerical_names = create_lists.get_numerical_names(preprocessed_df)

    # preprocessed_df = preprocessed_preprocessed_df[numerical_names]
    st.write(preprocessed_df.head(100))

    # Create sidebar to select type of transformation
    st.sidebar.title(":twisted_rightwards_arrows: Log Transformations")

    feature_to_transform = st.sidebar.multiselect("Select the feature to transform", numerical_names)

    if feature_to_transform:

        if st.sidebar.checkbox("Apply log transformation to data"):
            for i in feature_to_transform:
                # st.subheader(i)
                trans_data = preprocessed_df[i]
                log_trans = trans_data.apply(np.sign) * (abs(trans_data) + 1).apply(np.log10)
                transformed_variable = pd.concat([trans_data, log_trans], axis=1)
                preprocessed_df[i] = log_trans
            st.subheader("Transformed DataFrame")
            st.write(preprocessed_df.head(100))
            # if st.checkbox("Export to Excel"):
            #     preprocessed_df.to_excel("transformed_dataset.xlsx")

    return preprocessed_df
