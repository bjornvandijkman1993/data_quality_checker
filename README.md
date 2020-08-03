
# Data Quality Checker in Streamlit

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
$ git clone [https link]
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

