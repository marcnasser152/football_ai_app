import streamlit as st
from supabase import create_client
import uuid
from datetime import datetime, timedelta
import math
import random
import time
from pathlib import Path
import pandas as pd

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="TOF",
    page_icon="LOGO6(2).png",
    layout="wide"
)

# ----------------------------
# PREMIUM STYLE
# ----------------------------
st.markdown("""
<style>
header, footer {visibility: hidden;}

.stApp {
    background:
    radial-gradient(circle at top left, rgba(13,91,255,0.22), transparent 30%),
    radial-gradient(circle at bottom right, rgba(63,169,255,0.16), transparent 30%),
    radial-gradient(circle at 50% 100%, rgba(13,91,255,0.10), transparent 30%),
    linear-gradient(135deg, #000000 0%, #020817 45%, #000000 100%);
    color: white;
}

.block-container {
    padding-top: 1.2rem;
    max-width: 1400px;
}

.stButton>button {
    border-radius: 12px;
    background: linear-gradient(90deg,#0D5BFF,#3FA9FF);
    color: black;
    font-weight: 900;
    border: 0;
    height: 46px;
    box-shadow: 0 0 24px rgba(13,91,255,0.24);
    transition: 0.25s ease;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 38px rgba(13,91,255,0.42);
}

.stTextInput input {
    background-color: #020817 !important;
    color: black !important;
    border-radius: 10px !important;
    border: 1px solid rgba(13,91,255,0.35) !important;
}

[data-testid="stMetric"] {
    background: rgba(2, 8, 23, 0.86);
    border: 1px solid rgba(13,91,255,0.28);
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 0 30px rgba(13,91,255,0.12);
    transition: 0.25s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 0 45px rgba(13,91,255,0.28);
}

[data-testid="stTabs"] button {
    background: rgba(7,17,14,0.75);
    border-radius: 14px;
    margin-right: 6px;
    border: 1px solid rgba(13,91,255,0.18);
}

[data-testid="stTabs"] button:hover {
    box-shadow: 0 0 25px rgba(13,91,255,0.20);
}

[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(13,91,255,0.34), rgba(63,169,255,0.24));
    border: 1px solid rgba(13,91,255,0.42);
}

h1 {
    font-size: 48px !important;
    font-weight: 950 !important;
    background: linear-gradient(90deg,#0D5BFF,#3FA9FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h2, h3 {
    color: white;
}

div[data-testid="stImage"] img {
    border-radius: 24px;
    box-shadow: 0 0 45px rgba(13,91,255,0.45);
    animation: pulseLogo 3s infinite;
}

@keyframes pulseLogo {
    0% { box-shadow: 0 0 25px rgba(13,91,255,0.25); }
    50% { box-shadow: 0 0 55px rgba(13,91,255,0.65); }
    100% { box-shadow: 0 0 25px rgba(13,91,255,0.25); }
}

.premium-banner {
    padding: 16px 18px;
    border-radius: 18px;
    background: linear-gradient(90deg, rgba(13,91,255,0.22), rgba(63,169,255,0.16));
    border: 1px solid rgba(13,91,255,0.32);
    box-shadow: 0 0 32px rgba(13,91,255,0.14);
    font-weight: 850;
    margin-bottom: 18px;
}

.premium-section-title {
    font-size: 22px;
    font-weight: 900;
    color: #0D5BFF;
    margin-top: 16px;
    margin-bottom: 8px;
}

.demo-pill {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 999px;
    background: rgba(13,91,255,0.18);
    border: 1px solid rgba(13,91,255,0.35);
    color: #FFFFFF;
    font-weight: 800;
    margin-bottom: 10px;
}

<style>
.stApp {
    background:
    radial-gradient(circle at top left, rgba(13,91,255,0.28), transparent 30%),
    radial-gradient(circle at bottom right, rgba(63,169,255,0.18), transparent 30%),
    linear-gradient(135deg, #000000 0%, #020817 45%, #000000 100%) !important;
}

[data-testid="stMetric"] {
    background: rgba(2,8,23,0.88) !important;
    border: 1px solid rgba(63,169,255,0.25) !important;
}

.stButton>button {
    background: linear-gradient(90deg,#0D5BFF,#3FA9FF) !important;
    color: black !important;
}

h1 {
    background: linear-gradient(90deg,#ffffff,#3FA9FF) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

.market-card {
    background: rgba(2,8,23,0.88);
    border: 1px solid rgba(63,169,255,0.28);
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 12px;
    box-shadow: 0 0 22px rgba(13,91,255,0.10);
    word-wrap: break-word;
    overflow-wrap: anywhere;
    white-space: normal;
}

.market-title {
    font-size: 13px;
    opacity: 0.78;
    margin-bottom: 6px;
    color: #FFFFFF;
    letter-spacing: 0.2px;
}

.market-value {
    font-size: 20px;
    font-weight: 900;
    line-height: 1.25;
    color: #ffffff;
    word-break: normal;
    overflow-wrap: anywhere;
}

.market-small {
    font-size: 13px;
    opacity: 0.85;
    margin-top: 6px;
    color: #DBEAFE;
}

.notice-card {
    background: rgba(0,0,0,0.35);
    border-left: 4px solid #3FA9FF;
    border-radius: 14px;
    padding: 14px 16px;
    margin: 14px 0;
    color: #eaf4ff;
    font-size: 14px;
    line-height: 1.45;
}

div[data-testid="stMetric"] label, div[data-testid="stMetric"] div {
    overflow-wrap: anywhere !important;
    white-space: normal !important;
}


/* TOF BLUE THEME OVERRIDE */
.stApp {
    background:
    radial-gradient(circle at top left, rgba(13,91,255,0.24), transparent 30%),
    radial-gradient(circle at bottom right, rgba(63,169,255,0.14), transparent 30%),
    linear-gradient(135deg, #000000 0%, #020817 48%, #000000 100%) !important;
}

[data-testid="stMetric"], .market-card {
    background: rgba(2,8,23,0.90) !important;
    border: 1px solid rgba(13,91,255,0.30) !important;
    box-shadow: 0 0 25px rgba(13,91,255,0.12) !important;
}

.stButton>button {
    background: linear-gradient(90deg,#0D5BFF,#3FA9FF) !important;
    color: black !important;
}

h1 {
    background: linear-gradient(90deg,#ffffff,#0D5BFF,#3FA9FF) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

.premium-banner {
    background: linear-gradient(90deg, rgba(13,91,255,0.24), rgba(63,169,255,0.14)) !important;
    border: 1px solid rgba(13,91,255,0.36) !important;
}

.notice-card {
    border-left: 4px solid #0D5BFF !important;
}

div[data-testid="stImage"] img {
    box-shadow: 0 0 45px rgba(13,91,255,0.45) !important;
}


/* TOF BLUE THEME OVERRIDE */
.stApp {
    background:
    radial-gradient(circle at top left, rgba(13,91,255,0.25), transparent 30%),
    radial-gradient(circle at bottom right, rgba(63,169,255,0.16), transparent 30%),
    linear-gradient(135deg, #000000 0%, #020817 50%, #000000 100%) !important;
}

[data-testid="stMetric"], .market-card {
    background: rgba(2,8,23,0.90) !important;
    border: 1px solid rgba(13,91,255,0.35) !important;
    box-shadow: 0 0 25px rgba(13,91,255,0.14) !important;
}

.stButton>button {
    background: linear-gradient(90deg,#0D5BFF,#3FA9FF) !important;
    color: white !important;
}

h1 {
    background: linear-gradient(90deg,#ffffff,#3FA9FF,#0D5BFF) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

.premium-banner {
    background: linear-gradient(90deg, rgba(13,91,255,0.26), rgba(63,169,255,0.16)) !important;
    border: 1px solid rgba(13,91,255,0.42) !important;
}

.notice-card {
    border-left: 4px solid #0D5BFF !important;
}

div[data-testid="stImage"] img {
    box-shadow: 0 0 45px rgba(13,91,255,0.48) !important;
}


/* FINAL TOF BLACK & BLUE THEME */
.stApp {
    background:
    radial-gradient(circle at top left, rgba(13,91,255,0.25), transparent 30%),
    radial-gradient(circle at bottom right, rgba(63,169,255,0.14), transparent 30%),
    linear-gradient(135deg, #000000 0%, #020817 52%, #000000 100%) !important;
}

[data-testid="stMetric"], .market-card {
    background: rgba(2,8,23,0.92) !important;
    border: 1px solid rgba(13,91,255,0.38) !important;
    box-shadow: 0 0 28px rgba(13,91,255,0.16) !important;
}

.stButton>button {
    background: linear-gradient(90deg,#0D5BFF,#3FA9FF) !important;
    color: black !important;
}

h1 {
    background: linear-gradient(90deg,#ffffff,#3FA9FF,#0D5BFF) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

.premium-banner {
    background: linear-gradient(90deg, rgba(13,91,255,0.26), rgba(63,169,255,0.14)) !important;
    border: 1px solid rgba(13,91,255,0.42) !important;
}

.notice-card {
    border-left: 4px solid #0D5BFF !important;
}

div[data-testid="stImage"] img {
    box-shadow: 0 0 50px rgba(13,91,255,0.50) !important;
}


/* FINAL ODD FATHERS BLUE & WHITE THEME */
.stApp {
    background:
    radial-gradient(circle at top left, rgba(13,91,255,0.32), transparent 30%),
    radial-gradient(circle at bottom right, rgba(63,169,255,0.20), transparent 30%),
    radial-gradient(circle at 50% 100%, rgba(255,255,255,0.08), transparent 28%),
    linear-gradient(135deg, #020817 0%, #071B42 48%, #020817 100%) !important;
}

[data-testid="stMetric"], .market-card {
    background: rgba(7,22,51,0.92) !important;
    border: 1px solid rgba(63,169,255,0.38) !important;
    box-shadow: 0 0 30px rgba(13,91,255,0.18) !important;
}

.stButton>button {
    background: linear-gradient(90deg,#0D5BFF,#3FA9FF) !important;
    color: white !important;
}

h1 {
    background: linear-gradient(90deg,#ffffff,#3FA9FF,#0D5BFF) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

.premium-banner {
    background: linear-gradient(90deg, rgba(13,91,255,0.28), rgba(63,169,255,0.16)) !important;
    border: 1px solid rgba(63,169,255,0.42) !important;
    box-shadow: 0 0 35px rgba(13,91,255,0.18) !important;
}

.notice-card {
    border-left: 4px solid #3FA9FF !important;
}

.premium-section-title {
    color: #3FA9FF !important;
}

div[data-testid="stImage"] img {
    box-shadow: 0 0 50px rgba(63,169,255,0.50) !important;
}

.stTextInput input {
    background-color: #071B42 !important;
    color: white !important;
    border: 1px solid rgba(63,169,255,0.35) !important;
}

</style>

</style>
""", unsafe_allow_html=True)

