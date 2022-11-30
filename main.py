import streamlit as st
import pandas as pd
import altair as alt
import datetime
import pytz
import requests

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
today_str = pst_now.strftime("%b %d, %Y")
dailyBreadRes = requests.get('https://scs-app-backend-481f8.web.app/api/v1/daily_bread')
dailyBreadRes = dailyBreadRes.json()

st.title('SCS Daily Bread Dashboard')
st.subheader(today_str + ' - ' + dailyBreadRes["bookName"] + ' ' + str(dailyBreadRes["chapterIdx"]+1))
st.markdown("""---""")
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    log = pd.read_json('https://scs-app-backend-481f8.web.app/api/v1/daily_bread/reading_log?startDate=Oct13,2022')
    st.bar_chart(data=log, x='date', y='readCounts')

