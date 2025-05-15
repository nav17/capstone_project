import streamlit as st
from etl.load.load import fetch_db_data
import plotly.express as px
import pydeck as pdk


def render_top_10_live():
    st.subheader("Live Crowding Analysis")

    # SQL query for top 10 live crowding stations
    query = """
        SELECT name, live_crowding_percentage, last_updated
        FROM c12de.nav_stations
        WHERE live_crowding_percentage IS NOT NULL
    """
    live_crowding_df = fetch_db_data(query)

    oldest = live_crowding_df["last_updated"].min()

    sort_options = ["Top 10 Busiest Stations", "Top 10 Least Crowded Stations"]
    sort_order = st.segmented_control(
        "",
        sort_options,
        default="Top 10 Busiest Stations"
        )
    if sort_order == "Top 10 Busiest Stations":
        sorted_df = live_crowding_df.sort_values(
            by="live_crowding_percentage",
            ascending=False
            ).head(10)
        bar_title = "Top 10 Busiest Stations"
    else:
        sorted_df = live_crowding_df.sort_values(
            by="live_crowding_percentage",
            ascending=True
            ).head(10)
        bar_title = "Top 10 Least Crowded Stations"

    st.write(f"Last updated at: {oldest}")
    sorted_df["rank"] = range(1, 11)

    st.dataframe(
        sorted_df,
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
        sorted_df,
        x="live_crowding_percentage",
        y="name",
        orientation="h",
        labels={"live_crowding_percentage": "Crowding (%)", "name": "Station"},
    )

    fig.update_traces(marker_color=bar_colors)

    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        height=500,
        title=bar_title,
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Map plot
    st.subheader("Live Map of Crowding")

    query = """
        SELECT name, lat, lon, live_crowding_percentage
        FROM c12de.nav_stations
        """
    location_df = fetch_db_data(query)

    location_df["crowding_rank"] = location_df[
        "live_crowding_percentage"].rank(pct=True)

    def percentile_colour(rank):
        # colours have to be colour codes for some reason
        # red
        if rank >= 0.95:
            return [255, 0, 0, 180]
        # orange
        elif rank >= 0.50:
            return [255, 165, 0, 180]
        # yellow
        elif rank >= 0.20:
            return [255, 215, 0, 180]
        # grey
        else:
            return [160, 160, 160, 180]

    location_df["fill_color"] = location_df[
        "crowding_rank"].apply(percentile_colour)

    location_df["elevation"] = location_df["live_crowding_percentage"]

    layer = pdk.Layer(
        "ColumnLayer",
        data=location_df,
        get_position='[lon, lat]',
        get_elevation='elevation',
        elevation_scale=100,
        radius=200,
        get_fill_color='fill_color',
        pickable=True,
        auto_highlight=True,
        extruded=True,
    )

    view_state = pdk.ViewState(
        latitude=location_df["lat"].mean(),
        longitude=location_df["lon"].mean(),
        zoom=10,
        pitch=60,
    )

    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state=view_state,
            layers=[layer],
            tooltip={
                "text": "{name}\nCrowding: {live_crowding_percentage}%"}
        ))

    st.write("""
             **Crowding Rank Colours**  
             🟥 Top 5%  
             🟧 50 – 89%  
             🟨 20 – 49%  
             ⬜️ Bottom 20%
             """)
