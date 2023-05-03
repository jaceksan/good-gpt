# Download CSV file from the URL
# The CSV file contains data about static site generators (SSGs) with columns:
# 'name', 'url', 'created', 'stars', 'forks', 'issues', 'license', 'language', 'description'
url = "https://raw.githubusercontent.com/epogrebnyak/ssg-dataset/main/data/ssg.csv"
df = pd.read_csv(url)

# Read file to data frame and convert 'created' column to datetime format, keeping only the year
df['created'] = pd.to_datetime(df['created']).dt.year

# Group the data frame by 'created' (year) and calculate the sum of 'stars' for each year
df_grouped = df.groupby('created')['stars'].sum().reset_index()

# Create a line chart to display the sum of stars by created (year)
chart = alt.Chart(df_grouped).mark_line().encode(
    x='created',
    y='stars'
)

# Display the line chart in the Streamlit app
st.altair_chart(chart)