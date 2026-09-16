import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px



st.title("IPL Data Analysis")

df = pd.read_csv("IPL_Matches_Data_2008_2026.csv")


df["total_runs"] = (
    df["team1_runs"] +
    df["team2_runs"]
)


st.sidebar.title("Filters")

selected_season = st.sidebar.selectbox(
    "Select Season",
    sorted(df["season"].dropna().unique())
)

filtered_df = df[
    df["season"] == selected_season
]


st.subheader("Key Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Matches",
    len(df)
)

col2.metric(
    "Seasons",
    df["season"].nunique()
)

col3.metric(
    "Venues",
    df["venue"].nunique()
)

col4.metric(
    "Average Runs",
    round(df["total_runs"].mean(), 2)
)


st.subheader(
    f"Analysis for Season: {selected_season}"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Matches",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Average Runs",
        round(
            filtered_df["total_runs"].mean(),
            2
        )
    )

with col3:
    st.metric(
        "Highest Score",
        filtered_df["total_runs"].max()
    )


st.subheader("Filtered Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)


season_matches = (
    df.groupby("season")
    .size()
    .reset_index(name="matches")
)

st.subheader("Matches by Season")

st.bar_chart(
    season_matches.set_index("season")
)


season_runs = (
    df.groupby("season")["total_runs"]
    .sum()
    .reset_index()
)

st.subheader("Runs by Season")

st.line_chart(
    season_runs.set_index("season")
)


wins = (
    df["winner"]
    .value_counts()
    .head(10)
    .reset_index()
)

wins.columns = [
    "Team",
    "Wins"
]

fig = px.bar(
    wins,
    x="Team",
    y="Wins",
    title="Top Winning Teams"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


team_wins = (
    filtered_df["winner"]
    .value_counts()
    .reset_index()
)

team_wins.columns = [
    "Team",
    "Wins"
]

fig1 = px.bar(
    team_wins.head(10),
    x="Team",
    y="Wins",
    title=f"Winning Teams - {selected_season}"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


toss_decision = (
    df["toss_decision"]
    .value_counts()
    .reset_index()
)

toss_decision.columns = [
    "Decision",
    "Count"
]

fig2 = px.pie(
    toss_decision,
    names="Decision",
    values="Count",
    title="Toss Decision Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)



fig3 = px.histogram(
    df,
    x="total_runs",
    nbins=30,
    title="Distribution of Total Match Runs"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


fig4 = px.histogram(
    filtered_df,
    x="total_runs",
    nbins=20,
    title=f"Match Run Distribution - {selected_season}"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


fig5 = px.scatter(
    df,
    x="team1_runs",
    y="team2_runs",
    title="Team 1 Runs vs Team 2 Runs"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)


fig, ax = plt.subplots()

ax.hist(
    df["total_runs"].dropna(),
    bins=30
)

ax.set_title(
    "Distribution of Match Runs"
)

ax.set_xlabel(
    "Total Runs"
)

ax.set_ylabel(
    "Number of Matches"
)

st.pyplot(fig)


col1, col2 = st.columns(2)

with col1:

    st.subheader("Season Analysis")

    st.bar_chart(
        season_matches.set_index("season")
    )

with col2:

    st.subheader("Run Analysis")

    st.line_chart(
        season_runs.set_index("season")
    )


with st.expander("View Complete Dataset"):

    st.dataframe(
        df,
        use_container_width=True
    )


with st.expander("View Statistical Summary"):

    st.dataframe(
        df.describe()
    )