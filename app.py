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

# Panggil fungsi untuk dapatkan data imej
UITM_LOGO_SRC = get_local_logo_base64()


# ======================================================
# HIGHLY AGGRESSIVE UI CSS (FORCING TRUE SOFT PURPLE SYSTEM Theme)
# ======================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght=600;700;800&family=Inter:wght=300;400;500;600;700&display=swap');
    
    /* PENGURUSAN FONT */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
    }}
    
    h1, h2, h3, .uitm-title {{
        font-family: 'Cinzel', serif !important;
    }}

    /* 1. TUKAR KESELURUHAN BACKGROUND UTAMA KEPADA UNGU LEMBUT CAIR */
    .stApp, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"],
    [data-testid="stMainBlockContainer"] {{
        background-color: #f3ecf8 !important; 
        background: #f3ecf8 !important;
        color: #2e1065 !important;
    }}
    
    .block-container {{
        padding: 2.5rem 5rem !important;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* TULISAN LABEL INPUT */
    [data-testid="stWidgetLabel"] p, 
    label[data-testid="stWidgetLabel"], 
    .stTextInput label, 
    .stNumberInput label, 
    .stSelectbox label {{
        color: #4b2e83 !important;
        font-weight: 600 !important;
    }}

    /* LOGO BLENDING EFFECT */
    .logo-container {{
        text-align: center;
        padding: 15px 0;
    }}
    .uitm-logo {{
        width: 140px;
        filter: drop-shadow(0px 4px 10px rgba(75, 46, 131, 0.2));
        display: block;
        margin: 0 auto;
    }}

    /* SIDEBAR GELAP PREMIUM */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #161224 0%, #0d0a14 100%) !important; 
        border-right: 2px solid #fabf2c !important;
    }}
    
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label {{
        color: #ffffff !important;
    }}

    /* NAVIGATION TILES IN SIDEBAR (PREMIUM GLASSMORPHIC UPGRADE) */
    div[role="radiogroup"] {{
        display: flex;
        flex-direction: column;
        gap: 12px !important;
        padding-top: 10px;
    }}

    div[role="radiogroup"] label {{
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 16px !important;
        padding: 16px 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.05), 0 4px 6px rgba(0, 0, 0, 0.2) !important;
        transition: all 0.25s ease-in-out !important;
        cursor: pointer !important;
    }}

    /* EFEK HOVER: Menyala lembut & bergerak sedikit ke kanan */
    div[role="radiogroup"] label:hover {{
        background: rgba(75, 46, 131, 0.25) !important;
        border-color: rgba(250, 191, 44, 0.3) !important;
        transform: translateX(4px);
        box-shadow: 0 6px 15px rgba(75, 46, 131, 0.4) !important;
    }}

    /* APABILA MEMILIH/ACTIVE TILE (PREMIUM GOLD GLOW) */
    div[role="radiogroup"] label[data-selected="true"] {{
        background: linear-gradient(135deg, rgba(75, 46, 131, 0.8) 0%, rgba(42, 22, 77, 0.9) 100%) !important; 
        border: 1px solid #fabf2c !important; 
        box-shadow: 0 0 15px rgba(250, 191, 44, 0.25), inset 0 1px 2px rgba(255, 255, 255, 0.1) !important;
        transform: translateX(6px);
    }}

    /* Tukar warna teks & tebalkan bila aktif */
    div[role="radiogroup"] label[data-selected="true"] p {{
        color: #fabf2c !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }}

    /* Suntikan Ikon Indikator Visual Semasa */
    div[role="radiogroup"] label [data-testid="stMarkdownContainer"]::before {{
        content: "⚡ ";
        margin-right: 8px;
        font-size: 14px;
        opacity: 0.7;
    }}
    
    div[role="radiogroup"] label[data-selected="true"] [data-testid="stMarkdownContainer"]::before {{
        content: "✨ ";
        opacity: 1;
    }}

    /* KAD KONTEN UTAMA (Ungu Kontras Pertengahan) */
    .content-card {{
        background: #e6daf2 !important; 
        border-radius: 24px;
        padding: 40px;
        border: 1px solid #d3beeb !important;
        box-shadow: 0 10px 30px rgba(75, 46, 131, 0.05) !important;
        margin-bottom: 30px;
    }}

    /* 2. PAKSA KAD METRIKS JADI WARNA PURPLE SOFT */
    .metric-grid {{
        display: flex !important;
        gap: 24px !important;
        margin-bottom: 30px !important;
    }}
    
    .pro-metric {{
        flex: 1 !important;
        background-color: #dcc8f2 !important; 
        background: #dcc8f2 !important;
        padding: 22px 26px !important;
        border-radius: 16px !important;
        border: 1px solid #c7a9e6 !important;
        box-shadow: 0 4px 18px rgba(75, 46, 131, 0.1) !important;
    }}

    .metric-1 {{ border-left: 6px solid #4b2e83 !important; }}  
    .metric-2 {{ border-left: 6px solid #8b5cf6 !important; }}  
    .metric-3 {{ border-left: 6px solid #ec4899 !important; }}  

    .metric-title {{
        font-size: 12px !important;
        color: #3b2366 !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
    }}
    
    .metric-value {{
        font-size: 38px !important;
        font-weight: 800 !important;
        color: #1e004b !important;
    }}

    /* BUTTONS */
    .stButton > button {{
        border-radius: 14px !important;
        color: #ffffff !important; 
        background: linear-gradient(135deg, #4b2e83 0%, #3b2366 100%) !important;
        border: 1px solid #4b2e83 !important;
    }}
    .stButton > button:hover {{
        background: linear-gradient(135deg, #5c39a1 0%, #4b2e83 100%) !important;
    }}

    /* INPUT CONTROLS */
    .stTextInput input, .stNumberInput input, textarea, .stSelectbox div[data-baseweb="select"] {{
        border-radius: 12px !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
    }}

    /* 3. HIAS & PAKSA TABEL DATAFRAME KEPADA THEME SOFT PURPLE (TIADA LAGI CELL PUTIH) */
    [data-testid="stDataFrame"] {{
        border: 2px solid #b392e3 !important;
        border-radius: 18px !important;
        background-color: #eae0f5 !important; 
    }}

    /* Overriding canvas/glide-data-grid inner styles */
    div[data-testid="stDataFrame"] [role="grid"] div, 
    div[data-testid="stDataFrame"] [class*="glide-grid"],
    div[data-testid="stDataFrame"] td,
    div[data-testid="stDataFrame"] th {{
        background-color: #eae0f5 !important; 
        color: #2e1065 !important;
    }}

    /* Header Tabel */
    div[data-testid="stDataFrame"] [data-testid="table-header"],
    div[data-testid="stDataFrame"] thead tr th {{
        background-color: #4b2e83 !important; 
        color: #ffffff !important;
        font-weight: 700 !important;
    }}

    /* Efek Zebra Baris Selang-Seli */
    div[data-testid="stDataFrame"] tbody tr:nth-of-type(even) td,
    div[data-testid="stDataFrame"] tr:nth-of-type(even) {{
        background-color: #dfceff !important; 
    }}
    
    div[data-testid="stDataFrame"] tbody tr:nth-of-type(odd) td,
    div[data-testid="stDataFrame"] tr:nth-of-type(odd) {{
        background-color: #f6f0fc !important; 
    }}

    /* Apabila di-hover */
    div[data-testid="stDataFrame"] tr:hover, 
    div[data-testid="stDataFrame"] td:hover {{
        background-color: #ccb0f7 !important; 
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
        <img src="{UITM_LOGO_SRC}" class="uitm-logo" alt="UiTM Logo">
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
            <img src="{UITM_LOGO_SRC}" class="uitm-logo" style="width:110px;" alt="UiTM Logo">
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

        # Kad metriks dengan latar belakang ungu lembut padat
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

            fig = px.bar(
                country_chart,
                x="Country",
                y="Total",
                color="Country",  
                color_discrete_sequence=px.colors.qualitative.Bold, 
                text_auto=True
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#1e1b4b",
                xaxis=dict(showgrid=False, title_font=dict(size=14, color="#4b2e83")),
                yaxis=dict(showgrid=True, gridcolor="rgba(75,46,131,0.1)", title_font=dict(size=14, color="#4b2e83")),
                margin=dict(t=20, b=20, l=15, r=15),
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

        st.dataframe(
            df, 
            use_container_width=True, 
            height=430,
            hide_index=True, 
            column_config={
                "ID": st.column_config.NumberColumn("Record ID", format="%d"),
                "Agreement Title": st.column_config.TextColumn("Agreement Title"),
                "Duration": st.column_config.TextColumn("⏱️ Duration"),
                "Department": st.column_config.TextColumn("Department / Faculty"),
                "Partner": st.column_config.TextColumn("🤝 Partner Institution"),
                "Country": st.column_config.TextColumn("📍 Country"),
                "Category": st.column_config.TextColumn("Category Designation")
            }
        )
        
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