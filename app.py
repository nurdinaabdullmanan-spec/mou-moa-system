import plotly.express as px
import streamlit as st
import sqlite3
import pandas as pd

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
# DATABASE CONNECTION
# ======================================================

conn = sqlite3.connect(
    "mou_moa_db.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ======================================================
# CREATE USERS TABLE
# ======================================================

cursor.execute("""
               
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password TEXT
)
""")

conn.commit()

# ======================================================
# MODERN UI CSS
# ======================================================

st.markdown("""
<style>

/* FONT */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* BACKGROUND */
.stApp {
    background: linear-gradient(
        135deg,
        #f5f3ff,
        #eef2ff,
        #f8fafc
    );
}

/* HIDE STREAMLIT DEFAULT */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* MAIN CONTAINER */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(18px);
    border-right: 1px solid rgba(255,255,255,0.3);
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #4338ca !important;
    font-weight: 500;
}

/* TITLES */
h1, h2, h3 {
    color: #312e81;
    font-weight: 700;
}

/* METRIC CARDS */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.6);
    border-radius: 24px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.3);
    box-shadow: 0 8px 32px rgba(31,38,135,0.08);
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

    transition: 0.3s ease;
}

/* BUTTON HOVER */
.stButton > button:hover {

    transform: translateY(-2px);

    background: linear-gradient(
        135deg,
        #4f46e5,
        #7c3aed
    );

    color: white;
}

/* INPUT */
.stTextInput input,
.stNumberInput input {

    border-radius: 14px !important;
    background-color: rgba(255,255,255,0.85) !important;
}

/* SELECTBOX */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 14px !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {

    border-radius: 18px;
    overflow: hidden;
}

/* ALERT BOX */
.stSuccess,
.stWarning,
.stInfo,
.stError {
    border-radius: 14px;
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

    # ======================================================
    # LOGIN
    # ======================================================

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
            WHERE username=%s
            AND password=%s
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

    # ======================================================
    # REGISTER
    # ======================================================

    elif auth == "Register":

        st.subheader("Create Account")

        new_username = st.text_input(
            "Username"
        )

        new_email = st.text_input(
            "Email"
        )

        new_password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Register"):

            sql = """
            INSERT INTO users
            (username, email, password)
            VALUES (%s,%s,%s)
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

    # ======================================================
    # RESET PASSWORD
    # ======================================================

    elif auth == "Reset Password":

        st.subheader("Reset Password")

        email = st.text_input(
            "Enter Email"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        if st.button("Reset Password"):

            sql = """
            UPDATE users
            SET password=%s
            WHERE email=%s
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

    # ======================================================
    # SIDEBAR
    # ======================================================

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

    st.sidebar.success(
        f"Welcome, {st.session_state.username}"
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

    # ======================================================
    # DASHBOARD
    # ======================================================

    if menu == "Dashboard":

        st.title(
            "MoU/MoA Collaboration Record Management System"
        )

        st.write(
            "Professional dashboard for collaboration agreement management."
        )

        cursor.execute(
            "SELECT * FROM collaboration_data"
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

        # ======================================================
        # METRICS
        # ======================================================

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Agreements",
                total_records
            )

        with col2:
            st.metric(
                "Countries",
                total_country
            )

        with col3:
            st.metric(
                "Agreement Categories",
                total_category
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ======================================================
        # CHART
        # ======================================================

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

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                family="Poppins",
                size=14
            ),
            xaxis_title="Country",
            yaxis_title="Total Agreements",
            height=500
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
            WHERE title LIKE %s
            OR partner LIKE %s
            OR country LIKE %s
            """

            val = (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            )

            cursor.execute(sql, val)

        else:

            cursor.execute(
                "SELECT * FROM collaboration_data"
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
                step=1
            )

            title = st.text_input(
                "Agreement Title"
            )

            duration = st.text_input(
                "Duration"
            )

            location = st.text_input(
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
            (id, title, duration, location, partner, country, category)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """

            val = (
                id,
                title,
                duration,
                location,
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
            step=1
        )

        cursor.execute(
            "SELECT * FROM collaboration_data WHERE id=%s",
            (uid,)
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

                location = st.text_input(
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
                    title=%s,
                    duration=%s,
                    location=%s,
                    partner=%s,
                    country=%s,
                    category=%s
                WHERE id=%s
                """

                val = (
                    title,
                    duration,
                    location,
                    partner,
                    country,
                    category,
                    uid
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
            step=1
        )

        st.warning(
            "Deleted records cannot be recovered."
        )

        if st.button("Delete Record"):

            cursor.execute(
                "DELETE FROM collaboration_data WHERE id=%s",
                (del_id,)
            )

            conn.commit()

            st.success(
                "Record deleted successfully."
            )