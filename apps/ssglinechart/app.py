import pandas as pd
import altair as alt
import streamlit as st

# Download CSV file
url = 'https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/ssg.csv'
df = pd.read_csv(url)

# Calculate sum of stars by created (year)
df['created'] = pd.to_datetime(df['created'])
df['year'] = df['created'].dt.year
df = df.groupby('year').agg({'stars': 'sum'}).reset_index()

# Display line chart
chart = alt.Chart(df).mark_line().encode(
    x='year',
    y='stars'
).properties(
    width=800,
    height=400
)
st.altair_chart(chart)
