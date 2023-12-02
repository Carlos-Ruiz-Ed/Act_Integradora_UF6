import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
from bokeh.plotting import figure
import matplotlib.pyplot as plt
from Funciones import *

st.set_page_config(
    page_title="Incident Reports"
)


logo_image = st.sidebar.image('LAPD.png')
logo_image = st.image('banner.JPEG')
st.title('Police Incident Reports from 2018 to 2020 in San Francisco')

df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")

st.markdown('The data shown below belongs to incident reports in the city of San Francisco, from the year 2018 to 2020, with details from each case such as date, day of the week, police district, neighborhood in which it happened, type of incident in category and subcategory, exact location and resolution.')


mapa = pd.DataFrame()
mapa['Date'] = pd.to_datetime(df['Incident Date'])
mapa['Day'] = df['Incident Day of Week']
mapa['Police District'] = df['Police District']
mapa['Neighborhood'] = df['Analysis Neighborhood']
mapa['Incident Category'] = df['Incident Category']
mapa['Incident Subcategory'] = df['Incident Subcategory']
mapa['Incident Description'] = df['Incident Description']
mapa['Resolution'] = df['Resolution']
mapa['lat'] = df['Latitude']
mapa['lon'] = df['Longitude']
mapa = mapa.dropna()

subset_data3 = mapa
police_district_input = st.sidebar.multiselect(
    'Police District',
    mapa.groupby('Police District').count().reset_index()['Police District'].tolist())
if len(police_district_input) > 0:
    subset_data3 = mapa[mapa['Police District'].isin(police_district_input)]

subset_data2 = subset_data3
neighborhood_input = st.sidebar.multiselect(
    'Neighborhood',
    subset_data3.groupby('Neighborhood').count().reset_index()['Neighborhood'].tolist())
if len (neighborhood_input) > 0:
    subset_data2 = subset_data3[subset_data3['Neighborhood'].isin(neighborhood_input)]

subset_data1 = subset_data2
incident_input = st.sidebar.multiselect(
    'Incident Category',
    subset_data2.groupby('Incident Category').count().reset_index()['Incident Category'].tolist())
if len (incident_input) > 0:
    subset_data1 = subset_data2[subset_data2['Incident Category'].isin(incident_input)]

subset_data = subset_data1
date_range = st.sidebar.date_input("Select Date Range", [subset_data1['Date'].min(),\
                                                         subset_data1['Date'].max()])
if date_range and len(date_range) == 2:
    date_range = [pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])]
    subset_data = subset_data1[(subset_data1['Date'] >= date_range[0])\
                          & (subset_data1['Date'] <= date_range[1])]
else:
    st.warning("Please select both the start and end dates.")


subset_data

st.markdown('''It is important to mention that any police dristrict can answer to any incident, the
            neighborhood in which it happened is not related to the police district.''')
st.markdown('Crime locations in San Francisco')
st.map(subset_data)

safety_level = safety_lvl(subset_data)
colors = {'High': 'red', 'Medium': 'orange', 'Low': 'green'}
safety_color = colors.get(safety_level, 'gray')
st.markdown(f'''<p style="background-color:{safety_color}; padding: 20px; border-radius: 10px;">
            Risk level: {safety_level} <br>
            </p>
            </div>
            ''',
            unsafe_allow_html=True)


st.markdown('Crimes ocurred per day fo the week')
st.bar_chart(subset_data['Day'].value_counts())
st.line_chart(subset_data['Date'].value_counts())
st.markdown('Type of crimes committed')
st.bar_chart(subset_data['Incident Category'].value_counts())
if len(neighborhood_input) >= 2:
    neighborhood_comparison = px.histogram(subset_data, x='Neighborhood', color='Incident Category',
                                       title='Incident Comparison Across Neighborhoods')
    st.plotly_chart(neighborhood_comparison, use_container_width=True)

agree = st.checkbox('Click to see Incident Subcategories')
if agree:
    st.markdown('Subtype of crimes commited')
    st.bar_chart(subset_data['Incident Subcategory'].value_counts())

    selected_incident = st.selectbox('Select Incident for Detailed Analysis', subset_data['Incident Subcategory'].unique())

    detailed_data = subset_data[subset_data['Incident Subcategory'] == selected_incident][['Date','Day','Police District',
                                                                                          'Neighborhood', 'Incident Description',
                                                                                          'Resolution']]

    st.markdown(f'**Details for Incident: {selected_incident}**')
    st.write(detailed_data)

st.markdown('Resolucion status')
fig1, ax1 = plt.subplots()
labels = subset_data['Resolution'].unique()
ax1.pie(subset_data['Resolution'].value_counts(), labels = labels, autopct='1.1f%%', startangle=20)
st.pyplot(fig1)
            
            
