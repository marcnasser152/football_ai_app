import streamlit as st
import random
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

# ----------------------------
# COOLDOWN
# ----------------------------
if "last_used" not in st.session_state:
    st.session_state.last_used = 0

def can_use():
    return time.time() - st.session_state.last_used > COOLDOWN

# ----------------------------
# BIG LEAGUES MATCH GENERATOR
# ----------------------------
def generate_matches():
    leagues = {
        "Premier League": [
            ("Arsenal", "Chelsea"),
            ("Liverpool", "Tottenham"),
            ("Man City", "Man United"),
        ],
        "La Liga": [
            ("Real Madrid", "Valencia"),
            ("Barcelona", "Sevilla"),
            ("Atletico Madrid", "Villarreal"),
        ],
        "Serie A": [
            ("Juventus", "Roma"),
            ("Inter", "Milan"),
            ("Napoli", "Lazio"),
        ],
        "Bundesliga": [
            ("Bayern Munich", "Dortmund"),
            ("Leipzig", "Leverkusen"),
            ("Frankfurt", "Stuttgart"),
        ]
    }

    matches = []
    for league, games in leagues.items():
        for home, away in games:
            matches.append({
                "league": league,
                "home": home,
                "away": away
            })

    return matches

# ----------------------------
# TEAM STRENGTH (DIFFERENT FOR EACH TEAM)
# ----------------------------
def team_strength(name):
    base = sum(ord(c) for c in name)

    random.seed(base)  # ensures consistency per team

    attack = random.uniform(1.2, 2.5)
    defense = random.uniform(0.8, 1.8)

    return attack, defense

# ----------------------------
# POISSON
# ----------------------------
def poisson(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)

# ----------------------------
# PREDICTION ENGINE
# ----------------------------
def predict(team1, team2):

    att1, def1 = team_strength(team1)
    att2, def2 = team_strength(team2)

    xg1 = (att1 * def2) / 1.5 + 0.4
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
# LOAD MATCHES
# ----------------------------
matches = generate_matches()

options = [
    f"{m['league']} | {m['home']} vs {m['away']}"
    for m in matches
]

selected = st.selectbox("Top Matches Today", options)
match = matches[options.index(selected)]

# ----------------------------
# ANALYSIS
# ----------------------------
if st.button("🚀 RUN AI ANALYSIS"):

    if not can_use():
        st.error("Wait before next prediction")
        st.stop()

    st.session_state.last_used = time.time()

    pred = predict(match["home"], match["away"])

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"{match['home']} vs {match['away']}")
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

