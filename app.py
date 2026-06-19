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
# ULTRA MODERN PRO UI CSS (UiTM THEME - NO MORE STARK WHITE)
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* 1. TUKAR BACKGROUND UTAMA KAWASAN KANAN (Soft UiTM Tone) */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #f3f2f9 !important; /* Soft Lavender Grey */
    }
    
    .block-container {
        padding: 2.5rem 3.5rem !important;
        background-color: #f3f2f9 !important;
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 2. SIDEBAR SYSTEM PANELS (Deep Corporate UiTM Purple) */
    section[data-testid="stSidebar"] {
        background-color: #1a1640 !important; 
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* NAVIGATION BUTTON RESHAPE */
    div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.03) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin-bottom: 0px !important;
        transition: all 0.25s ease !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Hide radio dot */
    div[role="radiogroup"] label [data-testid="stMarkdownContainer"]::before {
        display: none !important;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }

    div[role="radiogroup"] label p {
        color: #e2e8f0 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }

    /* ACTIVE MENU STATE (UiTM Gold) */
    div[role="radiogroup"] label[data-selected="true"] {
        background: #fabf2c !important; 
        border: 1px solid #fabf2c !important;
        box-shadow: 0 4px 12px rgba(250, 191, 44, 0.2) !important;
    }

    div[role="radiogroup"] label[data-selected="true"] p {
        color: #1a1640 !important;
        font-weight: 700 !important;
    }

    /* HEADINGS & TEXTS */
    h1 {
        color: #3b2063 !important; /* UiTM Purple Title */
        font-weight: 700 !important;
        font-size: 32px !important;
    }
    h2, h3 {
        color: #1e40af !important; /* Blue Accent */
        font-weight: 600 !important;
    }
    
    .subtitle-fix {
        color: #52525b !important;
        font-size: 15px;
        margin-top: -15px;
        margin-bottom: 25px;
    }
    
    label {
        color: #27272a !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }

    /* 3. TUKAR BACKGROUND KAD KANDUNGAN (View, Add, dsb) SUPAYA SELARI */
    .content-card {
        background: #eae7f2 !important; /* Terang tapi berasaskan tema ungu cair */
        border-radius: 16px;
        padding: 30px;
        border: 1px solid #dcd7e9;
        box-shadow: 0 4px 20px -2px rgba(59, 32, 99, 0.05);
        margin-bottom: 20px;
    }

    /* METRIC CARDS OVERRIDE */
    div[data-testid="metric-container"] {
        background: #eae7f2 !important;
        border-radius: 16px !important;
        padding: 24px !important;
        border-left: 6px solid #3b2063 !important;
        border-top: 1px solid #dcd7e9 !important;
        border-right: 1px solid #dcd7e9 !important;
        border-bottom: 1px solid #dcd7e9 !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #3b2063 !important; 
        font-weight: 700 !important;
        font-size: 36px !important;
    }

    /* BUTTONS */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 14px;
        font-weight: 600;
        color: white !important;
        background: linear-gradient(135deg, #3b2063, #251342) !important;
        box-shadow: 0 4px 12px rgba(59, 32, 99, 0.2);
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(59, 32, 99, 0.3);
    }

    /* LOGOUT BUTTON */
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: 1px solid #f87171 !important;
        color: #f87171 !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #ef4444 !important;
        color: white !important;
    }

    /* INPUT ELEMENT BOXES & DROPDOWNS */
    .stTextInput input, .stNumberInput input, textarea {
        border-radius: 10px !important;
        border: 1px solid #bdaec6 !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
    }
    
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px !important;
        background-color: #ffffff !important;
        border: 1px solid #bdaec6 !important;
    }
    .stSelectbox div[data-baseweb="select"] * {
        color: #0f172a !important;
    }

    /* DATAFRAME BLOCK */
    [data-testid="stDataFrame"] {
        border: 1px solid #cbd5e1;
        border-radius: 14px;
        background: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ======================================================
# SESSION STATE
# ======================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ======================================================
# LOGIN / REGISTER / RESET
# ======================================================
if not st.session_state.logged_in:
    st.title("🎓 MoU/MoA Collaboration Record Management System")
    st.markdown('<p class="subtitle-fix">Secure collaboration agreement management platform.</p>', unsafe_allow_html=True)

    auth = st.sidebar.selectbox("Account Gateway", ["Login", "Register", "Reset Password"])

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if auth == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign In"):
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    elif auth == "Register":
        st.subheader("Create Account")
        new_username = st.text_input("Username")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")

        if st.button("Register"):
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (new_username, new_email, new_password))
            conn.commit()
            st.success("Account created successfully.")

    elif auth == "Reset Password":
        st.subheader("Reset Password")
        email = st.text_input("Enter Email")
        new_password = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            cursor.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
            conn.commit()
            st.success("Password updated successfully.")
    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# MAIN SYSTEM
# ======================================================
else:
    # Sidebar Profile Header
    st.sidebar.markdown(
        f"""
        <div style="text-align:center; padding: 10px 0 25px 0;">
            <h2 style="color:#fabf2c; margin:0; font-size:22px; font-weight:700;">UiTM Record System</h2>
            <p style="color:#cbd5e1; margin:6px 0 0 0; font-size:13px; opacity:0.8;">Logged in as: <span style="color:#fabf2c; font-weight:600;">{st.session_state.username}</span></p>
        </div>
        """,
        unsafe_allow_html=True
    )

    menu = st.sidebar.radio(
        "NAVIGATION MENU",
        ["Dashboard", "View Data", "Add Data", "Update Data", "Delete Data"]
    )

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    if st.sidebar.button("Logout Session"):
        st.session_state.logged_in = False
        st.rerun()

    # Load DB data
    cursor.execute("SELECT * FROM collaboration_data ORDER BY id ASC")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

    # DASHBOARD
    if menu == "Dashboard":
        st.title("📊 System Dashboard")
        st.markdown('<p class="subtitle-fix">Real-time Overview of Institutional Agreements & External Collaborations.</p>', unsafe_allow_html=True)

        total_records = len(df)
        total_country = df["Country"].nunique() if total_records > 0 else 0
        total_category = df["Category"].nunique() if total_records > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Agreements", total_records)
        with col2:
            st.metric("Countries", total_country)
        with col3:
            st.metric("Agreement Categories", total_category)

        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.subheader("🌐 Country Distribution")
        
        if total_records > 0:
            country_chart = df["Country"].value_counts().reset_index()
            country_chart.columns = ["Country", "Total"]

            # BAR MACAM-MACAM WARNA (Prism Colorful Theme)
            fig = px.bar(
                country_chart,
                x="Country",
                y="Total",
                color="Country",  
                color_discrete_sequence=px.colors.qualitative.Prism, 
                text_auto=True
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, title_font=dict(size=13, color="#4b2e83")),
                yaxis=dict(showgrid=True, gridcolor="#e2e8f0", title_font=dict(size=13, color="#4b2e83")),
                margin=dict(t=20, b=20, l=10, r=10),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No records available to display data graphs. Go to 'Add Data' to populate database.")
        st.markdown('</div>', unsafe_allow_html=True)

    # VIEW DATA
    elif menu == "View Data":
        st.title("🗂️ Collaboration Records")
        st.markdown('<p class="subtitle-fix">Search and browse full records from the system database.</p>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        search = st.text_input("🔍 Search by Agreement Title, Partner or Country")

        if search:
            sql = "SELECT * FROM collaboration_data WHERE title LIKE ? OR partner LIKE ? OR country LIKE ?"
            cursor.execute(sql, (f"%{search}%", f"%{search}%", f"%{search}%"))
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

        st.dataframe(df, use_container_width=True, height=450)
        st.markdown('</div>', unsafe_allow_html=True)

    # ADD DATA
    elif menu == "Add Data":
        st.title("➕ Add New Collaboration Record")
        st.markdown('<p class="subtitle-fix">Insert certified institutional MoU/MoA metadata into database.</p>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            id_in = st.number_input("Record ID", min_value=1, step=1, format="%d")
            title = st.text_input("Agreement Title")
            duration = st.text_input("Duration")
            department = st.text_input("Department")
        with col2:
            partner = st.text_input("Partner Institution")
            country = st.text_input("Country")
            category = st.selectbox("Agreement Category", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"])

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save Record"):
            cursor.execute("INSERT INTO collaboration_data (id, title, duration, department, partner, country, category) VALUES (?,?,?,?,?,?,?)",
                           (int(id_in), title, duration, department, partner, country, category))
            conn.commit()
            st.success("Record inserted successfully.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # UPDATE DATA
    elif menu == "Update Data":
        st.title("📝 Update Collaboration Record")
        st.markdown('<p class="subtitle-fix">Modify properties of existing collaboration data securely.</p>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        uid = st.number_input("Enter Record ID", min_value=1, step=1, format="%d")
        cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(uid),))
        result = cursor.fetchone()

        if result:
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Agreement Title", result[1])
                duration = st.text_input("Duration", result[2])
                department = st.text_input("Department", result[3])
            with col2:
                partner = st.text_input("Partner Institution", result[4])
                country = st.text_input("Country", result[5])
                category = st.selectbox("Agreement Category", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"])

            if st.button("Update Record"):
                cursor.execute("UPDATE collaboration_data SET title=?, duration=?, department=?, partner=?, country=?, category=? WHERE id=?",
                               (title, duration, department, partner, country, category, int(uid)))
                conn.commit()
                st.success("Record updated successfully.")
                st.rerun()
        else:
            st.warning("Record not found.")
        st.markdown('</div>', unsafe_allow_html=True)

    # DELETE DATA
    elif menu == "Delete Data":
        st.title("🗑️ Delete Collaboration Record")
        st.markdown('<p class="subtitle-fix">Purge records permanently from the system configuration.</p>', unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        del_id = st.number_input("Enter Record ID to Delete", min_value=1, step=1, format="%d")
        st.error("Deleted records cannot be recovered.")

        if st.button("Delete Record"):
            cursor.execute("DELETE FROM collaboration_data WHERE id=?", (int(del_id),))
            conn.commit()
            st.success("Record deleted successfully.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)