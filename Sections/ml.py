# # Begin by importing all necessary libraries
# import streamlit as st
# import pandas as pd
# import numpy as np
# import helpers
# from sklearn.model_selection import train_test_split
# from sklearn.svm import SVC
# from sklearn.metrics import classification_report, confusion_matrix
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LogisticRegression


def classification(df):

    st.title("The dataset")
    st.write(df)

    predictor_names = helpers.get_predictor_names(df)
    predictor = st.sidebar.selectbox("Select your predictor variable", predictor_names)

    if predictor is None:
        st.error("Your dataset is not suitable for binary classification.")

    else:
        x = df.drop(predictor, axis=1)
        y = np.ravel(df[predictor])
        y = y.astype("int")

        test_size = st.sidebar.slider(
            "Determines the fraction of your test set",
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.1
        )

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=test_size, random_state=50
        )

        try:
            scaler = StandardScaler().fit(x_train)
        except ValueError:
            scaler = "Contains non-numerical"
            st.error(
                "Your dataset contains non-numerical data. Please make the appropriate transformations "
                "before running the analysis."
            )

        if scaler != "Contains non-numerical":
            x_train = scaler.transform(x_train)
            x_test = scaler.transform(x_test)

            ml_options = ["SVM", "Logistic Regression", "KNN"]
            choice_ml = st.sidebar.selectbox(
                "Which ML Algorithm do you want to use?", ml_options
            )

            if st.checkbox("Run the Analysis"):

                if choice_ml == "SVM":
                    svc_model = SVC()
                    svc_model.fit(x_train, y_train)
                    y_predict = svc_model.predict(x_test)
                elif choice_ml == "Logistic Regression":
                    logreg = LogisticRegression()
                    logreg.fit(x_train, y_train)
                    y_predict = logreg.predict(x_test)

                cm = np.array(confusion_matrix(y_test, y_predict, labels=[0, 1]))
                confusion = pd.DataFrame(
                    cm,
                    index=["Diabetic", "Not Diabetic"],
                    columns=["Predicted Diabetes", "Predicted Not Diabetic"],
                )

                helpers.innersection_space()

                st.subheader("Confusion Matrix")
                st.table(confusion)

                helpers.innersection_space()

                st.subheader("Classification Report")
                report = classification_report(y_test, y_predict, output_dict=True)
                report = pd.DataFrame(report).transpose()
                st.write(report)