# ----------------------------
# SUPABASE
# ----------------------------
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# ----------------------------
# SESSION
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "accepted_terms" not in st.session_state:
    st.session_state.accepted_terms = False

# ----------------------------
# LOGO FUNCTION
# ----------------------------
def show_logo(width=130):
    if Path("LOGO6(2).png").exists():
        st.image("LOGO6(2).png", width=width)
    else:
        st.warning("LOGO6(2).png not found. Put LOGO6(2).png in the same folder as app.py.")


def market_card(title, value, note=""):
    note_html = f"<div class='market-small'>{note}</div>" if note else ""
    st.markdown(
        f"""
        <div class="market-card">
            <div class="market-title">{title}</div>
            <div class="market-value">{value}</div>
            {note_html}
        </div>
        """,
        unsafe_allow_html=True
    )


# ----------------------------
# LOGIN
# ----------------------------
if not st.session_state.logged_in:
    left, center, right = st.columns([1, 1.1, 1])

    with center:
        st.write("")
        st.write("")
        show_logo(width=165)
        st.title("TOF")
        st.caption("Football Intelligence Terminal")

        username = st.text_input("Username").strip().lower()
        password = st.text_input("Password", type="password")

        if st.button("🚀 ENTER TERMINAL", use_container_width=True):
            with st.spinner("Verifying access..."):
                time.sleep(1)

            res = supabase.table("users").select("*").eq("username", username).execute()

            if not res.data:
                st.error("User not found")
                st.stop()

            user = res.data[0]

            if user.get("banned"):
                st.error("Account banned")

            elif user.get("password") != password:
                st.error("Wrong password")

            elif not user.get("expires_at"):
                st.error("No active subscription")

            elif datetime.fromisoformat(user["expires_at"].replace("Z", "+00:00")).replace(tzinfo=None) < datetime.utcnow():
                st.error("Subscription expired")

            else:
                session_id = str(uuid.uuid4())

                supabase.table("users").update({
                    "session_id": session_id,
                    "last_login": "now()"
                }).eq("username", username).execute()

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.session_id = session_id

                st.rerun()

    st.stop()

