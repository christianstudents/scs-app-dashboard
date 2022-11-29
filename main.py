import streamlit as st
import pandas as pd
from datetime import date

today = date.today()
today_str = today.strftime("%b %d, %Y")
st.title('SCS Daily Bread Dashboard')
st.text(today_str)
