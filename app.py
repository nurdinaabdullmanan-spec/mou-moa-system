import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(page_title="MoU/MoA Management System", layout="wide")

# ======================================================
# DATABASE SETUP
# ======================================================
conn = sqlite3.connect("mou_moa_db.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS collaboration_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    title TEXT, duration TEXT, department TEXT, 
    partner TEXT, country TEXT, category TEXT
)
""")
conn.commit()

# ======================================================
# CSS (MODERN LIGHT & PROFESSIONAL)
# ======================================================
st.markdown("""
<style>
    /* Global Styles */
    .stApp { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    
    /* Headers */
    h1, h2, h3 { color: #1e293b !important; }
    
    /* Card UI */
    .content-card { 
        background: #ffffff; padding: 25px; border-radius: 16px; 
        border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    
    /* Scorecards */
    .metric-container { display: flex; gap: 20px; }
    .metric-card { flex: 1; padding: 20px; border-radius: 16px; color: white; text-align: center; }
    .bg-1 { background: linear-gradient(135deg, #6366f1, #4f46e5); }
    .bg-2 { background: linear-gradient(135deg, #10b981, #059669); }
    .bg-3 { background: linear-gradient(135deg, #f59e0b, #d97706); }
    
    /* Buttons */
    .stButton > button { border-radius: 8px; width: 100%; background: #1e293b; color: white; border: none; }
    .stButton > button:hover { background: #334155; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# NAVIGATION
# ======================================================
if "page" not in st.session_state: st.session_state.page = "Dashboard"

st.sidebar.title("🎓 Collaboration System")
menu = ["Dashboard", "View Data", "Add Data", "Update Data", "Delete Data"]
choice = st.sidebar.radio("Navigation Menu", menu)
st.session_state.page = choice

# Helper to refresh dataframe
def get_data(): return pd.read_sql("SELECT * FROM collaboration_data", conn)

# ======================================================
# MAIN CONTENT
# ======================================================
df = get_data()

if st.session_state.page == "Dashboard":
    st.title("📊 Analytics Dashboard")
    
    # Scorecards
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-card bg-1"><h3>{len(df)}</h3><p>Total Records</p></div>
        <div class="metric-card bg-2"><h3>{df['country'].nunique() if not df.empty else 0}</h3><p>Countries</p></div>
        <div class="metric-card bg-3"><h3>{df['category'].nunique() if not df.empty else 0}</h3><p>Categories</p></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### Global Distribution")
    if not df.empty:
        fig = px.bar(df['country'].value_counts().reset_index(), x='country', y='count', color='country')
        st.plotly_chart(fig, use_container_width=True)

elif st.session_state.page == "View Data":
    st.title("📋 Repository Data")
    st.dataframe(df, use_container_width=True)

elif st.session_state.page == "Add Data":
    st.title("➕ Add New Record")
    with st.form("add_form"):
        col1, col2 = st.columns(2)
        title = col1.text_input("Agreement Title")
        dur = col1.text_input("Duration")
        dept = col1.text_input("Department")
        part = col2.text_input("Partner Institution")
        cntry = col2.text_input("Country")
        cat = col2.selectbox("Category", ["Memorandum of Understanding (MoU)", "Memorandum of Agreement (MoA)"])
        
        if st.form_submit_button("Commit Data"):
            cursor.execute("INSERT INTO collaboration_data (title, duration, department, partner, country, category) VALUES (?,?,?,?,?,?)", (title, dur, dept, part, cntry, cat))
            conn.commit()
            st.success("Record added successfully!")

elif st.session_state.page == "Update Data":
    st.title("📝 Edit Existing Records")
    uid = st.number_input("Enter Record ID to Edit", min_value=1, step=1)
    record = cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (uid,)).fetchone()
    
    if record:
        with st.form("upd_form"):
            t = st.text_input("Title", record[1])
            d = st.text_input("Duration", record[2])
            dept = st.text_input("Department", record[3])
            p = st.text_input("Partner", record[4])
            c = st.text_input("Country", record[5])
            cat = st.selectbox("Category", ["Memorandum of Understanding (MoU)", "Memorandum of Agreement (MoA)"], index=0 if record[6]=="MoU" else 1)
            
            if st.form_submit_button("Update Record"):
                cursor.execute("UPDATE collaboration_data SET title=?, duration=?, department=?, partner=?, country=?, category=? WHERE id=?", (t, d, dept, p, c, cat, uid))
                conn.commit()
                st.success("Record updated!")
    else:
        st.warning("Please enter a valid ID.")

elif st.session_state.page == "Delete Data":
    st.title("🗑️ Delete Record")
    del_id = st.number_input("Enter ID to permanently remove", min_value=1, step=1)
    if st.button("Confirm Deletion"):
        cursor.execute("DELETE FROM collaboration_data WHERE id=?", (del_id,))
        conn.commit()
        st.error("Record has been purged.")