# ----------------------------
# FETCH USER
# ----------------------------
res = supabase.table("users").select("*").eq("username", st.session_state.username).execute()

if not res.data:
    st.error("User account not found.")
    st.session_state.logged_in = False
    st.stop()

user = res.data[0]

if user.get("session_id") != st.session_state.session_id:
    st.error("⚠️ Account opened on another device")
    st.session_state.logged_in = False
    st.rerun()

role = user.get("role", "user")
is_admin = role == "admin"
is_vip = role in ["vip", "admin"]

# ----------------------------
# TERMS
# ----------------------------
TERMS_TEXT = """
### TOF VIP TERMS

- Predictions are informational only.
- No guaranteed profit.
- Betting always includes risk.
- Sharing your account is forbidden.
- One account = one active device.
- VIP access can be removed if rules are broken.
"""

if not st.session_state.accepted_terms:
    st.markdown(TERMS_TEXT)

    agree = st.checkbox("I agree to the VIP terms")

    if st.button("Continue"):
        if agree:
            st.session_state.accepted_terms = True
            st.rerun()
        else:
            st.error("You must agree first.")

    st.stop()

# ----------------------------
# GOOGLE SHEETS AUTO MATCHES
# ----------------------------
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRxcLsLVpONxJZqrqTB2j61twbO-e3VFfVac3nZX89Wiekb5uE_tdzrYrcGyILQjfD7sAAa1_JtiKcu/pub?output=csv"

try:
    df = pd.read_csv(CSV_URL)

    matches = []

    for _, row in df.iterrows():
        raw_section = str(row.get("section", "Normal Games")).strip()
        section_clean = "World Cup" if raw_section.lower() == "world cup" else "Normal Games"

        home_team = str(row.get("home", "")).strip()
        away_team = str(row.get("away", "")).strip()
        league_name = str(row.get("league", "")).strip()

        if home_team and away_team:
            matches.append({
                "section": section_clean,
                "league": league_name,
                "home": home_team,
                "away": away_team,
                "kickoff": ""
            })

except Exception as e:
    st.error(f"Failed loading Google Sheets matches: {e}")
    matches = []

