import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(
    page_title="Visualize Your Connections", 
    page_icon="💽", 
    layout="wide",
    initial_sidebar_state="collapsed")

instructions = Image.open('images/inst.png')

# \\\ Sidebar /// #

algae = px.colors.sequential.algae
blues = px.colors.sequential.Blues

#with st.sidebar:
#    color_scheme = st.selectbox("select color of visuals: ", ("coming soon"))

# \\\ Functions /// #

@st.cache_data
def load_data(csv, dataset):
    if csv is not None: # if file is uploaded
        df = pd.read_csv(csv, skiprows=3)
        df['Connected On'] = pd.to_datetime(df['Connected On'])
        df['Year'] = df['Connected On'].dt.year
        df['Company'] = df['Company'].fillna('No Company Data')
        df['Position'] = df['Position'].fillna('No Position Data')

    else:               # if no file is uploaded or removed
        df = pd.read_csv(f'data/{dataset}.csv', skiprows=3)
        df['Connected On'] = pd.to_datetime(df['Connected On'])
        df['Year'] = df['Connected On'].dt.year
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
    color='count',
    height=200,
    color_continuous_scale=px.colors.sequential.Aggrnyl,
    labels={'year':'','count':''}
    )
    bar.update_traces(textfont_size=14, textposition='outside', 
                    marker_line_width=0, hovertemplate='%{x} connections for %{y}.')

    bar.update_layout(margin=dict(t=0, l=0, r=0, b=0),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)')
    
    bar.update_coloraxes(showscale=False)

    bar.update_xaxes(color='#03b5aa',
                    gridcolor='white',
                    linecolor='rgba(0,0,0,0)')

    bar.update_yaxes(color='#03b5aa',
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
    color_discrete_sequence=px.colors.sequential.Aggrnyl
    )
    fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), 
                    font=dict(family='Arial', size=14),
                    plot_bgcolor='rgba(0,0,0,0)')

    fig.update_traces(root_color='rgba(0,0,0,0)',  # to match background color of app
                    marker=dict(cornerradius=10),
                    hovertemplate='%{value} Connection(s) <br> at %{label}')
    
    return fig

@st.cache_data
def polar_px(df):
    df['Month'] = df['Connected On'].dt.month_name()
    month = df['Month'].value_counts().reset_index()
    month = month.rename(columns={'index':'month','Month':'count'})
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    chart = px.bar_polar(
    month,
    theta='month',
    r='count',
    color='count',
    template='plotly_dark',
    color_discrete_map=px.colors.sequential.Redor,
    category_orders={'month': month_order})

    return chart

with st.container():
    st.title("my LinkedIn connections: ")
    st.subheader("the visual: ")
    st.write("after finding out it was possible to export LinkedIn connections data, I immediately started to brainstorm a project to visualize the data")

with st.container():
    left, right = st.columns((3, 2))
    with left:
        st.subheader("important notice")
        notice = st.expander("about the uploaded data:")
        notice.write(""" 
            you may be asking - "are you collecting my data without my consent?"
            
            the answer is simply, no.

            after you close this tab or remove your uploaded file, all information is gone and not kept in any way.

            this [post by Streamlit](https://docs.streamlit.io/knowledge-base/using-streamlit/where-file-uploader-store-when-deleted) explains this as well
            """)
        left.subheader("how to")
        how_to = st.expander("steps to get your own data: ")
        how_to.write("""
        [click on this link](https://www.linkedin.com/mypreferences/d/download-my-data) and select to export your connections data

        you will receive an email with a zipped folder containing your connections data

        extract the file and then you will be ready to visualize your connections!  
        """)
        how_to.image(instructions, width=500, use_column_width='auto', output_format='PNG')
    with right:
        st.subheader("")
        right.write("")
        dataset = st.selectbox('choose a sample dataset:', ('diego','alberto'))
        csv_file = st.file_uploader('upload your file here 👇 ')
        tree_height = st.slider("change the height of the visual 🔍", 500, 2000, 1000)
        df = load_data(csv_file, dataset)
        treemap = treemap_px(df, tree_height)

st.write("##")        

# \\\ Treemap /// #

with st.container():
    st.plotly_chart(treemap, use_container_width=True)

# \\\ Bar Chart /// #

st.write("##")

st.subheader("break it down! 🤸")

bar = bar_px(df)

with st.container():
        st.write("by year:")
        st.plotly_chart(bar, use_container_width=True)
