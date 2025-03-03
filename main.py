import streamlit as st
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
# Hide Streamlit menu and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

st.set_page_config(layout="wide")
import plotly.graph_objects as go
import time
from attr.converters import optional
time_sleep = 1
from ellsberg1 import ellsberg_task
from matching_probability import matching_probability
from lotteries import display_lotteries
from training1 import training1
from training2 import training2
from training3 import training3
from monty_hall import three_doors

# def next_page():
#    st.session_state.page += 1


# Initialize session state for tracking progress
if "page" not in st.session_state:
    st.session_state["page"] = 0
    st.session_state["responses"] = []

# Get current scenario
page = st.session_state["page"]
if st.session_state["page"] == 0:
    ellsberg_task()
if st.session_state["page"] == 1:
    display_lotteries(10, 0, .7, 15, -5, 1-.7)
if st.session_state["page"] == 2:
    three_doors()
if st.session_state["page"] == 3:
    training1()
if st.session_state["page"] == 4:
    training2()
if st.session_state["page"] == 5:
    training3()
##################################################

