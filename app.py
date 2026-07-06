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
# REFINED UI CSS (CLEAN SIDEBAR, BEAUTIFUL TABLE)
# ======================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght=600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* PENGURUSAN FONT */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    h1, h2, h3, .uitm-title {{
        font-family: 'Cinzel', serif !important;
    }}

    /* BACKGROUND UTAMA PUTIH/KELABU CAIR */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: #f8fafc !important; 
        color: #1e293b !important;
    }}
    
    .block-container {{
        padding: 2.5rem 5rem !important;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* FIX WARNA LABEL */
    [data-testid="stWidgetLabel"] p, 
    label[data-testid="stWidgetLabel"] {{
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }}

    /* ======================================================
       MINIMALIST SIDEBAR (NEW CLEAN DESIGN)
       ====================================================== */
    section[data-testid="stSidebar"] {{
        background-color: #ffffff !important; 
        border-right: 1px solid #e2e8f0 !important;
        box-shadow: none !important;
    }}
    
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label {{
        color: #334155 !important;
    }}

    /* HIDE THE RADIO BUTTON CIRCLES */
    div[role="radiogroup"] label [data-testid="stMarkdownContainer"]::before,
    div[role="radiogroup"] label [data-baseweb="radio"] div {{
        display: none !important;
    }}

    /* CLEAN LIST STYLING FOR SIDEBAR MENU */
    div[role="radiogroup"] {{
        display: flex;
        flex-direction: column;
        gap: 2px !important;
        padding-top: 5px;
    }}

    div[role="radiogroup"] label {{
        background: transparent !important;
        border-radius: 8px !important;
        padding: 10px 15px !important;
        border: none !important;
        box-shadow: none !important;
        transition: background-color 0.2s ease, color 0.2s ease !important;
        margin: 0 !important;
        cursor: pointer;
    }}

    div[role="radiogroup"] label:hover {{
        background: #f1f5f9 !important;
        transform: none !important; /* No jumping effect */
    }}

    div[role="radiogroup"] label p {{
        color: #64748b !important;
        font-size: 15px !important;
        font-weight: 500 !important;
    }}

    /* ACTIVE MENU ITEM */
    div[role="radiogroup"] label[data-selected="true"] {{
        background: #f1f5f9 !important; 
        border: none !important; 
        box-shadow: none !important;
    }}

    div[role="radiogroup"] label[data-selected="true"] p {{
        color: #0f172a !important;
        font-weight: 600 !important;
    }}

    /* LOGO & PROFILE DI SIDEBAR (CLEAN THEME) */
    .sidebar-profile {{
        text-align: center; 
        padding: 10px 0 25px 0;
        border-bottom: 1px solid #f1f5f9;
        margin-bottom: 15px;
    }}
    .sidebar-profile .uitm-title {{
        font-family: 'Cinzel', serif; 
        font-size: 18px; 
        font-weight: 700; 
        color: #334155; 
    }}
    .sidebar-profile .campus {{
        color: #94a3b8; 
        font-size: 10px; 
        margin-top: 2px; 
        text-transform: uppercase; 
        letter-spacing: 1px;
    }}
    .sidebar-profile .badge {{
        margin-top: 12px; 
        background: #f8fafc; 
        padding: 6px 14px; 
        border-radius: 30px; 
        display: inline-block; 
        border: 1px solid #e2e8f0;
    }}
    .sidebar-profile .badge span:first-child {{ color: #10b981; font-size: 10px; }}
    .sidebar-profile .badge span:last-child {{ color: #475569; font-size: 12px; font-weight: 600; margin-left: 5px; }}


    /* LOGO BLENDING EFFECT (LOGIN PAGE) */
    .logo-container {{ text-align: center; padding: 15px 0; }}
    .uitm-logo {{
        width: 140px;
        filter: drop-shadow(0px 0px 12px rgba(75, 46, 131, 0.15));
        display: block;
        margin: 0 auto;
    }}

    /* TYPOGRAPHY UTAMA */
    h1 {{
        color: #1e293b !important; 
        font-weight: 700 !important;
        margin-bottom: 30px !important;
    }}
    h2, h3 {{ color: #334155 !important; font-weight: 600 !important; }}

    /* KAD CONTAINER CERAH */
    .content-card {{
        background: #ffffff !important; 
        border-radius: 16px;
        padding: 30px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
        margin-bottom: 30px;
    }}

    /* METRIC PANELS (SCORECARDS WARNA WARNI) */
    .metric-grid {{ display: flex; gap: 20px; margin-bottom: 30px; }}
    .pro-metric {{
        flex: 1;
        background: #ffffff;
        padding: 24px 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }}
    .metric-1 {{ border-left: 6px solid #5a3982 !important; }}
    .metric-2 {{ border-left: 6px solid #1f6a8d !important; }}
    .metric-3 {{ border-left: 6px solid #edb100 !important; }}

    .metric-title {{
        font-size: 10px; color: #64748b; font-weight: 600;
        text-transform: uppercase; letter-spacing: 1px;
    }}
    .metric-value {{
        font-size: 32px; font-weight: 800; color: #1e293b;
        margin-top: 5px; font-family: 'Inter', sans-serif;
    }}

    /* BUTTONS UMUM */
    .stButton > button {{
        width: 100%;
        border-radius: 8px;
        border: none;
        padding: 10px;
        font-weight: 600;
        color: #ffffff !important; 
        background: #4b2e83 !important;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{ background: #3b2466 !important; }}

    /* LOGOUT BUTTON CLEAN */
    section[data-testid="stSidebar"] .stButton > button {{
        background: #f1f5f9 !important;
        color: #64748b !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: none !important;
    }}
    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: #fee2e2 !important;
        color: #ef4444 !important;
        border-color: #fca5a5 !important;
    }}

    /* INPUT CONTROLS */
    .stTextInput input, .stNumberInput input, textarea, .stSelectbox div[data-baseweb="select"] {{
        border-radius: 8px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #ffffff !important;
        color: #1e293b !important;
    }}

    /* ======================================================
       BEAUTIFUL CUSTOM TABLE CSS
       ====================================================== */
    .table-container {{
        width: 100%;
        overflow-x: auto;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        margin-top: 15px;
    }}
    .styled-table {{
        width: 100%;
        border-collapse: collapse;
        margin: 0;
        font-size: 14px;
        font-family: 'Inter', sans-serif;
        background-color: #ffffff;
    }}
    .styled-table thead tr {{
        background-color: #f8fafc;
        color: #475569;
        text-align: left;
    }}
    .styled-table th {{
        padding: 16px 20px;
        font-weight: 600;
        border-bottom: 2px solid #e2e8f0;
        white-space: nowrap;
    }}
    .styled-table td {{
        padding: 16px 20px;
        border-bottom: 1px solid #f1f5f9;
        color: #334155;
    }}
    .styled-table tbody tr {{
        transition: background-color 0.2s ease;
    }}
    .styled-table tbody tr:hover {{
        background-color: #f8fafc;
    }}
    .styled-table tbody tr:last-of-type td {{
        border-bottom: none;
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
    # Buang emoji masa nak set page nama (emoji cuma untuk visual)
    clean_name = page_name.split(" ", 1)[1] if " " in page_name and len(page_name.split(" ", 1)[0]) <= 2 else page_name
    st.session_state.current_page = clean_name
    st.rerun()

# ======================================================
# GATEWAY LOGIN / REGISTER / RESET
# ======================================================
if not st.session_state.logged_in:
    st.markdown(f"""
    <div class="logo-container">
        <img src="{UITM_LOGO_SRC}" class="uitm-logo" alt="UiTM Logo">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; width:100%'><h1 style='border:none; margin-bottom:0;'>MoU/MoA Record Management</h1></div>", unsafe_allow_html=True)

    auth = st.sidebar.selectbox("Secure Authentication Access", ["Login", "Register", "Reset Password"])

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if auth == "Login":
        st.subheader("🔑 Corporate Sign In")
        username = st.text_input("Corporate Username")
        password = st.text_input("Account Password", type="password")

        if st.button("Authenticate Session"):
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Session secured.")
                st.rerun()
            else:
                st.error("Invalid database authentication keys.")
    elif auth == "Register":
        st.subheader("📝 System Account Registration")
        new_username = st.text_input("Desired Username")
        new_email = st.text_input("Staff Email Address")
        new_password = st.text_input("Secure Password", type="password")

        if st.button("Deploy Account Meta"):
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (new_username, new_email, new_password))
            conn.commit()
            st.success("Account committed successfully to cluster database.")
    elif auth == "Reset Password":
        st.subheader("🔄 Credential Key Recovery")
        email = st.text_input("Registered Email Profile")
        new_password = st.text_input("Target New Password", type="password")

        if st.button("Override Encryption Key"):
            cursor.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
            conn.commit()
            st.success("Password override processed successfully.")
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# ENTERPRISE CONSOLE APPLICATION WORKSPACE
# ======================================================
else:
    # Minimalist Sidebar Profile
    st.sidebar.markdown(f"""
        <div class="logo-container" style="padding-top: 0;">
            <img src="{UITM_LOGO_SRC}" class="uitm-logo" style="width:90px;" alt="UiTM Logo">
        </div>
        <div class="sidebar-profile">
            <div class="uitm-title">UiTM MoU/MoA</div>
            <div class="campus">PERMATANG PAUH</div>
            <div class="badge">
                <span>●</span> 
                <span>{st.session_state.username}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar Navigation System dengan Emoji (Nampak macam Icons)
    menu_options_display = ["🏠 Dashboard", "📂 View Data", "➕ Add Data", "📝 Update Data", "🗑️ Delete Data"]
    
    # Cari index yang betul berdasarkan nama page (tanpa emoji)
    current_index = 0
    for i, opt in enumerate(menu_options_display):
        if st.session_state.current_page in opt:
            current_index = i
            break
    
    selected_menu = st.sidebar.radio(
        "MENU",
        menu_options_display,
        index=current_index,
        label_visibility="collapsed" # Sembunyikan label "MENU" untuk nampak lebih clean
    )
    
    # Check if page changed
    clean_selected = selected_menu.split(" ", 1)[1]
    if clean_selected != st.session_state.current_page:
        st.session_state.current_page = clean_selected
        st.rerun()

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("Sign Out", key="logout_btn"):
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
        st.title("Record Analytics Dashboard")

        total_records = len(df)
        total_country = df["Country"].nunique() if total_records > 0 else 0
        total_category = df["Category"].nunique() if total_records > 0 else 0

        st.markdown(f"""
        <div class="metric-grid">
            <div class="pro-metric metric-1">
                <div class="metric-title">TOTAL ACTIVE AGREEMENTS</div>
                <div class="metric-value">{total_records}</div>
            </div>
            <div class="pro-metric metric-2">
                <div class="metric-title">PARTNER COUNTRIES</div>
                <div class="metric-value">{total_country}</div>
            </div>
            <div class="pro-metric metric-3">
                <div class="metric-title">UNIQUE CATEGORIES</div>
                <div class="metric-value">{total_category}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("Global Distribution Portfolio")
        
        if total_records > 0:
            country_chart = df["Country"].value_counts().reset_index()
            country_chart.columns = ["Country", "Total"]
            bright_colors = ["#5a3982", "#1f6a8d", "#38a3a0", "#147f3b", "#70ad47", "#edb100", "#e84c22"]

            fig = px.bar(
                country_chart,
                x="Country",
                y="Total",
                color="Country",  
                color_discrete_sequence=bright_colors, 
                text_auto=True
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#1e293b",
                xaxis=dict(showgrid=False, title_font=dict(size=12, color="#64748b")),
                yaxis=dict(showgrid=True, gridcolor="#f1f5f9", title_font=dict(size=12, color="#64748b")),
                margin=dict(t=15, b=15, l=10, r=10),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No records available to generate charts. Insert records via 'Add Data' module panel.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: VIEW DATA (BEAUTIFIED TABLE)
    # ------------------------------------------------------
    elif st.session_state.current_page == "View Data":
        st.title("Repository View")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        search = st.text_input("🔍 Search Database (Title, Partner, or Country)")

        if search:
            sql = "SELECT * FROM collaboration_data WHERE title LIKE ? OR partner LIKE ? OR country LIKE ?"
            cursor.execute(sql, (f"%{search}%", f"%{search}%", f"%{search}%"))
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

        # GENERATE BEAUTIFUL HTML TABLE
        if len(df) > 0:
            # Tukar DataFrame ke HTML yang dipadankan dengan kelas CSS kita
            html_table = df.to_html(index=False, classes="styled-table", escape=False)
            st.markdown(f'<div class="table-container">{html_table}</div>', unsafe_allow_html=True)
        else:
            st.info("No data found in the repository.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: ADD DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "Add Data":
        st.title("Deploy New Record Entry")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            id_in = st.number_input("Record ID", min_value=1, step=1, format="%d")
            title = st.text_input("Agreement Title")
            duration = st.text_input("Duration (e.g. 3 Years)")
            department = st.text_input("Executing Department / Faculty")
        with col2:
            partner = st.text_input("External Partner Institution")
            country = st.text_input("Country")
            category = st.selectbox("Agreement Core Category Designation", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Commit Data Stream"):
            cursor.execute("INSERT INTO collaboration_data (id, title, duration, department, partner, country, category) VALUES (?,?,?,?,?,?,?)",
                           (int(id_in), title, duration, department, partner, country, category))
            conn.commit()
            st.success("New legal record successfully mapped into SQL table cluster.")
            switch_page("View Data")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: UPDATE DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "Update Data":
        st.title("Edit Existing Records Mapping")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        uid = st.number_input("Target Record ID", min_value=1, step=1, format="%d")
        cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(uid),))
        result = cursor.fetchone()

        if result:
            st.markdown("<hr style='border: 1px solid #f1f5f9; margin:20px 0;'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Agreement Title", result[1])
                duration = st.text_input("Duration", result[2])
                department = st.text_input("Department", result[3])
            with col2:
                partner = st.text_input("External Partner", result[4])
                country = st.text_input("Country", result[5])
                category = st.selectbox("Category", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"])

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Update Changes"):
                cursor.execute("UPDATE collaboration_data SET title=?, duration=?, department=?, partner=?, country=?, category=? WHERE id=?",
                               (title, duration, department, partner, country, category, int(uid)))
                conn.commit()
                st.success("Record completely updated.")
                switch_page("View Data")
        else:
            st.warning("Target ID does not exist.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: DELETE DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "Delete Data":
        st.title("Purge Log Entry")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        del_id = st.number_input("Target Record ID to Delete", min_value=1, step=1, format="%d")
        
        @st.dialog("⚠️ Confirm Permanent Deletion")
        def confirm_delete_dialog(record_id):
            st.warning(f"Are you sure you want to permanently delete Record ID **{record_id}**?")
            col_yes, col_cancel = st.columns([1, 1])
            with col_yes:
                if st.button("Yes, Delete", use_container_width=True):
                    cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(record_id),))
                    if cursor.fetchone():
                        cursor.execute("DELETE FROM collaboration_data WHERE id=?", (int(record_id),))
                        conn.commit()
                        st.success(f"Record {record_id} deleted.")
                        switch_page("View Data")
                    else:
                        st.error("Target ID unmapped.")
            with col_cancel:
                if st.button("Cancel", use_container_width=True):
                    st.rerun()

        if st.button("Confirm Delete"):
            confirm_delete_dialog(del_id)
        st.markdown('</div>', unsafe_allow_html=True)