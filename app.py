import streamlit as st
import requests
from datetime import datetime
import time
import math

COOLDOWN = 3600

st.set_page_config(page_title="ODDFATHERS PRO", layout="wide")

st.markdown("""
<style>
body {background: linear-gradient(135deg,#020617,#0f172a);}
.title {text-align:center;font-size:50px;color:#22c55e;font-weight:bold;}
.card {background:#111827;padding:20px;border-radius:15px;margin-bottom:15px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🔥 ODDFATHERS PRO AI</div>', unsafe_allow_html=True)

# cooldown
if "last_used" not in st.session_state:
    st.session_state.last_used = 0

def can_use():
    return time.time() - st.session_state.last_used > COOLDOWN

# ----------------------------
# MATCHES (NO API KEY)
# ----------------------------
@st.cache_data(ttl=300)
def get_matches():
    today = datetime.now().strftime("%Y-%m-%d")

    url = f"https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d={today}&s=Soccer"
    res = requests.get(url).json()

    matches = res.get("events", [])

    # fallback if empty
    if not matches:
        url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=4328"
        res = requests.get(url).json()
        matches = res.get("events", [])

    return matches

# ----------------------------
# SIMPLE TEAM STRENGTH
# ----------------------------
def team_strength(name):
    base = sum(ord(c) for c in name) % 100
    attack = 1.2 + (base % 10) * 0.1
    defense = 1.0 + (base % 7) * 0.1
    return attack, defense

# ----------------------------
# POISSON
# ----------------------------
def poisson(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

# ----------------------------
# PREDICT
# ----------------------------
def predict(t1, t2):
    att1, def1 = team_strength(t1)
    att2, def2 = team_strength(t2)

    xg1 = (att1 * def2) / 1.5 + 0.4
    xg2 = (att2 * def1) / 1.5

    xg1 = max(0.2, xg1)
    xg2 = max(0.2, xg2)

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
        "btts": round(btts*100,1)
    }

# ----------------------------
# LOAD
# ----------------------------
matches = get_matches()

if not matches:
    st.error("Still no matches available")
    st.stop()

options = [
    f"{m['strLeague']} | {m['strHomeTeam']} vs {m['strAwayTeam']}"
    for m in matches
]

selected = st.selectbox("Matches", options)
match = matches[options.index(selected)]

t1 = match["strHomeTeam"]
t2 = match["strAwayTeam"]

# ----------------------------
# RUN
# ----------------------------
if st.button("🚀 RUN AI ANALYSIS"):

    if not can_use():
        st.error("Wait before next prediction")
        st.stop()

    st.session_state.last_used = time.time()

    pred = predict(t1, t2)

    st.subheader(f"{t1} vs {t2}")
    st.write(pred)
