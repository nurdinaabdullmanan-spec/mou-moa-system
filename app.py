import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="MoU/MoA Collaboration Hub",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

conn = sqlite3.connect("mou_moa_db.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS collaboration_data(
    id INTEGER PRIMARY KEY,
    title TEXT,
    duration TEXT,
    location TEXT,
    partner TEXT,
    country TEXT,
    category TEXT
)
""")
conn.commit()

st.markdown("""
<style>
#MainMenu, footer {visibility:hidden;}

.stApp{
background:#f5f7fb;
}

section[data-testid="stSidebar"]{
background:#ffffff;
border-right:1px solid #e5e7eb;
}

.hero{
background:white;
padding:30px;
border-radius:24px;
border:1px solid #e5e7eb;
margin-bottom:20px;
}

.card{
background:white;
padding:20px;
border-radius:20px;
border:1px solid #e5e7eb;
text-align:center;
}

.stButton button{
border-radius:14px;
font-weight:600;
}

.metric-box{
background:white;
padding:20px;
border-radius:20px;
border:1px solid #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("MoU / MoA Collaboration Hub")
    st.caption("Global partnership monitoring platform")

    auth = st.sidebar.selectbox(
        "Account",
        ["Login","Register","Reset Password"]
    )

    if auth == "Login":

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username,password)
            )

            if cursor.fetchone():
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password")

    elif auth == "Register":

        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):
            cursor.execute(
                "INSERT INTO users(username,email,password) VALUES(?,?,?)",
                (username,email,password)
            )
            conn.commit()
            st.success("Account created successfully")

    else:

        email = st.text_input("Email")
        password = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            cursor.execute(
                "UPDATE users SET password=? WHERE email=?",
                (password,email)
            )
            conn.commit()
            st.success("Password updated")

else:

    st.sidebar.title("🌍 Collaboration Hub")

    menu = st.sidebar.radio(
        "Navigation",
        ["Dashboard","View Data","Add Data","Update Data","Delete Data"]
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if menu == "Dashboard":

        cursor.execute("SELECT * FROM collaboration_data")
        rows = cursor.fetchall()

        df = pd.DataFrame(
            rows,
            columns=[
                "ID","Agreement Title","Duration",
                "Department","Partner","Country","Category"
            ]
        )

        st.markdown("""
        <div class="hero">
        <h4>🌍 GLOBAL PARTNERSHIP MONITOR</h4>
        <h1>MoU / MoA Collaboration Hub</h1>
        <p>Monitor global academic alignments and partnership activities.</p>
        </div>
        """, unsafe_allow_html=True)

        total = len(df)
        countries = df["Country"].nunique() if not df.empty else 0
        categories = df["Category"].nunique() if not df.empty else 0

        c1,c2,c3 = st.columns(3)

        c1.metric("Total Agreements", total)
        c2.metric("Countries", countries)
        c3.metric("Categories", categories)

        if not df.empty:
            country_chart = df["Country"].value_counts().reset_index()
            country_chart.columns = ["Country","Total"]

            fig = px.bar(
                country_chart,
                x="Country",
                y="Total",
                color="Country"
            )

            st.plotly_chart(fig, use_container_width=True)

    elif menu == "View Data":

        st.title("Collaboration Records")

        cursor.execute(
            "SELECT * FROM collaboration_data ORDER BY id"
        )

        data = cursor.fetchall()

        df = pd.DataFrame(
            data,
            columns=[
                "ID","Agreement Title","Duration",
                "Department","Partner","Country","Category"
            ]
        )

        st.dataframe(df, use_container_width=True)

    elif menu == "Add Data":

        st.title("New Agreement")

        id_ = st.number_input("ID", min_value=1)

        title = st.text_input("Agreement Title")
        duration = st.text_input("Duration")
        location = st.text_input("Department")
        partner = st.text_input("Partner Institution")
        country = st.text_input("Country")

        category = st.selectbox(
            "Category",
            [
                "Memorandum of Understanding (MoU)",
                "Agreement for MyRA Purpose"
            ]
        )

        if st.button("Save Record"):

            cursor.execute("""
            INSERT INTO collaboration_data
            VALUES(?,?,?,?,?,?,?)
            """,
            (
                int(id_),title,duration,
                location,partner,country,category
            ))

            conn.commit()
            st.success("Record inserted")

    elif menu == "Update Data":

        st.title("Update Record")

        uid = st.number_input("Record ID", min_value=1)

        cursor.execute(
            "SELECT * FROM collaboration_data WHERE id=?",
            (int(uid),)
        )

        row = cursor.fetchone()

        if row:

            title = st.text_input("Title", row[1])
            duration = st.text_input("Duration", row[2])
            location = st.text_input("Department", row[3])
            partner = st.text_input("Partner", row[4])
            country = st.text_input("Country", row[5])

            category = st.selectbox(
                "Category",
                [
                    "Memorandum of Understanding (MoU)",
                    "Agreement for MyRA Purpose"
                ]
            )

            if st.button("Update"):

                cursor.execute("""
                UPDATE collaboration_data
                SET title=?,duration=?,location=?,
                partner=?,country=?,category=?
                WHERE id=?
                """,
                (
                    title,duration,location,
                    partner,country,category,
                    int(uid)
                ))

                conn.commit()
                st.success("Record updated")

    elif menu == "Delete Data":

        st.title("Delete Record")

        did = st.number_input(
            "Record ID",
            min_value=1
        )

        if st.button("Delete"):

            cursor.execute(
                "DELETE FROM collaboration_data WHERE id=?",
                (int(did),)
            )

            conn.commit()
            st.success("Record deleted")
