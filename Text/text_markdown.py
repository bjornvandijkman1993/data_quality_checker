import streamlit as st

_SUSCEPTIBLE_COLOR = "rgba(230,230,230,.4)"
_RECOVERED_COLOR = "rgba(180,200,180,.4)"

COLOR_MAP = {
    "default": "#262730",
    "pink": "#E22A5B",
    "purple": "#985FFF",
    "susceptible": _SUSCEPTIBLE_COLOR,
    "recovered": _RECOVERED_COLOR,
}

def generate_html(
    text,
    color=COLOR_MAP["default"],
    bold=False,
    font_family=None,
    font_size=None,
    line_height=None,
    tag="div",
):
    if bold:
        text = f"<strong>{text}</strong>"
    css_style = f"color:{color};"
    if font_family:
        css_style += f"font-family:{font_family};"
    if font_size:
        css_style += f"font-size:{font_size};"
    if line_height:
        css_style += f"line-height:{line_height};"

    return f"<{tag} style={css_style}>{text}</{tag}>"


def intro_page():
    # Uploader widget
    BITBUCKET_LINK = (
        "https://bitbucket.org/aimdeloittenl/data_quality_checker/src/master/"
    )

    # introductory text

    st.markdown(
        body=generate_html(text=f"Data Quality Checker", bold=True, tag="h1"),
        unsafe_allow_html=True,
    )
    st.markdown(
        body=generate_html(
            tag="h2", text="A tool that checks the quality of your dataset.<br>",
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        body=generate_html(
            tag="h4",
            text=f"<u><a href=\"{BITBUCKET_LINK}\" target=\"_blank\" style=color:{COLOR_MAP['pink']};>"
            "Source Code</a></u> <span> &nbsp;&nbsp;&nbsp;&nbsp</span>"
            "<hr>",
        ),
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    This tool checks and visualizes any excel or csv file that you upload, which makes it a great way to 
    quickly get a sense of the data that you are dealing with.

    👈 **Please _upload a csv or excel file_ in the sidebar to explore your own dataset.**
    """
    )

    return


def missings_recommendation():
    st.markdown(
        """
    ### **Complete Case Analysis**
    The simplest thing to do is to ignore the missing values. This approach is known as
    complete case analysis where we only consider observations where all variables are observed.

    In general, this method **should not be used** unless the proportion of missing values is very small (<5%).
    Complete case analysis has the cost of having less data and the result is highly likely to be biased if the
    missing mechanism is not MCAR.

    ### **Mean, median, mode imputation**
    A simple guess of a missing value is the mean, median, or mode (most frequently appeared value) of that
    variable.



    ### **Regression Imputation**
    Mean, median or mode imputation only look at the distribution of the values of the variable with missing
    entries.
    If we know there is a correlation between the missing value and other variables, we can often get better
    guesses by
    regressing the missing variable on other variables.

    ### **KNN imputation**
    Besides model-based imputation like regression imputation, neighbour-based imputation can also be used.
    K-nearest
    neighbour (KNN) imputation is an example of neighbour-based imputation. For a discrete variable,
    KNN imputer uses
    the most frequent value among the k nearest neighbours and, for a continuous variable, use the mean or mode.
    To use KNN for imputation, first, a KNN model is trained using complete data. For continuous data, commonly used
    distance metric include Euclidean, Mahapolnis, and Manhattan distance and, for discrete data, hamming distance is a
    frequent choice.


    ### **Last observation carried forward**
    For example, for longitudinal data, such as patients’ weights over a period of visits, it might make sense to use
    last valid observation to fill the NA’s. This is known as Last observation carried forward (LOCF).

    In other cases, for instance, if we are dealing with time-series data, it might make senes to use interpolation
    of observed values before and after a timestamp for missing values

    ### **Multiple Imputations**
    There are a variety of MI algorithms and implementations available. One of the most popular ones is MICE
    (multivariate imputation by chained equations) and a python implementation is available in the
    fancyimpute package.

    """
    )
