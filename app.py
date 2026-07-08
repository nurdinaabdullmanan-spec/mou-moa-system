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
# CUSTOM UI CSS (CLEAN SIDEBAR & REMOVED RADIO DOTS)
# ======================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* PENGURUSAN FONT UTAMA */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
    }}

    /* BACKGROUND UTAMA - CERAH & PREMIUM */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: #f8fafc !important; 
        color: #0f172a !important;
    }}
    
    .block-container {{
        padding: 2.5rem 4rem !important;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* INPUT LABELS STYLE */
    [data-testid="stWidgetLabel"] p, 
    label[data-testid="stWidgetLabel"], 
    .stTextInput label, 
    .stNumberInput label, 
    .stSelectbox label,
    div[data-baseline="select"] label {{
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }}

    /* ======================================================
       DARK DEEP PURPLE SIDEBAR (BERDASARKAN GAMBAR)
       ====================================================== */
    section[data-testid="stSidebar"] {{
        background: #190525 !important; /* Deep dark plum/purple */
        border-right: none !important;
        box-shadow: 2px 0 15px rgba(0,0,0,0.1) !important;
    }}

    /* BUANG BULATAN RADIO DAN INPUT NATIVE STREAMLIT */
    div[role="radiogroup"] [data-testid="stSelectionControlBase"] {{
        display: none !important;
    }}

    div[role="radiogroup"] {{
        display: flex;
        flex-direction: column;
        gap: 2px !important;
        padding-top: 25px;
    }}

    div[role="radiogroup"] label {{
        display: flex !important;
        align-items: center !important;
        background: transparent !important;
        padding: 14px 25px !important;
        border: none !important;
        border-radius: 0 !important; 
        transition: all 0.2s ease !important;
        margin: 0 !important;
        cursor: pointer;
    }}

    /* HOVER EFFECT MENU */
    div[role="radiogroup"] label:hover {{
        background: rgba(255, 255, 255, 0.03) !important;
    }}

    /* TYPOGRAPHY NAVIGASI MENU (UPPERCASE GREY) */
    div[role="radiogroup"] label p {{
        color: #94a3b8 !important; 
        font-size: 13px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        margin: 0 !important;
        padding: 0 !important;
    }}

    /* ACTIVE MENU ITEM - DARK BG + GOLD LEFT BORDER */
    div[role="radiogroup"] label[data-selected="true"] {{
        background: rgba(0, 0, 0, 0.2) !important;
        border-left: 4px solid #eab308 !important; /* Gold border */
    }}

    div[role="radiogroup"] label[data-selected="true"] p {{
        color: #ffffff !important; 
        font-weight: 700 !important;
    }}

    /* ======================================================
       GOLD GRADIENT LOGOUT BUTTON (TERMINATED ACCESS)
       ====================================================== */
    .logout-container-box {{
        margin-top: 50px;
        display: flex;
        justify-content: center;
    }}
    
    section[data-testid="stSidebar"] div.logout-container-box button {{
        background: linear-gradient(135deg, #fcd34d 0%, #d97706 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(217, 119, 6, 0.3) !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        text-align: center !important;
        padding: 10px 20px !important;
        width: 85% !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }}
    
    section[data-testid="stSidebar"] div.logout-container-box button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(217, 119, 6, 0.5) !important;
        color: #ffffff !important;
    }}

    /* ======================================================
       MAIN CONTENT STYLING
       ====================================================== */
    h1 {{
        color: #0f172a !important;
        font-weight: 800 !important;
        font-size: 26px !important;
        letter-spacing: -0.5px;
        margin-bottom: 25px !important;
    }}

    h2, h3, h4 {{
        color: #1e293b !important;
        font-weight: 600 !important;
    }}

    .content-card {{
        background: #ffffff !important; 
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        margin-bottom: 25px;
    }}

    /* ======================================================
       SCORECARD METRIC GRID (SEBIJIK GAMBAR 2)
       ====================================================== */
    .metric-grid {{ 
        display: flex; 
        gap: 20px; 
        margin-bottom: 25px; 
    }}
    .pro-metric {{
        flex: 1; 
        background: #ffffff; 
        padding: 22px 25px;
        border-radius: 8px; 
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02); 
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}
    /* Colored Left Borders */
    .metric-purple {{ border-left: 4px solid #6b21a8; }} 
    .metric-teal {{ border-left: 4px solid #0f766e; }} 
    .metric-gold {{ border-left: 4px solid #d97706; }} 

    .metric-title {{
        font-size: 10px; 
        color: #64748b; 
        font-weight: 700;
        text-transform: uppercase; 
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }}
    .metric-value {{
        font-size: 26px; 
        font-weight: 800; 
        color: #0f172a;
        line-height: 1;
    }}

    /* BUTTON UTAMA UTK LUAR SIDEBAR */
    .stButton > button {{
        width: 100%; 
        border-radius: 8px; 
        border: none !important;
        padding: 10px 20px; 
        font-weight: 600; 
        font-size: 14px; 
        color: #ffffff !important; 
        background: #7c3aed !important; 
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        background: #6d28d9 !important;
        transform: translateY(-1px);
    }}

    /* BACK BUTTON MINIMALIST */
    .back-btn-container .stButton > button {{
        width: auto !important; 
        background: transparent !important; 
        color: #64748b !important;
        border: 1px solid #e2e8f0 !important; 
    }}
    .back-btn-container .stButton > button:hover {{ 
        background: #f8fafc !important; 
        color: #0f172a !important;
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
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    with col_l2:
        st.markdown(f"""
        <div style="text-align:center; margin-top:60px; margin-bottom:20px;">
            <div style="background: white; display: inline-block; padding: 12px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                <img src="{UITM_LOGO_SRC}" style="width:150px;" alt="UiTM Logo">
            </div>
            <h2 style="font-size:22px; font-weight:700; color:#0f172a; margin-top:15px; margin-bottom:0;">Record Management System</h2>
            <p style="color:#64748b; font-size:14px; margin-top:5px;">UiTM Kampus Permatang Pauh</p>
        </div>
        """, unsafe_allow_html=True)
        
        auth = st.selectbox("Secure Authentication Access", ["Login", "Register", "Reset Password"])

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        if auth == "Login":
            st.subheader("🔑 Sign In")
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
            st.subheader("📝 Registration")
            new_username = st.text_input("Desired Username")
            new_email = st.text_input("Staff Email Address")
            new_password = st.text_input("Secure Password", type="password")

            if st.button("Deploy Account Meta"):
                cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (new_username, new_email, new_password))
                conn.commit()
                st.success("Account committed successfully to cluster database.")

        elif auth == "Reset Password":
            st.subheader("🔄 Key Recovery")
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
    # ------------------------------------------------------
    # SIDEBAR DESIGN (BERDASARKAN GAMBAR & FORCE GOLD TEXT)
    # ------------------------------------------------------
    st.sidebar.markdown(f"""
        <div style="text-align: center; padding-top: 15px; margin-bottom: 5px;">
            <img src="{UITM_LOGO_SRC}" style="width: 100px; display: inline-block; filter: drop-shadow(0px 2px 5px rgba(0,0,0,0.3));" alt="UiTM Logo">
            <!-- TULISAN EMAS DIPAKSA GUNA !IMPORTANT SUPAYA TIDAK GELAP -->
            <h3 style="color: #facc15 !important; font-size: 15px; font-weight: 800; margin-top: 18px; margin-bottom: 5px; line-height: 1.4; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
                UiTM MoU/MoA Collaboration<br>Record Management
            </h3>
            <p style="color: #cbd5e1 !important; font-size: 10px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; margin-top: 4px;">
                Kampus Permatang Pauh
            </p>
            <div style="display: inline-block; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.05); border-radius: 20px; padding: 4px 14px; margin-top: 12px;">
                <span style="color: #facc15; font-size: 10px; margin-right: 5px;">●</span>
                <span style="color: #f8fafc !important; font-size: 11px; font-weight: 600;">{st.session_state.username}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar Navigation System (Bulatan Dibuang melalui CSS stSelectionControlBase)
    menu_options = ["Dashboard", "View Data", "Add Data", "Update Data", "Delete Data"]
    
    current_index = 0
    if st.session_state.current_page in menu_options:
        current_index = menu_options.index(st.session_state.current_page)
            
    selected_menu = st.sidebar.radio(
        "SYSTEM MODULE",
        menu_options,
        index=current_index,
        label_visibility="collapsed"
    )
    
    if selected_menu != st.session_state.current_page:
        st.session_state.current_page = selected_menu
        st.rerun()

    # Beautiful Gold Gradient Logout Button
    st.sidebar.markdown('<div class="logout-container-box">', unsafe_allow_html=True)
    if st.sidebar.button("Terminated Access", key="logout_btn"):
        st.session_state.logged_in = False
        st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)


    # Read Core Table Stream
    cursor.execute("SELECT * FROM collaboration_data ORDER BY id ASC")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

    # ------------------------------------------------------
    # MODULE: DASHBOARD
    # ------------------------------------------------------
    if st.session_state.current_page == "Dashboard":
        st.title("📊 Record Analytics Dashboard")

        total_records = len(df)
        total_country = df["Country"].nunique() if total_records > 0 else 0
        total_category = df["Category"].nunique() if total_records > 0 else 0

        # Beautiful Scorecard Grid Design (SEBIJIK GAMBAR 2)
        st.markdown(f"""
        <div class="metric-grid">
            <div class="pro-metric metric-purple">
                <div class="metric-title">Total Active Agreements</div>
                <div class="metric-value">{total_records}</div>
            </div>
            <div class="pro-metric metric-teal">
                <div class="metric-title">Partner Countries</div>
                <div class="metric-value">{total_country}</div>
            </div>
            <div class="pro-metric metric-gold">
                <div class="metric-title">Unique Categories</div>
                <div class="metric-value">{total_category}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("🌐 Global Distribution Portfolio")
        
        if total_records > 0:
            country_chart = df["Country"].value_counts().reset_index()
            country_chart.columns = ["Country", "Total"]
            modern_colors = ["#7c3aed", "#0d9488", "#d97706", "#ec4899", "#3b82f6", "#8b5cf6"]

            fig = px.bar(
                country_chart,
                x="Country",
                y="Total",
                color="Country",  
                color_discrete_sequence=modern_colors, 
                text_auto=True
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#334155",
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
    # MODULE: VIEW DATA
    # ------------------------------------------------------
    elif st.session_state.current_page == "View Data":
        st.title("🗂️ Repository View")

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        search = st.text_input("🔍 Filter Stream Matrix (Enter Title, Partner or Country)", placeholder="Type details to filter records dynamically...")

        if search:
            sql = "SELECT * FROM collaboration_data WHERE title LIKE ? OR partner LIKE ? OR country LIKE ?"
            cursor.execute(sql, (f"%{search}%", f"%{search}%", f"%{search}%"))
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

        # GENERATE PREMIUM HTML TABLE WITH COLORED PILL BADGES
        if len(df) > 0:
            html_table = "<table class='styled-table' style='width:100%; border-collapse:collapse; font-size:13px; background-color:#ffffff; border:1px solid #e2e8f0; border-radius:8px; overflow:hidden;'>"
            html_table += "<thead style='background-color:#f8fafc; color:#475569; border-bottom:1px solid #e2e8f0;'><tr>"
            for col in df.columns:
                html_table += f"<th style='padding:14px 18px; font-weight:600; text-align:left;'>{col}</th>"
            html_table += "</tr></thead><tbody>"
            
            for _, row in df.iterrows():
                html_table += "<tr style='border-bottom:1px solid #f1f5f9; color:#334155;'>"
                html_table += f"<td style='padding:14px 18px;'>{row['ID']}</td>"
                html_table += f"<td style='padding:14px 18px;'>{row['Agreement Title']}</td>"
                html_table += f"<td style='padding:14px 18px;'>{row['Duration']}</td>"
                html_table += f"<td style='padding:14px 18px;'>{row['Department']}</td>"
                html_table += f"<td style='padding:14px 18px;'>{row['Partner']}</td>"
                html_table += f"<td style='padding:14px 18px;'>{row['Country']}</td>"
                
                cat_val = str(row['Category'])
                if "mou" in cat_val.lower():
                    badge_markup = f"<td style='padding:14px 18px;'><span style='background-color:#f3e8ff; color:#7c3aed; padding:4px 8px; border-radius:6px; font-size:11px; font-weight:600;'>{cat_val}</span></td>"
                elif "moa" in cat_val.lower():
                    badge_markup = f"<td style='padding:14px 18px;'><span style='background-color:#fff7ed; color:#ea580c; padding:4px 8px; border-radius:6px; font-size:11px; font-weight:600;'>{cat_val}</span></td>"
                else:
                    badge_markup = f"<td style='padding:14px 18px;'><span style='background-color:#f1f5f9; color:#475569; padding:4px 8px; border-radius:6px; font-size:11px; font-weight:600;'>{cat_val}</span></td>"
                
                html_table += badge_markup
                html_table += "</tr>"
                
            html_table += "</tbody></table>"
            st.markdown(f'<div style="width:100%; overflow-x:auto;">{html_table}</div>', unsafe_allow_html=True)
        else:
            st.info("No data found in the repository.")
        
        st.markdown("<br><hr style='border:0.5px solid #e2e8f0;'><br>", unsafe_allow_html=True)
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
            
        st.markdown("<br><hr style='border:0.5px solid #e2e8f0;'><br>", unsafe_allow_html=True)
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

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        uid = st.number_input("Target Record ID Vector Lookup", min_value=1, step=1, format="%d")
        cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(uid),))
        result = cursor.fetchone()

        if result:
            st.markdown("<hr style='border: 1px dashed #e2e8f0; margin:20px 0;'>", unsafe_allow_html=True)
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
            
        st.markdown("<br><hr style='border:0.5px solid #e2e8f0;'><br>", unsafe_allow_html=True)
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

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        del_id = st.number_input("Target Discard Record ID", min_value=1, step=1, format="%d")
        st.error("💣 Critical: Purging actions cannot be rolled back or undone from the database nodes.")

        @st.dialog("⚠️ Confirm Permanent Deletion")
        def confirm_delete_dialog(record_id):
            st.warning(f"Are you absolutely sure you want to permanently delete Record ID {record_id}?")
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
                
        st.markdown("<br><hr style='border:0.5px solid #e2e8f0;'><br>", unsafe_allow_html=True)
        st.markdown('<div class="back-btn-container">', unsafe_allow_html=True)
        if st.button("← Cancel & Back", key="back_delete"):
            switch_page("Dashboard")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)