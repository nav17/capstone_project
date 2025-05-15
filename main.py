import streamlit as st
from ui.pages.landing_page import render_landing_page
from ui.pages.overview import render_top_10_live
from ui.pages.station_insights import render_station_insights
from ui.pages.components import render_components
from etl.load.load import fetch_db_data

# get list of stations
station_df = fetch_db_data("SELECT id, name FROM c12de.nav_stations")
station_names = station_df["name"].tolist()

# set default page to landing page
if "page" not in st.session_state:
    st.session_state.page = "landing_page"

# load landing page
if st.session_state.page == "landing_page":
    render_landing_page()
# side bar page selector
elif st.session_state.page == "main":
    st.sidebar.title("Navigation")
    st.sidebar.divider()
    pages = {
        "Top 10 Busiest Stations (Live)": render_top_10_live,
        "Crowding by Station": render_station_insights,
        "Components": render_components
    }
    selected_page = st.sidebar.radio("Go to", list(pages.keys()))
    pages[selected_page]()
