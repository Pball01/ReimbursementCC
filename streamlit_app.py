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


df = pd.read_csv("Employee_Reimbursements_Through_Payroll_System.csv")
df['Pay Date'] = pd.to_datetime(df['Pay Date'], format= '%m/%d/%Y')
df['Year']=pd.to_datetime(pd.DatetimeIndex(df['Pay Date']).year, format='%Y')
df['Month']=df['Pay Date'].dt.strftime('%B')
df['Month_Year']=df['Pay Date'].dt.strftime('%Y-%m')
df['Month_Year'] = pd.to_datetime(df['Month_Year'], format= '%Y-%m')


df_monthyear = df.groupby(['Month_Year','Year','Month','Employee Name','Reimbursement Type', 'Department Name', 'Job Title']).sum().reset_index()
df_monthyear_s = df.groupby(['Month_Year','Year','Month','Reimbursement Type', 'Department Name', 'Job Title']).sum('Amount').reset_index()

df_year_s = df.groupby(['Year','Reimbursement Type', 'Department Name', 'Job Title']).sum('Amount').reset_index()


st.set_page_config(
    page_title="Final Project"
)


st.image('https://di-uploads-development.dealerinspire.com/perillobmw/uploads/2018/01/ChicagoSkyline.jpg')

st.title('City of Chicago')
st.header('Employee Reimbursement through Payroll')





#Sidebar



st.sidebar.image('https://design.chicago.gov/assets/img/logo/LOGO-CHICAGO-horizontal.png')
st.sidebar.title("Navigation")
data_type = st.sidebar.radio(
    "Go to",
    ('Reimbursement Trend', 'Job Title & Departments','Employee Name'))

#if data_type == 'Cases/Deaths/Hospitalization Trend':
     #trend()
#elif data_type == 'Hospital Bed Capacity':
     #capacity()

st.sidebar.title('Download Full Dataset')
st.sidebar.write("check it out [here](https://catalog.data.gov/dataset/employee-reimbursements-through-payroll-system)")
