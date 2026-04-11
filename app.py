import streamlit as st
import requests
from datetime import datetime
import time
import math

# ----------------------------
# CONFIG
# ----------------------------
API_KEY = "861e03a7b958c0290c80086dfde844de"

HEADERS = {
    "x-apisports-key": API_KEY
}

BASE_URL = "https://v3.football.api-sports.io"
COOLDOWN = 3600

# ----------------------------
# DESIGN
# ----------------------------
st.set_page_config(page_title="ODDFATHERS PRO", layout="wide")

st.markdown("""
<style>
body {background: linear-gradient(135deg,#020617,#0f172a);}
.title {text-align:center;font-size:50px;color:#22c55e;font-weight:bold;}
.card {
    background:#111827;
    padding:20px;
    border-radius:15px;
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🔥 ODDFATHERS PRO AI</div>', unsafe_allow_html=True)

# ----------------------------
# COOLDOWN SYSTEM
# ----------------------------
if "last_used" not in st.session_state:
    st.session_state.last_used = 0

def can_use():
    return time.time() - st.session_state.last_used > COOLDOWN

# ----------------------------
# API FUNCTIONS
# ----------------------------
@st.cache_data(ttl=300)
def get_matches():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    url = f"{BASE_URL}/fixtures?date={today}&timezone=Asia/Beirut"
    return requests.get(url, headers=HEADERS).json().get("response", [])

@st.cache_data(ttl=600)
def get_last(team_id):
    url = f"{BASE_URL}/fixtures?team={team_id}&last=10"
    return requests.get(url, headers=HEADERS).json().get("response", [])

# ----------------------------
# FIXED TEAM STATS (NEW)
# ----------------------------
def team_stats(team_id):
    matches = get_last(team_id)

    home_scored, home_conceded = [], []
    away_scored, away_conceded = [], []

    for m in matches:
        if m["teams"]["home"]["id"] == team_id:
            home_scored.append(m["goals"]["home"])
            home_conceded.append(m["goals"]["away"])
        else:
            away_scored.append(m["goals"]["away"])
            away_conceded.append(m["goals"]["home"])

    home_attack = sum(home_scored)/len(home_scored) if home_scored else 1.2
    home_defense = sum(home_conceded)/len(home_conceded) if home_conceded else 1.2

    away_attack = sum(away_scored)/len(away_scored) if away_scored else 1.2
    away_defense = sum(away_conceded)/len(away_conceded) if away_conceded else 1.2

    return home_attack, home_defense, away_attack, away_defense

# ----------------------------
# POISSON
# ----------------------------
def poisson(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

# ----------------------------
# FIXED PREDICTION (NEW)
# ----------------------------
def predict(t1_id, t2_id):

    t1_home_att, t1_home_def, t1_away_att, t1_away_def = team_stats(t1_id)
    t2_home_att, t2_home_def, t2_away_att, t2_away_def = team_stats(t2_id)

    league_avg = 1.4

    xg1 = (t1_home_att * t2_away_def) / league_avg + 0.3
    xg2 = (t2_away_att * t1_home_def) / league_avg

    probs = {}

    for i in range(6):
        for j in range(6):
            probs[(i, j)] = poisson(xg1, i) * poisson(xg2, j)

    home = sum(p for (i,j), p in probs.items() if i>j)
    draw = sum(p for (i,j), p in probs.items() if i==j)
    away = sum(p for (i,j), p in probs.items() if i<j)

    over25 = sum(p for (i,j), p in probs.items() if i+j>2)
    btts = sum(p for (i,j), p in probs.items() if i>0 and j>0)

    best_score = max(probs, key=probs.get)

    return {
        "score": f"{best_score[0]} - {best_score[1]}",
        "xg1": round(xg1,2),
        "xg2": round(xg2,2),
        "home": round(home*100,1),
        "draw": round(draw*100,1),
        "away": round(away*100,1),
        "over25": round(over25*100,1),
        "btts": round(btts*100,1)
    }

# ----------------------------
# LOAD MATCHES
# ----------------------------
matches = get_matches()

if not matches:
    st.error("No matches found today")
    st.stop()

options = [
    f"{m['league']['name']} | {m['teams']['home']['name']} vs {m['teams']['away']['name']}"
    for m in matches
]

selected = st.selectbox("Today's Matches", options)
match = matches[options.index(selected)]

t1 = match["teams"]["home"]
t2 = match["teams"]["away"]

# ----------------------------
# ANALYSIS
# ----------------------------
if st.button("🚀 RUN AI ANALYSIS"):

    if not can_use():
        st.error("Wait before next prediction")
        st.stop()

    st.session_state.last_used = time.time()

    pred = predict(t1["id"], t2["id"])

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"{t1['name']} vs {t2['name']}")
    st.write(f"⚽ Most Likely Score: {pred['score']}")
    st.write(f"xG: {pred['xg1']} - {pred['xg2']}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Match Probabilities")

    st.write(f"Home Win: {pred['home']}%")
    st.write(f"Draw: {pred['draw']}%")
    st.write(f"Away Win: {pred['away']}%")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Betting Markets")

    st.write(f"BTTS: {pred['btts']}%")
    st.write(f"Over 2.5 Goals: {pred['over25']}%")

    st.markdown('</div>', unsafe_allow_html=True)

   
