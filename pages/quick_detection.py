# import libraries
import numpy as np
import pandas as pd
import streamlit as st
# Outlier detection models
from pyod.models.cblof import CBLOF
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.knn import KNN
# standardizer
from pyod.utils.utility import standardizer

from helper_functions import create_lists
from helper_functions import summary_stats
# import external functions
from helper_functions import univariate_outliers
# layout
from layout import create_space


def outlier_detection(raw_df, df):
    """
    :param df:
    :param numerical_names:
    :param factor_names:
    :return:
    """
    st.title(":computer: Modelling")
    st.markdown("""
    In this tool it is possible to apply one of five outlier detection techniques, or to all use them. The 
    following outlier detection methods have been included:
    
    - Cluster-based local outlier factor ([CBLOF](https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.cblof))
    - Histogram-base outlier detection ([HBOS](https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.hbos))
    - Isolation Forest ([IForest](https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.iforest))
    - K-neirest neighbors ([KNN](https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.knn))
    - Average KNN ([KNN](https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.knn))
    - All of the methods above. The results are combined into a single score.
        
    Furthermore, per row an indication will be given which column value can considered to be an outlier
    in a single dimension. The two methods that can be chosen from are the **Standard Deviation Method** 
    and the **Inter Quartile Range (IQR)** method. 
    
    The **outlier fraction** slider decides on the fraction of observations that will be classified as an outlier.
    
    👈 **Select the _algorithm(s)_, the _univeriate dimension method_ and the _outlier fraction_ in the sidebar under 
    the Modelling tab. Select the checkbox to run the model.** 
    """)

    factor_names = create_lists.get_categorical_names(df)
    df1 = pd.DataFrame()
    for col in factor_names:
        df1 = df[col].value_counts().reset_index(name=col + '_count').rename(columns={'index': col})
        df = pd.merge(df, df1, on=[col], how='left')

    integer_names = create_lists.get_int_names(df)
    float_names = create_lists.get_float_names(df)
    numerical_names = integer_names + float_names

    data = df[numerical_names]
    data.columns = data.columns.str.rstrip('_count')  # strip suffix at the right end only.

    integer_names = create_lists.get_int_names(data)
    float_names = create_lists.get_float_names(data)
    numerical_names = integer_names + float_names

    results = pd.DataFrame()
    counts = []

    st.write(data.head(100))

    st.sidebar.title(":computer: Modelling")
    st.sidebar.subheader("Exclude Columns")

    # exclude columns
    exclude_choice = st.sidebar.radio("Do you want to exclude variables from the outlier detection analysis?", ("yes", "no"))
    if exclude_choice == "yes":
        excluded_columns = st.sidebar.multiselect("Exclude Columns", numerical_names)

        if excluded_columns and st.sidebar.checkbox("Exclude these columns"):
            data.drop(excluded_columns, axis=1, inplace=True)
            numerical_names = data.columns.tolist()


    st.sidebar.subheader("Algorithms")

    # select an algorithm
    outlier_choice = st.sidebar.selectbox("Which algorithm do you want to use?",
                                  ("Cluster-based Local Outlier Factor (CBLOF)",
                                    "Histogram-base Outzlier Detection (HBOS)",
                                    "Isolation Forest",
                                    "K neirest neighbors (KNN)",
                                    "Average KNN",
                                    "All of the above"))


    st.sidebar.subheader("Univariate outliers")
    method_choice = st.sidebar.selectbox("How do you want to identify the outliers in a univariate dimension?",
                                 ("Standard deviation method", "IQR method"))

    # standardize the entire dataset, which is mainly import for the clustering methods
    data_columns = data.columns.tolist()
    standardized_data = standardizer(data)

    create_space.innersection_space()

    st.subheader("The input for your model (standardized)")
    standardized_data_withnames = pd.DataFrame(standardized_data.copy())
    standardized_data_withnames.columns = data_columns

    # Gets the names of missing values, a dataframe with the missings, the number of rows/columns
    # of the original df, and two tables with summary statistics
    data_characteristics = summary_stats.describe_table(standardized_data_withnames)
    st.write(data_characteristics)

    create_space.innersection_space()


    # allows the user to set the fraction of outliers for the data
    outliers_fraction = st.sidebar.slider("Which outlier fraction do you wish to select?", 0.0, 0.2, 0.02)

    st.success("**If you are ready to run the model then click "
               "on the checkbox below.**")

    if st.checkbox("Run the script"):

        # set the random state, allows for reproduction of the results
        random_state = np.random.RandomState(42)


        if outlier_choice == "Cluster-based Local Outlier Factor (CBLOF)":
            clf = CBLOF(contamination=outliers_fraction, check_estimator=False, random_state=random_state)

        elif outlier_choice == "Histogram-base Outlier Detection (HBOS)":
            clf = HBOS(contamination=outliers_fraction, random_state = random_state)

        elif outlier_choice == "Isolation Forest":
            clf = IForest(contamination=outliers_fraction,random_state=random_state)

        elif outlier_choice == "K neirest neighbors (KNN)":
            clf = KNN(n_neighbors=20, method='largest', contamination=outliers_fraction)

        elif outlier_choice == "Average KNN":
            clf = KNN(n_neighbors=20, method='mean', contamination=outliers_fraction)


        elif outlier_choice == "All of the above":
            # select all classifiers
            classifiers = {
                'Cluster-based Local Outlier Factor (CBLOF)': CBLOF(contamination=outliers_fraction,
                                                                    check_estimator=False,
                                                                    random_state=random_state),
                # 'Histogram-base Outlier Detection (HBOS)': HBOS(contamination=outliers_fraction),
                'Isolation Forest': IForest(contamination=outliers_fraction, random_state=random_state),
                'K Nearest Neighbors (KNN)': KNN(n_neighbors= 20, contamination=outliers_fraction),
                'Average KNN': KNN(n_neighbors=20, method='mean', contamination=outliers_fraction)
            }

            @st.cache(allow_output_mutation=True)
            def run_model(classifiers):
                outcome = []
                models = []
                score = 0
                total_pred = 0
                for i, (clf_name, clf) in enumerate(classifiers.items()):
                    clf.fit(standardized_data)
                    name = str(clf_name)

                    # predict raw anomaly score
                    scores_pred = clf.decision_function(standardized_data)
                    test_scores = scores_pred.reshape(-1, 1).tolist()

                    # convert ndarray into Dataframe
                    test_scores_series = pd.DataFrame.from_records(test_scores)
                    ser = test_scores_series

                    # scale these values between 0 and 1
                    ser = (ser.values - ser.values.min()) / (ser.values.max() - ser.values.min())

                    # aggregate score to total score
                    score += ser

                    # prediction of a datapoint category outlier or inlier
                    y_pred = pd.DataFrame(clf.predict(standardized_data))
                    # Because it is '0' and '1', we can run a count statistic.
                    unique, counts = np.unique(y_pred, return_counts=True)

                    # st.write("**{}** observations have been detected as an outlier, while **{}** observations are a "
                    #          "non-outlier".format(counts[1], counts[0]))

                    # aggregate predictions to know how many algorithms predicted the row to be an outlier
                    total_pred += y_pred

                    # append the predictions into a list
                    outcome.append(y_pred)

                    # append the scores into a list
                    ser = pd.DataFrame(ser)
                    outcome.append(ser)

                    # Append the model name twice, once for the prediction column and one for the score
                    models.append(name)
                    models.append(name + "_score")
                return outcome, models, score, total_pred, counts

            # run the model function
            outcome, models, score, total_pred, counts = run_model(classifiers)

            outcome = pd.concat(outcome, axis = 1)
            outcome = pd.DataFrame(outcome)

            # models is the list of appended names, one for prediction and 1 for score
            outcome.columns = models
            # convert to series
            ser = score

            # ser = (ser.values - ser.values.min()) / (ser.values.max() - ser.values.min())

            outcome['Score'] = ser
            outcome['Total outlier prediction'] = total_pred

        if outlier_choice == "All of the above":
            data = data.reset_index()

            outcome = outcome.reset_index()
            results = pd.concat([raw_df, outcome], axis = 1)

            results = pd.DataFrame(results)

            x = results['Score']
            ser = (x.values - x.values.min()) / (x.values.max() - x.values.min())
            results['Score'] = ser

        else:
            # Fit the chosen model to the training data

            @st.cache(allow_output_mutation=True)
            def run_model(standardize_data):
                clf.fit(standardized_data)

                # Now we have the trained K-NN model, let's apply to the test data to get the predictions
                y_test_pred = clf.predict(standardized_data)  # outlier labels (0 or 1)

                # Because it is '0' and '1', we can run a count statistic.
                unique, counts = np.unique(y_test_pred, return_counts=True)

                # And you can generate the anomaly score using clf.decision_function:
                y_test_scores = clf.decision_function(standardized_data)
                test_scores = y_test_scores.reshape(-1, 1)
                test_scores_norm = standardizer(test_scores)

                # convert to list
                # TODO: not sure if this step is necessary
                # X_test['Score'] = test_scores_norm.tolist()
                # test_scores_norm = test_scores_norm.tolist()
                my_list = map(lambda x: x[0], test_scores_norm)

                # convert to series
                ser = pd.Series(my_list)

                ser = (ser.values - ser.values.min()) / (ser.values.max() - ser.values.min())
                ser = pd.Series(ser)
                ser = ser.rename("Score")
                # Add the y test scores to the data
                results = pd.concat([raw_df, ser], axis = 1)

                # reshape the predictions and add to test data
                test_pred = y_test_pred.reshape(-1, 1)
                results['Pred'] = test_pred

                # convert back to dataframe
                # TODO: possibly adding the column names to this frame
                results = pd.DataFrame(results)

                return counts, results

            counts, results = run_model(standardized_data)
            # Do a value counts on the prediction

        # univariate outlier detection
        outliers_above, outliers_below = univariate_outliers.detect(data, numerical_names, method_choice)

        results['outliers_above'] = outliers_above.eq(1).dot(outliers_above.columns + ', ').str.rstrip(', ')
        results['outliers_below'] = outliers_below.eq(1).dot(outliers_below.columns + ', ').str.rstrip(', ')



    return results, outlier_choice, counts