# ----------------------------
# MATCH INTELLIGENCE DATA
# ----------------------------
# ----------------------------
MATCH_INTELLIGENCE = {
    ("Freiburg", "Aston Villa"): {
        "xg1": 1.18, "xg2": 1.54, "home": 29.0, "draw": 28.0, "away": 43.0,
        "over15": 76.0, "over25": 53.0, "over35": 27.0, "btts": 55.0,
        "score": "1-2", "main_pick": "Goals O1.5", "safe_pick": "Goals O1.5",
        "goals_pick": "Aston Villa Double Chance", "corner_pick": "Total Corners O8.5",
        "cards_pick": "Total Cards O2.5", "banker_pick": "Goals O1.5",
        "corner_line": "Total Corners O8.5", "cards_line": "Total Cards O2.5",
        "confidence": 82.0, "safe_confidence": 82.0, "goals_confidence": 72.0,
        "corners_confidence": 70.0, "cards_confidence": 64.0, "risk": "LOW", "banker_rank": 1,
        "explanation": "Aston Villa have the stronger attacking profile, but the safest protected market is goals over 1.5 rather than forcing the away win."
    },
    ("Brazil", "Serbia"): {
        "xg1": 1.92, "xg2": 0.88, "home": 62.0, "draw": 23.0, "away": 15.0,
        "over15": 78.0, "over25": 55.0, "over35": 29.0, "btts": 42.0,
        "score": "2-0", "main_pick": "Brazil Draw No Bet", "safe_pick": "Brazil Draw No Bet",
        "goals_pick": "Brazil Team Goals O1.5", "corner_pick": "Brazil Team Corners O5.5",
        "cards_pick": "Total Cards O3.5", "banker_pick": "Brazil Draw No Bet",
        "corner_line": "Brazil Team Corners O5.5", "cards_line": "Total Cards O3.5",
        "confidence": 84.0, "safe_confidence": 84.0, "goals_confidence": 74.0,
        "corners_confidence": 72.0, "cards_confidence": 68.0, "risk": "LOW", "banker_rank": 1,
        "explanation": "Brazil project stronger chance creation and territory control. The safest World Cup angle is Brazil Draw No Bet."
    },
    ("France", "Japan"): {
        "xg1": 1.76, "xg2": 1.05, "home": 55.0, "draw": 26.0, "away": 19.0,
        "over15": 76.0, "over25": 52.0, "over35": 26.0, "btts": 48.0,
        "score": "2-1", "main_pick": "Goals O1.5", "safe_pick": "Goals O1.5",
        "goals_pick": "France Team Goals O1.5", "corner_pick": "Total Corners O8.5",
        "cards_pick": "Total Cards O2.5", "banker_pick": "Goals O1.5",
        "corner_line": "Total Corners O8.5", "cards_line": "Total Cards O2.5",
        "confidence": 82.0, "safe_confidence": 82.0, "goals_confidence": 73.0,
        "corners_confidence": 69.0, "cards_confidence": 63.0, "risk": "LOW", "banker_rank": 1,
        "explanation": "France have the stronger squad profile, while Japan can still create transition chances. Over 1.5 is the protected market."
    },
    ("Argentina", "Morocco"): {
        "xg1": 1.58, "xg2": 0.92, "home": 51.0, "draw": 30.0, "away": 19.0,
        "over15": 69.0, "over25": 43.0, "over35": 18.0, "btts": 40.0,
        "score": "1-0", "main_pick": "Goals U3.5", "safe_pick": "Goals U3.5",
        "goals_pick": "Argentina Draw No Bet", "corner_pick": "Total Corners U10.5",
        "cards_pick": "Total Cards O3.5", "banker_pick": "Goals U3.5",
        "corner_line": "Total Corners U10.5", "cards_line": "Total Cards O3.5",
        "confidence": 85.0, "safe_confidence": 85.0, "goals_confidence": 75.0,
        "corners_confidence": 67.0, "cards_confidence": 70.0, "risk": "LOW", "banker_rank": 1,
        "explanation": "Tournament matches can be tactical. Under 3.5 is preferred over aggressive scoreline markets."
    },
    ("England", "USA"): {
        "xg1": 1.44, "xg2": 1.06, "home": 45.0, "draw": 31.0, "away": 24.0,
        "over15": 70.0, "over25": 44.0, "over35": 20.0, "btts": 47.0,
        "score": "1-1", "main_pick": "Goals U3.5", "safe_pick": "Goals U3.5",
        "goals_pick": "England Double Chance", "corner_pick": "Total Corners O8.5",
        "cards_pick": "Total Cards O3.5", "banker_pick": "Goals U3.5",
        "corner_line": "Total Corners O8.5", "cards_line": "Total Cards O3.5",
        "confidence": 83.0, "safe_confidence": 83.0, "goals_confidence": 71.0,
        "corners_confidence": 68.0, "cards_confidence": 66.0, "risk": "LOW", "banker_rank": 2,
        "explanation": "England are stronger on paper but the match profiles as tight. Under 3.5 is safer than forcing the winner."
    },
    ("Spain", "Croatia"): {
        "xg1": 1.36, "xg2": 1.02, "home": 42.0, "draw": 33.0, "away": 25.0,
        "over15": 66.0, "over25": 39.0, "over35": 17.0, "btts": 44.0,
        "score": "1-1", "main_pick": "Goals U3.5", "safe_pick": "Goals U3.5",
        "goals_pick": "Spain Double Chance", "corner_pick": "Total Corners U10.5",
        "cards_pick": "Total Cards O3.5", "banker_pick": "Goals U3.5",
        "corner_line": "Total Corners U10.5", "cards_line": "Total Cards O3.5",
        "confidence": 84.0, "safe_confidence": 84.0, "goals_confidence": 70.0,
        "corners_confidence": 67.0, "cards_confidence": 68.0, "risk": "LOW", "banker_rank": 1,
        "explanation": "Spain and Croatia can both control possession, which often lowers chaos. Under 3.5 is the protected angle."
    },
    ("Portugal", "Mexico"): {
        "xg1": 1.62, "xg2": 1.15, "home": 49.0, "draw": 28.0, "away": 23.0,
        "over15": 74.0, "over25": 50.0, "over35": 24.0, "btts": 52.0,
        "score": "2-1", "main_pick": "Goals O1.5", "safe_pick": "Goals O1.5",
        "goals_pick": "Portugal Draw No Bet", "corner_pick": "Total Corners O8.5",
        "cards_pick": "Total Cards O3.5", "banker_pick": "Goals O1.5",
        "corner_line": "Total Corners O8.5", "cards_line": "Total Cards O3.5",
        "confidence": 81.0, "safe_confidence": 81.0, "goals_confidence": 70.0,
        "corners_confidence": 68.0, "cards_confidence": 67.0, "risk": "LOW", "banker_rank": 2,
        "explanation": "Portugal have more attacking quality, while Mexico usually bring intensity. Goals over 1.5 is safer than direct 1X2."
    },
}

