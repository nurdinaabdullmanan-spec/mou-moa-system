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
# REFINED UI CSS (BESAR, JELAS, CLEAN & NO RADIO DOTS)
# ======================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* BACKGROUND UTAMA */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: #f8fafc !important; 
        color: #0f172a !important;
    }}

    /* HIDE DEFAULT ELEMENTS */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* ======================================================
       SIDEBAR MENU (PUTIH BERSIH)
       ====================================================== */
    section[data-testid="stSidebar"] {{
        background-color: #ffffff !important; 
        border-right: 1px solid #e2e8f0 !important;
    }}
    
    /* 💥 BUANG BULATAN RADIO SECARA KEKAL 💥 */
    div[data-baseweb="radio"] > div:first-child {{
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
    }}

    /* GAYA MENU ITEM (INACTIVE) - BESAR DAN JELAS */
    div[data-baseweb="radio"] {{
        display: flex !important;
        align-items: center !important;
        padding: 14px 24px !important;
        margin-bottom: 8px !important;
        border-radius: 10px !important;
        background: transparent !important;
        transition: all 0.2s ease-in-out;
        cursor: pointer;
        border: none !important;
    }}

    div[data-baseweb="radio"] p {{
        color: #475569 !important; 
        font-size: 15px !important;
        font-weight: 500 !important;
        margin-left: 0px !important;
    }}

    div[data-baseweb="radio"]:hover {{
        background: #f1f5f9 !important;
    }}

    /* GAYA MENU ITEM (ACTIVE - PURPLE TERANG) */
    div[role="radiogroup"] label[data-selected="true"] div[data-baseweb="radio"] {{
        background: #7c3aed !important; 
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25) !important;
    }}

    div[role="radiogroup"] label[data-selected="true"] p {{
        color: #ffffff !important; 
        font-weight: 700 !important;
        font-size: 15.5px !important;
    }}

    /* ======================================================
       KAD METRIK & DASHBOARD (WARNA WARNI & BESAR)
       ====================================================== */
    .metric-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 35px; }}
    .metric-card {{
        background: #ffffff; padding: 25px 20px; border-radius: 16px;
        border: 1px solid #e2e8f0; display: flex; align-items: center; gap: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }}
    .metric-icon-box {{
        width: 60px; height: 60px; border-radius: 14px;
        display: flex; justify-content: center; align-items: center; font-size: 30px;
    }}
    
    /* WARNA IKON SCORECARD YANG TERANG */
    .icon-purple {{ background: #e9d5ff; color: #7e22ce; }}
    .icon-green {{ background: #bbf7d0; color: #15803d; }}
    .icon-orange {{ background: #fed7aa; color: #c2410c; }}
    .icon-blue {{ background: #bfdbfe; color: #1d4ed8; }}
    
    .metric-info h3 {{ margin: 0; font-size: 28px; color: #0f172a; font-weight: 800; line-height: 1.1; }}
    .metric-info p {{ margin: 0; font-size: 13.5px; color: #64748b; font-weight: 500; margin-top: 4px; }}
    
    .content-card {{
        background: #ffffff !important; 
        border-radius: 16px; padding: 25px; border: 1px solid #e2e8f0;
        margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }}

    /* BUTTONS UMUM (PURPLE) */
    .stButton > button {{
        width: 100%; border-radius: 10px; border: none;
        padding: 12px; font-weight: 700; font-size: 15px;
        color: #ffffff !important; background: #7c3aed !important;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover {{ background: #6d28d9 !important; box-shadow: 0 4px 12px rgba(109, 40, 217, 0.3); }}

    /* BACK SYSTEM BUTTON */
    .back-btn-container .stButton > button {{
        width: auto !important; background: transparent !important; color: #7c3aed !important;
        border: 2px solid #e2e8f0 !important; padding: 8px 20px !important; box-shadow: none !important;
    }}
    .back-btn-container .stButton > button:hover {{ background: #f8fafc !important; border-color: #cbd5e1 !important; }}

    /* TABLE STYLES */
    .table-container {{
        width: 100%; overflow-x: auto; border-radius: 12px;
        border: 1px solid #e2e8f0; margin-top: 15px;
    }}
    .styled-table {{
        width: 100%; border-collapse: collapse; margin: 0;
        font-size: 14px; font-family: 'Inter', sans-serif; background-color: #ffffff;
    }}
    .styled-table thead tr {{ background-color: #f1f5f9; color: #334155; text-align: left; }}
    .styled-table th {{ padding: 16px 20px; font-weight: 700; border-bottom: 2px solid #e2e8f0; white-space: nowrap; }}
    .styled-table td {{ padding: 16px 20px; border-bottom: 1px solid #f1f5f9; color: #475569; }}
    .styled-table tbody tr:hover {{ background-color: #f8fafc; }}
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
        st.markdown(f"""
        <div style="text-align: center; padding: 15px 0;">
            <img src="{UITM_LOGO_SRC}" alt="UiTM Logo" style="width: 130px;">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align:center; width:100%; margin-bottom: 25px;'>
            <h2 style='color:#0f172a !important; border:none; margin-bottom: 5px; font-weight: 800; font-size: 26px !important;'>
                Record Management System
            </h2>
            <p style='color: #64748b; font-size: 15px; margin-top: 0; font-weight: 500;'>UiTM Kampus Permatang Pauh</p>
        </div>
        """, unsafe_allow_html=True)
        
        auth = st.selectbox("Authentication Type", ["Login", "Register", "Reset Password"], label_visibility="collapsed")

        st.markdown('<div class="content-card" style="padding: 30px; margin-top: 15px; border: none; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
        
        if auth == "Login":
            st.markdown("<h3 style='margin-bottom: 20px; font-size: 22px !important; color: #0f172a !important;'>🔑 Sign In</h3>", unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Log In"):
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
                user = cursor.fetchone()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password.")

        elif auth == "Register":
            st.markdown("<h3 style='margin-bottom: 20px; font-size: 22px !important; color: #0f172a !important;'>📝 Register Account</h3>", unsafe_allow_html=True)
            new_username = st.text_input("New Username")
            new_email = st.text_input("Staff Email Address")
            new_password = st.text_input("New Password", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Register Account"):
                cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (new_username, new_email, new_password))
                conn.commit()
                st.success("Account successfully created. Please switch to Login.")

        elif auth == "Reset Password":
            st.markdown("<h3 style='margin-bottom: 20px; font-size: 22px !important; color: #0f172a !important;'>🔄 Reset Credentials</h3>", unsafe_allow_html=True)
            email = st.text_input("Registered Email")
            new_password = st.text_input("New Password", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Reset Password"):
                cursor.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
                conn.commit()
                st.success("Password has been reset.")
                
        st.markdown('</div>', unsafe_allow_html=True)


# ======================================================
# ENTERPRISE CONSOLE APPLICATION WORKSPACE
# ======================================================
else:
    current_date = datetime.now().strftime("%d %B %Y")

    # SIDEBAR UI
    st.sidebar.markdown(f"""
        <div style="text-align:center; margin-bottom: 25px; margin-top: 10px;">
            <img src="{UITM_LOGO_SRC}" style="width:110px; margin-bottom:15px;" alt="UiTM Logo">
            <h3 style="color:#0f172a; font-size:18px; font-weight:800; margin:0;">MoU/MoA</h3>
            <p style="color:#64748b; font-size:12px; margin:0; line-height:1.4; font-weight: 500;">Collaboration Record<br>Management System</p>
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

    # User Menu & Logout
    st.sidebar.markdown("<hr style='margin: 30px 0 15px 0; border: 0.5px solid #e2e8f0;'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='font-size:11px; color:#94a3b8; font-weight:700; letter-spacing: 0.5px; text-transform:uppercase;'>USER PROFILE</p>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p style='color:#334155; font-size:15px; font-weight:600; margin-bottom:20px;'>👤 {st.session_state.username}</p>", unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Logout", key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # Data Fetching
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
            <h2 style='color:#0f172a; margin-bottom: 5px; font-weight:800; font-size: 32px;'>Good Afternoon, {st.session_state.username}! 👋</h2>
            <p style='color:#64748b; font-size:16px; margin-top:0;'>Welcome back to your Collaboration Management System.</p>
            """, unsafe_allow_html=True)
        with col_date:
            st.markdown(f"""
            <div style='background:#ffffff; padding:12px 20px; border-radius:12px; border:1px solid #e2e8f0; display:flex; align-items:center; gap:12px; float:right; box-shadow: 0 2px 8px rgba(0,0,0,0.02);'>
                <span style='font-size:22px;'>📅</span>
                <div>
                    <div style='font-size:11px; color:#64748b; font-weight: 600; text-transform:uppercase;'>Today's Date</div>
                    <div style='font-size:14px; font-weight:700; color:#0f172a;'>{current_date}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        total_records = len(df)
        total_country = df["Country"].nunique() if total_records > 0 else 0
        total_category = df["Category"].nunique() if total_records > 0 else 0
        active_agreements = len(df) 

        # KAD METRIK WARNA WARNI
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-icon-box icon-purple">📄</div>
                <div class="metric-info">
                    <h3>{total_records}</h3>
                    <p>Total Agreements</p>
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-icon-box icon-green">🌐</div>
                <div class="metric-info">
                    <h3>{total_country}</h3>
                    <p>Countries Involved</p>
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-icon-box icon-orange">🤝</div>
                <div class="metric-info">
                    <h3>{total_category}</h3>
                    <p>Categories</p>
                </div>
            </div>
            <div class="metric-card">
                <div class="metric-icon-box icon-blue">📂</div>
                <div class="metric-info">
                    <h3>{active_agreements}</h3>
                    <p>Active Agreements</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # CARTA WARNA WARNI
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("<p style='font-weight:700; font-size:18px; color:#0f172a; margin-bottom: 20px;'>Agreements by Country</p>", unsafe_allow_html=True)
            if total_records > 0:
                country_chart = df["Country"].value_counts().reset_index()
                country_chart.columns = ["Country", "Total"]
                # Tambah color_discrete_sequence untuk warna warni terang
                fig1 = px.bar(
                    country_chart, x="Country", y="Total", text_auto=True, 
                    color="Country", 
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig1.update_layout(showlegend=False, margin=dict(t=10, b=10, l=0, r=0), height=320, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("No data available.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_chart2:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("<p style='font-weight:700; font-size:18px; color:#0f172a; margin-bottom: 20px;'>Agreements by Category</p>", unsafe_allow_html=True)
            if total_records > 0:
                cat_chart = df["Category"].value_counts().reset_index()
                cat_chart.columns = ["Category", "Total"]
                # Guna tema warna warni Set3
                fig2 = px.pie(
                    cat_chart, values="Total", names="Category", hole=0.45,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig2.update_layout(margin=dict(t=10, b=10, l=0, r=0), height=320)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No data available.")
            st.markdown('</div>', unsafe_allow_html=True)

        # RECENT RECORDS PREVIEW
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("<p style='font-weight:700; font-size:18px; color:#0f172a; margin-bottom:15px;'>Recent Records</p>", unsafe_allow_html=True)
        if len(df) > 0:
            st.dataframe(df.tail(5), use_container_width=True, hide_index=True)
        else:
            st.info("No records to display.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: VIEW DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "View All Records":
        st.title("📂 View All Records")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        search = st.text_input("🔍 Search Database (Title, Partner, or Country)")

        if search:
            sql = "SELECT * FROM collaboration_data WHERE title LIKE ? OR partner LIKE ? OR country LIKE ?"
            cursor.execute(sql, (f"%{search}%", f"%{search}%", f"%{search}%"))
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

        if len(df) > 0:
            html_table = df.to_html(index=False, classes="styled-table", escape=False)
            st.markdown(f'<div class="table-container">{html_table}</div>', unsafe_allow_html=True)
        else:
            st.info("No data found.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Back to Dashboard", key="back_view"):
            switch_page("Dashboard")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: ADD DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "Add New Record":
        st.title("➕ Add New Record")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            id_in = st.number_input("Record ID", min_value=1, step=1, format="%d")
            title = st.text_input("Agreement Title")
            duration = st.text_input("Duration (e.g., 3 Years)")
            department = st.text_input("Department / Faculty")
        with col2:
            partner = st.text_input("External Partner")
            country = st.text_input("Country")
            category = st.selectbox("Category", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save Record"):
            cursor.execute("INSERT INTO collaboration_data (id, title, duration, department, partner, country, category) VALUES (?,?,?,?,?,?,?)",
                           (int(id_in), title, duration, department, partner, country, category))
            conn.commit()
            st.success("New record successfully saved.")
            switch_page("View All Records")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Cancel & Back", key="back_add"):
            switch_page("Dashboard")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: UPDATE DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "Update Record":
        st.title("📝 Update Record")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        uid = st.number_input("Enter Record ID to Update", min_value=1, step=1, format="%d")
        cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(uid),))
        result = cursor.fetchone()

        if result:
            st.markdown("<hr style='border: 1px dashed #e2e8f0; margin:20px 0;'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Agreement Title", result[1])
                duration = st.text_input("Duration", result[2])
                department = st.text_input("Department", result[3])
            with col2:
                partner = st.text_input("Partner Institution", result[4])
                country = st.text_input("Country", result[5])
                category = st.selectbox("Category", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"])

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Update Changes"):
                cursor.execute("UPDATE collaboration_data SET title=?, duration=?, department=?, partner=?, country=?, category=? WHERE id=?",
                               (title, duration, department, partner, country, category, int(uid)))
                conn.commit()
                st.success("Record updated successfully.")
                switch_page("View All Records")
        else:
            st.warning("ID not found in database.")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Cancel & Back", key="back_update"):
            switch_page("Dashboard")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: DELETE DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "Delete Record":
        st.title("🗑️ Delete Record")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        del_id = st.number_input("Enter Record ID to Delete", min_value=1, step=1, format="%d")
        st.error("💣 Warning: Deletions are permanent.")

        @st.dialog("⚠️ Confirm Deletion")
        def confirm_delete_dialog(record_id):
            st.warning(f"Are you sure you want to delete Record ID **{record_id}**?")
            
            col_yes, col_cancel = st.columns([1, 1])
            with col_yes:
                if st.button("Yes, Delete", use_container_width=True):
                    cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(record_id),))
                    if cursor.fetchone():
                        cursor.execute("DELETE FROM collaboration_data WHERE id=?", (int(record_id),))
                        conn.commit()
                        st.success(f"Record {record_id} deleted.")
                        switch_page("View All Records")
                    else:
                        st.error("ID not found.")
            with col_cancel:
                if st.button("Cancel", use_container_width=True):
                    st.rerun()

        if st.button("Confirm Delete"):
            confirm_delete_dialog(del_id)
                
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Cancel & Back", key="back_delete"):
            switch_page("Dashboard")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)