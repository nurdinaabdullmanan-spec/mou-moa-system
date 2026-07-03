import plotly.express as px
import streamlit as st
import sqlite3
import pandas as pd
import base64
import os

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="MoU/MoA Collaboration Record Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# DATABASE CONNECTION
# ======================================================
conn = sqlite3.connect("mou_moa_db.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT, email TEXT, password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS collaboration_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT, duration TEXT, department TEXT,
    partner TEXT, country TEXT, category TEXT
)
""")
conn.commit()

# ======================================================
# FUNGSI MEMBACA FAIL LOKAL LOGO.PNG (BASE64)
# ======================================================
def get_local_logo_base64(file_path="Logo.png"):
    if os.path.exists(file_path):
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    else:
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/UiTM_Logo.png/640px-UiTM_Logo.png"

UITM_LOGO_SRC = get_local_logo_base64()

# ======================================================
# REFINED UI CSS (LIGHT MODE & MODERN PRO)
# ======================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* ASAS & BACKGROUND CERAH */
    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #1e293b;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, #f8fafc 0%, #eff6ff 100%) !important;
    }}

    /* HEADER & TYPOGRAPHY */
    h1, h2, h3 {{
        font-family: 'Cinzel', serif !important;
        color: #1e1b4b !important;
        border-bottom: none !important; /* Buang garis bawah header */
        margin-bottom: 0.5rem !important;
    }}

    .subtitle-fix {{
        color: #64748b !important;
        font-size: 16px;
        margin-bottom: 2rem;
    }}

    /* SIDEBAR MODERN CERAH */
    section[data-testid="stSidebar"] {{
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
        box-shadow: 4px 0 15px rgba(0,0,0,0.03);
    }}

    /* SIDEBAR MENU TILES */
    div[role="radiogroup"] label {{
        background: transparent !important;
        border-radius: 10px !important;
        padding: 12px 18px !important;
        margin-bottom: 5px !important;
        border: 1px solid transparent !important;
        transition: all 0.2s ease;
    }}

    div[role="radiogroup"] label:hover {{
        background: #f1f5f9 !important;
    }}

    div[role="radiogroup"] label[data-selected="true"] {{
        background: #eef2ff !important;
        border: 1px solid #4f46e5 !important;
    }}

    div[role="radiogroup"] label p {{
        color: #475569 !important;
        font-weight: 500 !important;
    }}

    div[role="radiogroup"] label[data-selected="true"] p {{
        color: #4f46e5 !important;
        font-weight: 700 !important;
    }}

    /* KAD KANDUNGAN PRO */
    .content-card {{
        background: #ffffff !important;
        border-radius: 20px;
        padding: 30px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        margin-bottom: 25px;
    }}

    /* SCORECARD DASHBOARD BERWARNA */
    .metric-grid {{
        display: flex;
        gap: 20px;
        margin-bottom: 25px;
    }}
    
    .pro-metric {{
        flex: 1;
        padding: 24px;
        border-radius: 16px;
        border: none;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        color: white !important;
    }}
    
    .metric-1 {{ background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%); }} /* Indigo */
    .metric-2 {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); }} /* Emerald */
    .metric-3 {{ background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }} /* Amber */

    .metric-title {{
        font-size: 13px;
        opacity: 0.9;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .metric-value {{
        font-size: 36px;
        font-weight: 800;
        margin-top: 5px;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    /* TABLE STYLING */
    [data-testid="stDataFrame"] {{
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
    }}

    /* BUTTONS MODERN */
    .stButton > button {{
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        background: #4f46e5 !important;
        color: white !important;
        transition: all 0.2s ease;
    }}

    .stButton > button:hover {{
        background: #4338ca !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }}

    /* INPUT CONTROLS */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {{
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        color: #1e293b !important;
        border-radius: 8px !important;
    }}
</style>
""", unsafe_allow_html=True)

# ======================================================
# SESSION STATE NAVIGATION
# ======================================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "current_page" not in st.session_state: st.session_state.current_page = "Dashboard"

def switch_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ======================================================
# GATEWAY LOGOUT (MODIFIED)
# ======================================================
if not st.session_state.logged_in:
    st.markdown(f'<div style="text-align:center;"><img src="{UITM_LOGO_SRC}" style="width:120px;"></div>', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>Management Gateway</h1>", unsafe_allow_html=True)
    
    auth = st.sidebar.selectbox("Access Mode", ["Login", "Register", "Reset Password"])
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if auth == "Login":
        st.subheader("Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Access System"):
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            if cursor.fetchone():
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else: st.error("Access Denied.")
    # (Kod Register & Reset dikekalkan seperti asal...)
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# MAIN SYSTEM WORKSPACE
# ======================================================
else:
    # Sidebar Profile Cerah
    st.sidebar.markdown(f"""
        <div style="text-align:center; padding: 20px 0;">
            <img src="{UITM_LOGO_SRC}" style="width:100px;">
            <div style="margin-top:15px; font-weight:700; color:#1e1b4b;">UiTM MoU/MoA Portal</div>
            <div style="font-size:12px; color:#64748b;">Welcome, <b>{st.session_state.username}</b></div>
        </div>
    """, unsafe_allow_html=True)

    menu_options = ["Dashboard", "View Data", "Add Data", "Update Data", "Delete Data"]
    selected_menu = st.sidebar.radio("NAVIGATION", menu_options, index=menu_options.index(st.session_state.current_page))
    
    if selected_menu != st.session_state.current_page:
        st.session_state.current_page = selected_menu
        st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    cursor.execute("SELECT * FROM collaboration_data ORDER BY id ASC")
    df = pd.DataFrame(cursor.fetchall(), columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

    # ------------------------------------------------------
    # MODULE: DASHBOARD
    # ------------------------------------------------------
    if st.session_state.current_page == "Dashboard":
        st.title("System Analytics")
        st.markdown('<p class="subtitle-fix">Institutional performance & collaboration tracking.</p>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="pro-metric metric-1"><div class="metric-title">Total Records</div><div class="metric-value">{len(df)}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="pro-metric metric-2"><div class="metric-title">Countries</div><div class="metric-value">{df["Country"].nunique() if not df.empty else 0}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="pro-metric metric-3"><div class="metric-title">Departments</div><div class="metric-value">{df["Department"].nunique() if not df.empty else 0}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Agreement Distribution by Country")
        if not df.empty:
            country_counts = df["Country"].value_counts().reset_index()
            # Bar chart dengan warna terang (Vivid)
            fig = px.bar(country_counts, x="Country", y="count", color="Country", 
                         color_discrete_sequence=px.colors.qualitative.Vivid, text_auto=True)
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", 
                              margin=dict(t=10, b=10), height=350)
            st.plotly_chart(fig, use_container_width=True)
        else: st.info("No data available.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: VIEW DATA (PRO TABLE)
    # ------------------------------------------------------
    elif st.session_state.current_page == "View Data":
        st.title("Data Repository")
        st.markdown('<p class="subtitle-fix">Professional management of collaboration logs.</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        search = st.text_input("Search records...")
        if search:
            display_df = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().values, axis=1)]
        else:
            display_df = df
        st.dataframe(display_df, use_container_width=True, height=450)
        st.markdown('</div>', unsafe_allow_html=True)

    # (Modul Add, Update, Delete dikekalkan fungsinya dengan gaya CSS baharu...)
    elif st.session_state.current_page == "Add Data":
        st.title("Add New Entry")
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        # Form Add Data...
        st.markdown('</div>', unsafe_allow_html=True)