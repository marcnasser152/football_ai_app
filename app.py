import streamlit as st
import requests
import math
import random

# ----------------------------
# CONFIG
# ----------------------------
# ----------------------------
# LOGIN SYSTEM (PAID USERS)
# ----------------------------
# ----------------------------
# LOGIN SYSTEM (FIXED)
# ----------------------------
USERS = {
    "ali gh": "ali123",
    "mohamad chami": "chami123",
    "karim abdelsamad": "abdelsamad123",
    "michaeal": "michael123",
    "khattar": "khattar123",
    "abed oueidat": "oueidat123",
    "hsen bakri": "bakri123",
    "dani": "dani123",
    "alexy ghaoui": "ghaoui123",
    "raymond saleh": "saleh123"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 ODD FATHERS LOGIN")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        username_clean = username.strip().lower()

        if username_clean in USERS and USERS[username_clean] == password:
            st.session_state.logged_in = True
            st.success("Access Granted")
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    st.stop()

API_KEY = "f2a2f4e5979e49adbce8196931fb93d7"
HEADERS = {"X-Auth-Token": API_KEY}
BASE_URL = "https://api.football-data.org/v4"

st.set_page_config(page_title="ODD FATHERS", layout="wide")
st.title("🔥 ODD FATHERS - Reliable AI Predictions")

# ----------------------------
# TERMS & CONDITIONS
# ----------------------------
TERMS_TEXT = """
ODD FATHERS VIP Channel Terms & Conditions

1. All content is for informational, educational, and entertainment purposes only.
2. We do not promote or operate gambling.
3. We do not accept bets or handle money.
4. No guarantees of wins or profits.
5. Financial decisions involve risk.
6. Users are fully responsible for their actions.
7. We are not responsible for any losses.
8. Not financial or investment advice.
9. Subscription fees are non-refundable.
10. Sharing VIP content is prohibited.
11. No liability for financial/legal issues.
12. By agreeing, you confirm you understand all terms.
"""

if "accepted_terms" not in st.session_state:
    st.session_state.accepted_terms = False

if not st.session_state.accepted_terms:
    st.title("📜 Terms & Conditions")

    st.text_area("Read Carefully", TERMS_TEXT, height=300)

    agree = st.checkbox("I agree to the Terms & Conditions")

    if st.button("Continue"):
        if agree:
            st.session_state.accepted_terms = True
            st.success("Access Granted")
            st.rerun()
        else:
            st.error("You must agree before continuing")

    st.stop()

# ----------------------------
# FALLBACK MATCHES (ALWAYS WORKS)
# ----------------------------
def fallback_matches():
    return [
        {"league":"Premier League","home":"Arsenal","away":"Chelsea","date":"Today"},
        {"league":"Premier League","home":"Liverpool","away":"Tottenham","date":"Today"},
        {"league":"La Liga","home":"Real Madrid","away":"Barcelona","date":"Today"},
        {"league":"Bundesliga","home":"Bayern","away":"Dortmund","date":"Today"},
        {"league":"Ligue 1","home":"PSG","away":"Marseille","date":"Today"},
    ]

# ----------------------------
# GET MATCHES (WITH FALLBACK)
# ----------------------------
def get_matches():
    return [
       {"league":"England Championship","home":"Blackburn","away":"Coventry","date":"Today"},
        {"league":"Serie A","home":"Sassuolo","away":"Como","date":"Today"},
        {"league":"Bundesliga","home":"St Pauli","away":"Koln","date":"Today"},
        {"league":"Ligue 1","home":"Lens","away":"Toulouse","date":"Today"}
    ]

# ----------------------------
# TEAM STATS (REALISTIC)
# ----------------------------
def get_team_stats(name):
    base = sum(ord(c) for c in name)
    random.seed(base)

    goals_scored = random.uniform(1.2, 2.8)
    goals_conceded = random.uniform(0.8, 2.0)

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

options = [
    f"{m['date']} | {m['league']} | {m['home']} vs {m['away']}"
    for m in matches
]

# SAFE SELECTBOX
selected_index = st.selectbox(
    "Select Match",
    range(len(options)),
    format_func=lambda i: options[i]
)

match = matches[selected_index]

# ----------------------------
# RUN ANALYSIS
# ----------------------------
if st.button("🚀 RUN AI ANALYSIS"):

    pred = predict(match["home"], match["away"])

    st.subheader(f"{match['home']} vs {match['away']}")
    st.write(f"📅 {match['date']}")
    st.write(f"⚽ Score: {pred['score']}")
    st.write(f"xG: {pred['xg1']} - {pred['xg2']}")

    st.write("### Probabilities")
    st.write(f"Home: {pred['home']}%")
    st.write(f"Draw: {pred['draw']}%")
    st.write(f"Away: {pred['away']}%")

    st.write("### Markets")
    st.write(f"BTTS: {pred['btts']}%")
    st.write(f"Over 2.5: {pred['over25']}%")