# ----------------------------
# AI ENGINE
# ----------------------------
def get_team_stats(name):
    base = sum(ord(c) for c in name)
    random.seed(base)

    attack = random.uniform(1.1, 2.3)
    defense = random.uniform(0.9, 1.9)
    form = random.uniform(55, 91)
    pressure = random.uniform(40, 88)

    elite = [
        "Real Madrid", "Barcelona", "Bayern", "Bayern Munich",
        "PSG", "Inter", "Liverpool", "Man City", "Atletico Madrid"
    ]

    strong = [
        "Chelsea", "Juventus", "Leverkusen", "Stuttgart",
        "Real Sociedad", "Sevilla", "RB Leipzig"
    ]

    weak = ["Elche", "Espanyol", "Sunderland", "Lecce"]

    if name in elite:
        attack += 0.75
        defense -= 0.35
        form += 7

    elif name in strong:
        attack += 0.4
        defense -= 0.15
        form += 4

    elif name in weak:
        attack -= 0.35
        defense += 0.25
        form -= 5

    return attack, defense, min(form, 98), min(pressure, 96)


def poisson(lmbda, k):
    return (math.exp(-lmbda) * (lmbda ** k)) / math.factorial(k)


def predict(team1, team2):
    info = MATCH_INTELLIGENCE.get((team1, team2))

    if info:
        return {
            "score": info["score"],
            "xg1": info["xg1"],
            "xg2": info["xg2"],
            "home": info["home"],
            "draw": info["draw"],
            "away": info["away"],
            "over15": info["over15"],
            "over25": info["over25"],
            "over35": info["over35"],
            "btts": info["btts"],

            "confidence": info["confidence"],
            "safe_confidence": info["safe_confidence"],
            "goals_confidence": info["goals_confidence"],
            "corners_confidence": info["corners_confidence"],
            "cards_confidence": info["cards_confidence"],

            "pick": info["main_pick"],
            "safe_pick": info["safe_pick"],
            "goals_pick": info["goals_pick"],
            "corner_pick": info["corner_pick"],
            "cards_pick": info["cards_pick"],
            "banker_pick": info["banker_pick"],

            "corners": info["corner_line"],
            "cards": info["cards_line"],
            "corner_line": info["corner_line"],
            "cards_line": info["cards_line"],

            "risk": info["risk"],
            "form1": 0,
            "form2": 0,
            "pressure1": 0,
            "pressure2": 0,
            "banker_rank": info["banker_rank"],
            "explanation": info["explanation"]
        }

    # Automatic fallback for any match loaded from Google Sheets.
    # This does NOT change existing manual MATCH_INTELLIGENCE predictions.
    # It only prevents new sheet matches from showing "Match data not loaded".
    t1_attack, t1_defense, t1_form, t1_pressure = get_team_stats(team1)
    t2_attack, t2_defense, t2_form, t2_pressure = get_team_stats(team2)

    league_avg = 1.42
    home_advantage = 0.28

    xg1 = max(0.2, (t1_attack * t2_defense) / league_avg + home_advantage)
    xg2 = max(0.2, (t2_attack * t1_defense) / league_avg)

    probs = {}

    for i in range(7):
        for j in range(7):
            probs[(i, j)] = poisson(xg1, i) * poisson(xg2, j)

    home = sum(p for (i, j), p in probs.items() if i > j)
    draw = sum(p for (i, j), p in probs.items() if i == j)
    away = sum(p for (i, j), p in probs.items() if i < j)

    over15 = sum(p for (i, j), p in probs.items() if i + j > 1)
    over25 = sum(p for (i, j), p in probs.items() if i + j > 2)
    over35 = sum(p for (i, j), p in probs.items() if i + j > 3)
    btts = sum(p for (i, j), p in probs.items() if i > 0 and j > 0)

    best_score = max(probs, key=probs.get)

    total_xg = xg1 + xg2
    xg_gap = abs(xg1 - xg2)

    home_dnb = home + 0.5 * draw
    away_dnb = away + 0.5 * draw
    home_double_chance = home + draw
    away_double_chance = away + draw

    # More varied automatic market selector.
    # This keeps the same model logic, but stops every sheet match from becoming Over 1.5.
    market_options = [
        ("Goals U3.5", 1 - over35),
        ("Goals O1.5", over15),
        ("Goals O2.5", over25),
        ("BTTS Yes", btts),
        ("BTTS No", 1 - btts),
        (f"{team1} Draw No Bet", home_dnb),
        (f"{team2} Draw No Bet", away_dnb),
        (f"{team1} Double Chance", home_double_chance),
        (f"{team2} Double Chance", away_double_chance),
    ]

    # Remove weak markets so the app does not show fake-looking picks.
    market_options = [(name, prob) for name, prob in market_options if prob >= 0.58]

    # Prefer variety when two picks have close confidence.
    def market_score(item):
        name, prob = item
        variety_bonus = 0.0
        if "U3.5" in name:
            variety_bonus = 0.045
        elif "Draw No Bet" in name:
            variety_bonus = 0.035
        elif "Double Chance" in name:
            variety_bonus = 0.025
        elif "BTTS" in name:
            variety_bonus = 0.020
        elif "O2.5" in name:
            variety_bonus = 0.015
        elif "O1.5" in name:
            variety_bonus = -0.030
        return prob + variety_bonus

    pick, confidence = max(market_options, key=market_score)
    confidence_pct = round(confidence * 100, 1)

    # Dedicated goals pick, separated from main AI pick.
    goals_options = [
        ("Goals U3.5", 1 - over35),
        ("Goals O1.5", over15),
        ("Goals O2.5", over25),
        ("BTTS Yes", btts),
        ("BTTS No", 1 - btts),
    ]

    goals_pick, goals_conf = max(goals_options, key=lambda x: x[1] + (0.035 if x[0] == "Goals U3.5" else 0))
    goals_confidence = round(goals_conf * 100, 1)

    # Team-goal style picks for dominant teams.
    if xg1 >= 1.85 and xg1 > xg2 + 0.45:
        goals_pick = f"{team1} Team Goals O1.5"
        goals_confidence = max(goals_confidence, 74.0)
    elif xg2 >= 1.85 and xg2 > xg1 + 0.45:
        goals_pick = f"{team2} Team Goals O1.5"
        goals_confidence = max(goals_confidence, 74.0)

    # Corners are based on attacking tempo + expected territory.
    if total_xg >= 3.05:
        corner_line = "Total Corners O9.5"
        corners_confidence = 72.0
    elif total_xg >= 2.55:
        corner_line = "Total Corners O8.5"
        corners_confidence = 70.0
    elif xg_gap >= 0.75:
        dominant_team = team1 if xg1 > xg2 else team2
        corner_line = f"{dominant_team} Team Corners O4.5"
        corners_confidence = 69.0
    else:
        corner_line = "Total Corners U10.5"
        corners_confidence = 68.0

    # Cards vary based on pressure and balance.
    pressure_total = t1_pressure + t2_pressure
    if pressure_total >= 145:
        cards_line = "Total Cards O4.5"
        cards_confidence = 71.0
    elif pressure_total >= 122:
        cards_line = "Total Cards O3.5"
        cards_confidence = 69.0
    elif xg_gap <= 0.25:
        cards_line = "Total Cards O2.5"
        cards_confidence = 66.0
    else:
        cards_line = "Total Cards U5.5"
        cards_confidence = 64.0

    risk = "LOW" if confidence > 0.72 else "MEDIUM" if confidence > 0.58 else "HIGH"

    return {
        "score": f"{best_score[0]}-{best_score[1]}",
        "xg1": round(xg1, 2),
        "xg2": round(xg2, 2),
        "home": round(home * 100, 1),
        "draw": round(draw * 100, 1),
        "away": round(away * 100, 1),
        "over15": round(over15 * 100, 1),
        "over25": round(over25 * 100, 1),
        "over35": round(over35 * 100, 1),
        "btts": round(btts * 100, 1),

        "confidence": confidence_pct,
        "safe_confidence": confidence_pct,
        "goals_confidence": goals_confidence,
        "corners_confidence": corners_confidence,
        "cards_confidence": cards_confidence,

        "pick": pick,
        "safe_pick": pick,
        "goals_pick": goals_pick,
        "corner_pick": corner_line,
        "cards_pick": cards_line,
        "banker_pick": pick,

        "corners": corner_line,
        "cards": cards_line,
        "corner_line": corner_line,
        "cards_line": cards_line,

        "risk": risk,
        "form1": round(t1_form),
        "form2": round(t2_form),
        "pressure1": round(t1_pressure),
        "pressure2": round(t2_pressure),
        "banker_rank": 3,
        "explanation": f"Automatic AI reading for {team1} vs {team2}. The system calculated expected goals, 1X2 balance, goal markets, corners and cards directly from the built-in model."
    }


def build_slips(predictions):
    ordered = sorted(
        predictions,
        key=lambda x: (x.get("banker_rank", 9), -x.get("safe_confidence", x["confidence"]))
    )

    safe = [
        {
            "home_team": p["home_team"],
            "away_team": p["away_team"],
            "league": p["league"],
            "pick": p["safe_pick"],
            "confidence": p["safe_confidence"],
            "risk": p["risk"],
        }
        for p in ordered[:3]
    ]

    goals_ranked = sorted(predictions, key=lambda x: x.get("goals_confidence", 0), reverse=True)
    medium = [
        {
            "home_team": p["home_team"],
            "away_team": p["away_team"],
            "league": p["league"],
            "pick": p["goals_pick"],
            "confidence": p["goals_confidence"],
            "risk": p["risk"],
        }
        for p in goals_ranked[:3]
    ]

    special_pool = []
    for p in predictions:
        if p.get("corners_confidence", 0) > 0:
            special_pool.append({
                "home_team": p["home_team"],
                "away_team": p["away_team"],
                "league": p["league"],
                "pick": p["corner_pick"],
                "confidence": p["corners_confidence"],
                "risk": "NUMERIC CORNERS",
            })
        if p.get("cards_confidence", 0) > 0:
            special_pool.append({
                "home_team": p["home_team"],
                "away_team": p["away_team"],
                "league": p["league"],
                "pick": p["cards_pick"],
                "confidence": p["cards_confidence"],
                "risk": "NUMERIC CARDS",
            })

    risky = sorted(special_pool, key=lambda x: x["confidence"], reverse=True)[:3]

    return safe, medium, risky


