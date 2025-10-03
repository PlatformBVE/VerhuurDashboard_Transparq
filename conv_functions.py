import streamlit as st

def perc_to_days():
    st.session_state.occ_day = st.session_state.occ_perc / 100 * 365

def days_to_perc():
    st.session_state.occ_perc = st.session_state.occ_day / 365 * 100