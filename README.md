
# Data Quality Checker in Streamlit

> Provides a nice UI for outlier detection, making it reusable across projects

> Written purely in Python, made possible by Streamlit

---


## Installation

1. Navigate to a folder within your local system in the terminal.
2. Clone the repository and install the dependencies.
3. Run streamlit from the command line

```shell
$ git clone git@bitbucket.org:aimdeloittenl/data_quality_checker.git
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

