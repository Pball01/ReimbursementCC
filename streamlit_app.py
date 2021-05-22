import streamlit as st

import numpy as np
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import datetime
from PIL import Image
import plotly.offline as pyo
from datetime import time,datetime,date


import plotly.offline as py 
from plotly.figure_factory import create_table # for creating nice table

import matplotlib as mpl

from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS
from plotly.offline import init_notebook_mode, iplot



#Setting streamlit pages
st.set_page_config(
    page_title="Final Project",
    layout = "wide",
    initial_sidebar_state="expanded"
)


st.image('https://di-uploads-development.dealerinspire.com/perillobmw/uploads/2018/01/ChicagoSkyline.jpg')
st.title('City of Chicago')
st.header('Employee Reimbursement through Payroll')



#uploading and cacheing Files
@st.cache
def load_data():
    df = pd.read_csv("Employee_Reimbursements_Through_Payroll_System.csv")
    df.rename(columns = {'Pay Date':'Pay_Date',
                      'Employee Name': 'Employee_Name',
                      'Reimbursement Type': 'Reimbursement_Type',
                      'Department Name': 'Department_Name',
                      'Job Title':'Job_Title'}, inplace = True)
    
    df['Department_Name'] = df['Department_Name'].str.lower()
    df['Job_Title'] = df['Job_Title'].str.lower()
    df['Pay_Date'] = pd.to_datetime(df['Pay_Date'], format= '%m/%d/%Y')
    df['Year']=pd.to_datetime(pd.DatetimeIndex(df['Pay_Date']).year, format='%Y')
    df['Year_Only'] = df['Year'].dt.strftime('%Y')
    df['Month']=df['Pay_Date'].dt.strftime('%b')
    df['Month_Year']=df['Pay_Date'].dt.strftime('%Y-%m')
    df['Month_Year'] = pd.to_datetime(df['Month_Year'], format= '%Y-%m')
    return df
df = load_data()

@st.cache
def load_df_monthyear():
    df = load_data()
    df_monthyear = df.groupby(['Month_Year','Year','Month','Employee_Name','Reimbursement_Type', 'Department_Name', 'Job_Title']).sum().reset_index()
    return df_monthyear
df_monthyear = load_df_monthyear()

@st.cache
def load_df_monthyear_s():
    df = load_data()
    df_monthyear_s = df.groupby(['Month_Year','Year','Month','Reimbursement_Type', 'Department_Name', 'Job_Title']).sum('Amount').reset_index()
    return df_monthyear_s
df_monthyear_s = load_df_monthyear_s()

@st.cache
def load_df_year_s():
    df = load_data()
    df_year_s = df.groupby(['Year','Reimbursement_Type', 'Department_Name', 'Job_Title']).sum('Amount').reset_index()
    return df_year_s
df_year_s = load_df_year_s()


layout = go.Layout(
    plot_bgcolor="#FFF",  # Sets background color to white
    xaxis=dict(
        linecolor="#BCCCDC",  # Sets color of X-axis line
        showgrid=False  # Removes X-axis grid lines
    ),
    yaxis=dict(
        linecolor="#BCCCDC",  # Sets color of Y-axis line
        showgrid=False,  # Removes Y-axis grid lines    
    )
)

