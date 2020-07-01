import base64
import datetime
import time
import streamlit as st
from helper_functions import highlighting


def export_consistency(results, col1, col2):
    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H%M%S')
    results.to_excel("output/Consistency/{}_{}_{}_.xlsx".format(col1, col2, stamp))
    st.success("The results have been exported to output/Consistency"
               "/{}.xlsx".format(stamp))
    return


def export_preprocessing(df):
    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H%M%S')
    df.to_csv("output/Processed Data/{}.csv".format(stamp), index=False)
    st.success("The results have been exported to output/Processed Data"
               "/{}.csv".format(stamp))
    return


def export_results(results, name_project, outlier_choice):
    st.markdown("---")
    st.markdown("### Export Options")
    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H%M%S')
    results = results.sort_values('Score', ascending=False)

    if len(results) > 50000:
        export_choice = st.radio("Do you want to export the whole dataframe, or the first 50000 rows",
                                 ("First", "Full"))
        if export_choice == "First":
            results = results.head(1000)
        elif export_choice == "Full":
            results = results
        st.write(results.head(1000))

        # styled = results.style.apply(highlighting.highlight_outliers, axis=None)
        results.to_excel("output/Results/{}_{}_{}.xlsx".format(name_project, stamp, outlier_choice), engine='xlsxwriter')
        st.success("The results have been exported to output/Results"
                   "/{}_{}_{}.xlsx".format(name_project, stamp, outlier_choice))

    else:
        styled = results.style.apply(highlighting.highlight_outliers, axis=None)
        styled.to_excel("output/Results/{}_{}_{}.xlsx".format(name_project, stamp, outlier_choice), engine='xlsxwriter')
        st.success("The results have been exported to output/Results"
                   "/{}_{}_{}.xlsx".format(name_project, stamp, outlier_choice))

    # csv = results.to_csv(index=False)
    # b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    # href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
    # st.markdown(href, unsafe_allow_html=True)

    # if st.checkbox("Export the Results to an Excel file in your results folder"):
    #     timestamp = time.time()
    #     stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H%M%S')
    #     results = results.sort_values('Score', ascending=False)
    #     styled = results.style.apply(highlighting.highlight_outliers, axis=None)
    #     styled.to_excel("output/Results/{}_{}_{}.xlsx".format(name_project, stamp, outlier_choice), engine='xlsxwriter')
    #     st.success("The results have been exported to output/Results"
    #                "/{}_{}_{}.xlsx".format(name_project, stamp, outlier_choice))

    return

