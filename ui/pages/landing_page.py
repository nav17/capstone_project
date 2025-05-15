import streamlit as st
from streamlit_extras.let_it_rain import rain


def render_landing_page():
    st.title("Crowding in the London Underground")
    st.divider()
    st.write(
        """
        An analysis of typical and real time crowding data across stations for
        stations on the London Underground. Crowding data is not currently
        avialable for the Elizabeth line so it has been excluded.
        """)
    st.image("https://images.unsplash.com/photo-1530458738063-22ed42fa27c9")
    if st.button("Enter App"):
        rain(
            emoji="🚇",
            font_size=104,
            falling_speed=3,
            animation_length=1
        )
        st.session_state.page = "main"
