
# Outlier Detection in Streamlit

> Provides a nice UI for outlier detection, making it reusable across projects

> Written purely in Python, made possible by Streamlit

---

## Streamlit
![ttystudio GIF](https://camo.githubusercontent.com/5ae1dcfd188be26bbb0648fb62e9d6d593dbb6f5/68747470733a2f2f617773312e646973636f757273652d63646e2e636f6d2f7374616e6461726431302f75706c6f6164732f73747265616d6c69742f6f726967696e616c2f31582f323932653938356637663735656637626566386332376235383939663731663736636435373765302e676966)

---

## Installation

1. Navigate to a folder within your local system in the terminal.
2. Clone the repository and install the dependencies.
3. Run streamlit

```shell
$ git clone git@bitbucket.org:anschipper/react-descriptive-statistics.git
$ pip install -r requirements.txt

$ streamlit run main.py
```

A more elaborate introduction on Streamlit can be found [here](https://lunch-share-app.herokuapp.com/).

---

## Sample Code

```python
import streamlit as st
import pandas as pd

df = pd.read_csv("data.csv")
choice_size = st.sidebar.radio("Do you want to see the full dataset or the first 100 rows?", ("First 100", "Full"))

@st.cache
def get_head_df(df):
    """
    Functino that lets the user choose whether they want to display the whole dataframe or only the first
    100 rows.
    """
    if choice_size == "Full":
        head_df = df
    elif choice_size == "First 100":
        head_df = df.head(100)
    return head_df

st.write(get_head_df(df))
```

---

## Features
1. Provides descriptive statistics for the data
2. Boxplot and scatterplot visualizations
3. Preprocessing steps:
    - Convert data types
    - Impute missing values
4. Log transformations to skewed variables
5. Outlier detections using the following techniques:
    - Cluster-based local outlier factor ([CBLOF](https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.cblof))
    - Histogram-base outlier detection ([HBOS](https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.hbos))
    - Isolation Forest ([IForest](https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.iforest))
    - K-neirest neighbors ([KNN](https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.knn))
    - Average KNN ([KNN](https://pyod.readthedocs.io/en/latest/pyod.models.html#module-pyod.models.knn))
    - All of the methods above. The results are combined into a single score.

    Furthermore, per row an indication will be given which column value can considered to be an outlier
    in a single dimension. The two methods that can be chosen from are the **Standard Deviation Method**
    and the **Inter Quartile Range (IQR)** method.
6. Plot the results to explore them.
7. Export the dataframe, which is sorted on the outlier score.