def first_page():
#First chart
    fig = go.Figure(
    data=[
        go.Bar(
            x=df_monthyear_s['Month_Year'],
            y=df_monthyear_s['Amount'],
            #hoverinfo='none',
            marker_color=px.colors.qualitative.G10[0]
        )
    ]
    )
    #pyo.plot(fig)
    fig.update_traces(marker_line_width=0)
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(layout)
    st.plotly_chart(fig, use_container_width=True)


    #setting 2 columns 


    col1, col2 = st.beta_columns(2)

    with col1:
        st.markdown('### **Trend in Departments**')
        st.markdown("***")
        selected_dep = st.multiselect(
        'Select the Department', options=list(df_year_s['Department_Name'].unique()),
        default = ["department of buildings", "chicago department of transportation",
        'department of water management','dept of streets & sanitation','fire department']
        )
        st.markdown('##### Yearly Trends of Departments')

        fig = px.bar(df_year_s[df_year_s.Department_Name.isin(selected_dep)], x="Year", y="Amount", color= 'Department_Name', barmode = 'stack')
        fig.update_traces(marker_line_width=0)
        #fig.update_layout(showlegend=False)
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1), legend_title_text = '')
        fig.update_layout(layout)
        st.plotly_chart(fig, use_container_width=True)


        st.markdown("***")
        st.markdown('##### Monthly Trends of Departments')
        fig = px.bar(df_monthyear_s[df_monthyear_s.Department_Name.isin(selected_dep)], x="Month", y="Amount", 
                                    color= 'Department_Name', barmode = 'stack',
                                    category_orders={"Month": ["Jan", "Feb", "Mar", "Apr", "May",
                                                                "Jun", "Jul", "Aug", "Sep","Oct",
                                                                "Nov", "Dec"]})
        fig.update_traces(marker_line_width=0)
        #fig.update_layout(showlegend=False)
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1), legend_title_text = '')
        fig.update_layout(layout)
        st.plotly_chart(fig, use_container_width=True)


    with col2:
        st.markdown('### **Trend in Job Titles**')
        st.markdown("***")
        selected_job = st.multiselect(
        'Select the Job Title', options=list(df_year_s['Job_Title'].unique()),
        default = ['building/construction inspector','lineman', 'plumbing inspector', 'traffic signal repairman','field service specialist ii']
        )
        st.markdown('##### Yearly Trends of Job Titles')

        fig = px.bar(df_year_s[df_year_s.Job_Title.isin(selected_job)], x="Year", y="Amount", color= 'Job_Title', barmode = 'stack',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_traces(marker_line_width=0)
        #fig.update_layout(showlegend=False)
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1),legend_title_text = '')
        fig.update_layout(layout)
        st.plotly_chart(fig, use_container_width=True)


        st.markdown("***")
        st.markdown('##### Monthly Trends of Job Titles')
        fig = px.bar(df_monthyear_s[df_monthyear_s.Job_Title.isin(selected_job)], x="Month", y="Amount", 
                                    color= 'Job_Title', barmode = 'stack',
                                    color_discrete_sequence=px.colors.qualitative.Pastel,
                                    category_orders={"Month": ["Jan", "Feb", "Mar", "Apr", "May",
                                                                "Jun", "Jul", "Aug", "Sep","Oct",
                                                                "Nov", "Dec"]})
        fig.update_traces(marker_line_width=0)
        #fig.update_layout(showlegend=False)
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1),legend_title_text = '')
        fig.update_layout(layout)
        st.plotly_chart(fig, use_container_width=True)




def second_page():
    st.write("")

# Fig1 
    #df2007 = df.query('Year == 2006')
    selected_year = st.selectbox(
        label="Choose the year...", options=df['Year_Only'].unique(),

    )
    fig = px.scatter(df[df.Year.isin([selected_year])],
                    x='Amount', y='Department_Name')
    fig.update_layout(layout)
    st.plotly_chart(fig, use_container_width=True)


#FIG2
    mpl.rcParams['font.size']=12                
    mpl.rcParams['savefig.dpi']=100             
    mpl.rcParams['figure.subplot.bottom']=.1 
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(
                            background_color='white',
                            stopwords=stopwords,
                            max_words=200,
                            max_font_size=40, 
                            random_state=42
                            ).generate(str(df['Job_Title']))
    print(wordcloud)
    plt.imshow(wordcloud)
    plt.axis('off')
    fig = plt.figure(1)
    plt.show()
    fig.savefig("word1.png", dpi=700)
    st.pyplot(fig, use_container_width=False)


#FIG3
    fig=go.Figure(
                go.Histogram2dContour(x=df['Department_Name'], 
                                    y=df['Amount'], 
                                    contours=go.Contours(coloring='heatmap')))

    fig.add_trace(go.Scatter(
            x=df['Department_Name'], 
            y=df['Amount'],
            mode='markers'))
    #py.iplot(fig)
    fig.update_layout(layout)
    fig.update_layout(
        autosize=False,
        width=500,
        height=800)

    st.plotly_chart(fig, use_container_width=True)











#Sidebar
st.sidebar.image('https://design.chicago.gov/assets/img/logo/LOGO-CHICAGO-horizontal.png')
st.sidebar.title("Navigation")
data_type = st.sidebar.radio(
    "Go to",
    ('Reimbursement Trend', 'Job Title & Departments','Employee Name'))
if data_type == 'Reimbursement Trend':
     first_page()
elif data_type == 'Job Title & Departments':
     second_page()

st.sidebar.title('Download Full Dataset')
st.sidebar.write("check it out [here](https://catalog.data.gov/dataset/employee-reimbursements-through-payroll-system)")

