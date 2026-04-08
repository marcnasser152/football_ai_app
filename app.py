import streamlit as st
import requests
import numpy as np

# -----------------------------
# CONFIG
# -----------------------------
API_KEY = "5e39f2e3f5ee4ed2862023b14e841588"
HEADERS = {"X-Auth-Token": API_KEY}
COMPETITION = "CL"

# -----------------------------
# GET TEAMS
# -----------------------------
def get_teams():
    url = f"https://api.football-data.org/v4/competitions/{COMPETITION}/teams"
    res = requests.get(url, headers=HEADERS)
    return res.json().get("teams", [])

# -----------------------------
# GET ALL MATCHES
# -----------------------------
def get_all_matches():
    url = f"https://api.football-data.org/v4/competitions/{COMPETITION}/matches"
    res = requests.get(url, headers=HEADERS)
    return res.json().get("matches", [])

# -----------------------------
# FILTER TEAM MATCHES
# -----------------------------
def get_team_matches(team_id, all_matches):
    team_matches = []

    for m in all_matches:
        if m["status"] != "FINISHED":
            continue

        if m["homeTeam"]["id"] == team_id or m["awayTeam"]["id"] == team_id:
            team_matches.append(m)

    return team_matches[-10:]  # last 10 matches

# -----------------------------
# COMPUTE STATS
# -----------------------------
def compute_team_stats(matches, team_id):
    gf, ga, games = 0, 0, 0

    for m in matches:
        if m["homeTeam"]["id"] == team_id:
            gf += m["score"]["fullTime"]["home"] or 0
            ga += m["score"]["fullTime"]["away"] or 0
        else:
            gf += m["score"]["fullTime"]["away"] or 0
            ga += m["score"]["fullTime"]["home"] or 0

        games += 1

    if games == 0:
        return [0.1, 0.1]  # avoid zero issues

    return [gf/games, ga/games]

# -----------------------------
# ADVANCED INSIGHTS
# -----------------------------
def advanced_predictions(t1, t2):
    t1_a, t1_d = t1
    t2_a, t2_d = t2

    t1_xg = (t1_a + t2_d) / 2
    t2_xg = (t2_a + t1_d) / 2

    total = t1_xg + t2_xg

    return {
        "t1_xg": t1_xg,
        "t2_xg": t2_xg,
        "total": total,
        "over25": total > 2.5,
        "btts": t1_xg > 0.8 and t2_xg > 0.8
    }

# -----------------------------
# REAL LOGIC PREDICTION
# -----------------------------
def predict(t1, t2):
    t1_attack, t1_def = t1
    t2_attack, t2_def = t2

    t1_score = t1_attack - t2_def
    t2_score = t2_attack - t1_def

    total = abs(t1_score) + abs(t2_score) + 1e-5

    home_prob = max(t1_score, 0) / total
    away_prob = max(t2_score, 0) / total
    draw_prob = 1 - (home_prob + away_prob)

    probs = [home_prob, draw_prob, away_prob]

    result = np.argmax(probs)

    return result, probs

# -----------------------------
# FAKE ODDS (for demo)
# -----------------------------
def get_odds():
    return {"home": 2.2, "draw": 3.1, "away": 2.7}

def value_bet(prob, odds):
    return {
        "home": prob[0]*odds["home"],
        "draw": prob[1]*odds["draw"],
        "away": prob[2]*odds["away"]
    }

# -----------------------------
# UI
# -----------------------------
st.set_page_config(layout="wide")
st.title("⚽ PRO Football Betting AI")

teams = get_teams()

if not teams:
    st.error("❌ API ERROR - Check your key")
    st.stop()

team_names = [t["name"] for t in teams]

col1, col2 = st.columns(2)
team1 = col1.selectbox("Team 1", team_names)
team2 = col2.selectbox("Team 2", team_names)

if team1 == team2:
    st.warning("⚠️ Select different teams")

if st.button("🚀 Analyze Match"):

    with st.spinner("Running analysis..."):

        t1_id = [t["id"] for t in teams if t["name"] == team1][0]
        t2_id = [t["id"] for t in teams if t["name"] == team2][0]

        all_matches = get_all_matches()

        m1 = get_team_matches(t1_id, all_matches)
        m2 = get_team_matches(t2_id, all_matches)

        f1 = compute_team_stats(m1, t1_id)
        f2 = compute_team_stats(m2, t2_id)

        result, prob = predict(f1, f2)
        adv = advanced_predictions(f1, f2)

        odds = get_odds()
        value = value_bet(prob, odds)

    outcomes = ["Home Win", "Draw", "Away Win"]

    # -----------------------------
    # DASHBOARD
    # -----------------------------
    st.markdown("## 🎯 AI Verdict")

    best = np.argmax(prob)
    confidence = prob[best] * 100

    st.markdown(f"""
    ### {team1} vs {team2}
    ### 🔥 Prediction: **{outcomes[result]}**
    ### 📊 Confidence: **{confidence:.1f}%**
    """)

    # Probabilities
    st.markdown("## 📊 Probabilities")

    c1, c2, c3 = st.columns(3)
    c1.metric("Home", f"{prob[0]*100:.1f}%")
    c2.metric("Draw", f"{prob[1]*100:.1f}%")
    c3.metric("Away", f"{prob[2]*100:.1f}%")

    # Value betting
    st.markdown("## 💰 Value Betting")

    value_pick = max(value, key=value.get)

    if value[value_pick] > 1:
        st.success(f"🔥 VALUE BET: {value_pick.upper()}")
    else:
        st.warning("⚠️ No value bet")

    # Insights
    st.markdown("## ⚽ Match Insights")

    st.write(f"xG: {adv['t1_xg']:.2f} - {adv['t2_xg']:.2f}")
    st.write("Over 2.5:", "✅" if adv["over25"] else "❌")
    st.write("BTTS:", "✅" if adv["btts"] else "❌")

    # Final decision
    st.markdown("## 🧠 Final Decision")

    if confidence > 60 and value[value_pick] > 1:
        st.success("💸 STRONG BET")
    elif confidence > 50:
        st.info("📊 MEDIUM CONFIDENCE")
    else:
        st.error("❌ AVOID")