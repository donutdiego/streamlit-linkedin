import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="LinkedIn - Visualize Connections", 
    page_icon="💽", 
    layout="wide",
    initial_sidebar_state="collapsed")

# \\\ Sidebar /// #

options = {
    "BuPu": "px.colors.sequential.BuPu",
    "BuGn": "px.colors.sequential.BuGn",
}

with st.sidebar:
    color_scheme = st.selectbox("change the feel of the visuals!", ("px.colors.sequential.BuGn","px.colors.sequential.BuPu"))

# \\\ Functions /// #

@st.cache_data
def load_data(csv, dataset):
    if csv is not None: # if file is uploaded
        df = pd.read_csv(csv, skiprows=3)
        df['Connected On'] = pd.to_datetime(df['Connected On'])
        df['Year'] = df['Connected On'].dt.year
        df['Company'] = df['Company'].fillna('No Company Data')
        df['Position'] = df['Position'].fillna('No Position Data')

    else: # if no file is uploaded or removed
        df = pd.read_csv(f'data/{dataset}.csv', skiprows=3)
        df['Connected On'] = pd.to_datetime(df['Connected On'])
        df['Year'] = df['Connected On'].dt.year
        df['Company'] = df['Company'].fillna('No Company Data')
        df['Position'] = df['Position'].fillna('No Position Data')
        # apply formatting
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
    color='count',
    height=200,
    color_continuous_scale=px.colors.sequential.BuGn,
    labels={'year':'','count':''}
    )
    bar.update_traces(textfont_size=14, textposition='outside', 
                    marker_line_width=0, hovertemplate='%{x} connections for %{y}.')

    bar.update_layout(margin=dict(t=0, l=0, r=0, b=0),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)')

    bar.update_xaxes(color='white',
                    gridcolor='white',
                    linecolor='rgba(0,0,0,0)')

    bar.update_yaxes(color='white',
                    linecolor='rgba(0,0,0,0)',
                    dtick=1)

    return bar 

@st.cache_data
def treemap_px(df, px_height):
    fig = px.treemap(
    df,
    height=px_height,
    path=['Company','Position'],
    color='Company',
    color_discrete_sequence=px.colors.sequential.Redor 
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), 
                    font=dict(family='Arial', size=14),
                    plot_bgcolor='rgba(0,0,0,0)')

    fig.update_traces(root_color='rgba(0,0,0,0)',  # to match background color of app
                    marker=dict(cornerradius=10),
                    hovertemplate='%{value} Connections <br> at %{label}')
    
    return fig

@st.cache_data
def polar_px(df):
    month = df['Month'].value_counts().reset_index()
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    polar = px.bar_polar(
    month,
    theta='index',
    r='Month',
    color='Month',
    template='plotly_dark',
    color_discrete_map=px.colors.sequential.BuPu,
    category_orders={'index':month_order}
)
    return polar



# \\\ Data Collection Notice /// #

with st.container():
    left, middle, right = st.columns(3)
    with left:
        notice = st.expander("⚠️please read⚠️")
        notice.write(""" 
            you may be asking, "are you collecting my data without my consent?"
            
            the answer is simply, no.

            after you close this tab or remove your uploaded file, all information is gone and not kept in any way.

            here is post by Streamlit that explains this as well.
            """)


st.title("linkedin visual: ")

with st.container():
    left, middle, right = st.columns(3)
    with left:
        st.subheader("step 1: ")
    with middle:
        st.subheader(color_scheme)
    with right:
        right.subheader("testing:")

st.write("##")

with st.container():
    left, middle, right = st.columns((3, 3, 3))
    with left:
        dataset = st.selectbox('check out:', ('diego','alberto'))
    with middle:
        tree_height = st.slider("change the pixel height of the visual", 500, 2000, 500)
    with right:
        csv_file = st.file_uploader('upload your file here 👇 ')
        df = load_data(csv_file, dataset)

treemap = treemap_px(df, tree_height)

with st.container():
    st.plotly_chart(treemap, use_container_width=True)

st.write("##")

st.subheader("break it down! 🤸")

bar = bar_px(df)

with st.container():
    st.plotly_chart(bar, use_container_width=True)
