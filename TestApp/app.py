import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Streamlit + Plotly Test App")

# Sample dataset
df = px.data.iris()

# Create Plotly figure
fig = px.scatter(
    df,
    x="sepal_width",
    y="sepal_length",
    color="species",
    title="Iris Dataset Scatter Plot"
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)
