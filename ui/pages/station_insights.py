import streamlit as st
from etl.load.load import fetch_db_data


def render_station_insights():
    st.subheader("Crowding by Station")
    st.write("placeholder")

    # get station names
    station_df = fetch_db_data("SELECT id, name FROM c12de.nav_stations")
    station_names = station_df["name"].tolist()

    # station selection
    selected_station = st.selectbox("Select station", station_names, index=0)

    print(selected_station)
    # find id of selected station
    station_id = station_df.loc[
        station_df["name"] == selected_station, "id"].values[0]

    query = f"""
        SELECT day_of_week, avg_crowding_percentage, time_band
        FROM c12de.nav_static_crowding
        WHERE id = '{station_id}'
    """
    static_crowding_df = fetch_db_data(query)
    if selected_station == ["Select a station"]:
        st.warning("No station selected")
    elif static_crowding_df.empty:
        st.warning("No crowding data for this station")
