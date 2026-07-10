import plotly.express as px
import streamlit as st
import sqlite3
import pandas as pd
import base64
import os
from datetime import datetime

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="MoU/MoA Collaboration Record Management",
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
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS collaboration_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    duration TEXT,
    department TEXT,
    partner TEXT,
    country TEXT,
    category TEXT
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
# SUPERIOR UI CSS (GLASSMORPHISM & MESH GRADIENT)
# ======================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Quicksand:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Quicksand', sans-serif;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Poppins', sans-serif !important;
        letter-spacing: -0.5px;
    }}
    
    /* MESH GRADIENT BACKGROUND - WOW FACTOR */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #f4f0fa !important;
        background-image: 
            radial-gradient(at 88% 0%, hsla(273, 73%, 89%, 1) 0px, transparent 50%), 
            radial-gradient(at 10% 28%, hsla(242, 100%, 93%, 1) 0px, transparent 50%), 
            radial-gradient(at 59% 79%, hsla(284, 100%, 93%, 1) 0px, transparent 50%) !important;
        background-attachment: fixed;
        color: #1e293b !important;
    }}

    /* HIDE DEFAULT ELEMENTS */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* SIDEBAR MENU - GLASSMORPHISM */
    section[data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.8) !important;
    }}
    
    div[role="radiogroup"] label input[type="radio"],
    div[role="radiogroup"] label > div:first-child {{
        display: none !important;
    }}

    div[role="radiogroup"] label {{
        display: flex !important;
        align-items: center !important;
        padding: 14px 20px !important;
        margin-bottom: 8px !important;
        border-radius: 12px !important;
        background: transparent !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        border: 1px solid transparent !important;
    }}

    div[role="radiogroup"] label p {{
        color: #475569 !important; 
        font-size: 15px !important;
        font-weight: 600 !important;
        margin-left: 0px !important;
        font-family: 'Poppins', sans-serif !important;
    }}

    div[role="radiogroup"] label:hover {{
        background: rgba(255, 255, 255, 0.9) !important;
        transform: translateX(5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }}

    div[role="radiogroup"] label[data-selected="true"] {{
        background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important; 
        box-shadow: 0 8px 20px rgba(124, 58, 237, 0.3) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }}

    div[role="radiogroup"] label[data-selected="true"] p {{
        color: #ffffff !important; 
        font-weight: 700 !important;
    }}

    /* KAD METRIK & DASHBOARD - FLOATING EFFECTS */
    .metric-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 35px; }}
    .metric-card {{
        background: rgba(255, 255, 255, 0.7); 
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 24px; 
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.8); 
        display: flex; align-items: center; gap: 18px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(124, 58, 237, 0.12);
    }}
    .metric-icon-box {{
        width: 60px; height: 60px; border-radius: 14px;
        display: flex; justify-content: center; align-items: center; font-size: 28px;
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);
    }}
    
    .metric-info h3 {{ margin: 0; font-size: 28px; color: #0f172a; font-weight: 800; line-height: 1.2; }}
    .metric-info p {{ margin: 0; font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
    
    .content-card {{
        background: rgba(255, 255, 255, 0.65) !important; 
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px; padding: 30px; 
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 12px 35px rgba(31, 38, 135, 0.04);
        margin-bottom: 24px;
        transition: all 0.3s ease;
    }}
    .content-card:hover {{
        box-shadow: 0 15px 45px rgba(31, 38, 135, 0.08);
    }}

    /* BUTTONS - GRADIENT & PILL SHAPE */
    .stButton > button, 
    button[kind="primary"], 
    button[kind="secondary"] {{
        border-radius: 50px !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        padding: 12px 28px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.25) !important;
    }}

    .stButton > button:hover, 
    button[kind="primary"]:hover, 
    button[kind="secondary"]:hover {{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 25px rgba(124, 58, 237, 0.4) !important;
        color: #ffffff !important;
    }}

    /* INPUT CONTROLS */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        border-radius: 12px !important; 
        border: 2px solid #e2e8f0 !important;
        background-color: rgba(255, 255, 255, 0.9) !important; 
        color: #1e293b !important; 
        padding: 12px 16px !important;
        font-family: 'Quicksand', sans-serif !important;
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.1) !important;
    }}
    
    /* TABLE STYLES - MODERNIZED */
    .table-container {{
        width: 100%; overflow-x: auto; border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.8); margin-top: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }}
    .styled-table {{
        width: 100%; border-collapse: collapse; margin: 0;
        font-size: 14px; font-family: 'Quicksand', sans-serif; 
        background-color: rgba(255,255,255,0.9);
    }}
    .styled-table thead tr {{
        background: linear-gradient(90deg, #f8fafc 0%, #f1f5f9 100%); 
        color: #334155; text-align: left;
    }}
    .styled-table th {{ 
        padding: 18px 24px; font-family: 'Poppins', sans-serif; 
        font-weight: 600; border-bottom: 2px solid #cbd5e1; white-space: nowrap; 
    }}
    .styled-table td {{ 
        padding: 16px 24px; border-bottom: 1px solid #f1f5f9; color: #475569; font-weight: 500; 
    }}
    .styled-table tbody tr {{ transition: background-color 0.2s ease; }}
    .styled-table tbody tr:hover {{ background-color: #f8fafc; cursor: pointer; }}

    /* LOGO BLENDING */
    .uitm-logo {{
        mix-blend-mode: multiply;
        filter: drop-shadow(0px 8px 16px rgba(124, 58, 237, 0.15));
        transition: transform 0.4s ease;
    }}
    .uitm-logo:hover {{
        transform: scale(1.05);
    }}
</style>
""", unsafe_allow_html=True)

# ======================================================
# SESSION STATE NAVIGATION CONTROLLER
# ======================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

def switch_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ======================================================
# GATEWAY LOGIN / REGISTER / RESET
# ======================================================
if not st.session_state.logged_in:
    spacer_left, center_col, spacer_right = st.columns([1, 1.5, 1])
    
    with center_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; padding: 16px 0;">
            <img src="{UITM_LOGO_SRC}" class="uitm-logo" alt="UiTM Logo" style="width: 280px;">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align:center; width:100%; margin-bottom: 30px;'>
            <h2 style='color:#0f172a !important; margin-bottom: 5px; font-weight: 800; font-size: 32px !important;'>
                Record Management System
            </h2>
            <p style='color: #64748b; font-size: 15px; margin-top: 0; font-weight: 600; letter-spacing: 1px;'>UiTM KAMPUS PERMATANG PAUH</p>
        </div>
        """, unsafe_allow_html=True)
        
        auth = st.selectbox("Secure Authentication Access", ["Login", "Register", "Reset Password"])

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        if auth == "Login":
            st.markdown("<h3 style='margin-bottom: 25px; font-size: 22px !important; color: #5b21b6 !important;'>🔑 Sign In to Portal</h3>", unsafe_allow_html=True)
            username = st.text_input("Corporate Username")
            password = st.text_input("Account Password", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Authenticate Session", use_container_width=True):
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
                user = cursor.fetchone()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Session secured. Redirecting...")
                    st.rerun()
                else:
                    st.error("Invalid database authentication keys.")

        elif auth == "Register":
            st.markdown("<h3 style='margin-bottom: 25px; font-size: 22px !important; color: #5b21b6 !important;'>📝 Register Account</h3>", unsafe_allow_html=True)
            new_username = st.text_input("Desired Username")
            new_email = st.text_input("Staff Email Address")
            new_password = st.text_input("Secure Password", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Deploy Account Meta", use_container_width=True):
                cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (new_username, new_email, new_password))
                conn.commit()
                st.success("Account committed successfully to cluster database.")

        elif auth == "Reset Password":
            st.markdown("<h3 style='margin-bottom: 25px; font-size: 22px !important; color: #5b21b6 !important;'>🔄 Reset Credentials</h3>", unsafe_allow_html=True)
            email = st.text_input("Registered Email Profile")
            new_password = st.text_input("Target New Password", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Override Encryption Key", use_container_width=True):
                cursor.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
                conn.commit()
                st.success("Password override processed successfully.")
                
        st.markdown('</div>', unsafe_allow_html=True)


# ======================================================
# ENTERPRISE CONSOLE APPLICATION WORKSPACE
# ======================================================
else:
    current_date = datetime.now().strftime("%d %B %Y")

    # SIDEBAR UI
    st.sidebar.markdown(f"""
        <div style="text-align:center; margin-bottom: 30px; padding-top: 10px;">
            <img src="{UITM_LOGO_SRC}" class="uitm-logo" style="width:140px; margin-bottom:15px;" alt="UiTM Logo">
            <h3 style="color:#0f172a; font-size:18px; font-weight:800; margin:0;">UiTM Permatang Pauh</h3>
            <p style="color:#64748b; font-size:12px; margin-top:4px; font-weight:600; line-height:1.4;">MoU/MoA Collaboration Record<br>Management System</p>
        </div>
        """, unsafe_allow_html=True)

    menu_options = [
        "🏠 Dashboard", 
        "📂 View All Records", 
        "➕ Add New Record", 
        "📝 Update Record", 
        "🗑️ Delete Record"
    ]
    
    clean_menu_options = [m.split(" ", 1)[1] for m in menu_options]
    
    current_index = 0
    if st.session_state.current_page in clean_menu_options:
        current_index = clean_menu_options.index(st.session_state.current_page)
    elif st.session_state.current_page == "Dashboard":
         current_index = 0
            
    selected_menu = st.sidebar.radio(
        "NAVIGATION",
        menu_options,
        index=current_index,
        label_visibility="collapsed"
    )
    
    selected_page_name = selected_menu.split(" ", 1)[1]
    if selected_page_name != st.session_state.current_page:
        st.session_state.current_page = selected_page_name
        st.rerun()

    st.sidebar.markdown("<hr style='margin: 30px 0 20px 0; border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(0,0,0,0.1), transparent);'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase; letter-spacing: 1px;'>Active Session</p>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <div style='background: rgba(124, 58, 237, 0.05); padding: 12px; border-radius: 12px; margin-bottom: 20px; border: 1px solid rgba(124, 58, 237, 0.1);'>
        <p style='color:#334155; font-size:15px; margin:0; font-family: "Poppins", sans-serif;'>👤 <b>{st.session_state.username}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Logout Session", key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # Read Core Table Stream
    cursor.execute("SELECT * FROM collaboration_data ORDER BY id ASC")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

    # ------------------------------------------------------
    # MODULE: DASHBOARD
    # ------------------------------------------------------
    if st.session_state.current_page == "Dashboard":
        col_greet, col_date = st.columns([3, 1])
        with col_greet:
            st.markdown(f"""
            <h1 style='color:#0f172a; margin-bottom: 8px; font-weight:800; font-size: 34px;'>Good Afternoon, {st.session_state.username}! 👋</h1>
            <p style='color:#64748b; font-size:16px; margin-top:0; font-weight:500;'>Here is the latest overview of the MoU/MoA Collaboration Data.</p>
            """, unsafe_allow_html=True)
        with col_date:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.8); backdrop-filter:blur(10px); padding:12px 20px; border-radius:16px; border:1px solid rgba(255,255,255,0.9); display:flex; align-items:center; gap:15px; float:right; box-shadow: 0 8px 20px rgba(0,0,0,0.03);'>
                <div style='background: #f3e8ff; width: 40px; height: 40px; border-radius: 10px; display: flex; justify-content: center; align-items: center; font-size:20px;'>📅</div>
                <div>
                    <div style='font-size:11px; color:#64748b; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;'>Today's Date</div>
                    <div style='font-size:14px; font-weight:700; color:#1e293b;'>{current_date}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        valid_categories = ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"]
        df_filtered = df[df["Category"].isin(valid_categories)]
        
        total_records = len(df)
        total_country = df["Country"].nunique() if total_records > 0 else 0
        total_category = 2 
        active_agreements = len(df)

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card" style="border-bottom: 4px solid #8b5cf6;">
                <div class="metric-icon-box" style="background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%); color:#8b5cf6;">📄</div>
                <div class="metric-info">
                    <h3>{total_records}</h3>
                    <p style="color: #6d28d9;">Total Agreements</p>
                </div>
            </div>
            <div class="metric-card" style="border-bottom: 4px solid #10b981;">
                <div class="metric-icon-box" style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); color:#10b981;">🌐</div>
                <div class="metric-info">
                    <h3>{total_country}</h3>
                    <p style="color: #059669;">Countries Involved</p>
                </div>
            </div>
            <div class="metric-card" style="border-bottom: 4px solid #f59e0b;">
                <div class="metric-icon-box" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); color:#f59e0b;">🤝</div>
                <div class="metric-info">
                    <h3>{total_category}</h3>
                    <p style="color: #d97706;">Core Categories</p>
                </div>
            </div>
            <div class="metric-card" style="border-bottom: 4px solid #ef4444;">
                <div class="metric-icon-box" style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); color:#ef4444;">📂</div>
                <div class="metric-info">
                    <h3>{active_agreements}</h3>
                    <p style="color: #dc2626;">Active Records</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 20px; color:#0f172a; margin-bottom: 20px;'>🌍 Agreements by Country</h3>", unsafe_allow_html=True)
            if total_records > 0:
                country_chart = df["Country"].value_counts().reset_index()
                country_chart.columns = ["Country", "Total"]
                fig1 = px.bar(country_chart, x="Country", y="Total", text_auto=True, 
                              color="Country", color_discrete_sequence=px.colors.qualitative.Pastel)
                fig1.update_layout(showlegend=False, margin=dict(t=10, b=10, l=0, r=0), height=320, 
                                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                   font=dict(family="Quicksand"))
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("No mapping data available yet.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_chart2:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 20px; color:#0f172a; margin-bottom: 20px;'>📊 Agreements by Category</h3>", unsafe_allow_html=True)
            
            if total_records > 0:
                cat_data = df["Category"].value_counts().reindex(
                    ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"], 
                    fill_value=0
                ).reset_index()
                cat_data.columns = ["Category", "Total"]
                
                fig2 = px.pie(cat_data, values="Total", names="Category", hole=0.6, 
                              color_discrete_sequence=["#8b5cf6", "#10b981"]) 
                
                fig2.update_layout(margin=dict(t=10, b=10, l=0, r=0), height=320,
                                   paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Quicksand"),
                                   legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No distribution data available yet.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 20px; color:#0f172a; margin-bottom: 20px;'>⚡ Recent Added Records</h3>", unsafe_allow_html=True)
        
        if len(df) > 0:
            st.markdown(f"""
            <div class="table-container">
                {df.tail(5).to_html(index=False, classes="styled-table", escape=False)}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No recent records to display.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: VIEW DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "View All Records":
        st.markdown("<h1 style='color:#0f172a; margin-bottom: 20px;'>📂 Master Data Repository</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        search = st.text_input("🔍 Search Matrix (Enter Title, Partner or Country)", placeholder="Type to filter records...")

        if search:
            sql = "SELECT * FROM collaboration_data WHERE title LIKE ? OR partner LIKE ? OR country LIKE ?"
            cursor.execute(sql, (f"%{search}%", f"%{search}%", f"%{search}%"))
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

        if len(df) > 0:
            html_table = df.to_html(index=False, classes="styled-table", escape=False)
            st.markdown(f'<div class="table-container">{html_table}</div>', unsafe_allow_html=True)
        else:
            st.info("No data found in the repository matching your query.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_spacer, col_btn_cancel = st.columns([8, 2])
        with col_btn_cancel:
            if st.button("← Return Dashboard", key="back_view", use_container_width=True):
                switch_page("Dashboard")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: ADD DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "Add New Record":
        st.markdown("<h1 style='color:#0f172a; margin-bottom: 20px;'>➕ Create New Record</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        st.markdown("<h4 style='color:#5b21b6; margin-bottom: 15px;'>📄 Document Details</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            id_in = st.number_input("Assign Record ID", min_value=1, step=1, format="%d")
            category = st.selectbox("Agreement Core Category", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"])
        with col2:
            title = st.text_input("Agreement Title")
            duration = st.text_input("Active Duration (e.g. 3 Years)")

        st.markdown("<hr style='border: 1px dashed rgba(0,0,0,0.1); margin:25px 0;'>", unsafe_allow_html=True)

        st.markdown("<h4 style='color:#5b21b6; margin-bottom: 15px;'>🤝 Partnership Information</h4>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            department = st.text_input("Executing Department / Faculty")
            country = st.text_input("Country Location")
        with col4:
            partner = st.text_input("External Partner Institution")

        st.markdown("<hr style='border: 1px solid rgba(0,0,0,0.05); margin:30px 0 20px 0;'>", unsafe_allow_html=True)

        col_btn_save, col_spacer, col_btn_cancel = st.columns([2.5, 5, 2.5])
        
        with col_btn_save:
            if st.button("💾 Save Record Securely", use_container_width=True):
                cursor.execute("INSERT INTO collaboration_data (id, title, duration, department, partner, country, category) VALUES (?,?,?,?,?,?,?)",
                               (int(id_in), title, duration, department, partner, country, category))
                conn.commit()
                st.success("New legal record successfully mapped into SQL table cluster.")
                switch_page("View All Records")
                
        with col_btn_cancel:
            if st.button("❌ Cancel & Return", key="back_add", use_container_width=True):
                switch_page("Dashboard")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: UPDATE DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "Update Record":
        st.markdown("<h1 style='color:#0f172a; margin-bottom: 20px;'>📝 Modify Existing Record</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        uid = st.number_input("Target Record ID to Modify", min_value=1, step=1, format="%d")
        cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(uid),))
        result = cursor.fetchone()

        if result:
            st.markdown("<hr style='border: 1px dashed rgba(0,0,0,0.1); margin:25px 0;'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Agreement Title Statement", result[1])
                duration = st.text_input("Active Lifespan Duration", result[2])
                department = st.text_input("Executing Department", result[3])
            with col2:
                partner = st.text_input("External Partner Institution", result[4])
                country = st.text_input("Country Location", result[5])
                category = st.selectbox("Agreement Core Category Designation", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"], 
                                        index=["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"].index(result[6]) if result[6] in ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"] else 0)

            st.markdown("<br>", unsafe_allow_html=True)
            
            col_btn_update, col_spacer, col_btn_cancel = st.columns([2.5, 5, 2.5])
            
            with col_btn_update:
                if st.button("🔄 Update Changes", use_container_width=True):
                    cursor.execute("UPDATE collaboration_data SET title=?, duration=?, department=?, partner=?, country=?, category=? WHERE id=?",
                                   (title, duration, department, partner, country, category, int(uid)))
                    conn.commit()
                    st.success("Record has been successfully synchronized.")
                    switch_page("View All Records")
                    
            with col_btn_cancel:
                if st.button("❌ Cancel & Return", key="back_update", use_container_width=True):
                    switch_page("Dashboard")
                
        else:
            st.warning("Target ID does not exist in the database system. Please verify the ID.")
            st.markdown("<br>", unsafe_allow_html=True)
            col_spacer, col_btn_cancel = st.columns([8, 2])
            with col_btn_cancel:
                if st.button("← Return", key="back_update_fail", use_container_width=True):
                    switch_page("Dashboard")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: DELETE DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "Delete Record":
        st.markdown("<h1 style='color:#0f172a; margin-bottom: 20px;'>🗑️ Purge Record Data</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        del_id = st.number_input("Target Record ID to Delete", min_value=1, step=1, format="%d")
        
        st.markdown("""
        <div style='background: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; border-radius: 8px; margin-top: 15px;'>
            <p style='color: #991b1b; margin: 0; font-weight: 600;'>💣 Critical Warning: Purging actions cannot be rolled back or undone.</p>
        </div>
        """, unsafe_allow_html=True)

        @st.dialog("⚠️ Confirm Permanent Deletion")
        def confirm_delete_dialog(record_id):
            st.warning(f"Are you absolutely sure you want to permanently delete Record ID **{record_id}**?")
            st.write("This action will immediately wipe the data from the database.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_yes, col_spacer_dialog, col_cancel = st.columns([4, 2, 4])
            
            with col_yes:
                if st.button("Yes, Purge Now", use_container_width=True):
                    cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(record_id),))
                    if cursor.fetchone():
                        cursor.execute("DELETE FROM collaboration_data WHERE id=?", (int(record_id),))
                        conn.commit()
                        st.success(f"Record ID {record_id} cleared safely.")
                        switch_page("View All Records")
                    else:
                        st.error("Deletion failed: Target ID is not found.")
            
            with col_cancel:
                if st.button("Cancel Operation", key="dialog_cancel", use_container_width=True):
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_btn_del, col_spacer, col_btn_cancel = st.columns([3, 4, 3])
        
        with col_btn_del:
            if st.button("🚨 Authorize Deletion", use_container_width=True):
                confirm_delete_dialog(del_id)
                
        with col_btn_cancel:
            if st.button("❌ Cancel & Return", key="back_delete", use_container_width=True):
                switch_page("Dashboard")
            
        st.markdown('</div>', unsafe_allow_html=True)