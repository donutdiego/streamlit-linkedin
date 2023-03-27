import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="LinkedIn - Visualize Connections", 
    page_icon=":doughnut:", 
    layout="wide",
    initial_sidebar_state="collapsed")

# \\\ Functions /// #



@st.cache_data
def load_data(csv):
    df = pd.read_csv(csv, skiprows=3)

    df['Connected On'] = pd.to_datetime(df['Connected On'])
    df['Year'] = df['Connected On'].dt.year
    df['Year'] = df['Year'].apply(str)
    df['Company'] = df['Company'].fillna('No Company Data')
    df['Position'] = df['Position'].fillna('No Position Data')

    return df

@st.cache_data
def bar_px(df):
    year = df['Year'].value_counts().reset_index()
    year = year.rename(columns={'index':'year','Year':'count'})

    bar = px.bar(
    year,
    y='year',
    x='count',
    orientation='h',
    text_auto=True,
    color_continuous_scale=['rgba(0,0,0,0)'],
    labels={'year':'','count':''}
    )
    bar.update_traces(textfont_size=14, textangle=0, textposition='outside', 
                    marker_line_width=3, marker_line_color='red')

    bar.update_layout(margin=dict(t=0, l=0, r=0, b=0),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)')

    bar.update_xaxes(color='red',
                    gridcolor='grey',
                    linecolor='green')

    bar.update_yaxes(color='yellow',
                    linecolor='green')

    return bar 

@st.cache_data
def treemap_px(df):
    fig = px.treemap(
    df,
    path=['Company','Position'],
    width=1600, 
    height=1200,
    hover_name=px.Constant('Your connections'),
    color='Company',
    color_discrete_sequence=px.colors.sequential.algae
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), 
                    font=dict(family='Arial', size=14),
                    plot_bgcolor='rgba(0,0,0,0)')
                    #paper_bgcolor='rgba(0,0,0,0)')

    fig.update_traces(root_color='rgba(0,0,0,0)',  # to match background color of app
                    marker=dict(cornerradius=10),
                    hovertemplate='%{value} Connections <br> at %{label}')
    
    return fig

notice = st.expander("⚠️please read⚠️")
notice.write(""" 
    you may be asking, "are you collecting my data without my consent?"
    
    the answer is simply, no.

    after you close the this tab or remove your uploaded file, all information is gone and not kept in any way.

    here is post by Streamlit that explains this as well.
    """)

@st.cache_data
def loading_data(csv):
    if csv is not None:
        df = pd.read_csv('data/connections.csv', skiprows=3)
        df['Connected On'] = pd.to_datetime(df['Connected On'])
        df['Year'] = df['Connected On'].dt.year
        df['Year'] = df['Year'].apply(str)
        df['Company'] = df['Company'].fillna('No Company Data')
        df['Position'] = df['Position'].fillna('No Position Data')
        # apply formatting
    else:
        df = pd.read_csv(csv, skiprows=3)
        df['Connected On'] = pd.to_datetime(df['Connected On'])
        df['Year'] = df['Connected On'].dt.year
        df['Year'] = df['Year'].apply(str)
        df['Company'] = df['Company'].fillna('No Company Data')
        df['Position'] = df['Position'].fillna('No Position Data')
        # apply formatting
    return df

st.title("linkedin visual: ")

with st.container():
    left, middle, right = st.columns(3)
    with left:
        st.subheader("step 1: ")
    with middle:
        st.subheader("step 2: ")
    with right:
        st.subheader("step 3: ")

st.write("##")

with st.container():
    left, middle, right = st.columns((3, 3, 3))
    with left:
        csv_file = st.file_uploader('upload your file here: ')
        df = loading_data(csv_file)


treemap = treemap_px(df)

with st.container():
    st.plotly_chart(treemap, use_container_width=True)

st.write("##")

st.subheader("broken down by year: ")

