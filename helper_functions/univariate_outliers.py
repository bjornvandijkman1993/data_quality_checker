import streamlit as st
from numpy import percentile
from statistics import mean
from statistics import stdev
import pandas as pd

@st.cache
def detect(df, numerical_names, method_choice):
    outliers_above = pd.DataFrame()
    outliers_below = pd.DataFrame()
    for i in df[numerical_names]:

        if method_choice == "IQR method":
            q25, q75 = percentile(df[i], 25), percentile(df[i], 75)
            iqr = q75 - q25

            cut_off = iqr * 1.5
            lower, upper = q25 - cut_off, q75 + cut_off

        if method_choice == "Standard deviation method":
            data_mean, data_std = mean(df[i]), stdev(df[i])
            cut_off = data_std * 3
            lower, upper = data_mean - cut_off, data_mean + cut_off

        # identify outliers
        outliers_above[i] = (df[i] > upper)
        outliers_below[i] = (df[i] < lower)
    return outliers_above, outliers_below