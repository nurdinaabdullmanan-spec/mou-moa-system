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

# CREATE TABLES
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, email TEXT, password TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS collaboration_data (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, duration TEXT, department TEXT, partner TEXT, country TEXT, category TEXT)")
conn.commit()

def get_local_logo_base64(file_path="Logo.png"):
    if os.path.exists(file_path):
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/UiTM_Logo.png/640px-UiTM_Logo.png"

UITM_LOGO_SRC = get_local_logo_base64()

# ======================================================
# REFINED UI CSS (PURPLE & GOLD RETAINED + PRO IMPROVEMENTS)
# ======================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
    
    /* 1. BACKGROUND PURPLE YANG LEBIH CERAH/VIBRANT */
    .stApp {{
        background: linear-gradient(135deg, #4b2e83 0%, #2e2640 100%) !important;
        color: #ffffff !important;
    }}

    /* 2. BUANG GARIS BAWAH TAJUK (HEADER) */
    h1, h2, h3 {{ 
        font-family: 'Cinzel', serif !important; 
        border-bottom: none !important; 
        color: #ffffff !important;
    }}

    /* 3. SIDEBAR MODERN & CANTIK (PURPLE THEME) */
    section[data-testid="stSidebar"] {{
        background: rgba(20, 15, 30, 0.95) !important;
        border-right: 1px solid rgba(250, 191, 44, 0.2) !important;
    }}
    
    div[role="radiogroup"] label {{
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 10px !important;
        margin-bottom: 8px !important;
        transition: 0.3s;
    }}
    
    div[role="radiogroup"] label[data-selected="true"] {{
        background: linear-gradient(90deg, #fabf2c 0%, #b45309 100%) !important;
    }}
    
    div[role="radiogroup"] label[data-selected="true"] p {{
        color: #000000 !important;
        font-weight: 700 !important;
    }}

    /* 4. BUTTON YELLOW GOLD KEKAL */
    .stButton > button {{
        background: linear-gradient(135deg, #fcd34d 0%, #fabf2c 50%, #b45309 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(250, 191, 44, 0.3);
    }}

    /* 5. TABLE PRO & KEMAS */
    [data-testid="stDataFrame"] {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
    }}

    /* 6. SCORECARD DASHBOARD WARNA WARNI */
    .metric-grid {{ display: flex; gap: 20px; margin-bottom: 30px; }}
    .pro-metric {{
        flex: 1; padding: 25px; border-radius: 18px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }}
    .metric-1 {{ background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%); }} /* Indigo */
    .metric-2 {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); }} /* Emerald */
    .metric-3 {{ background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }} /* Amber */
    
    .metric-title {{ font-size: 13px; font-weight: 600; opacity: 0.9; text-transform: uppercase; }}
    .metric-value {{ font-size: 38px; font-weight: 800; margin-top: 5px; }}

    .content-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 25px;
    }}
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOGIC NAVIGATION
# ======================================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "current_page" not in st.session_state: st.session_state.current_page = "Dashboard"

def switch_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ======================================================
# WORKSPACE
# ======================================================
if not st.session_state.logged_in:
    st.markdown(f'<div style="text-align:center;"><img src="{UITM_LOGO_SRC}" style="width:130px;"><h1>MoU/MoA Gateway</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Secure Login"):
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if cursor.fetchone():
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else: st.error("Invalid Credentials")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Sidebar Modern
    st.sidebar.markdown(f'<div style="text-align:center; padding:20px;"><img src="{UITM_LOGO_SRC}" style="width:100px;"><h3 style="color:#fabf2c;">{st.session_state.username}</h3></div>', unsafe_allow_html=True)
    
    menu = ["Dashboard", "View Data", "Add Data", "Update Data", "Delete Data"]
    choice = st.sidebar.radio("SYSTEM MENU", menu, index=menu.index(st.session_state.current_page))
    
    if choice != st.session_state.current_page:
        st.session_state.current_page = choice
        st.rerun()

    if st.sidebar.button("Terminated Session"):
        st.session_state.logged_in = False
        st.rerun()

    cursor.execute("SELECT * FROM collaboration_data")
    df = pd.DataFrame(cursor.fetchall(), columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

    if st.session_state.current_page == "Dashboard":
        st.title("📊 Analytics Dashboard")
        
        # 1. SCORECARD WARNA WARNI
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="pro-metric metric-1"><div class="metric-title">Agreements</div><div class="metric-value">{len(df)}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="pro-metric metric-2"><div class="metric-title">Countries</div><div class="metric-value">{df["Country"].nunique() if not df.empty else 0}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="pro-metric metric-3"><div class="metric-title">Partners</div><div class="metric-value">{df["Partner"].nunique() if not df.empty else 0}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("🌐 Global Distribution")
        if not df.empty:
            # 2. BAR CHART WARNA TERANG
            fig = px.bar(df["Country"].value_counts().reset_index(), x="Country", y="count", 
                         color="Country", color_discrete_sequence=px.colors.qualitative.Vivid)
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="white")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.current_page == "View Data":
        st.title("🗂️ Data Repository")
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        # 3. TABLE PRO & KEMAS
        st.dataframe(df, use_container_width=True, height=500)
        st.markdown('</div>', unsafe_allow_html=True)