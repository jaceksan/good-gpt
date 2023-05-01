# Download CSV file
url = "https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/ssg.csv"
df = pd.read_csv(url)

# Read file to data frame
df['created'] = pd.to_datetime(df['created']).dt.year
df_grouped = df.groupby('created')['stars'].sum().reset_index()

# Calculate sum of stars by created (year) and display it as line chart
chart = alt.Chart(df_grouped).mark_line().encode(
    x='created',
    y='stars'
)

st.altair_chart(chart)