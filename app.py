import plotly.express as px
import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect(r'C:\Users\nurdi\OneDrive\Desktop\my_streamlit_app\mou_moa_db.db')

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="MoU/MoA Collaboration Record Management System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# FORCE SIDEBAR SHOWA
# ======================================================

st.markdown("""
<style>        

/* HIDE STREAMLIT */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    min-width: 280px !important;
    max-width: 280px !important;
    border-right: 1px solid #e5e7eb !important;
    box-shadow: 4px 0px 25px rgba(0,0,0,0.05);
}

/* SIDEBAR CONTENT */
section[data-testid="stSidebar"] > div {
    padding-top: 20px;
}

/* SIDEBAR MENU */
div[role="radiogroup"] label {
    background: transparent;
    border-radius: 12px;
    padding: 10px 15px;
    margin-bottom: 8px;
    transition: 0.3s;
}

div[role="radiogroup"] label:hover {
    background: #eef2ff;
}

/* RADIO TEXT */
div[role="radiogroup"] label p {
    color: #374151 !important;
    font-size: 15px;
    font-weight: 500;
}

/* ACTIVE MENU */
div[role="radiogroup"] label[data-selected="true"] {
    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );
    border-radius: 12px;
}

div[role="radiogroup"] label[data-selected="true"] p {
    color: white !important;
}

/* SIDEBAR BUTTON */
section[data-testid="stSidebar"] .stButton button {
    border-radius: 12px;
}
                 
</style>
""", unsafe_allow_html=True)

# ======================================================
# DATABASE CONNECTION
# ======================================================

conn = sqlite3.connect(
    "mou_moa_db.db",
    check_same_thread=False
)

import os

st.write(os.path.abspath("mou_moa_db.db"))

cursor = conn.cursor()

# ======================================================
# CREATE TABLES
# ======================================================

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
# MODERN UI CSS
# ======================================================

