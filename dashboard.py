import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
from collections import defaultdict
import base64
import json
import re
import os
import requests

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Rédaction",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --accent:     #C0184A;
    --accent-dim: #8B1035;
    --accent-bg:  #FDF1F5;
    --bg:         #F5F3F5;
    --surface:    #FFFFFF;
    --border:     #EAE4E8;
    --border-soft:#F0ECF0;
    --text:       #1A0F14;
    --text-muted: #7E6674;
    --text-faint: #B09BA8;
    --radius:     14px;
    --shadow-sm:  0 1px 4px rgba(0,0,0,.06);
    --shadow-md:  0 4px 16px rgba(0,0,0,.07);
}

/* ── Police & base ── */
html, body, [class*="css"], .stMarkdown, .stText, button, input, label, p, td, th {
    font-family: 'Inter', sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

/* ── Fond principal ── */
.main, [data-testid="stAppViewContainer"] { background: var(--bg) !important; }
[data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
[data-testid="stAppViewBlockContainer"] { padding-top: 1.2rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0E0812 !important;
    border-right: 1px solid rgba(255,255,255,.05) !important;
}
[data-testid="stSidebar"] > div { padding-top: 1.5rem; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,.85) !important; font-family: 'Inter', sans-serif !important; }
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 {
    color: #fff !important; font-weight: 600 !important; letter-spacing: -.2px;
}
[data-testid="stSidebar"] .stTextInput input {
    background: rgba(255,255,255,.07) !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-radius: 8px !important; color: #fff !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder { color: rgba(255,255,255,.3) !important; }
[data-testid="stSidebar"] .stFileUploader [data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,.05) !important;
    border: 1.5px dashed rgba(255,255,255,.2) !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,.07) !important;
    border-color: rgba(255,255,255,.12) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stButton button {
    background: rgba(255,255,255,.09) !important;
    color: rgba(255,255,255,.9) !important; font-weight: 500 !important;
    border: 1px solid rgba(255,255,255,.14) !important;
    border-radius: 8px !important;
    width: 100%; margin-top: .2rem;
    transition: all .15s;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(192,24,74,.35) !important;
    border-color: rgba(192,24,74,.5) !important;
}
[data-testid="stSidebar"] .stButton button p,
[data-testid="stSidebar"] .stButton button span,
[data-testid="stSidebar"] .stButton button div {
    color: rgba(255,255,255,.9) !important; font-weight: 500 !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button,
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button span,
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button p {
    background: rgba(255,255,255,.1) !important;
    color: rgba(255,255,255,.85) !important; font-weight: 500 !important;
    border: 1px solid rgba(255,255,255,.15) !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] code,
[data-testid="stSidebar"] .stMarkdown small {
    color: rgba(255,255,255,.4) !important;
    background: transparent !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,.08) !important; }

/* ── Onglets ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 2px;
    background: transparent;
    border-bottom: 1px solid var(--border);
    border-radius: 0;
    padding: 0;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 0 !important;
    font-weight: 500 !important;
    font-size: .88rem !important;
    color: var(--text-muted) !important;
    background: transparent !important;
    padding: .6rem 1.1rem !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -1px;
    transition: all .15s;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    color: var(--text) !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: transparent !important;
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}

/* ── Cartes KPI ── */
.kpi-grid { display:flex; gap:12px; margin:.8rem 0 1.4rem; flex-wrap:wrap; }
.kpi-card {
    flex:1; min-width:130px;
    background: var(--surface);
    border-radius: var(--radius);
    border: 1px solid var(--border-soft);
    padding: 1.2rem 1.3rem 1rem;
    box-shadow: var(--shadow-sm);
}
.kpi-icon { font-size:1.3rem; margin-bottom:.5rem; opacity:.85; }
.kpi-val  { font-size:1.7rem; font-weight:700; color:var(--accent); line-height:1; letter-spacing:-.5px; }
.kpi-lbl  { font-size:.71rem; font-weight:500; color:var(--text-faint); text-transform:uppercase; letter-spacing:.5px; margin-top:.3rem; }

/* ── Cartes articles top/flop ── */
.art-card {
    display:flex; align-items:flex-start; gap:.7rem;
    background: var(--surface);
    border-radius: 10px; padding:.65rem .9rem;
    margin:.25rem 0;
    border: 1px solid var(--border-soft);
    font-size:.83rem; line-height:1.4;
    transition: box-shadow .15s;
}
.art-card:hover { box-shadow: var(--shadow-md); }
.art-card.top  { border-left: 3px solid #22c55e; }
.art-card.flop { border-left: 3px solid #f43f5e; }
.art-rank { font-weight:700; font-size:.78rem; min-width:50px; padding-top:1px; }
.art-rank.top  { color:#16a34a; }
.art-rank.flop { color:#e11d48; }
.art-title { color: var(--text); line-height:1.4; flex:1; }

/* ── Titres de section ── */
h3 { color: var(--text) !important; font-weight:700 !important; font-size:1.05rem !important; letter-spacing:-.3px; }
h4 { color: var(--text) !important; font-weight:600 !important; font-size:.92rem !important; letter-spacing:-.2px; }

/* ── DataFrames ── */
div[data-testid="stDataFrame"] {
    border-radius: var(--radius); overflow:hidden;
    box-shadow: var(--shadow-sm); border: 1px solid var(--border-soft) !important;
}

/* ── Boutons principaux ── */
.main .stButton > button, [data-testid="stAppViewContainer"] .stButton > button {
    background: var(--accent) !important; color: #fff !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 500 !important; transition: background .15s !important;
}
.main .stButton > button:hover { background: var(--accent-dim) !important; }

/* ── Alerts ── */
[data-testid="stAlert"] { border-radius: 10px !important; border: none !important; }

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    border-radius: 8px !important; border-color: var(--border) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(192,24,74,.1) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border-soft) !important;
    background: var(--surface) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] > div { border-top-color: var(--accent) !important; }

/* ── Séparateurs ── */
hr { border: none !important; border-top: 1px solid var(--border-soft) !important; margin: 1.2rem 0 !important; }

/* ── Masquer UI Streamlit inutile ── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="ScrollToTopButton"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }
button[kind="scrollToTopButton"] { display: none !important; }
.stAppHeader { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
section[data-testid="stSidebar"] { min-width: 280px !important; max-width: 280px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
ARCHIVE_DIR       = os.path.join(os.path.dirname(os.path.abspath(__file__)), "archives")
SEO_MONITOR_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "seo-monitor", "reports")
os.makedirs(ARCHIVE_DIR, exist_ok=True)

EXCLUDED_AUTHORS = {
    "Louise Millon", "Sebastian Danila", "Enzo Bonucci",
    "Manon Carpentier", "Antoine Michaud", "Vincent Bouvier",
}
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

CATEGORIES = {
    "🎬 Pop Culture": [
        "film", "série", "netflix", "anime", "one piece", "harry potter", "marvel",
        "disney", "prime video", "streaming", "cinéma", "trailer", "bande-annonce",
        "saison", "acteur", "live-action", "jojo", "avengers", "pixar", "thrash",
        "disclosure", "man on fire", "raiponce", "rooster", "day one", "bass x",
        "jumpers", "conan", "seigneur des anneaux", "malcolm",
    ],
    "🎮 Jeux Vidéo": [
        "xbox", "playstation", "steam", "nintendo", "switch", "jeu ", "jeux",
        "pokémon", "pokemon", "fortnite", "mario", "gaming", "gamer", "ps5",
        "fps", "rpg", "mmorpg", "bioshock", "overwatch", "game", "yoshi",
        "pickmon", "pokopia", "resident evil", "life is strange", "blizzard",
        "odyssey 3d", "steam machine", "tcg", "lego mario",
    ],
    "💻 Nouvelles Tech": [
        "iphone", "apple", "samsung", "android", " ia ", "openai", "chatgpt",
        "google", "microsoft", "windows", "mac", "macbook", "smartphone", "5g",
        "puce", "processeur", "alexa", "siri", "grok", "meta ", "x money",
        "oppo", "xiaomi", "nothing headphone", "dyson", "notion", "promptspy",
        "rabbit ", "chrome", "android 16", "ssd", "nvidia", "amd", "photonique",
        "leakbase", "macrohard", "moltbook",
    ],
    "🛒 Conso & Produits": [
        "amazon", "cdiscount", "bon plan", "bonplan", "remise", "réduction",
        "vente flash", "bouygues", "free ", "orange ", "sfr", "abonnement",
        "forfait", "lego", "fnac", "darty", "boulanger", "airpods", "galaxy buds",
        "navigo", "shein", "carburant", "essence", "voiture électrique", "tesla",
        "renault", "byd", "denza", "zendure", "shokz", "ninja foodi", "ecoflow",
        "sihoo", "iptv", "mondial relay", "canal+", "panneaux solaires",
    ],
    "🔬 Sciences": [
        "espace", "nasa", "planète", "astéroïde", "étoile", "fusée", "satellite",
        "scientifique", "recherche", "biologie", "chimie", "physique",
        "découverte", "astronomie", "pieuvre", "cerveau", "adn", "neurone",
        "artemis", "lune", "mars", "esa", "solaire", "imprimante 3d",
        "disque dur moléculaire", "matériau", "quantique",
    ],
    "📱 Réseaux Sociaux": [
        "tiktok", "instagram", "twitter", "bluesky", "threads", "mastodon",
        "youtube", "twitch", "snapchat", "linkedin", "facebook", "x.com",
        "réseau social", "influenceur", "créateur de contenu", "algorithme",
        "viral", "trend", "reel", "story", "live stream",
    ],
    "₿ Crypto & Web3": [
        "bitcoin", "ethereum", "crypto", "blockchain", "nft", "web3",
        "defi", "token", "binance", "coinbase", "altcoin", "stablecoin",
        "mining", "minage", "wallet", "cryptomonnaie", "bourse crypto",
    ],
    "🔒 Cybersécurité": [
        "hack", "hacker", "faille", "virus", "malware", "phishing", "ransomware",
        "cyberattaque", "cybersécurité", "piratage", "vulnérabilité", "données personnelles",
        "rgpd", "spyware", "botnet", "zero-day", "fuite de données", "darkweb",
        "mot de passe", "authentification", "vpn", "antivirus",
    ],
    "🚗 Auto & Mobilité": [
        "voiture", "automobile", "moto", "véhicule", "conduite autonome", "trottinette",
        "vélo électrique", "vae", "hybride", "thermique", "permis", "autoroute",
        "uber", "blablacar", "covoiturage", "borne de recharge", "moteur",
    ],
    "🌍 Société & Numérique": [
        "loi", "réglementation", "gouvernement", "parlement", "censure", "liberté",
        "surveillance", "vie privée", "numérique", "inclusion", "accessibilité",
        "travail", "emploi", "télétravail", "startup", "licenciement", "grève",
        "école", "éducation", "université", "bourse", "économie",
    ],
}

TYPE_LABELS = {
    "post": "Article",
    "bonplan": "Bon Plan",
    "critique": "Critique",
    "test": "Test",
    "dossier": "Dossier",
}

JOURS_FR = {
    "Monday": "Lundi", "Tuesday": "Mardi", "Wednesday": "Mercredi",
    "Thursday": "Jeudi", "Friday": "Vendredi", "Saturday": "Samedi", "Sunday": "Dimanche",
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def fmt(n: int) -> str:
    """Format number with French thousands separator."""
    return f"{int(n):,}".replace(",", "\u202f")  # narrow no-break space


def parse_views(v) -> int:
    if v is None or (isinstance(v, float) and v != v):  # NaN check
        return 0
    if isinstance(v, (int, float)):
        return int(v)
    cleaned = str(v).replace(" ", "").replace('"', "").replace("\u202f", "").strip()
    return int(cleaned) if cleaned.isdigit() else 0


def categorize(title: str) -> str:
    tl = title.lower()
    scores: dict[str, int] = defaultdict(int)
    for cat, kws in CATEGORIES.items():
        for kw in kws:
            if kw.lower() in tl:
                scores[cat] += 1
    return max(scores, key=scores.get) if scores else "📦 Autre"


# ── Cache fichier persistant pour les URLs ──
URL_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "url_cache.json")

def _load_url_cache() -> dict:
    try:
        with open(URL_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_url_cache(cache: dict):
    try:
        with open(URL_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def get_article_url(titre: str) -> str:
    """Retourne l'URL d'un article — depuis le cache fichier ou via requête JDG."""
    cache = _load_url_cache()
    if titre in cache:
        return cache[titre]
    try:
        query = " ".join(titre.split()[:6])
        resp = requests.get(
            "https://www.journaldugeek.com/",
            params={"s": query},
            timeout=4,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        if resp.status_code == 200:
            match = re.search(
                r'href="(https://www\.journaldugeek\.com/(?:\d{4}/\d{2}/\d{2}/|[^"]+?/)[^"]+?/)"',
                resp.text,
            )
            url = match.group(1) if match else ""
        else:
            url = ""
    except Exception:
        url = ""
    cache[titre] = url
    _save_url_cache(cache)
    return url


def prefetch_urls(titres: tuple):
    """Récupère les URLs manquantes en parallèle, max 3 workers, 300ms entre chaque."""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time
    cache = _load_url_cache()
    manquantes = [t for t in titres if t not in cache]
    if not manquantes:
        return
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(get_article_url, t): t for t in manquantes}
        for f in as_completed(futures):
            f.result()
            time.sleep(0.3)


@st.cache_data(show_spinner="Chargement du CSV…")
def load_data(file) -> pd.DataFrame:
    df = pd.read_csv(file, sep=";", encoding="utf-8")
    df.columns = ["Titre", "Type", "Rédacteur", "Mots", "Vues", "Date"]
    df["Vues"] = df["Vues"].apply(parse_views)
    df["Mots"] = df["Mots"].apply(parse_views)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Catégorie"] = df["Titre"].apply(categorize)
    df["Type_Label"] = df["Type"].map(TYPE_LABELS).fillna(df["Type"])
    df = df[~df["Rédacteur"].isin(EXCLUDED_AUTHORS)].reset_index(drop=True)
    return df


def week_dates(filename: str, df: pd.DataFrame):
    m = re.search(r"(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})", filename)
    if m:
        return m.group(1), m.group(2)
    return df["Date"].min().strftime("%Y-%m-%d"), df["Date"].max().strftime("%Y-%m-%d")




# ─────────────────────────────────────────────
# ARCHIVAGE
# ─────────────────────────────────────────────

def auto_archive(source, filename: str) -> bool:
    """Save CSV to GitHub (cloud) or local archives/ folder (local).
    Returns True if a new file was actually saved."""
    if isinstance(source, bytes):
        csv_bytes = source
    else:
        with open(source, "rb") as f:
            csv_bytes = f.read()

    if _is_cloud():
        gh_save_archive(csv_bytes, filename)
        return True
    else:
        dest = os.path.join(ARCHIVE_DIR, filename)
        if not os.path.exists(dest):
            with open(dest, "wb") as f:
                f.write(csv_bytes)
            return True
        return False


@st.cache_data(show_spinner=False, ttl=300)
def load_archive_summaries() -> pd.DataFrame:
    rows = []
    if _is_cloud():
        filenames = gh_list_archives()
    else:
        filenames = sorted(
            [f for f in os.listdir(ARCHIVE_DIR) if f.endswith(".csv")], reverse=True
        )

    MOIS_FR = ["janvier","février","mars","avril","mai","juin",
               "juillet","août","septembre","octobre","novembre","décembre"]

    for fname in filenames:
        try:
            if _is_cloud():
                csv_bytes = gh_load_archive(fname)
                if csv_bytes is None:
                    continue
                import io
                df_a = load_data(io.BytesIO(csv_bytes))
            else:
                df_a = load_data(os.path.join(ARCHIVE_DIR, fname))

            m = re.search(r"(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})", fname)
            if m:
                w_s = m.group(1)
                w_e = m.group(2)
            else:
                w_s = df_a["Date"].min().strftime("%Y-%m-%d")
                w_e = df_a["Date"].max().strftime("%Y-%m-%d")
            d_s = datetime.strptime(w_s, "%Y-%m-%d")
            d_e = datetime.strptime(w_e, "%Y-%m-%d")
            nb_jours = (d_e - d_s).days

            is_monthly = nb_jours > 20
            if is_monthly:
                label = f"{MOIS_FR[d_s.month - 1].capitalize()} {d_s.year}"
                type_label = "🗓️ Mensuel"
            else:
                label = f"{d_s.strftime('%d/%m')} → {d_e.strftime('%d/%m/%Y')}"
                type_label = "📅 Hebdo"

            top_auth = df_a.groupby("Rédacteur")["Vues"].sum().idxmax()
            top_art  = df_a.loc[df_a["Vues"].idxmax(), "Titre"]
            rows.append({
                "Période":       label,
                "Type":          type_label,
                "week_start":    w_s,
                "filename":      fname,
                "Vues totales":  df_a["Vues"].sum(),
                "Articles":      len(df_a),
                "Vues moyennes": int(df_a["Vues"].mean()),
                "Top rédacteur": top_auth,
                "Top article":   top_art[:70] + ("…" if len(top_art) > 70 else ""),
            })
        except Exception:
            continue
    return pd.DataFrame(rows)


def _is_cloud() -> bool:
    """Detect if running on Streamlit Cloud (st.secrets has github_token)."""
    try:
        return bool(st.secrets.get("github_token", ""))
    except Exception:
        return False


def _gh_headers() -> dict:
    try:
        return {"Authorization": f"token {st.secrets['github_token']}",
                "Accept": "application/vnd.github.v3+json"}
    except Exception:
        return {}


def _gh_repo() -> str:
    try:
        return st.secrets.get("github_repo", "")
    except Exception:
        return ""


def gh_list_archives() -> list[str]:
    r = requests.get(
        f"https://api.github.com/repos/{_gh_repo()}/contents/archives",
        headers=_gh_headers(), timeout=8,
    )
    if r.ok:
        return sorted([f["name"] for f in r.json() if f["name"].endswith(".csv")], reverse=True)
    return []


def gh_save_archive(csv_bytes: bytes, filename: str):
    url = f"https://api.github.com/repos/{_gh_repo()}/contents/archives/{filename}"
    r = requests.get(url, headers=_gh_headers(), timeout=8)
    if r.status_code == 200:
        return  # Already exists
    requests.put(url, headers=_gh_headers(), timeout=10, json={
        "message": f"Archive semaine {filename}",
        "content": base64.b64encode(csv_bytes).decode(),
    })


def gh_load_archive(filename: str) -> bytes | None:
    url = f"https://api.github.com/repos/{_gh_repo()}/contents/archives/{filename}"
    r = requests.get(url, headers=_gh_headers(), timeout=8)
    if r.ok:
        return base64.b64decode(r.json()["content"])
    return None


def gh_delete_archive(filename: str):
    url = f"https://api.github.com/repos/{_gh_repo()}/contents/archives/{filename}"
    r = requests.get(url, headers=_gh_headers(), timeout=8)
    if r.ok:
        sha = r.json()["sha"]
        requests.delete(url, headers=_gh_headers(), timeout=8, json={
            "message": f"Suppression archive {filename}",
            "sha": sha,
        })


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo-jdg.jpg")


def logo_b64() -> str:
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

_logo = logo_b64()


# ─────────────────────────────────────────────
# AUTHENTIFICATION
# ─────────────────────────────────────────────
def _get_app_password() -> str:
    try:
        return st.secrets.get("app_password", "")
    except Exception:
        pass
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f).get("app_password", "")
        except Exception:
            pass
    return ""


_stored_pw = _get_app_password()
if _stored_pw and not st.session_state.get("authenticated"):
    st.markdown("""
    <style>
    [data-testid="stSidebar"], section[data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    _, col_c, _ = st.columns([1, 1.2, 1])
    with col_c:
        if _logo:
            st.markdown(
                f"<div style='text-align:center;padding:3rem 0 1.5rem;'>"
                f"<img src='data:image/jpeg;base64,{_logo}' "
                f"style='width:110px;border-radius:16px;box-shadow:0 6px 24px rgba(142,16,80,.25);'>"
                f"</div>",
                unsafe_allow_html=True,
            )
        st.markdown(
            "<h2 style='text-align:center;color:#C0184A;font-weight:800;"
            "margin-bottom:0.3rem;'>Dashboard Rédaction</h2>"
            "<p style='text-align:center;color:#999;font-size:.85rem;"
            "margin-bottom:1.8rem;'>Journal du Geek — accès réservé</p>",
            unsafe_allow_html=True,
        )
        with st.form("login_form"):
            pw_input = st.text_input(
                "Mot de passe",
                type="password",
                placeholder="Entrez le mot de passe…",
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button("Se connecter", use_container_width=True)
        if submitted:
            if pw_input == _stored_pw:
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Mot de passe incorrect.")
    st.stop()


with st.sidebar:
    if _logo:
        st.markdown(
            f"<div style='text-align:center;padding:.5rem 0 1rem;'>"
            f"<img src='data:image/jpeg;base64,{_logo}' style='width:90px;border-radius:14px;box-shadow:0 4px 16px rgba(0,0,0,.3);'>"
            f"</div>",
            unsafe_allow_html=True,
        )
    st.markdown("---")

    # File upload
    st.markdown("### 📂 Fichier de la semaine")
    uploaded = st.file_uploader("Importer un nouveau CSV", type=["csv"])

    # Archives
    archived_files = gh_list_archives() if _is_cloud() else sorted(
        [f for f in os.listdir(ARCHIVE_DIR) if f.endswith(".csv")], reverse=True
    )
    archive_choice = None
    if not uploaded and archived_files:
        st.markdown("### 🗂️ Semaines archivées")
        archive_choice = st.selectbox(
            "Charger une semaine précédente",
            ["— Sélectionner —"] + archived_files,
        )
        if archive_choice == "— Sélectionner —":
            archive_choice = None

    st.markdown("---")

    # Bouton mise à jour manuelle du cache URLs
    if st.button("🔄 Rafraîchir les liens articles"):
        cache = _load_url_cache()
        # Vider uniquement les entrées sans URL trouvée pour retenter
        vides = [k for k, v in cache.items() if not v]
        for k in vides:
            del cache[k]
        _save_url_cache(cache)
        st.cache_data.clear()
        st.success(f"{len(vides)} liens retentés — rechargement en cours…")
        st.rerun()

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
df = None
filename = ""

if uploaded:
    _is_new = auto_archive(uploaded.getvalue(), uploaded.name)
    if _is_new:
        load_archive_summaries.clear()
    df = load_data(uploaded)
    filename = uploaded.name
elif archive_choice:
    if _is_cloud():
        import io
        _bytes = gh_load_archive(archive_choice)
        df = load_data(io.BytesIO(_bytes)) if _bytes else None
    else:
        df = load_data(os.path.join(ARCHIVE_DIR, archive_choice))
    filename = archive_choice

# Préchargement de toutes les URLs du CSV — uniquement celles absentes du cache fichier
if df is not None:
    prefetch_urls(tuple(df["Titre"].tolist()))

# ─────────────────────────────────────────────
# LANDING PAGE (no file)
# ─────────────────────────────────────────────
if df is None:
    st.title("📰 Dashboard Réunion Rédaction")
    st.markdown(
        """
        ### Bienvenue 👋

        Importez votre export CSV hebdomadaire pour afficher :

        | Onglet | Contenu |
        |---|---|
        | 📊 Vue d'ensemble | Vues totales, articles, auteurs, timeline |
        | 👥 Stats par auteur | Top 5 et flops de chaque rédacteur |
        | 📈 Tendances | Catégories, types, heatmap, insights |
        | 📅 Planning | Sorties ciné/TV (TMDB), événements tech, idées |

        👈 **Importez votre CSV dans la barre latérale pour commencer.**
        """
    )
    st.stop()

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
w_start, w_end = week_dates(filename, df)
next_monday = (datetime.strptime(w_end, "%Y-%m-%d") + timedelta(days=2)).strftime("%d/%m/%Y")
is_monthly = (datetime.strptime(w_end, "%Y-%m-%d") - datetime.strptime(w_start, "%Y-%m-%d")).days > 20

_logo_tag = f"<img src='data:image/jpeg;base64,{_logo}' style='height:52px;border-radius:9px;margin-right:1rem;vertical-align:middle;box-shadow:0 2px 8px rgba(0,0,0,.2);'>" if _logo else ""
st.markdown(
    f"""<div style='
        background: #0E0812;
        border-radius: 14px; padding: 1.3rem 1.8rem; margin-bottom: 1.4rem;
        box-shadow: 0 2px 12px rgba(0,0,0,.12);
        display:flex; align-items:center; gap:0;
    '>
        {_logo_tag}
        <div>
            <div style='font-size:1.55rem;font-weight:900;color:#fff;letter-spacing:-.5px;line-height:1.1;'>
                Réunion de Rédaction
            </div>
            <div style='color:rgba(255,255,255,.75);font-size:.9rem;margin-top:.3rem;font-weight:500;'>
                📅 Semaine du <b style='color:#fff;'>{datetime.strptime(w_start, '%Y-%m-%d').strftime('%d/%m/%Y')}</b>
                au <b style='color:#fff;'>{datetime.strptime(w_end, '%Y-%m-%d').strftime('%d/%m/%Y')}</b>
                &nbsp;·&nbsp; Réunion lundi <b style='color:#fff;'>{next_monday}</b>
            </div>
        </div>
    </div>""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["📊 Vue d'ensemble", "👥 Stats par auteur", "📈 Tendances", "🗂️ Historique"]
)

# ─────────────────────────────────────────────
# TAB 1 — VUE D'ENSEMBLE
# ─────────────────────────────────────────────
with tab1:
    total_vues = df["Vues"].sum()
    total_arts = len(df)
    total_auteurs = df["Rédacteur"].nunique()
    avg_vues = int(df["Vues"].mean())
    top_row = df.loc[df["Vues"].idxmax()]

    kpis = [
        ("👁️", fmt(total_vues),      "Vues totales"),
        ("📝", str(total_arts),       "Articles publiés"),
        ("✍️", str(total_auteurs),    "Rédacteurs actifs"),
        ("📊", fmt(avg_vues),         "Vues moyennes"),
        ("🏆", fmt(top_row["Vues"]),  "Record de la semaine"),
    ]
    cards_html = "".join(
        f"<div class='kpi-card'><div class='kpi-icon'>{ico}</div>"
        f"<div class='kpi-val'>{val}</div><div class='kpi-lbl'>{lbl}</div></div>"
        for ico, val, lbl in kpis
    )
    st.markdown(f"<div class='kpi-grid'>{cards_html}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='font-size:.85rem;color:#7E6674;margin-top:-.5rem;margin-bottom:1rem;'>"
        f"🏆 <i>{top_row['Titre'][:90]}</i> — {top_row['Rédacteur']}</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    col_l, col_r = st.columns([3, 2])

    with col_l:
        author_vues = (
            df.groupby("Rédacteur")["Vues"]
            .sum()
            .sort_values(ascending=True)
            .reset_index()
        )
        fig = px.bar(
            author_vues, x="Vues", y="Rédacteur", orientation="h",
            title="Vues totales par rédacteur",
            color="Vues", color_continuous_scale=["#F9ECF2", "#C0184A", "#8B1035"],
            labels={"Vues": "Vues totales", "Rédacteur": ""},
        )
        fig.update_layout(coloraxis_showscale=False, height=420, margin=dict(l=0))
        st.plotly_chart(fig, width='stretch')

    with col_r:
        type_vues = df.groupby("Type_Label")["Vues"].sum().reset_index()
        fig2 = px.pie(
            type_vues, values="Vues", names="Type_Label",
            title="Répartition des vues par format",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig2.update_traces(textposition="inside", textinfo="percent+label")
        fig2.update_layout(showlegend=False, height=420)
        st.plotly_chart(fig2, width='stretch')

    # Timeline journalière — uniquement pour les fichiers hebdomadaires
    if not is_monthly:
        week_monday = datetime.strptime(w_start, "%Y-%m-%d")
        week_monday -= timedelta(days=week_monday.weekday())  # recaler au lundi
        all_days = pd.DataFrame({
            "Date": [week_monday.date() + timedelta(days=i) for i in range(7)]
        })
        daily_raw = df.groupby(df["Date"].dt.date)["Vues"].sum().reset_index()
        daily_raw.columns = ["Date", "Vues"]
        daily = all_days.merge(daily_raw, on="Date", how="left").fillna(0)
        daily["Vues"] = daily["Vues"].astype(int)
        daily["Jour"] = daily["Date"].apply(lambda d: JOURS_FR[d.strftime("%A")] + " " + d.strftime("%d/%m"))
        fig3 = px.area(
            daily, x="Jour", y="Vues",
            title="Vues par jour (lundi → dimanche)",
            color_discrete_sequence=["#C0184A"],
            markers=True,
        )
        fig3.update_layout(height=240, margin=dict(t=40, b=20))
        st.plotly_chart(fig3, width='stretch')

    # Top 10
    _top10_label = "mois" if is_monthly else "semaine"
    st.markdown(f"### 🏆 Top 10 articles du {_top10_label}")
    top10 = df.nlargest(10, "Vues")[["Titre", "Rédacteur", "Type_Label", "Vues", "Date"]].copy()
    top10["Date"] = top10["Date"].dt.strftime("%d/%m %H:%M")
    top10["Vues"] = top10["Vues"].apply(fmt)
    top10 = top10.rename(columns={"Type_Label": "Format"})
    top10["Lien"] = top10["Titre"].apply(get_article_url)
    st.dataframe(
        top10.reset_index(drop=True),
        column_config={"Lien": st.column_config.LinkColumn("↗", display_text="↗")},
        width='stretch',
        hide_index=True,
    )

    # Top 3 par format éditorial
    st.markdown("### 🎯 Top 3 par format éditorial")
    col_cr, col_te, col_do = st.columns(3)

    MEDAL_COLORS = ["#F59E0B", "#94A3B8", "#B45309"]

    def format_top3_cards(subset):
        medals = ["🥇", "🥈", "🥉"]
        cards = ""
        for i, (_, row) in enumerate(subset.head(3).iterrows()):
            titre_full = row["Titre"]
            titre = titre_full[:65] + ("…" if len(titre_full) > 65 else "")
            color = MEDAL_COLORS[i]
            url = get_article_url(titre_full)
            titre_html = (
                f"<a href='{url}' target='_blank' style='color:#1a0a12;text-decoration:none;"
                f"border-bottom:1px dotted #C0184A;'>{titre}</a>"
                if url else titre
            )
            cards += (
                f"<div style='background:#fff;border:1px solid #EAE4E8;border-left:4px solid {color};"
                f"border-radius:10px;padding:.65rem .9rem;margin:.3rem 0;'>"
                f"<div style='font-size:.95rem;line-height:1;margin-bottom:.25rem;'>{medals[i]}"
                f"&nbsp;<span style='font-weight:800;color:#C0184A;'>{fmt(row['Vues'])} vues</span></div>"
                f"<div style='font-size:.82rem;color:#1a0a12;line-height:1.35;margin-bottom:.2rem;'>{titre_html}</div>"
                f"<div style='font-size:.75rem;color:#7E6674;'>✍️ {row['Rédacteur']}</div>"
                f"</div>"
            )
        return cards

    with col_cr:
        st.markdown("#### ✍️ Critiques")
        critiques = df[df["Type"] == "critique"].sort_values("Vues", ascending=False)
        if len(critiques):
            st.markdown(format_top3_cards(critiques), unsafe_allow_html=True)
        else:
            st.caption("Aucune critique cette semaine.")

    with col_te:
        st.markdown("#### 🔬 Tests")
        tests = df[df["Type"] == "test"].sort_values("Vues", ascending=False)
        if len(tests):
            st.markdown(format_top3_cards(tests), unsafe_allow_html=True)
        else:
            st.caption("Aucun test cette semaine.")

    with col_do:
        st.markdown("#### 📂 Dossiers")
        dossiers = df[df["Type"] == "dossier"].sort_values("Vues", ascending=False)
        if len(dossiers):
            st.markdown(format_top3_cards(dossiers), unsafe_allow_html=True)
        else:
            st.caption("Aucun dossier cette semaine.")

# ─────────────────────────────────────────────
# TAB 2 — STATS PAR AUTEUR
# ─────────────────────────────────────────────
with tab2:
    st.markdown("### 👥 Performance par rédacteur")

    authors_sorted = (
        df.groupby("Rédacteur")["Vues"].sum()
        .sort_values(ascending=False)
        .index.tolist()
    )
    selected = st.multiselect(
        "Filtrer les rédacteurs",
        authors_sorted,
        default=authors_sorted,
    )

    if not selected:
        st.warning("Sélectionnez au moins un rédacteur.")
        st.stop()

    sub = df[df["Rédacteur"].isin(selected)]

    # Tableau récap
    summary = (
        sub.groupby("Rédacteur")
        .agg(
            Articles=("Titre", "count"),
            Vues_totales=("Vues", "sum"),
            Vues_moyennes=("Vues", "mean"),
            Meilleure_perf=("Vues", "max"),
            Mots_moy=("Mots", "mean"),
        )
        .round(0)
        .astype(int)
        .sort_values("Vues_totales", ascending=False)
    )
    display_sum = summary.copy()
    for col in ["Vues_totales", "Vues_moyennes", "Meilleure_perf"]:
        display_sum[col] = display_sum[col].apply(fmt)
    st.dataframe(display_sum, width='stretch')

    st.markdown("---")
    st.markdown("### Top 5 / Flops par rédacteur")

    cols = st.columns(2)
    for i, author in enumerate(
        sorted(selected, key=lambda a: df[df["Rédacteur"] == a]["Vues"].sum(), reverse=True)
    ):
        adf = df[df["Rédacteur"] == author].sort_values("Vues", ascending=False)
        nb = len(adf)
        avg = int(adf["Vues"].mean())
        total = adf["Vues"].sum()

        with cols[i % 2]:
            st.markdown(f"#### ✍️ {author}")
            st.caption(f"{nb} articles · {fmt(total)} vues · moy. {fmt(avg)}")

            flop_df   = adf.iloc[5:].tail(5)  # strictement après le top 5
            has_flops = len(flop_df) > 0
            c_top, c_flop = st.columns(2) if has_flops else st.columns([1, 2])
            with c_top:
                st.markdown("**🟢 Top 5**")
                for rank, (_, row) in enumerate(adf.head(5).iterrows(), 1):
                    titre_full = row["Titre"]
                    titre = titre_full[:62] + ("…" if len(titre_full) > 62 else "")
                    url = get_article_url(titre_full)
                    titre_html = (
                        f"<a href='{url}' target='_blank' style='color:#1a0a12;text-decoration:none;"
                        f"border-bottom:1px dotted #16a34a;'>{titre}</a>" if url else titre
                    )
                    st.markdown(
                        f'<div class="art-card top">'
                        f'<span class="art-rank top">#{rank} &nbsp;{fmt(row["Vues"])}</span>'
                        f'<span class="art-title">{titre_html}</span></div>',
                        unsafe_allow_html=True,
                    )
            if has_flops:
                with c_flop:
                    st.markdown("**🔴 Flops**")
                    for rank, (_, row) in enumerate(flop_df.iterrows(), 1):
                        titre_full = row["Titre"]
                        titre = titre_full[:62] + ("…" if len(titre_full) > 62 else "")
                        url = get_article_url(titre_full)
                        titre_html = (
                            f"<a href='{url}' target='_blank' style='color:#1a0a12;text-decoration:none;"
                            f"border-bottom:1px dotted #dc2626;'>{titre}</a>" if url else titre
                        )
                        st.markdown(
                            f'<div class="art-card flop">'
                            f'<span class="art-rank flop">↓{fmt(row["Vues"])}</span>'
                            f'<span class="art-title">{titre_html}</span></div>',
                            unsafe_allow_html=True,
                        )
            st.markdown("---")

# ─────────────────────────────────────────────
# TAB 3 — TENDANCES
# ─────────────────────────────────────────────
with tab3:
    st.markdown("### 📈 Analyse des tendances")

    cat_stats = (
        df.groupby("Catégorie")
        .agg(Vues=("Vues", "sum"), Articles=("Titre", "count"), Vues_moy=("Vues", "mean"))
        .sort_values("Vues", ascending=False)
        .reset_index()
    )
    fig = px.bar(
        cat_stats, x="Catégorie", y="Vues",
        color="Catégorie",
        title="Vues totales par catégorie",
        text=cat_stats["Articles"].apply(lambda n: f"{n} art."),
        labels={"Vues": "Vues totales", "Catégorie": ""},
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, xaxis_tickangle=-30, height=400)
    st.plotly_chart(fig, width='stretch')

    # ── Scatter efficacité vs volume ──
    st.markdown("---")
    st.markdown("#### 🎯 Efficacité vs Volume par catégorie")
    st.caption("Axe X = nombre d'articles publiés · Axe Y = vues moyennes par article · Taille = vues totales")

    vues_moy_globale = df["Vues"].mean()
    articles_moy_globale = cat_stats["Articles"].mean()

    fig_scatter = px.scatter(
        cat_stats,
        x="Articles", y="Vues_moy",
        size="Vues", color="Catégorie",
        text="Catégorie",
        labels={"Articles": "Nb articles publiés", "Vues_moy": "Vues moyennes/article", "Vues": "Vues totales"},
        size_max=60,
        height=420,
    )
    fig_scatter.update_traces(textposition="top center", textfont_size=11)
    fig_scatter.add_hline(y=vues_moy_globale, line_dash="dot", line_color="#C0184A",
                          annotation_text=f"Moyenne globale ({fmt(int(vues_moy_globale))} v/art.)",
                          annotation_position="bottom right")
    fig_scatter.add_vline(x=articles_moy_globale, line_dash="dot", line_color="#aaa",
                          annotation_text="Volume moyen", annotation_position="top left")
    fig_scatter.update_layout(showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig_scatter, width='stretch')

    # Légende des quadrants
    qc1, qc2, qc3, qc4 = st.columns(4)
    qc1.markdown("<div style='background:#d4edda;border-radius:8px;padding:.5rem .8rem;font-size:.8rem;'>"
                 "↗ <b>Haut gauche</b><br>Efficace & sous-exploité → à pousser</div>", unsafe_allow_html=True)
    qc2.markdown("<div style='background:#cce5ff;border-radius:8px;padding:.5rem .8rem;font-size:.8rem;'>"
                 "↗ <b>Haut droite</b><br>Efficace & volumineux → pilier éditorial</div>", unsafe_allow_html=True)
    qc3.markdown("<div style='background:#fff3cd;border-radius:8px;padding:.5rem .8rem;font-size:.8rem;'>"
                 "↙ <b>Bas gauche</b><br>Faible perf. & peu publié → à surveiller</div>", unsafe_allow_html=True)
    qc4.markdown("<div style='background:#f8d7da;border-radius:8px;padding:.5rem .8rem;font-size:.8rem;'>"
                 "↙ <b>Bas droite</b><br>Beaucoup d'articles, peu de vues → à rationaliser</div>", unsafe_allow_html=True)

    # ── Insights automatiques ──
    st.markdown("---")
    periode_label_t3 = "du mois" if is_monthly else "de la semaine"
    st.markdown(f"#### 💡 Insights {periode_label_t3}")

    # Catégorie pépite : meilleur ratio vues/article parmi celles avec ≥2 articles
    cat_multi = cat_stats[cat_stats["Articles"] >= 2]
    pepite = cat_multi.sort_values("Vues_moy", ascending=False).iloc[0] if len(cat_multi) else cat_stats.iloc[0]
    # Catégorie surchargée : beaucoup d'articles mais ratio < moyenne globale
    surcharge_df = cat_stats[(cat_stats["Articles"] >= articles_moy_globale) & (cat_stats["Vues_moy"] < vues_moy_globale)]
    surcharge = surcharge_df.sort_values("Articles", ascending=False).iloc[0] if len(surcharge_df) else None
    # Format le plus efficace
    best_type_perf = (
        df.groupby("Type_Label")
        .agg(Vues_moy=("Vues", "mean"), n=("Titre", "count"))
        .query("n >= 2")
        .sort_values("Vues_moy", ascending=False)
        .reset_index()
    )
    # Meilleur jour (hebdo seulement)
    best_day_en = df.groupby(df["Date"].dt.day_name())["Vues"].mean().idxmax() if not is_monthly else None

    ia, ib, ic = st.columns(3)
    ia.success(
        f"**Catégorie pépite**\n\n"
        f"**{pepite['Catégorie']}**\n\n"
        f"{fmt(int(pepite['Vues_moy']))} vues/article · {int(pepite['Articles'])} articles"
    )
    if surcharge is not None:
        ib.error(
            f"**À rationaliser**\n\n"
            f"**{surcharge['Catégorie']}**\n\n"
            f"{int(surcharge['Articles'])} articles · seulement {fmt(int(surcharge['Vues_moy']))} vues/article"
        )
    elif len(best_type_perf) > 0:
        ib.info(
            f"**Format le plus rentable**\n\n"
            f"**{best_type_perf.iloc[0]['Type_Label']}**\n\n"
            f"{fmt(int(best_type_perf.iloc[0]['Vues_moy']))} vues/article"
        )
    if best_day_en:
        ic.info(
            f"**Meilleur jour de publication**\n\n"
            f"**{JOURS_FR.get(best_day_en, best_day_en)}**\n\n"
            f"Basé sur les vues moyennes sur la semaine"
        )
    elif len(best_type_perf) > 0:
        ic.info(
            f"**Format le plus rentable**\n\n"
            f"**{best_type_perf.iloc[0]['Type_Label']}**\n\n"
            f"{fmt(int(best_type_perf.iloc[0]['Vues_moy']))} vues/article"
        )


    # Tableau complet catégories
    with st.expander("📋 Détail par catégorie"):
        cat_detail = cat_stats.copy()
        cat_detail["Vues"] = cat_detail["Vues"].apply(fmt)
        cat_detail["Vues_moy"] = cat_detail["Vues_moy"].apply(lambda x: fmt(int(x)))
        cat_detail.columns = ["Catégorie", "Vues totales", "Articles", "Vues moyennes"]
        st.dataframe(cat_detail, width='stretch', hide_index=True)

    # Détail de la catégorie "Autre"
    autres_df = df[df["Catégorie"] == "📦 Autre"].copy()
    if len(autres_df) > 0:
        st.markdown("---")
        with st.expander(f"📦 Articles non catégorisés ({len(autres_df)} articles) — à surveiller pour affiner les règles"):
            autres_display = (
                autres_df[["Titre", "Rédacteur", "Vues", "Type_Label"]]
                .sort_values("Vues", ascending=False)
                .reset_index(drop=True)
            )
            autres_display["Vues"] = autres_display["Vues"].apply(fmt)
            autres_display.columns = ["Titre", "Rédacteur", "Vues", "Type"]
            st.dataframe(autres_display, width='stretch', hide_index=True)

    if not is_monthly:
        st.markdown("---")
        # ── Vue hebdomadaire : production par jour ──
        st.markdown("### 📆 Production quotidienne")
        week_monday2 = datetime.strptime(w_start, "%Y-%m-%d")
        week_monday2 -= timedelta(days=week_monday2.weekday())
        all_days2 = pd.DataFrame({
            "Date": [week_monday2.date() + timedelta(days=i) for i in range(7)]
        })
        daily_count_raw = df.groupby(df["Date"].dt.date).size().reset_index(name="Articles")
        daily_count_raw.columns = ["Date", "Articles"]
        daily_count = all_days2.merge(daily_count_raw, on="Date", how="left").fillna(0)
        daily_count["Articles"] = daily_count["Articles"].astype(int)
        daily_count["Jour"] = daily_count["Date"].apply(lambda d: JOURS_FR[d.strftime("%A")] + " " + d.strftime("%d/%m"))

        fig_daily = px.bar(
            daily_count, x="Jour", y="Articles",
            title="Nombre d'articles publiés par jour (lundi → dimanche)",
            labels={"Jour": "", "Articles": "Articles"},
            color="Articles",
            color_continuous_scale=["#F5F3F5", "#C0184A", "#8B1035"],
            text="Articles",
        )
        fig_daily.update_traces(textposition="outside")
        fig_daily.update_layout(showlegend=False, coloraxis_showscale=False, height=300, margin=dict(t=40, b=10))
        st.plotly_chart(fig_daily, width='stretch')

        # Heatmap rédacteur × jour
        st.markdown("#### ✍️ Articles par rédacteur par jour")
        df["Jour_label"] = df["Date"].apply(
            lambda d: JOURS_FR[d.strftime("%A")] + " " + d.strftime("%d/%m")
        )
        ordered_cols = daily_count["Jour"].tolist()
        pivot_redac = df.pivot_table(
            values="Titre", index="Rédacteur", columns="Jour_label",
            aggfunc="count", fill_value=0,
        ).reindex(columns=ordered_cols, fill_value=0)
        fig_heat = px.imshow(
            pivot_redac,
            text_auto=True,
            color_continuous_scale=["#FAFAFA", "#C0184A", "#8B1035"],
            aspect="auto",
            labels={"x": "", "y": "", "color": "Articles"},
        )
        fig_heat.update_layout(height=380, margin=dict(t=10, b=10))
        fig_heat.update_coloraxes(showscale=False)
        st.plotly_chart(fig_heat, width='stretch')

# ─────────────────────────────────────────────
# TAB 4 — HISTORIQUE
# ─────────────────────────────────────────────
with tab4:
    st.markdown("### 🗂️ Historique")

    hist = load_archive_summaries()

    if hist.empty:
        st.info("Aucune période archivée pour l'instant. Les données s'accumulent automatiquement à chaque chargement de CSV.")
    else:
        # ── Filtre type ──
        filtre = st.radio(
            "Afficher",
            ["Tout", "📅 Hebdo", "🗓️ Mensuel"],
            horizontal=True,
            label_visibility="collapsed",
        )
        if filtre != "Tout":
            hist = hist[hist["Type"] == filtre].reset_index(drop=True)

        hist = hist.sort_values("week_start").reset_index(drop=True)
        nb_weeks = len(hist)

        # ── KPIs historique ──
        kpis_h = [
            ("📅", str(nb_weeks),                                 "Périodes archivées"),
            ("👁️", fmt(hist["Vues totales"].sum()),               "Vues cumulées"),
            ("📝", str(hist["Articles"].sum()),                    "Articles au total"),
            ("📈", fmt(int(hist["Vues totales"].mean())),          "Vues moy. / période"),
        ]
        cards_h = "".join(
            f"<div class='kpi-card'><div class='kpi-icon'>{ico}</div>"
            f"<div class='kpi-val'>{val}</div><div class='kpi-lbl'>{lbl}</div></div>"
            for ico, val, lbl in kpis_h
        )
        st.markdown(f"<div class='kpi-grid'>{cards_h}</div>", unsafe_allow_html=True)

        # ── Évolution vues totales ──
        fig_h1 = px.area(
            hist, x="Période", y="Vues totales",
            title="Évolution des vues totales",
            color_discrete_sequence=["#C0184A"],
            markers=True,
        )
        fig_h1.update_layout(height=280, margin=dict(t=40, b=10), xaxis_tickangle=-20)
        st.plotly_chart(fig_h1, width='stretch')

        # ── Évolution articles + vues moyennes ──
        col_a, col_b = st.columns(2)
        with col_a:
            fig_h2 = px.bar(
                hist, x="Période", y="Articles",
                title="Nombre d'articles par période",
                color="Articles",
                color_continuous_scale=["#F5F3F5", "#C0184A", "#8B1035"],
                text="Articles",
            )
            fig_h2.update_traces(textposition="outside")
            fig_h2.update_layout(showlegend=False, coloraxis_showscale=False, height=280, margin=dict(t=40, b=10), xaxis_tickangle=-20)
            st.plotly_chart(fig_h2, width='stretch')

        with col_b:
            fig_h3 = px.line(
                hist, x="Période", y="Vues moyennes",
                title="Vues moyennes par article",
                color_discrete_sequence=["#C0184A"],
                markers=True,
            )
            fig_h3.update_layout(height=280, margin=dict(t=40, b=10), xaxis_tickangle=-20)
            st.plotly_chart(fig_h3, width='stretch')

        # ── Comparaison période courante vs précédente ──
        if nb_weeks >= 2:
            st.markdown("---")
            st.markdown("### 🔁 Comparaison période courante vs précédente")
            curr = hist.iloc[-1]
            prev = hist.iloc[-2]

            def delta_badge(curr_val, prev_val):
                if prev_val == 0:
                    return ""
                pct = (curr_val - prev_val) / prev_val * 100
                color = "#16a34a" if pct >= 0 else "#dc2626"
                arrow = "▲" if pct >= 0 else "▼"
                return f"<span style='color:{color};font-size:.85rem;font-weight:700;'>{arrow} {abs(pct):.1f}%</span>"

            comp_items = [
                ("👁️ Vues totales",   curr["Vues totales"],  prev["Vues totales"]),
                ("📝 Articles",        curr["Articles"],       prev["Articles"]),
                ("📊 Vues moyennes",   curr["Vues moyennes"], prev["Vues moyennes"]),
            ]
            cols_comp = st.columns(3)
            for col, (label, c_val, p_val) in zip(cols_comp, comp_items):
                badge = delta_badge(c_val, p_val)
                col.markdown(
                    f"<div style='background:#fff;border:1px solid #EAE4E8;border-top:4px solid #C0184A;"
                    f"border-radius:12px;padding:1rem 1.2rem;text-align:center;'>"
                    f"<div style='font-size:.72rem;font-weight:600;color:#7E6674;text-transform:uppercase;letter-spacing:.5px;'>{label}</div>"
                    f"<div style='font-size:1.6rem;font-weight:800;color:#C0184A;margin:.3rem 0;'>{fmt(c_val)}</div>"
                    f"<div style='font-size:.8rem;color:#999;'>vs {fmt(p_val)} &nbsp;{badge}</div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        # ── Tableau récap ──
        st.markdown("---")
        st.markdown("### 📋 Tableau de bord")
        display_hist = hist.drop(columns=["week_start", "filename"], errors="ignore").copy()
        display_hist["Vues totales"]  = display_hist["Vues totales"].apply(fmt)
        display_hist["Vues moyennes"] = display_hist["Vues moyennes"].apply(fmt)
        st.dataframe(display_hist[::-1].reset_index(drop=True), width='stretch', hide_index=True)

        # ── Suppression ──
        st.markdown("---")
        st.markdown("### 🗑️ Supprimer une semaine archivée")
        archived_list = gh_list_archives() if _is_cloud() else sorted([f for f in os.listdir(ARCHIVE_DIR) if f.endswith(".csv")], reverse=True)
        if archived_list:
            col_del, col_confirm = st.columns([3, 1])
            with col_del:
                to_delete = st.selectbox(
                    "Choisir la semaine à supprimer",
                    archived_list,
                    label_visibility="collapsed",
                )
            with col_confirm:
                if st.button("🗑️ Supprimer", type="primary"):
                    st.session_state["confirm_delete"] = to_delete

            if st.session_state.get("confirm_delete") == to_delete:
                st.warning(f"⚠️ Confirmer la suppression de **{to_delete}** ? Cette action est irréversible.")
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("✅ Oui, supprimer"):
                        if _is_cloud():
                            gh_delete_archive(to_delete)
                        else:
                            os.remove(os.path.join(ARCHIVE_DIR, to_delete))
                        st.cache_data.clear()
                        del st.session_state["confirm_delete"]
                        st.success(f"**{to_delete}** supprimé.")
                        st.rerun()
                with col_no:
                    if st.button("❌ Annuler"):
                        del st.session_state["confirm_delete"]
                        st.rerun()
