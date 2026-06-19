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
# PROFESSIONAL UI CSS (UiTM INSPIRED: PURPLE, GOLD, BLUE)
# ======================================================
st.markdown("""
<style>
    /* IMPORT FONT */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* BACKGROUND & MAIN CONTAINER */
    .stApp {
        background-color: #fcfcfd;
    }
    .block-container {
        padding: 2.5rem 3rem !important;
    }

    /* HIDE STREAMLIT FOOTER & MENU */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #1e1b4b !important; /* Deep Royal Purple/Navy */
        border-right: 1px solid #e5e7eb !important;
    }
    
    /* SIDEBAR TEXT & LABELS */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }

    /* SIDEBAR NAVIGATION (RADIO NAV) */
    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 12px 18px;
        margin-bottom: 10px;
        transition: all 0.2s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.15);
    }

    div[role="radiogroup"] label p {
        color: #f3f4f6 !important;
        font-weight: 500 !important;
    }

    /* ACTIVE NAVIGATION */
    div[role="radiogroup"] label[data-selected="true"] {
        background: #fabf2c !important; /* UiTM Gold */
        border: 1px solid #fabf2c !important;
    }

    div[role="radiogroup"] label[data-selected="true"] p {
        color: #1e1b4b !important; /* Dark text on Gold */
        font-weight: 600 !important;
    }

    /* TYPOGRAPHY / HEADINGS */
    h1 {
        color: #4b2e83 !important; /* UiTM Corporate Purple */
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    h2, h3 {
        color: #1e3a8a !important; /* Professional Blue */
        font-weight: 600 !important;
    }
    label {
        color: #374151 !important;
        font-weight: 500 !important;
    }

    /* METRIC CARDS */
    div[data-testid="metric-container"] {
        background: white;
        border-radius: 14px;
        padding: 20px;
        border-left: 5px solid #4b2e83; /* Purple accent */
        border-top: 1px solid #e5e7eb;
        border-right: 1px solid #e5e7eb;
        border-bottom: 1px solid #e5e7eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    div[data-testid="stMetricValue"] {
        color: #1e3a8a !important; /* Blue for data values */
        font-weight: 700 !important;
    }

    /* GENERAL BUTTONS */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: none;
        padding: 12px;
        font-weight: 600;
        color: white !important;
        background: #4b2e83 !important; /* Purple Main */
        box-shadow: 0 2px 4px rgba(75, 46, 131, 0.2);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #362161 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(75, 46, 131, 0.3);
    }

    /* LOGOUT BUTTON (SIDEBAR SPECIFIC) */
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: 1px solid #ef4444 !important;
        color: #ef4444 !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #ef4444 !important;
        color: white !important;
    }

    /* INPUT FIELDS & SELECTBOX FIX */
    .stTextInput input, .stNumberInput input, textarea {
        border-radius: 10px !important;
        border: 1px solid #d1d5db !important;
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* FIX FOR SELECTBOX TEXT VISIBILITY */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 10px !important;
        background-color: #ffffff !important;
    }
    .stSelectbox div[data-baseweb="select"] * {
        color: #1f2937 !important; /* Ensure text is dark and visible */
    }

    /* DATAFRAME */
    [data-testid="stDataFrame"] {
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
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
    st.write("Welcome back. Please secure your access session below.")
    st.markdown("---")

    auth = st.sidebar.selectbox(
        "System Access",
        ["Login", "Register", "Reset Password"]
    )

    # LOGIN
    if auth == "Login":
        st.subheader("Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign In to System"):
            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=?", 
                (username, password)
            )
            user = cursor.fetchone()

            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Access granted.")
                st.rerun()
            else:
                st.error("Invalid corporate credentials.")

    # REGISTER
    elif auth == "Register":
        st.subheader("Create Account")
        new_username = st.text_input("Username")
        new_email = st.text_input("Email Address")
        new_password = st.text_input("Password", type="password")

        if st.button("Register Account"):
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?,?,?)",
                (new_username, new_email, new_password)
            )
            conn.commit()
            st.success("Account registered successfully.")

    # RESET PASSWORD
    elif auth == "Reset Password":
        st.subheader("Reset Password")
        email = st.text_input("Enter Registered Email")
        new_password = st.text_input("New Password", type="password")

        if st.button("Update Password"):
            cursor.execute(
                "UPDATE users SET password=? WHERE email=?",
                (new_password, email)
            )
            conn.commit()
            st.success("Password updated successfully.")

# ======================================================
# MAIN SYSTEM
# ======================================================
else:
    # Sidebar Profile Header
    st.sidebar.markdown(
        f"""
        <div style="text-align:center; padding: 10px 0 20px 0;">
            <h2 style="color:#fabf2c; margin:0; font-size:22px;">UiTM Record System</h2>
            <p style="color:#9ca3af; margin:5px 0 0 0; font-size:13px;">Logged in as: <b>{st.session_state.username}</b></p>
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

    # Fetch fresh dataframe for views
    cursor.execute("SELECT * FROM collaboration_data ORDER BY id ASC")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])

    # DASHBOARD
    if menu == "Dashboard":
        st.title("📊 System Dashboard")
        st.write("Real-time Overview of Institutional Agreements & External Collaborations.")
        st.markdown("---")

        total_records = len(df)
        total_country = df["Country"].nunique() if total_records > 0 else 0
        total_category = df["Category"].nunique() if total_records > 0 else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Agreements", total_records)
        with col2:
            st.metric("Partner Countries", total_country)
        with col3:
            st.metric("Agreement Categories", total_category)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🌐 Global Distribution (By Country)")

        if total_records > 0:
            country_chart = df["Country"].value_counts().reset_index()
            country_chart.columns = ["Country", "Total"]

            # Customized Chart to blend with UiTM Colors (Purple to Blue gradient look)
            fig = px.bar(
                country_chart,
                x="Country",
                y="Total",
                color="Total",
                color_continuous_scale=["#1e3a8a", "#4b2e83"],
                text_auto=True
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No records available to display data charts. Go to 'Add Data' to populate database.")

    # VIEW DATA
    elif menu == "View Data":
        st.title("🗂️ Collaboration Records")
        st.write("Search and browse full records from the system database.")
        st.markdown("---")

        search = st.text_input("🔍 Quick Search (Enter Agreement Title, Partner or Country)")

        if search:
            sql = """
            SELECT * FROM collaboration_data
            WHERE title LIKE ? OR partner LIKE ? OR country LIKE ?
            """
            cursor.execute(sql, (f"%{search}%", f"%{search}%", f"%{search}%"))
            search_data = cursor.fetchall()
            display_df = pd.DataFrame(search_data, columns=["ID", "Agreement Title", "Duration", "Department", "Partner", "Country", "Category"])
        else:
            display_df = df

        st.dataframe(display_df, use_container_width=True, height=500)

    # ADD DATA
    elif menu == "Add Data":
        st.title("➕ Add New Collaboration Record")
        st.write("Insert certified institutional MoU/MoA metadata into database.")
        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            id_val = st.number_input("Record ID", min_value=1, step=1, format="%d")
            title = st.text_input("Agreement Title")
            duration = st.text_input("Duration (e.g., 3 Years)")
            department = st.text_input("Owner Department / Faculty")

        with col2:
            partner = st.text_input("Partner Institution")
            country = st.text_input("Country")
            category = st.selectbox(
                "Agreement Category",
                ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"]
            )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save Record into Database"):
            if title and partner:
                try:
                    cursor.execute(
                        "INSERT INTO collaboration_data (id, title, duration, department, partner, country, category) VALUES (?,?,?,?,?,?,?)",
                        (int(id_val), title, duration, department, partner, country, category)
                    )
                    conn.commit()
                    st.success("Record secured successfully.")
                except sqlite3.IntegrityError:
                    st.error("Record ID already exists. Please use a unique ID.")
            else:
                st.error("Please fill in key text fields (Title & Partner).")

    # UPDATE DATA
    elif menu == "Update Data":
        st.title("📝 Update Collaboration Record")
        st.write("Modify properties of existing collaboration data securely.")
        st.markdown("---")

        uid = st.number_input("Enter Record ID to Modify", min_value=1, step=1, format="%d")
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
                category = st.selectbox(
                    "Agreement Category",
                    ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"],
                    index=0 if result[6] == "Memorandum of Understanding (MoU)" else 1
                )

            if st.button("Push Updates"):
                cursor.execute(
                    "UPDATE collaboration_data SET title=?, duration=?, department=?, partner=?, country=?, category=? WHERE id=?",
                    (title, duration, department, partner, country, category, int(uid))
                )
                conn.commit()
                st.success("Data logs updated successfully.")
        else:
            st.warning("No entry found matching this Record ID.")

    # DELETE DATA
    elif menu == "Delete Data":
        st.title("🗑️ Revoke / Delete Record")
        st.write("Purge records permanently from the configuration cluster.")
        st.markdown("---")

        del_id = st.number_input("Enter Target Record ID to Delete", min_value=1, step=1, format="%d")
        
        st.warning("⚠️ Warning: Data cannot be restored once dropped from the database tables.")
        if st.button("Execute Hard Delete"):
            cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(del_id),))
            if cursor.fetchone():
                cursor.execute("DELETE FROM collaboration_data WHERE id=?", (int(del_id),))
                conn.commit()
                st.success("Record cleared safely.")
            else:
                st.error("Action aborted: Record ID not found.")