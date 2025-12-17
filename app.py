import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Load dataset
df = pd.read_csv("my_netflix_dataset.csv")

# Clean data
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['listed_in'] = df['listed_in'].fillna("Unknown")

# Title
st.title("🎬 Netflix Data Dashboard")

# Sidebar filter
content_type = st.sidebar.multiselect(
    "Select Content Type",
    df['type'].unique(),
    default=df['type'].unique()
)

filtered_df = df[df['type'].isin(content_type)]

# Movies vs TV Shows
st.subheader("Movies vs TV Shows")
fig1 = px.pie(filtered_df, names='type')
st.plotly_chart(fig1, use_container_width=True)

# Content Added Over Years
st.subheader("Content Added Over Years")
yearly = filtered_df.groupby('year_added').size().reset_index(name='count')
fig2 = px.line(yearly, x='year_added', y='count')
st.plotly_chart(fig2, use_container_width=True)

# Top Genres
st.subheader("Top Genres")
genres = filtered_df['listed_in'].str.spli__t(', ').explode()
top_genres = genres.value_counts().head(10).reset_index()
top_genres.columns = ['Genre', 'Count']
fig3 = px.bar(top_genres, x='Genre', y='Count')
st.plotly_chart(fig3, use_container_width=True)

# My Playlist
st.subheader("⭐ My Playlist")
my_playlist = ["Stranger Things", "Money Heist", "The Witcher", "Dark"]
playlist_df = df[df['title'].isin(my_playlist)]
st.dataframe(playlist_df[['title', 'type', 'release_year', 'rating']])
