import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ======================================================
# 1. PAGE CONFIG & DATABASE SETUP
# ======================================================
st.set_page_config(
    page_title="MoU/MoA Record Management",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database Connection
conn = sqlite3.connect("mou_moa_management.db", check_same_thread=False)
cursor = conn.cursor()

# Create Table with Status column
cursor.execute("""
CREATE TABLE IF NOT EXISTS collaboration_records (
    id INTEGER PRIMARY KEY,
    title TEXT,
    partner TEXT,
    country TEXT,
    category TEXT,
    duration TEXT,
    status TEXT
)
""")
conn.commit()

# Insert Sample Data if Database is Empty
cursor.execute("SELECT COUNT(*) FROM collaboration_records")
if cursor.fetchone()[0] == 0:
    samples = [
        (58, "MoU on Academic Collaboration", "Kyushu University", "Japan", "MoU", "2024 - 2027", "Active"),
        (57, "MoA for Student Exchange", "University of Indonesia", "Indonesia", "MoA", "2023 - 2026", "Active"),
        (56, "MoU on Research Collaboration", "University of Malaya", "Malaysia", "MoU", "2024 - 2029", "Active"),
        (55, "MoA for Industrial Training", "Microsoft Corporation", "United States", "MoA", "2023 - 2025", "Expired"),
        (54, "MoU on Joint Publication", "Tsinghua University", "China", "MoU", "2022 - 2026", "Active")
    ]
    cursor.executemany("INSERT INTO collaboration_records VALUES (?,?,?,?,?,?,?)", samples)
    conn.commit()

# ======================================================
# 2. CUSTOM CSS (REDESIGN THEME)
# ======================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #F8FAFC !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Custom Navigation Buttons */
    .stButton > button {
        border-radius: 10px;
        text-align: left;
        padding: 10px 15px;
        border: none;
        background-color: transparent;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #F1F5F9 !important;
        color: #6366F1 !important;
    }

    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .metric-val { font-size: 28px; font-weight: 700; color: #1E293B; margin: 5px 0; }
    .metric-label { color: #64748B; font-size: 13px; font-weight: 600; text-transform: uppercase; }

    /* Badges */
    .badge { padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; text-transform: uppercase; }
    .badge-active { background: #DCFCE7; color: #166534; }
    .badge-expired { background: #FEE2E2; color: #991B1B; }
    .badge-mou { background: #E0E7FF; color: #3730A3; border: 1px solid #C7D2FE; }
    .badge-moa { background: #FFEDD5; color: #9A3412; border: 1px solid #FED7AA; }

    /* Hide standard Streamlit header */
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ======================================================
# 3. SIDEBAR NAVIGATION
# ======================================================
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/UiTM_Logo.png/640px-UiTM_Logo.png", width=120)
    st.markdown("<h3 style='font-size:18px;'>MoU/MoA <br><span style='font-size:12px; color:gray; font-weight:normal;'>Collaboration Record System</span></h3>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("📊 Dashboard", use_container_width=True): st.session_state.page = "Dashboard"
    if st.button("📋 View All Records", use_container_width=True): st.session_state.page = "View"
    if st.button("➕ Add New Record", use_container_width=True): st.session_state.page = "Add"
    if st.button("📝 Update Record", use_container_width=True): st.session_state.page = "Update"
    if st.button("🗑️ Delete Record", use_container_width=True): st.session_state.page = "Delete"
    
    st.markdown("<br><hr style='border:0.1px solid #EEE'><p style='font-size:10px; color:silver;'>USER MENU</p>", unsafe_allow_html=True)
    st.button("👤 Profile", use_container_width=True)
    st.button("🚪 Logout", use_container_width=True)

    # Bottom Illustration
    st.markdown("""
    <div style="background: #F1F5F9; padding: 15px; border-radius: 15px; margin-top: 40px; text-align:center;">
        <img src="https://cdn-icons-png.flaticon.com/512/3126/3126589.png" width="60">
        <p style="font-weight:bold; font-size:13px; margin-top:10px; margin-bottom:5px;">Building Strategic Partnerships</p>
        <p style="font-size:10px; color:gray;">Together we create impact through collaboration.</p>
    </div>
    """, unsafe_allow_html=True)

# Helper function to refresh data
def get_df():
    return pd.read_sql("SELECT * FROM collaboration_records ORDER BY id DESC", conn)

# ======================================================
# 4. MODULE: DASHBOARD
# ======================================================
if st.session_state.page == "Dashboard":
    df = get_df()
    
    # Header
    c_h1, c_h2 = st.columns([3, 1])
    with c_h1:
        st.markdown(f"<h2>Good Afternoon, Dee! 👋</h2><p style='color:gray;'>Welcome back to MoU/MoA Collaboration Management System</p>", unsafe_allow_html=True)
    with c_h2:
        now = datetime.now()
        st.markdown(f"<div style='text-align:right; background:white; padding:10px; border-radius:10px; border:1px solid #EEE;'><p style='margin:0; font-size:12px; color:gray;'>{now.strftime('%A')}</p><p style='margin:0; font-weight:bold;'>{now.strftime('%d %B %Y')}</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><p class="metric-label">Total Agreements</p><p class="metric-val">{len(df)}</p><p style="font-size:10px; color:gray;">All records in system</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><p class="metric-label">Countries</p><p class="metric-val">{df["country"].nunique()}</p><p style="font-size:10px; color:gray;">Unique countries</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><p class="metric-label">Categories</p><p class="metric-val">2</p><p style="font-size:10px; color:gray;">MoU & MoA</p></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><p class="metric-label">Active Agreements</p><p class="metric-val">{len(df[df["status"]=="Active"])}</p><p style="font-size:10px; color:gray;">Currently active</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown('<div class="metric-card"><b>Agreements by Country</b>', unsafe_allow_html=True)
        counts = df['country'].value_counts().reset_index()
        fig1 = px.bar(counts, x='country', y='count', color='country', color_discrete_sequence=['#8B5CF6', '#3B82F6', '#10B981', '#F59E0B', '#EF4444'])
        fig1.update_layout(height=280, showlegend=False, margin=dict(t=20,b=0,l=0,r=0), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><b>Agreements by Category</b>', unsafe_allow_html=True)
        cat_counts = df['category'].value_counts()
        fig2 = go.Figure(data=[go.Pie(labels=cat_counts.index, values=cat_counts.values, hole=.7, marker=dict(colors=['#8B5CF6', '#F59E0B']))])
        fig2.update_layout(height=280, margin=dict(t=20,b=0,l=0,r=0), annotations=[dict(text=str(len(df)), x=0.5, y=0.5, font_size=20, showarrow=False)])
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent Table
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="metric-card"><b>Recent Records</b>', unsafe_allow_html=True)
    table_html = """<table style='width:100%; border-collapse: collapse; margin-top:15px;'><tr style='text-align:left; color:gray; font-size:12px; border-bottom:1px solid #EEE;'>
    <th style='padding:10px;'>ID</th><th style='padding:10px;'>Title</th><th style='padding:10px;'>Partner Institution</th><th style='padding:10px;'>Country</th><th style='padding:10px;'>Category</th><th style='padding:10px;'>Duration</th><th style='padding:10px;'>Status</th></tr>"""
    for _, row in df.head(5).iterrows():
        st_cls = "badge-active" if row['status'] == "Active" else "badge-expired"
        ct_cls = "badge-mou" if row['category'] == "MoU" else "badge-moa"
        table_html += f"<tr style='border-bottom:1px solid #F8FAFC; font-size:13px;'><td style='padding:12px;'>{row['id']}</td><td style='padding:12px; font-weight:500;'>{row['title']}</td><td style='padding:12px;'>{row['partner']}</td><td style='padding:12px;'>{row['country']}</td><td><span class='badge {ct_cls}'>{row['category']}</span></td><td style='color:gray;'>{row['duration']}</td><td><span class='badge {st_cls}'>{row['status']}</span></td></tr>"
    st.markdown(table_html + "</table></div>", unsafe_allow_html=True)

# ======================================================
# 5. MODULE: VIEW ALL
# ======================================================
elif st.session_state.page == "View":
    st.title("🗂️ All Collaboration Records")
    df = get_df()
    search = st.text_input("🔍 Search by Title, Partner, or Country")
    if search:
        df = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
    st.dataframe(df, use_container_width=True, hide_index=True)

# ======================================================
# 6. MODULE: ADD RECORD
# ======================================================
elif st.session_state.page == "Add":
    st.title("➕ Deploy New Record Entry")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            new_id = st.number_input("Record ID", min_value=1, step=1)
            new_title = st.text_input("Agreement Title")
            new_partner = st.text_input("Partner Institution")
        with col2:
            new_country = st.text_input("Country")
            new_cat = st.selectbox("Category", ["MoU", "MoA"])
            new_dur = st.text_input("Duration (e.g. 2024 - 2027)")
        
        new_status = st.selectbox("Status", ["Active", "Expired"])

        if st.button("🚀 Commit Record to Database", type="primary"):
            try:
                cursor.execute("INSERT INTO collaboration_records VALUES (?,?,?,?,?,?,?)", 
                               (new_id, new_title, new_partner, new_country, new_cat, new_dur, new_status))
                conn.commit()
                st.success("Successfully added to the system!")
            except Exception as e:
                st.error(f"Error: Record ID {new_id} might already exist.")

# ======================================================
# 7. MODULE: UPDATE RECORD
# ======================================================
elif st.session_state.page == "Update":
    st.title("📝 Edit Existing Records Mapping")
    search_id = st.number_input("Enter Record ID to Edit", min_value=1, step=1)
    
    cursor.execute("SELECT * FROM collaboration_records WHERE id=?", (search_id,))
    data = cursor.fetchone()

    if data:
        st.info(f"Editing: {data[1]}")
        with st.form("update_form"):
            col1, col2 = st.columns(2)
            with col1:
                u_title = st.text_input("Agreement Title", value=data[1])
                u_partner = st.text_input("Partner Institution", value=data[2])
                u_country = st.text_input("Country", value=data[3])
            with col2:
                u_cat = st.selectbox("Category", ["MoU", "MoA"], index=0 if data[4]=="MoU" else 1)
                u_dur = st.text_input("Duration", value=data[5])
                u_status = st.selectbox("Status", ["Active", "Expired"], index=0 if data[6]=="Active" else 1)
            
            if st.form_submit_button("Update Record"):
                cursor.execute("""UPDATE collaboration_records 
                               SET title=?, partner=?, country=?, category=?, duration=?, status=? 
                               WHERE id=?""", (u_title, u_partner, u_country, u_cat, u_dur, u_status, search_id))
                conn.commit()
                st.success("Record Updated Successfully!")
    else:
        st.warning("No record found with that ID.")

# ======================================================
# 8. MODULE: DELETE RECORD
# ======================================================
elif st.session_state.page == "Delete":
    st.title("🗑️ Purge Legal Log Entry")
    del_id = st.number_input("Enter Record ID to Permanently Delete", min_value=1, step=1)
    
    cursor.execute("SELECT * FROM collaboration_records WHERE id=?", (del_id,))
    target = cursor.fetchone()

    if target:
        st.error(f"WARNING: You are about to delete record: **{target[1]}**")
        if st.button("❌ Confirm Permanent Deletion", type="primary"):
            cursor.execute("DELETE FROM collaboration_records WHERE id=?", (del_id,))
            conn.commit()
            st.success("Record purged from database cluster.")
            st.rerun()
    else:
        st.info("Please enter a valid Record ID to proceed.")

# Close connection on exit
conn.close()