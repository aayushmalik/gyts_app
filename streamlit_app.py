import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json

# Load GeoJSON data
with open('./rwound_india.geojson') as f:
    geojson = json.load(f)

# Load your data
df = pd.read_csv('./gyts4.csv')  # Replace with your actual data path

# Streamlit app
st.title('GYTS India 2019 Dashboard')

# Dropdown for selecting indicator
indicator = st.selectbox('Select Indicator', sorted(df['Indicator'].unique()))

# Fixed area for now
area = "Urban"

# Filter DataFrame
df_filtered = df[(df['Indicator'] == indicator) & (df['Area'] == area)]

# Ensure 'Value' is treated as continuous and fill missing data
df_filtered['Value'] = pd.to_numeric(df_filtered['Value']).fillna(-1)

# Define the color scale with grey for < 0 and Teal for >= 0
colorscale = [
    [0, '#eeeeee'],  # Grey for values < 0
    [0.01, '#e7f265'],  # Start Teal at values >= 0
    [1, '#207089']  # End Teal at the maximum value
]

# Create the choropleth map
fig = px.choropleth_mapbox(
    df_filtered,
    geojson=geojson,
    color='Value',
    color_continuous_scale=colorscale,
    locations="State/UT",
    featureidkey="properties.State_Name",
    mapbox_style="carto-positron",
    center={"lat": 21.1458, "lon": 79.0882},
    zoom=3.5,
    range_color=[0, df_filtered['Value'].max()]
)

# Customize layout
fig.update_layout(
    height=600,
    margin={"r":0,"t":0,"l":0,"b":0},
    coloraxis_colorbar=dict(
        title="Percentage",
        tickvals=[df_filtered['Value'].min(), 0, df_filtered['Value'].max()],
        ticktext=['No Data', '0', df_filtered['Value'].max()]
    )
)

# Display map in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Additional text or information
st.sidebar.write("[Global Youth Tobacco Survey](https://www.who.int/teams/noncommunicable-diseases/surveillance/systems-tools/global-youth-tobacco-survey)")
st.sidebar.write("""The Global Youth Tobacco Survey (GYTS) is a self-administered, school-based survey of students in grades associated with 13 to 15 years of age designed to enhance the capacity of countries to monitor tobacco use among youth and to guide the implementation and evaluation of tobacco prevention and control programmes. The GYTS uses a standard methodology for constructing the sampling frame, selecting schools and classes, preparing questionnaires, following consistent field procedures, and using consistent data management procedures for data processing and analysis.""")
st.sidebar.write("Data Sources: [World Health Organisation](https://www.data.gov.in/catalog/global-youth-tobacco-survey-gyts-4)")
st.sidebar.write("Created by: [Aayush Malik](https://www.linkedin.com/in/aayushmalik/)")
st.sidebar.write("Tools Used: Python, Streamlit, and Plotly")
st.sidebar.write("Note: No data is available for Jammu and Kashmir.")
