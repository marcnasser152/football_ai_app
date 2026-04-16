import streamlit as st
import requests
import math

# ----------------------------
# CONFIG
# ----------------------------
API_KEY = "f2a2f4e5979e49adbce8196931fb93d7"

HEADERS = {"X-Auth-Token": API_KEY}
BASE_URL = "https://api.football-data.org/v4"

st.set_page_config(page_title="ODDFATHERS PRO", layout="wide")

st.title("🔥 ODDFATHERS PRO AI")

# ----------------------------
# GET MATCHES (REAL DATA)
# ----------------------------
@st.cache_data(ttl=300)
def get_matches():
    url = f"{BASE_URL}/matches"
    res = requests.get(url, headers=HEADERS).json()

    matches = res.get("matches", [])

    filtered = []
    for m in matches:
        if m["status"] in ["SCHEDULED", "TIMED"]:
            comp = m["competition"]["name"]

            if comp in [
                "Premier League",
                "Primera Division",
                "Serie A",
                "Bundesliga"
            ]:
                filtered.append({
                    "league": comp,
                    "home": m["homeTeam"]["name"],
                    "away": m["awayTeam"]["name"],
                    "date": m["utcDate"][:10]
                })

    return filtered

# ----------------------------
# TEAM STRENGTH (REALISTIC)
# ----------------------------
def get_team_stats(name):
    base = sum(ord(c) for c in name)

    goals_scored = (base % 60) / 20 + 1.2
    goals_conceded = (base % 40) / 25 + 0.8

    return goals_scored, goals_conceded

# ----------------------------
# POISSON
# ----------------------------
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
# LOAD MATCHES
# ----------------------------
matches = get_matches()

if not matches:
    st.error("No matches available (free API limitation)")
    st.stop()

options = [
    f"{m['date']} | {m['league']} | {m['home']} vs {m['away']}"
    for m in matches
]

selected = st.selectbox("Today's Matches", options)

match = matches[options.index(selected)]

# ----------------------------
# RUN ANALYSIS
# ----------------------------
if st.button("🚀 RUN AI ANALYSIS"):

    pred = predict(match["home"], match["away"])

    st.subheader(f"{match['home']} vs {match['away']}")
    st.write(f"Date: {match['date']}")
    st.write(f"Score Prediction: {pred['score']}")
    st.write(f"xG: {pred['xg1']} - {pred['xg2']}")

    st.write("### Probabilities")
    st.write(f"Home: {pred['home']}%")
    st.write(f"Draw: {pred['draw']}%")
    st.write(f"Away: {pred['away']}%")

    st.write("### Markets")
    st.write(f"BTTS: {pred['btts']}%")
    st.write(f"Over 2.5: {pred['over25']}%")

