import plotly.express as px
import streamlit as st
import sqlite3
import pandas as pd

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
# MODERN SAAS / GLASSMORPHISM UI CSS (UiTM DARK THEME)
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* BACKGROUND UTAMA - MENGIKUT GAMBAR CONTOH (Premium Dark/Indigo Fluid) */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: radial-gradient(circle at top right, #1a163a, #0b091a) !important; 
        color: #f1f5f9 !important;
    }
    
    .block-container {
        padding: 2rem 4rem !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* SIDEBAR (Glassmorphic & Sleek) */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 12, 30, 0.7) !important; 
        backdrop-filter: blur(12px) !important;
        border-right: 1px solid rgba(250, 191, 44, 0.15) !important; /* Soft Gold border */
    }
    
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* NAVIGATION BUTTON STYLE (MODERN INTERACTIVE TILES) */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding-top: 10px;
    }

    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 14px !important;
        padding: 14px 20px !important;
        margin-bottom: 0px !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
    }

    div[role="radiogroup"] label [data-testid="stMarkdownContainer"]::before {
        display: none !important;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(250, 191, 44, 0.3) !important; /* Hover highlight gold */
        transform: translateX(4px);
    }

    div[role="radiogroup"] label p {
        color: #94a3b8 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px;
    }

    /* ACTIVE MENU STATE (UiTM Royal Purple & Gold Glow) */
    div[role="radiogroup"] label[data-selected="true"] {
        background: linear-gradient(135deg, #4b2e83, #311d57) !important; 
        border: 1px solid #fabf2c !important; /* UiTM Gold Border */
        box-shadow: 0 8px 25px rgba(75, 46, 131, 0.45) !important;
    }

    div[role="radiogroup"] label[data-selected="true"] p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* TYPOGRAPHY CONFIGS */
    h1 {
        color: #ffffff !important; 
        font-weight: 800 !important;
        font-size: 34px !important;
        letter-spacing: -0.8px;
    }
    h2, h3, h4, h5, h6 {
        color: #fabf2c !important; /* UiTM Gold headings */
        font-weight: 700 !important;
    }
    
    .subtitle-fix {
        color: #94a3b8 !important;
        font-size: 15px;
        margin-top: -12px;
        margin-bottom: 30px;
        font-weight: 400;
    }
    
    label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-bottom: 6px !important;
    }

    /* MODERN GLASS SAAS CARD (Meniru Gaya Widget 'User Activity' Gambar Contoh) */
    .content-card {
        background: rgba(23, 20, 43, 0.6) !important; 
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 20px;
        padding: 35px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
        margin-bottom: 25px;
    }

    /* METRIC CARDS GRID */
    .metric-grid {
        display: flex;
        gap: 20px;
        margin-bottom: 25px;
    }
    
    .pro-metric {
        flex: 1;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 24px;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .pro-metric::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 6px; height: 100%;
    }
    
    .metric-1::before { background: #4b2e83; } /* UiTM Purple Neon */
    .metric-2::before { background: #38bdf8; } /* Cyber Blue */
    .metric-3::before { background: #fabf2c; } /* UiTM Gold Neon */

    .metric-title {
        font-size: 12px;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 38px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 5px;
    }

    /* PREMIUM GLOWING BUTTONS */
    .stButton > button {
        width: 100%;
        border-radius: 14px;
        border: none;
        padding: 15px;
        font-weight: 700;
        font-size: 15px;
        color: #110e26 !important; /* Dark text for contrast against Gold */
        background: linear-gradient(135deg, #fabf2c, #d99e16) !important;
        box-shadow: 0 6px 20px rgba(250, 191, 44, 0.3);
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(250, 191, 44, 0.5);
    }

    /* BACK BUTTON AT THE BOTTOM */
    .back-btn-container .stButton > button {
        width: auto !important;
        background: transparent !important;
        color: #fabf2c !important;
        border: 1px solid rgba(250, 191, 44, 0.4) !important;
        padding: 10px 24px !important;
        font-size: 14px !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }
    
    .back-btn-container .stButton > button:hover {
        background: rgba(250, 191, 44, 0.1) !important;
        border-color: #fabf2c !important;
    }

    /* INPUT FIELDS & SELECTBOXES (Meniru Gaya Gelap UI) */
    .stTextInput input, .stNumberInput input, textarea {
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        padding: 12px 16px !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #fabf2c !important;
    }
    
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 12px !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    .stSelectbox div[data-baseweb="select"] * {
        color: #ffffff !important;
    }

    /* DATA TABLES */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        background: rgba(20, 17, 38, 0.6) !important;
    }
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
    st.title("🎓 MoU/MoA Record Management System")
    st.markdown('<p class="subtitle-fix">UiTM Institutional Excellence Agreement Cluster Gateway.</p>', unsafe_allow_html=True)

    auth = st.sidebar.selectbox("Secure Authentication Access", ["Login", "Register", "Reset Password"])

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if auth == "Login":
        st.subheader("Sign In")
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
        st.subheader("System Account Registration")
        new_username = st.text_input("Desired Username")
        new_email = st.text_input("Staff Email Address")
        new_password = st.text_input("Secure Password", type="password")

        if st.button("Deploy Account Meta"):
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (new_username, new_email, new_password))
            conn.commit()
            st.success("Account committed successfully to cluster database.")

    elif auth == "Reset Password":
        st.subheader("Credential Key Recovery")
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
    # Sidebar Header Profile Panel
    st.sidebar.markdown(
        f"""
        <div style="text-align:center; padding: 15px 0 30px 0;">
            <div style="font-size:24px; font-weight:800; color:#fabf2c; letter-spacing:-0.5px; line-height: 1.2;">UiTM MoU/MoA System</div>
            <div style="color:#94a3b8; font-size:11px; margin-top:6px; text-transform:uppercase; letter-spacing:1px;">UiTM PERMATANG PAUH</div>
            <div style="margin-top:15px; background:rgba(255,255,255,0.06); padding:8px 12px; border-radius:10px; display:inline-block; border: 1px solid rgba(255,255,255,0.05);">
                <span style="color:#38bdf8; font-size:10px;">●</span> 
                <span style="color:#e2e8f0; font-size:13px; font-weight:600;">{st.session_state.username}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sidebar Navigation System 
    menu_options = ["Dashboard", "View Data", "Add Data", "Update Data", "Delete Data"]
    current_index = menu_options.index(st.session_state.current_page)
    
    selected_menu = st.sidebar.radio(
        "SYSTEM MODULE CONNECTOR",
        menu_options,
        index=current_index
    )
    
    if selected_menu != st.session_state.current_page:
        st.session_state.current_page = selected_menu
        st.rerun()

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("Terminated Access", key="logout_btn"):
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
        st.title("📊 Record Analytics Dashboard")
        st.markdown('<p class="subtitle-fix">Real-time Overview of Institutional Agreements & External Collaborations.</p>', unsafe_allow_html=True)

        total_records = len(df)
        total_country = df["Country"].nunique() if total_records > 0 else 0
        total_category = df["Category"].nunique() if total_records > 0 else 0

        # Custom HTML Enterprise Metrics Layout
        st.markdown(f"""
        <div class="metric-grid">
            <div class="pro-metric metric-1">
                <div class="metric-title">Total Active Agreements</div>
                <div class="metric-value">{total_records}</div>
            </div>
            <div class="pro-metric metric-2">
                <div class="metric-title">Partner Countries</div>
                <div class="metric-value">{total_country}</div>
            </div>
            <div class="pro-metric metric-3">
                <div class="metric-title">Unique Categories</div>
                <div class="metric-value">{total_category}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("🌐 Global Distribution Portfolio")
        
        if total_records > 0:
            country_chart = df["Country"].value_counts().reset_index()
            country_chart.columns = ["Country", "Total"]

            # Mengubah warna carta Plotly supaya sepadan dengan reka bentuk gelap (Gaya Neon Purple & Gold)
            fig = px.bar(
                country_chart,
                x="Country",
                y="Total",
                color="Total",  
                color_continuous_scale=["#4b2e83", "#fabf2c"],
                text_auto=True
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#ffffff",
                xaxis=dict(showgrid=False, title_font=dict(size=13, color="#fabf2c")),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title_font=dict(size=13, color="#fabf2c")),
                margin=dict(t=15, b=15, l=10, r=10),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No records available to generate charts. Insert records via 'Add Data' module panel.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: VIEW DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "View Data":
        st.title("🗂️ Collaboration Repository View")
        st.markdown('<p class="subtitle-fix">Search and browse full records from the system database.</p>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        search = st.text_input("🔍 Filter Stream Matrix (Enter Title, Partner or Country)")

        if search:
            sql = "SELECT * FROM collaboration_data WHERE title LIKE ? OR partner LIKE ? OR country LIKE ?"
            cursor.execute(sql, (f"%{search}%", f"%{search}%", f"%{search}%"))
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

        st.dataframe(df, use_container_width=True, height=400)
        
        st.markdown("<br><hr style='border:0.5px solid rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Back to Dashboard", key="back_view"):
            switch_page("Dashboard")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: ADD DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "Add Data":
        st.title("➕ Deploy New Record Entry")
        st.markdown('<p class="subtitle-fix">Insert certified institutional MoU/MoA metadata into database.</p>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            id_in = st.number_input("Record ID", min_value=1, step=1, format="%d")
            title = st.text_input("Agreement Title")
            duration = st.text_input("Duration")
            department = st.text_input("Executing Department / Faculty")
        with col2:
            partner = st.text_input("External Partner Institution")
            country = st.text_input("Country")
            category = st.selectbox("Agreement Core Category Designation", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Commit Data Stream to Database"):
            cursor.execute("INSERT INTO collaboration_data (id, title, duration, department, partner, country, category) VALUES (?,?,?,?,?,?,?)",
                           (int(id_in), title, duration, department, partner, country, category))
            conn.commit()
            st.success("New legal record successfully mapped into SQL table cluster.")
            switch_page("View Data")
            
        st.markdown("<br><hr style='border:0.5px solid rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Cancel & Back", key="back_add"):
            switch_page("Dashboard")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: UPDATE DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "Update Data":
        st.title("📝 Edit Existing Records Mapping")
        st.markdown('<p class="subtitle-fix">Modify properties of existing collaboration data securely.</p>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        uid = st.number_input("Target Record ID Vector Lookup", min_value=1, step=1, format="%d")
        cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(uid),))
        result = cursor.fetchone()

        if result:
            st.markdown("<hr style='border: 1px dashed rgba(255,255,255,0.1); margin:20px 0;'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Agreement Title Statement", result[1])
                duration = st.text_input("Active Lifespan Duration", result[2])
                department = st.text_input("Executing Department", result[3])
            with col2:
                partner = st.text_input("External Partner Institution", result[4])
                country = st.text_input("Country Location", result[5])
                category = st.selectbox("Agreement Core Category Designation", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"])

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Update Changes"):
                cursor.execute("UPDATE collaboration_data SET title=?, duration=?, department=?, partner=?, country=?, category=? WHERE id=?",
                               (title, duration, department, partner, country, category, int(uid)))
                conn.commit()
                st.success("Mutation vector completely updated inside system core table.")
                switch_page("View Data")
        else:
            st.warning("Target configuration ID vector does not exist in cluster indexing.")
            
        st.markdown("<br><hr style='border:0.5px solid rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Cancel & Back", key="back_update"):
            switch_page("Dashboard")
        st.markdown('=' '</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: DELETE DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "Delete Data":
        st.title("🗑️ Purge Legal Log Entry")
        st.markdown('<p class="subtitle-fix">Purge records permanently from the system configuration.</p>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        del_id = st.number_input("Target Discard Record ID", min_value=1, step=1, format="%d")
        st.error("💣 Critical: Purging actions cannot be rolled back or undone from the database nodes.")

        @st.dialog("⚠️ Confirm Permanent Deletion")
        def confirm_delete_dialog(record_id):
            st.warning(f"Are you absolutely sure you want to permanently delete Record ID **{record_id}**?")
            st.write("This action will immediately wipe the metadata cluster from the core database nodes.")
            
            col_yes, col_cancel = st.columns([1, 1])
            with col_yes:
                if st.button("Yes, Delete Record", use_container_width=True):
                    cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(record_id),))
                    if cursor.fetchone():
                        cursor.execute("DELETE FROM collaboration_data WHERE id=?", (int(record_id),))
                        conn.commit()
                        st.success(f"Record ID {record_id} cleared safely.")
                        switch_page("View Data")
                    else:
                        st.error("Deletion lifecycle terminated: Targeted ID index is unmapped.")
            
            with col_cancel:
                if st.button("Cancel", use_container_width=True):
                    st.rerun()

        if st.button("Confirm Delete"):
            confirm_delete_dialog(del_id)
                
        st.markdown("<br><hr style='border:0.5px solid rgba(255,255,255,0.08);'><br>", unsafe_allow_html=True)
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Cancel & Back", key="back_delete"):
            switch_page("Dashboard")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)