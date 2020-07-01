import altair as alt
import streamlit as st
import plotly.express as px

@st.cache
def boxplot(df, numerical, group, hoover):
    fig = px.box(df, x=numerical, y=group, hover_data=hoover)
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )
    fig.update_traces(orientation='h')  # horizontal box plots

    return fig

@st.cache
def line_chart(df, time_column, value_column):
    fig = px.line(df, x = time_column, y = value_column)
    return fig


@st.cache
def scatter(df, num1, num2, choice_factor, choice_hoover):
    fig = px.scatter(df, x=num1, y=num2, color=choice_factor, hover_data=choice_hoover)

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )

    return fig


@st.cache(allow_output_mutation=True)
def altair_bar(results):
    bars = alt.Chart(results).mark_bar().encode(
        x='Count:Q',
        y="Number of agreeing algorithms:O",
        color=alt.Color("Number of agreeing algorithms:O", scale=alt.Scale(scheme='tableau10'))
    )

    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=3  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='Count:Q'
    )

    chart = (bars + text).properties(height=300, width=750)
    return chart


@st.cache(allow_output_mutation=True)
def scatterplot(df, var1, var2, var_cat, index_name):
    chart = alt.Chart(df).mark_point().encode(
        x=var1,
        y=var2,
        tooltip=index_name,
        color=alt.Color(var_cat + ":O", scale=alt.Scale(scheme='tableau10'))).properties(
        width=900, height=600)
    return chart


@st.cache(allow_output_mutation=True)
def interactive_scatterplot(df, var1, var2, var_cat, index_name):
    brush = alt.selection(type='interval')

    points = alt.Chart(df).mark_point().encode(
        x=var1,
        y=var2,
        tooltip=index_name,
        color=alt.condition(brush, var_cat + ":O", alt.value('lightgray'),
                            scale=alt.Scale(scheme='tableau10'))
    ).add_selection(
        brush
    ).properties(width=700, height=450)

    bars = alt.Chart(df).mark_bar().encode(
        y=var_cat + ":O",
        color=var_cat + ":O",
        x='count():O'
    ).transform_filter(
        brush
    ).properties(width=700, height=70)

    chart = points & bars
    return chart


@st.cache(allow_output_mutation=True)
def density_plot(df, var1, var_cat):
    chart = alt.Chart(df).mark_area(
        opacity=0.3,
        interpolate='step'
    ).encode(
        alt.X(var1 + ':Q', bin=alt.Bin(maxbins=100)),
        alt.Y('count()', stack=None),
        alt.Color(var_cat + ":N")
    )
    return chart