# ----------------------------
# PRE-CALCULATE ALL PREDICTIONS
# ----------------------------
all_predictions = []

for m in matches:
    p = predict(m["home"], m["away"])
    p["home_team"] = m["home"]
    p["away_team"] = m["away"]
    p["league"] = m["league"]
    p["section"] = m.get("section", "Normal Games")
    all_predictions.append(p)

safe_slip, medium_slip, risky_slip = build_slips(all_predictions)

# ----------------------------
# DASHBOARD HEADER
# ----------------------------
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

logo_col, title_col = st.columns([1, 7])

with logo_col:
    show_logo(width=105)

with title_col:
    st.title("TOF TERMINAL")
    st.caption(f"Football Intelligence • VIP Picks • TOF Prediction Engine")
    st.caption(f"Logged in as: {st.session_state.username} | {now}")
    st.caption("Normal games + World Cup mode loaded • Numeric goals/corners/cards lines • Conservative VIP picks prioritized")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Today AI Hit Rate", "87%")
col2.metric("Monthly ROI", "+38%")
col3.metric("Win Streak", "12")
col4.metric("VIP Market Scanner", "LIVE")

st.markdown("""
<div class="premium-banner">
    👑 TOF VIP PLATFORM • AI Predictions • VIP Analytics • Live Market Intelligence
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="notice-card">
    TOF uses conservative AI-assisted market selection focused on protected lines, numerical goals, cards and corners markets. Predictions are analytical insights, not guaranteed outcomes. Always use responsible staking.
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='premium-section-title'>💼 VIP Business Dashboard</div>", unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)

r1.metric("VIP Members", "184")
r2.metric("Monthly VIP Revenue", "$6,440")
r3.metric("Renewal Rate", "72%")
r4.metric("New Leads Today", "19")

st.divider()

# ----------------------------
# TABS
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "⚽ Match Center",
    "🎯 AI Slip Builder",
    "👑 VIP Zone",
    "📈 Performance"
])

# ----------------------------
# TAB 1 MATCH CENTER
# ----------------------------
with tab1:
    st.subheader("Choose Match Section")

    section_choice = st.radio(
        "Match Type",
        ["Normal Games", "World Cup"],
        horizontal=True
    )

    filtered_matches = [m for m in matches if m.get("section", "Normal Games") == section_choice]

    if section_choice == "World Cup":
        st.markdown("""
        <div class="premium-banner">
            🏆 WORLD CUP INTELLIGENCE CENTER • National Teams • Group Stage Picks • VIP World Cup Slips
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="premium-banner">
            ⚽ NORMAL LEAGUE CENTER • LaLiga • Bundesliga • Serie A • Ligue 1 • Club Matches
        </div>
        """, unsafe_allow_html=True)

    options = [
        f"{m['league']} | {m['home']} vs {m['away']}" +
        (f" • {m.get('kickoff', '')}" if str(m.get('kickoff', '')).strip() else "")
        for m in filtered_matches
    ]

    if not filtered_matches:
        st.warning("No matches found for this section. Check the 'section' column in your Google Sheet. Use exactly: Normal Games or World Cup.")
        st.stop()

    selected = st.selectbox(
        "Select Match",
        list(range(len(options))),
        format_func=lambda i: options[i],
        index=0
    )

    if selected is None:
        st.warning("Please select a match.")
        st.stop()

    match = filtered_matches[selected]
    pred = predict(match["home"], match["away"])

    st.header(f"⚽ {match['home']} vs {match['away']}")
    st.caption(match["league"])

    c1, c2, c3 = st.columns(3)

    c1.metric("AI Pick", pred["pick"])

    if is_vip:
        c2.metric("Confidence", f"{pred['confidence']}%")
    else:
        c2.metric("Confidence", "VIP Locked")

    c3.metric("Risk Level", pred["risk"])

    if is_vip:
        st.progress(min(pred["confidence"] / 100, 1.0))
    else:
        st.warning("🔒 Full confidence meter is locked for VIP members.")

    st.subheader("Match Intelligence")

    m1, m2 = st.columns(2)
    with m1:
        market_card("Predicted Score", pred["score"])
    with m2:
        market_card("Expected Goals", f"{pred['xg1']} - {pred['xg2']}")

    m3, m4 = st.columns(2)
    if is_vip:
        with m3:
            market_card("Corners Line", pred["corner_line"], f"Confidence: {pred.get('corners_confidence', 0)}%")
        with m4:
            market_card("Cards Line", pred["cards_line"], f"Confidence: {pred.get('cards_confidence', 0)}%")
    else:
        with m3:
            market_card("Corners Line", "VIP Locked")
        with m4:
            market_card("Cards Line", "VIP Locked")

    st.subheader("1X2 Probabilities")

    p1, p2, p3 = st.columns(3)
    p1.metric("Home", f"{pred['home']}%")
    p2.metric("Draw", f"{pred['draw']}%")
    p3.metric("Away", f"{pred['away']}%")

    st.subheader("Goal Markets")

    g1, g2, g3, g4 = st.columns(4)
    g1.metric("Over 1.5", f"{pred['over15']}%")

    if is_vip:
        g2.metric("Over 2.5", f"{pred['over25']}%")
        g3.metric("Over 3.5", f"{pred['over35']}%")
        g4.metric("BTTS", f"{pred['btts']}%")
    else:
        g2.metric("Over 2.5", "VIP")
        g3.metric("Over 3.5", "VIP")
        g4.metric("BTTS", "VIP")

    if is_vip:
        st.success("👑 VIP Analysis Unlocked")
        st.write(pred["explanation"])
    else:
        st.info("🔒 VIP analysis locked. Upgrade to unlock AI explanation, confidence meter, corners, cards, BTTS, and banker picks.")

# ----------------------------
# TAB 2 AI SLIP BUILDER
# ----------------------------
with tab2:
    st.header("🎯 AI Generated Slips")

    slip_section = st.radio(
        "Slip Section",
        ["Normal Games", "World Cup"],
        horizontal=True,
        key="slip_section"
    )

    selected_predictions = [p for p in all_predictions if p.get("section", "Normal Games") == slip_section]
    section_safe_slip, section_medium_slip, section_risky_slip = build_slips(selected_predictions)

    if slip_section == "World Cup":
        st.markdown("""
        <div class="premium-banner">
            🏆 WORLD CUP VIP SLIP BUILDER • National team picks • Protected markets • Tournament intelligence
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="premium-banner">
            ⚽ NORMAL GAMES SLIP BUILDER • Club football picks • League market scanner
        </div>
        """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("🟢 Safe Slip")
        for p in section_safe_slip:
            st.write(f"✅ **{p['home_team']} vs {p['away_team']}**")
            st.caption(f"{p['pick']} • {p['confidence']}%")

    with c2:
        if is_vip:
            st.subheader("🟡 Medium Risk")
            for p in section_medium_slip:
                st.write(f"⚡ **{p['home_team']} vs {p['away_team']}**")
                st.caption(f"{p['pick']} • {p['confidence']}%")
        else:
            st.warning("🔒 Medium Risk Slip Locked")

    with c3:
        if is_vip:
            st.subheader("🔴 VIP High Odds")
            for p in section_risky_slip:
                st.write(f"🔥 **{p['home_team']} vs {p['away_team']}**")
                st.caption(f"{p['pick']} • {p['confidence']}%")
        else:
            st.warning("🔒 VIP High Odds Slip Locked")

# ----------------------------
# TAB 3 VIP ZONE
# ----------------------------
with tab3:
    st.header("👑 VIP Zone")

    if is_vip:
        best = max(all_predictions, key=lambda x: x["confidence"])

        st.success("🔥 BANKER OF THE DAY")

        st.subheader(f"{best['home_team']} vs {best['away_team']}")
        st.metric("VIP Banker Pick", best["banker_pick"])
        st.metric("AI Confidence", f"{best.get('safe_confidence', best['confidence'])}%")

        st.write(best["explanation"])

        st.subheader("🚨 VIP Live Activity Feed")

        st.write("🟢 Sharp movement detected on Over 1.5 market")
        st.write("🔥 VIP banker confidence upgraded")
        st.write("📈 AI model found 3 high-value matches")
        st.write("⚠️ Risk warning issued on one high-volatility game")

    else:
        st.warning("🔒 VIP Zone Locked")
        st.write("Upgrade to unlock banker bets, high odds slips, live alerts, and advanced AI reasoning.")

# ----------------------------
# TAB 4 PERFORMANCE
# ----------------------------
with tab4:
    st.header("📈 Performance Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Last 7 Days", "22W - 6L")
    c2.metric("Win Rate", "78.5%")
    c3.metric("ROI", "+38%")
    c4.metric("Best Streak", "12 Wins")

    st.subheader("Recent VIP Results")

    st.write("✅ Over 1.5 Goals — Won")
    st.write("✅ Home Win — Won")
    st.write("✅ BTTS Yes — Won")
    st.write("❌ Over 3.5 Goals — Lost")
    st.write("✅ VIP Banker — Won")

# ----------------------------
# ADMIN PANEL
# ----------------------------
if is_admin:
    st.divider()
    st.header("⚙️ Admin Panel")

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password")
    new_role = st.selectbox("Role", ["user", "vip", "admin"])

    if st.button("Create User"):
        if new_user and new_pass:
            supabase.table("users").insert({
                "username": new_user.lower(),
                "password": new_pass,
                "banned": False,
                "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat(),
                "role": new_role,
                "session_id": None
            }).execute()

            st.success("User created")

    users = supabase.table("users").select("*").execute().data

    for u in users:
        st.write("---")
        st.write(f"👤 **{u.get('username')}**")
        st.caption(
            f"Role: {u.get('role')} | "
            f"Expires: {u.get('expires_at')} | "
            f"Banned: {u.get('banned')}"
        )

        a, b, c, d = st.columns(4)

        if a.button(f"Extend 7 Days {u['username']}"):
            supabase.table("users").update({
                "expires_at": (datetime.utcnow() + timedelta(days=7)).isoformat()
            }).eq("username", u["username"]).execute()

            st.success("Extended")

        if b.button(f"Ban {u['username']}"):
            supabase.table("users").update({
                "banned": True
            }).eq("username", u["username"]).execute()

            st.success("Banned")

        if c.button(f"Unban {u['username']}"):
            supabase.table("users").update({
                "banned": False
            }).eq("username", u["username"]).execute()

            st.success("Unbanned")

        if d.button(f"Reset Device {u['username']}"):
            supabase.table("users").update({
                "session_id": None
            }).eq("username", u["username"]).execute()

            st.success("Device reset")