st.markdown("""
<style>

/* FONT */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* BACKGROUND */
.stApp {
    background: #f8fafc;
}

/* MAIN CONTAINER */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #4338ca !important;
    font-weight: 500;
}

/* TITLES */
h1 {
    color: #1e1b4b !important;
    font-weight: 800 !important;
}

h2 {
    color: #312e81 !important;
    font-weight: 700 !important;
}

h3 {
    color: #4338ca !important;
    font-weight: 700 !important;
}

/* TEXT */
p {
    color: #374151 !important;
}

/* LABEL */
label {
    color: #312e81 !important;
    font-weight: 500 !important;
}

/* METRIC */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 18px;
    padding: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* BUTTON */
.stButton > button {
    width: 100%;
    border-radius: 16px;
    border: none;
    padding: 14px;
    font-weight: 600;
    color: white;
    background: linear-gradient(
        135deg,
        #6366f1,
        #8b5cf6
    );
}

/* BUTTON HOVER */
.stButton > button:hover {
    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );
    color: white;
}

/* INPUT */
.stTextInput input,
.stNumberInput input,
textarea {
    border-radius: 14px !important;
    background-color: rgba(255,255,255,0.85) !important;
    color: #111827 !important;
    font-weight: 500 !important;
}

/* PLACEHOLDER */
.stTextInput input::placeholder,
textarea::placeholder {
    color: #6b7280 !important;
    opacity: 1 !important;
}

/* SELECTBOX */
.stSelectbox div[data-baseweb="select"] * {
    color: #ffffff !important;
    font-weight: 500 !important;
}
            
/* FIX SELECTBOX TEXT COLOR (LOGIN / REGISTER / RESET) */
.stSelectbox [data-baseweb="select"] * {
    color: #ffffff !important;
}            

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}
            
.dashboard-card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #e5e7eb;
    margin-bottom: 20px;
}

.dashboard-title {
    font-size: 40px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    color: #6b7280;
    font-size: 16px;
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

if st.session_state.logged_in == False:

    st.title("MoU/MoA Collaboration Record Management System")

    st.write(
        "Secure collaboration agreement management platform."
    )

    auth = st.sidebar.selectbox(
    "Account",
    [
        "Login",
        "Register",
        "Reset Password"
    ]
)

    # LOGIN

    if auth == "Login":

        st.subheader("Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            sql = """
            SELECT * FROM users
            WHERE username=?
            AND password=?
            """

            val = (username, password)

            cursor.execute(sql, val)

            user = cursor.fetchone()

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login successful.")

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )

    # REGISTER

    elif auth == "Register":

        st.subheader("Create Account")

        new_username = st.text_input("Username")

        new_email = st.text_input("Email")

        new_password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Register"):

            sql = """
            INSERT INTO users
            (username, email, password)
            VALUES (?,?,?)
            """

            val = (
                new_username,
                new_email,
                new_password
            )

            cursor.execute(sql, val)

            conn.commit()

            st.success(
                "Account created successfully."
            )

    # RESET PASSWORD

    elif auth == "Reset Password":

        st.subheader("Reset Password")

        email = st.text_input("Enter Email")

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        if st.button("Reset Password"):

            sql = """
            UPDATE users
            SET password=?
            WHERE email=?
            """

            val = (
                new_password,
                email
            )

            cursor.execute(sql, val)

            conn.commit()

            st.success(
                "Password updated successfully."
            )

# ======================================================
# MAIN SYSTEM
# ======================================================

else:

    st.sidebar.markdown(
        """
        <div style="text-align:center;">
            <h2 style="color:#4338ca;">
                MoU/MoA System
            </h2>
            <p style="color:gray;">
                Collaboration Management Platform
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    menu = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "View Data",
            "Add Data",
            "Update Data",
            "Delete Data"
        ]
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()

    # DASHBOARD

    if menu == "Dashboard":

        st.title(
            "MoU/MoA Collaboration Record Management System"
        )

        cursor.execute(
            "SELECT * FROM collaboration_data ORDER BY id ASC"
        )

        rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=[
            "ID",
            "Agreement Title",
            "Duration",
            "Department",
            "Partner",
            "Country",
            "Category"
        ])

        total_records = len(df)

        total_country = df["Country"].nunique()

        total_category = df["Category"].nunique()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Agreements", total_records)

        with col2:
            st.metric("Countries", total_country)

        with col3:
            st.metric("Agreement Categories", total_category)

        st.subheader("Country Distribution")

        country_chart = df["Country"].value_counts().reset_index()

        country_chart.columns = [
            "Country",
            "Total"
        ]

        fig = px.bar(
            country_chart,
            x="Country",
            y="Total",
            color="Country",
            text_auto=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
    # ======================================================
    # VIEW DATA
    # ======================================================

    elif menu == "View Data":

        st.title("Collaboration Records")

        search = st.text_input(
            "Search by Agreement Title, Partner or Country"
        )

        if search:

            sql = """
            SELECT * FROM collaboration_data
            WHERE title LIKE ?
            OR partner LIKE ?
            OR country LIKE ?
            """

            val = (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            )

            cursor.execute(sql, val)

        else:

            cursor.execute(
                 "SELECT * FROM collaboration_data ORDER BY id ASC"
            )

        data = cursor.fetchall()

        df = pd.DataFrame(data, columns=[
            "ID",
            "Agreement Title",
            "Duration",
            "Department",
            "Partner",
            "Country",
            "Category"
        ])

        st.dataframe(
            df,
            use_container_width=True,
            height=500
        )

    # ======================================================
    # ADD DATA
    # ======================================================

    elif menu == "Add Data":

        st.title("Add New Collaboration Record")

        col1, col2 = st.columns(2)

        with col1:

            id = st.number_input(
                "Record ID",
                min_value=1,
                step=1,
                format="%d"
            )

            title = st.text_input(
                "Agreement Title"
            )

            duration = st.text_input(
                "Duration"
            )

            department = st.text_input(
                "Department"
            )

        with col2:

            partner = st.text_input(
                "Partner Institution"
            )

            country = st.text_input(
                "Country"
            )

            category = st.selectbox(
                "Agreement Category",
                [
                    "Memorandum of Understanding (MoU)",
                    "Agreement for MyRA Purpose"
                ]
            )

        if st.button("Save Record"):

            sql = """
            INSERT INTO collaboration_data
            (id, title, duration, department, partner, country, category)
            VALUES (?,?,?,?,?,?,?)
            """

            val = (
                int(id),
                title,
                duration,
                department,
                partner,
                country,
                category
            )

            cursor.execute(sql, val)

            conn.commit()

            st.success(
                "Record inserted successfully."
            )

    # ======================================================
    # UPDATE DATA
    # ======================================================

    elif menu == "Update Data":

        st.title("Update Collaboration Record")

        uid = st.number_input(
            "Enter Record ID",
            min_value=1,
            step=1,
            format="%d"
        )

        cursor.execute(
            "SELECT * FROM collaboration_data WHERE id=?",
            (int(uid),)
        )

        result = cursor.fetchone()

        if result:

            col1, col2 = st.columns(2)

            with col1:

                title = st.text_input(
                    "Agreement Title",
                    result[1]
                )

                duration = st.text_input(
                    "Duration",
                    result[2]
                )

                department = st.text_input(
                    "Department",
                    result[3]
                )

            with col2:

                partner = st.text_input(
                    "Partner Institution",
                    result[4]
                )

                country = st.text_input(
                    "Country",
                    result[5]
                )

                category = st.selectbox(
                    "Agreement Category",
                    [
                        "Memorandum of Understanding (MoU)",
                        "Agreement for MyRA Purpose"
                    ]
                )

            if st.button("Update Record"):

                sql = """
                UPDATE collaboration_data
                SET
                    title=?,
                    duration=?,
                    department=?,
                    partner=?,
                    country=?,
                    category=?
                WHERE id=?
                """

                val = (
                    title,
                    duration,
                    department,
                    partner,
                    country,
                    category,
                    int(uid)
                )

                cursor.execute(sql, val)

                conn.commit()

                st.success(
                    "Record updated successfully."
                )

        else:

            st.warning(
                "Record not found."
            )

    # ======================================================
    # DELETE DATA
    # ======================================================

    elif menu == "Delete Data":

        st.title("Delete Collaboration Record")

        del_id = st.number_input(
            "Enter Record ID to Delete",
            min_value=1,
            step=1,
            format="%d"
        )

        st.warning(
            "Deleted records cannot be recovered."
        )

        if st.button("Delete Record"):

            cursor.execute(
                "DELETE FROM collaboration_data WHERE id=?",
                (int(del_id),)
            )

            conn.commit()

            st.success(
                "Record deleted successfully."
            )