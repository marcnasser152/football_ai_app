import streamlit as st
import requests
from datetime import datetime
import time
import math

# ----------------------------
# CONFIG
# ----------------------------
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
# COOLDOWN
# ----------------------------
if "last_used" not in st.session_state:
    st.session_state.last_used = 0

def can_use():
    return time.time() - st.session_state.last_used > COOLDOWN

# ----------------------------
# GET MATCHES (TheSportsDB)
# ----------------------------
@st.cache_data(ttl=300)
def get_matches():
    today = datetime.now().strftime("%Y-%m-%d")
    
    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today}&s=Soccer"
    res = requests.get(url).json()
    
    return res.get("events", [])

# ----------------------------
# SIMPLE TEAM STRENGTH (NAME BASED)
# ----------------------------
def team_strength(team_name):
    # fake variability based on name hash (to differentiate teams)
    base = sum(ord(c) for c in team_name) % 100
    
    attack = 1.2 + (base % 10) * 0.1
    defense = 1.0 + (base % 7) * 0.1
    
    return attack, defense

# ----------------------------
# POISSON
# ----------------------------
def poisson(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

# ----------------------------
# PREDICTION
# ----------------------------
def predict(team1, team2):

    att1, def1 = team_strength(team1)
    att2, def2 = team_strength(team2)

    xg1 = (att1 * def2) / 1.5 + 0.3
    xg2 = (att2 * def1) / 1.5

    xg1 = max(0.3, xg1)
    xg2 = max(0.3, xg2)

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
        "home": round(home*100,1),
        "draw": round(draw*100,1),
        "away": round(away*100,1),
        "over25": round(over25*100,1),
        "btts": round(btts*100,1),
        "xg1": round(xg1,2),
        "xg2": round(xg2,2)
    }

# ----------------------------
# LOAD MATCHES
# ----------------------------
matches = get_matches()

if not matches:
    st.error("No matches found (API issue)")
    st.stop()

options = [
    f"{m['strLeague']} | {m['strHomeTeam']} vs {m['strAwayTeam']}"
    for m in matches
]

selected = st.selectbox("Today's Matches", options)
match = matches[options.index(selected)]

team1 = match["strHomeTeam"]
team2 = match["strAwayTeam"]

# ----------------------------
# ANALYSIS
# ----------------------------
if st.button("🚀 RUN AI ANALYSIS"):

    if not can_use():
        st.error("Wait before next prediction")
        st.stop()

    st.session_state.last_used = time.time()

    pred = predict(team1, team2)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"{team1} vs {team2}")
    st.write(f"⚽ Score: {pred['score']}")
    st.write(f"xG: {pred['xg1']} - {pred['xg2']}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Probabilities")

    st.write(f"Home: {pred['home']}%")
    st.write(f"Draw: {pred['draw']}%")
    st.write(f"Away: {pred['away']}%")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Markets")

    st.write(f"BTTS: {pred['btts']}%")
    st.write(f"Over 2.5: {pred['over25']}%")

    st.markdown('</div>', unsafe_allow_html=True)
