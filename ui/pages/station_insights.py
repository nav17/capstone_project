import streamlit as st
from etl.load.load import fetch_db_data


def render_station_insights():
    st.subheader("Crowding by Station")

    # get station names
    station_df = fetch_db_data("SELECT id, name FROM c12de.nav_stations")
    station_names = station_df["name"].tolist()

    # station selection
    selected_station = st.selectbox("Select station", station_names, index=0)

    # find id of selected station
    station_id = station_df.loc[
        station_df["name"] == selected_station, "id"].values[0]

    # get static crowding data for selected station
    query = f"""
        SELECT day_of_week, avg_crowding_percentage, time_band
        FROM c12de.nav_static_crowding
        WHERE id = '{station_id}'
    """
    static_df = fetch_db_data(query)

    # get live crowding data for selected station
    query = f"""
        SELECT id, name, live_crowding_percentage, day_of_week, last_updated
        FROM c12de.nav_stations
        WHERE id = '{station_id}'
    """
    live_df = fetch_db_data(query)
    live_crowding = live_df["live_crowding_percentage"].iloc[0]
    live_last_updated = live_df["last_updated"].iloc[0]
    live_day = live_df["day_of_week"].iloc[0]

    if static_df.empty:
        st.warning("No crowding data for this station")
    else:
        # Line chart
        st.subheader("Line chart")
        st.write(f"""
                 Live crowding percentage: {live_crowding}% last updated
                 at {live_day} {live_last_updated}
                 """)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        chart, legend = st.columns([0.9, 0.2], border=True)
        with legend:
            selected_day = st.radio("Select day", days)
        with chart:
            filtered_df = static_df[
                static_df["day_of_week"] == selected_day.upper()]
            st.line_chart(
                filtered_df,
                x="time_band",
                y="avg_crowding_percentage")
            filtered_df = static_df[
                static_df["day_of_week"] == selected_day.upper()]
