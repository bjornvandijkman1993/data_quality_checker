import streamlit as st


def all_cards(df):
    """
    Create cards for df length, columns and missing values
    and align them side by side
    """
    pass
    st.markdown(
        f"""
            <div class="card-deck">
                <div class="card text-white bg-info">
                    <div class="card-body">
                        <h4 class="card-title">Number of Rows</h4>
                        <p class="card-text">{len(df):,d}</p>
                    </div>
                </div>
                <div class="card text-white bg-success">
                      <div class="card-body">
                        <h4 class="card-title">Number of Columns</h4>
                        <p class="card-text">{len(df.columns):,d}</p>
                      </div>
                </div>
                <div class="card text-white bg-danger">
                      <div class="card-body">
                        <h4 class="card-title">Total Missing Values</h4>
                        <p class="card-text">{df.isnull().values.ravel().sum():,d}</p>
                      </div>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )
