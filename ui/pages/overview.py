import streamlit as st
from etl.load.load import fetch_db_data
import plotly.express as px


def render_top_10_live():
    st.subheader("Top 10 Busiest Stations by Live Crowding %")

    # SQL query for top 10 live crowding stations
    query = """
        SELECT name, live_crowding_percentage
        FROM c12de.nav_stations
        WHERE live_crowding_percentage IS NOT NULL
        ORDER BY live_crowding_percentage DESC
        LIMIT 10
    """
    top10_live_df = fetch_db_data(query)
    top10_live_df["rank"] = range(1, 11)
    top10_live_df = top10_live_df

    st.dataframe(
        top10_live_df,
        hide_index=True,
        column_config={
            "rank": st.column_config.NumberColumn("Rank"),
            "name": st.column_config.TextColumn("Station Name"),
            "live_crowding_percentage": st.column_config.NumberColumn(
                "Live Crowding (%)",
                format="%.2f%%"
            )
        },
        column_order=("rank", "name", "live_crowding_percentage")
    )

    bar_colors = ['red'] + ['lightgrey']*9

    # top 10 live crowding bar chart
    fig = px.bar(
        top10_live_df,
        x="live_crowding_percentage",
        y="name",
        orientation="h",
        labels={"live_crowding_percentage": "Crowding (%)", "name": "Station"},
    )

    fig.update_traces(marker_color=bar_colors)

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        height=500,
        title="Top 10 Busiest Stations",
    )

    st.plotly_chart(fig, use_container_width=True)
