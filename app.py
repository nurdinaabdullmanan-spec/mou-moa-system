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

# LINK LOGO UITM YANG BARU & STABIL (MENGELAKKAN ISU GAMBAR PECAH)
UITM_LOGO_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/UiTM_Logo.png/640px-UiTM_Logo.png"

# ======================================================
# ULTIMATE MASTERPIECE UI CSS (SOFT LIGHT PURPLE MIX)
# ======================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* PENGURUSAN FONT */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    
    h1, h2, h3, .uitm-title {{
        font-family: 'Cinzel', serif !important;
    }}

    /* BACKGROUND UTAMA - DIUBAH KEPADA UNGU YANG SANGAT LEMBUT DAN PUDAR (LIGHT SUBTLE PURPLE) */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: linear-gradient(135deg, #f4f0fa 0%, #e8e2f2 100%) !important; 
        color: #211936 !important;
    }}
    
    .block-container {{
        padding: 2.5rem 5rem !important;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* LOGO BLENDING EFFECT (Disesuaikan semula untuk blend dengan background pudar) */
    .logo-container {{
        text-align: center;
        padding: 15px 0;
    }}
    .uitm-logo {{
        width: 150px;
        filter: drop-shadow(0px 4px 12px rgba(75, 46, 131, 0.15));
        mix-blend-mode: normal;
        display: block;
        margin: 0 auto;
        transition: transform 0.3s ease;
    }}
    .uitm-logo:hover {{
        transform: scale(1.05);
    }}

    /* SIDEBAR GELAP YANG DEE SUKA (STAY ORIGINAL PREMIUM DARK) */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #110d21 0%, #07050e 100%) !important; 
        border-right: 1px solid rgba(75, 46, 131, 0.2) !important;
        box-shadow: 5px 0 25px rgba(0,0,0,0.15);
    }}
    
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label {{
        color: #ffffff !important;
    }}

    /* NAVIGATION TILES IN SIDEBAR */
    div[role="radiogroup"] {{
        display: flex;
        flex-direction: column;
        gap: 12px;
        padding-top: 15px;
    }}

    div[role="radiogroup"] label {{
        background: rgba(255, 255, 255, 0.02) !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        border: 1px solid rgba(255, 255, 255, 0.03) !important;
    }}

    div[role="radiogroup"] label [data-testid="stMarkdownContainer"]::before {{
        display: none !important;
    }}

    div[role="radiogroup"] label:hover {{
        background: rgba(75, 46, 131, 0.2) !important;
        border-color: rgba(250, 191, 44, 0.4) !important;
        transform: translateY(-2px);
    }}

    div[role="radiogroup"] label p {{
        color: #94a3b8 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px;
    }}

    /* STATE ACTIVE AT SIDEBAR */
    div[role="radiogroup"] label[data-selected="true"] {{
        background: linear-gradient(135deg, #4b2e83 0%, #2a164d 100%) !important; 
        border: 1px solid #fabf2c !important; 
        box-shadow: 0 0 20px rgba(250, 191, 44, 0.25) !important;
    }}

    div[role="radiogroup"] label[data-selected="true"] p {{
        color: #fabf2c !important;
        font-weight: 700 !important;
    }}

    /* TYPOGRAPHY FOR LIGHT THEME */
    h1 {{
        color: #3b226b !important; 
        font-weight: 700 !important;
        letter-spacing: -0.5px;
        border-bottom: 3px solid #4b2e83;
        padding-bottom: 10px;
        display: inline-block;
    }}
    h2, h3 {{
        color: #4b2e83 !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
    }}
    
    .subtitle-fix {{
        color: #5d5370 !important;
        font-size: 15px;
        margin-top: 8px;
        margin-bottom: 35px;
        font-weight: 400;
    }}

    /* LUXURY WHITE GLASS CARD */
    .content-card {{
        background: #ffffff !important; 
        border-radius: 24px;
        padding: 40px;
        border: 1px solid rgba(75, 46, 131, 0.08);
        box-shadow: 0 15px 35px rgba(75, 46, 131, 0.04);
        margin-bottom: 30px;
    }}

    /* HIGH-END METRIC LAYOUT */
    .metric-grid {{
        display: flex;
        gap: 24px;
        margin-bottom: 30px;
    }}
    
    .pro-metric {{
        flex: 1;
        background: #ffffff;
        padding: 26px;
        border-radius: 20px;
        border: 1px solid rgba(75, 46, 131, 0.08);
        box-shadow: 0 8px 24px rgba(0,0,0,0.02);
        position: relative;
        overflow: hidden;
    }}
    
    .pro-metric::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 4px;
    }}
    
    .metric-1::before {{ background: linear-gradient(90deg, #4b2e83, #fabf2c); }}
    .metric-2::before {{ background: linear-gradient(90deg, #0284c7, #38bdf8); }}
    .metric-3::before {{ background: linear-gradient(90deg, #ec4899, #f472b6); }}

    .metric-title {{
        font-size: 12px;
        color: #6b627a;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .metric-value {{
        font-size: 42px;
        font-weight: 700;
        color: #3b226b;
        margin-top: 8px;
        font-family: 'Cinzel', serif;
    }}

    /* DEEP PURPLE HIGH-END BUTTONS */
    .stButton > button {{
        width: 100%;
        border-radius: 14px;
        border: 1px solid #4b2e83;
        padding: 14px;
        font-weight: 700;
        font-size: 15px;
        letter-spacing: 0.5px;
        color: #ffffff !important; 
        background: linear-gradient(135deg, #4b2e83 0%, #321d59 100%) !important;
        box-shadow: 0 6px 18px rgba(75, 46, 131, 0.15);
        transition: all 0.3s ease;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 25px rgba(75, 46, 131, 0.25);
        background: linear-gradient(135deg, #5b399c 0%, #4b2e83 100%) !important;
    }}

    /* BACK SYSTEM BUTTON */
    .back-btn-container .stButton > button {{
        width: auto !important;
        background: transparent !important;
        color: #4b2e83 !important;
        border: 1px solid rgba(75, 46, 131, 0.3) !important;
        padding: 10px 24px !important;
        box-shadow: none !important;
    }}
    
    .back-btn-container .stButton > button:hover {{
        background: rgba(75, 46, 131, 0.05) !important;
    }}

    /* MODERN CONTRAST INPUTS */
    .stTextInput input, .stNumberInput input, textarea, .stSelectbox div[data-baseweb="select"] {{
        border-radius: 12px !important;
        border: 1px solid #cbd5e1 !important;
        background-color: #fcfbfe !important;
        color: #211936 !important;
        padding: 2px 4px !important;
    }}
    .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: #4b2e83 !important;
        box-shadow: 0 0 10px rgba(75, 46, 131, 0.1) !important;
    }}

    /* DATA FRAME CUSTOMIZATION */
    [data-testid="stDataFrame"] {{
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        background: #ffffff !important;
        overflow: hidden;
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
    st.markdown(f"""
    <div class="logo-container">
        <img src="{UITM_LOGO_URL}" class="uitm-logo" alt="UiTM Logo">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; width:100%'><h1 style='border:none; margin-bottom:0;'>MoU/MoA Record Management</h1></div>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle-fix" style="text-align:center;">UiTM Institutional Excellence Agreement Cluster Gateway.</p>', unsafe_allow_html=True)

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
    # Sidebar Logo dan Profil
    st.sidebar.markdown(f"""
        <div class="logo-container">
            <img src="{UITM_LOGO_URL}" class="uitm-logo" style="width:110px; filter: drop-shadow(0px 0px 8px rgba(250,191,44,0.3));" alt="UiTM Logo">
        </div>
        <div style="text-align:center; padding: 10px 0 25px 0;">
            <div style="font-family:'Cinzel', serif; font-size:18px; font-weight:700; color:#fabf2c; letter-spacing:0.5px;">UiTM MoU/MoA</div>
            <div style="color:#94a3b8; font-size:10px; margin-top:4px; text-transform:uppercase; letter-spacing:1px;">PERMATANG PAUH</div>
            <div style="margin-top:12px; background:rgba(254, 240, 138, 0.05); padding:6px 14px; border-radius:30px; display:inline-block; border: 1px solid rgba(250,191,44,0.15);">
                <span style="color:#fabf2c; font-size:10px;">●</span> 
                <span style="color:#e2e8f0; font-size:12px; font-weight:600;">{st.session_state.username}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
        st.title("📊 Analytics Dashboard")
        st.markdown('<p class="subtitle-fix">Real-time Overview of Institutional Agreements & External Collaborations.</p>', unsafe_allow_html=True)

        total_records = len(df)
        total_country = df["Country"].nunique() if total_records > 0 else 0
        total_category = df["Category"].nunique() if total_records > 0 else 0

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

            # BAR CHART WARNA-WARNI CERIA
            fig = px.bar(
                country_chart,
                x="Country",
                y="Total",
                color="Country",  
                color_discrete_sequence=px.colors.qualitative.Pastel, 
                text_auto=True
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#211936",
                xaxis=dict(showgrid=False, title_font=dict(size=13, color="#4b2e83")),
                yaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,0.05)", title_font=dict(size=13, color="#4b2e83")),
                margin=dict(t=15, b=15, l=10, r=10),
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No records available to generate charts. Insert records via 'Add Data' module panel.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODULE: VIEW DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "View Data":
        st.title("🗂️ Repository View")
        st.markdown('<p class="subtitle-fix">Search and browse full records from the system database.</p>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        search = st.text_input("🔍 Filter Stream Matrix (Enter Title, Partner or Country)")

        if search:
            sql = "SELECT * FROM collaboration_data WHERE title LIKE ? OR partner LIKE ? OR country LIKE ?"
            cursor.execute(sql, (f"%{search}%", f"%{search}%", f"%{search}%"))
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

        st.dataframe(df, use_container_width=True, height=400)
        
        st.markdown("<br><hr style='border:0.5px solid #cbd5e1;'><br>", unsafe_allow_html=True)
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
            duration = st.text_input("Duration (e.g. 3 Years)")
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
            
        st.markdown("<br><hr style='border:0.5px solid #cbd5e1;'><br>", unsafe_allow_html=True)
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
            st.markdown("<hr style='border: 1px dashed #cbd5e1; margin:20px 0;'>", unsafe_allow_html=True)
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
            
        st.markdown("<br><hr style='border:0.5px solid #cbd5e1;'><br>", unsafe_allow_html=True)
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Cancel & Back", key="back_update"):
            switch_page("Dashboard")
        st.markdown('</div>', unsafe_allow_html=True)
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
                
        st.markdown("<br><hr style='border:0.5px solid #cbd5e1;'><br>", unsafe_allow_html=True)
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Cancel & Back", key="back_delete"):
            switch_page("Dashboard")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)