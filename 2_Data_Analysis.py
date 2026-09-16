import streamlit as st
import pandas as pd



from pathlib import Path
import pandas as pd

file_path = Path(__file__).parent.parent / "IPL_Matches_Data_2008_2026.csv"

df = pd.read_csv(file_path)


st.title("IPL Data Analysis")


st.subheader("Dataset")

st.dataframe(
    df,
    use_container_width=True
)

st.write("First 5 rows")
st.write(df.head())

st.write("Last 5 rows")
st.write(df.tail())

st.write("Dataset shape:", df.shape)

st.write("Columns:")
st.write(df.columns)

st.subheader("Dataset Shape")

rows, columns = df.shape

st.write("Rows:", rows)
st.write("Columns:", columns)


missing_values = df.isnull().sum()

st.subheader("Missing Values")

st.dataframe(missing_values)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Matches",
    len(df)
)

col2.metric(
    "Total Seasons",
    df["season"].nunique()
)

col3.metric(
    "Total Venues",
    df["venue"].nunique()
)

col4.metric(
    "Cities",
    df["city"].nunique()
)


df["total_runs"] = (
    df["team1_runs"] +
    df["team2_runs"]
)

df["total_wickets"] = (
    df["team1_wickets"] +
    df["team2_wickets"]
)


average_runs = df["total_runs"].mean()

st.metric(
    "Average Match Runs",
    round(average_runs, 2)
)


highest_score = df["total_runs"].max()

st.metric(
    "Highest Combined Score",
    highest_score
)


seasons = sorted(
    df["season"].dropna().unique()
)

teams = sorted(
    pd.concat([
        df["team1"],
        df["team2"]
    ]).dropna().unique()
)


st.sidebar.title("Filters")

selected_season = st.sidebar.selectbox(
    "Season",
    seasons
)

selected_team = st.sidebar.selectbox(
    "Team",
    teams
)


filtered_df = df[
    (df["season"] == selected_season) &
    (
        (df["team1"] == selected_team) |
        (df["team2"] == selected_team)
    )
]

st.subheader("Filtered Matches")

st.dataframe(
    filtered_df,
    use_container_width=True
)


st.subheader("Matches by Season")

matches_by_season = (
    df.groupby("season")
    .size()
    .reset_index(name="matches")
)

st.dataframe(matches_by_season)


st.subheader("Team Wins")

team_wins = (
    df["winner"]
    .value_counts()
    .reset_index()
)

team_wins.columns = [
    "Team",
    "Wins"
]

st.dataframe(team_wins)


st.subheader("Top 10 Winning Teams")

top_winners = (
    df["winner"]
    .value_counts()
    .head(10)
)

st.dataframe(top_winners)