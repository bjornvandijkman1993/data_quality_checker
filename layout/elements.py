import streamlit as st

def outliers_vs_non_outliers(outliers, non_outliers):
    _border_color = "light-gray"
    _number_format = "font-size:35px; font-style:bold;"
    _cell_style = f" border: 2px solid {_border_color}; border-bottom:2px solid white; margin:10px"
    st.markdown(
        f"<table style='width: 100%; font-size:14px;  border: 0px solid gray; border-spacing: 10px;  border-collapse: collapse;'> "
        f"<tr> "
        f"<td style='{_cell_style}'> Outliers</td> "
        f"<td style='{_cell_style}'> Inliers </td>"
        "</tr>"
        f"<tr style='border: 2px solid {_border_color}'> "
        f"<td style='border-right: 2px solid {_border_color}; border-spacing: 10px; {_number_format + 'color:red'}' > {outliers}</td> "
        f"<td style='{_number_format + 'color:black'}'> {int(non_outliers):,} </td>"
        "</tr>"
        "</table>"
        "<br>",
        unsafe_allow_html=True,
    )

    # Calls to streamlit render immediately, no need to return anything