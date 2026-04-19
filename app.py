import streamlit as st
import requests
import math
import random
import time
import datetime

# ----------------------------
# USERS (20 CLIENTS)
# ----------------------------
USERS = {
    "vip001": "A7k2Lp91",
    "vip002": "X9qT3mZ2",
    "vip003": "P4nL8sQ1",
    "vip004": "M2zR7kW9",
    "vip005": "T8vY3pL6",
    "vip006": "Q5xN2cB7",
    "vip007": "H3kP9sD4",
    "vip008": "Z1mX8rV5",
    "vip009": "L6qT4yN2",
    "vip010": "R9bC3kW8",
    "vip011": "F2vX7mP6",
    "vip012": "Y8nQ5sL3",
    "vip013": "D4kR1zT9",
    "vip014": "S7mB2xV6",
    "vip015": "K3pL9qW5",
    "vip016": "U5yN8rC2",
    "vip017": "B1tX4mZ7",
    "vip018": "J6kP3sL9",
    "vip019": "E9vR2qT4",
    "vip020": "W2mX7nK5"
}

ACTIVE_USERS = {}
SESSION_TIMEOUT = 3600

# ----------------------------
# SESSION INIT
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "login_time" not in st.session_state:
    st.session_state.login_time = 0

# ----------------------------
# LOGIN
# ----------------------------
def clean_username(u):
    return u.strip().lower()

if not st.session_state.logged_in:
    st.title("🔐 ODD FATHERS LOGIN")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        u = clean_username(username)

        if u in USERS and USERS[u] == password:

            if u in ACTIVE_USERS:
                st.error("⚠️ Account already in use")
                st.stop()

            ACTIVE_USERS[u] = time.time()

            st.session_state.logged_in = True
            st.session_state.username = u
            st.session_state.login_time = time.time()

            st.rerun()
        else:
            st.error("Invalid Username or Password")

    st.stop()

# ----------------------------
# SESSION TIMEOUT
# ----------------------------
if time.time() - st.session_state.login_time > SESSION_TIMEOUT:
    if st.session_state.username in ACTIVE_USERS:
        ACTIVE_USERS.pop(st.session_state.username)

    st.warning("Session expired")
    st.session_state.logged_in = False
    st.rerun()

# ----------------------------
# PAGE
# ----------------------------
st.set_page_config(page_title="ODD FATHERS", layout="wide")
st.title("🔥 ODD FATHERS - Reliable AI Predictions")

# ----------------------------
# WATERMARK
# ----------------------------
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"""
<div style="position:fixed;bottom:10px;right:10px;opacity:0.3;">
{st.session_state.username} | {now}
</div>
""", unsafe_allow_html=True)

# ----------------------------
# ANTI COPY
# ----------------------------
st.markdown("""
<script>
document.addEventListener('contextmenu', event => event.preventDefault());
document.body.style.userSelect = "none";
</script>
""", unsafe_allow_html=True)

# ----------------------------
# TERMS
# ----------------------------
TERMS_TEXT = """
ODD FATHERS VIP Terms

• No guaranteed profits  
• Informational only  
• Sharing account = permanent BAN  
"""

if "accepted_terms" not in st.session_state:
    st.session_state.accepted_terms = False

if not st.session_state.accepted_terms:
    st.markdown(f"<div style='height:400px;overflow:auto'>{TERMS_TEXT}</div>", unsafe_allow_html=True)
    agree = st.checkbox("I agree")

    if st.button("Continue"):
        if agree:
            st.session_state.accepted_terms = True
            st.rerun()
        else:
            st.error("You must agree")

    st.stop()

# ----------------------------
# MATCHES
# ----------------------------
def get_matches():
    return [
        {"league":"Premier League","home":"Crystal Palace","away":"West Ham","date":"Today"},
        {"league":"Serie A","home":"Lecce","away":"Fiorentina","date":"Today"},
        {"league":"AFC Champions League Elite","home":"Vissel Kobe","away":"Al Ahli","date":"Today"},
    ]

# ----------------------------
# TEAM STATS
# ----------------------------
def get_team_stats(name):
    base = sum(ord(c) for c in name)
    random.seed(base)
    return random.uniform(1.2, 2.8), random.uniform(0.8, 2.0)

def poisson(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

# ----------------------------
# PREDICT
# ----------------------------
def predict(team1, team2):
    t1_scored, t1_conceded = get_team_stats(team1)
    t2_scored, t2_conceded = get_team_stats(team2)

    league_avg = 1.4

    xg1 = (t1_scored * t2_conceded) / league_avg + 0.3
    xg2 = (t2_scored * t1_conceded) / league_avg

    probs = {}
    for i in range(6):
        for j in range(6):
            probs[(i, j)] = poisson(xg1, i) * poisson(xg2, j)

    home = sum(p for (i,j), p in probs.items() if i>j)
    draw = sum(p for (i,j), p in probs.items() if i==j)
    away = sum(p for (i,j), p in probs.items() if i<j)

    over25 = sum(p for (i,j), p in probs.items() if i+j>2)
    btts = sum(p for (i,j), p in probs.items() if i>0 and j>0)

    best = max(probs, key=probs.get)

    return {
        "score": f"{best[0]}-{best[1]}",
        "home": round(home*100,1),
        "draw": round(draw*100,1),
        "away": round(away*100,1),
        "over25": round(over25*100,1),
        "btts": round(btts*100,1),
        "xg1": round(xg1,2),
        "xg2": round(xg2,2)
    }

# ----------------------------
# UI
# ----------------------------
matches = get_matches()

options = [
    f"{m['date']} | {m['league']} | {m['home']} vs {m['away']}"
    for m in matches
]

selected_index = st.selectbox("Select Match", range(len(options)), format_func=lambda i: options[i])
match = matches[selected_index]

# ----------------------------
# REVEAL SYSTEM
# ----------------------------
if "reveal" not in st.session_state:
    st.session_state.reveal = False

if not st.session_state.reveal:
    if st.button("🔒 Reveal Predictions"):
        st.session_state.reveal = True
        st.rerun()
    st.stop()

# ----------------------------
# RUN
# ----------------------------
if st.button("🚀 RUN AI ANALYSIS"):

    pred = predict(match["home"], match["away"])

    st.subheader(f"{match['home']} vs {match['away']}")
    st.write(f"⚽ Score: {pred['score']}")
    st.write(f"xG: {pred['xg1']} - {pred['xg2']}")

    st.write("### Probabilities")
    st.write(f"Home: {pred['home']}%")
    st.write(f"Draw: {pred['draw']}%")
    st.write(f"Away: {pred['away']}%")

    st.write("### Markets")
    st.write(f"BTTS: {pred['btts']}%")
    st.write(f"Over 2.5: {pred['over25']}%")
