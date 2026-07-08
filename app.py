import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import hashlib

# ======================================================
# 1. DATABASE & AUTH FUNCTIONS
# ======================================================
conn = sqlite3.connect("mou_moa_pro.db", check_same_thread=False)
cursor = conn.cursor()

# Create Tables
cursor.execute("""CREATE TABLE IF NOT EXISTS users 
               (username TEXT PRIMARY KEY, password TEXT, email TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS records 
               (id INTEGER PRIMARY KEY, title TEXT, partner TEXT, country TEXT, 
                category TEXT, duration TEXT, status TEXT)""")
conn.commit()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# ======================================================
# 2. APP CONFIG & STYLING
# ======================================================
st.set_page_config(page_title="UiTM MoU/MoA System", layout="wide", page_icon="🎓")

# Custom CSS for the Light SaaS Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #F8FAFC !important; }

    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0; }
    
    /* Card Styling */
    .metric-card {
        background: white; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); text-align: left;
    }
    .metric-val { font-size: 24px; font-weight: 700; color: #1E293B; margin: 0; }
    .metric-label { color: #64748B; font-size: 12px; font-weight: 600; text-transform: uppercase; margin-bottom: 5px; }

    /* Badges */
    .badge { padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; }
    .badge-active { background: #DCFCE7; color: #166534; }
    .badge-expired { background: #FEE2E2; color: #991B1B; }
    .badge-mou { background: #E0E7FF; color: #3730A3; }
    .badge-moa { background: #FFEDD5; color: #9A3412; }

    /* Buttons */
    .stButton>button { border-radius: 8px; font-weight: 500; }
    
    /* Remove default padding */
    .block-container { padding-top: 2rem !important; }
</style>
""", unsafe_allow_html=True)

# ======================================================
# 3. AUTHENTICATION UI
# ======================================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/UiTM_Logo.png/640px-UiTM_Logo.png", width=120)
        st.markdown("## Collaboration Record Management")
        
        tab1, tab2, tab3 = st.tabs(["🔐 Login", "📝 Register", "🔄 Reset"])
        
        with tab1:
            user = st.text_input("Username", key="l_user")
            pw = st.text_input("Password", type="password", key="l_pw")
            if st.button("Access Dashboard", use_container_width=True):
                cursor.execute("SELECT password FROM users WHERE username=?", (user,))
                data = cursor.fetchone()
                if data and check_hashes(pw, data[0]):
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        with tab2:
            new_user = st.text_input("Choose Username")
            new_email = st.text_input("Email Address")
            new_pw = st.text_input("Choose Password", type="password")
            if st.button("Create Account", use_container_width=True):
                try:
                    cursor.execute("INSERT INTO users VALUES (?,?,?)", (new_user, make_hashes(new_pw), new_email))
                    conn.commit()
                    st.success("Account Created! Please Login.")
                except:
                    st.error("Username already exists.")

        with tab3:
            reset_user = st.text_input("Username", key="r_user")
            reset_pw = st.text_input("New Password", type="password")
            if st.button("Reset Password", use_container_width=True):
                cursor.execute("UPDATE users SET password=? WHERE username=?", (make_hashes(reset_pw), reset_user))
                conn.commit()
                st.success("Password Updated!")

    st.stop()

# ======================================================
# 4. MAIN SYSTEM UI (LOGGED IN)
# ======================================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/UiTM_Logo.png/640px-UiTM_Logo.png", width=100)
    st.markdown("### MoU/MoA <br><span style='font-size:12px; color:gray;'>Record Management System</span>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation
    menu = ["🏠 Dashboard", "📂 View All Records", "➕ Add New Record", "✏️ Update Record", "🗑️ Delete Record"]
    choice = st.radio("MAIN MENU", menu, label_visibility="collapsed")
    
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown(f"👤 **{st.session_state.user}**")
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # Sidebar Illustration
    st.markdown("""
    <div style="background: #F1F5F9; padding: 15px; border-radius: 12px; margin-top: 50px; text-align:center;">
        <img src="https://cdn-icons-png.flaticon.com/512/3126/3126589.png" width="60">
        <p style="font-weight:bold; font-size:13px; margin-top:10px;">Strategic Partnerships</p>
        <p style="font-size:10px; color:gray;">Building global impact together.</p>
    </div>
    """, unsafe_allow_html=True)

# Helper to load data
def get_data():
    return pd.read_sql("SELECT * FROM records", conn)

# ======================================================
# 5. MODULES
# ======================================================

# --- DASHBOARD ---
if "Dashboard" in choice:
    df = get_data()
    
    # Header
    h1, h2 = st.columns([3, 1])
    with h1:
        st.markdown(f"## Good Afternoon, {st.session_state.user}! 👋")
        st.markdown("<p style='color:gray;'>Welcome back to MoU/MoA Management Console</p>", unsafe_allow_html=True)
    with h2:
        st.markdown(f"<div style='text-align:right; padding:10px; background:white; border-radius:10px; border:1px solid #EEE;'><b>{datetime.now().strftime('%A')}</b><br><span style='color:gray;'>{datetime.now().strftime('%d %B %Y')}</span></div>", unsafe_allow_html=True)

    # Metric Row
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f'<div class="metric-card"><p class="metric-label">Total Agreements</p><p class="metric-val">{len(df)}</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-card"><p class="metric-label">Countries</p><p class="metric-val">{df["country"].nunique() if not df.empty else 0}</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-card"><p class="metric-label">Categories</p><p class="metric-val">2</p></div>', unsafe_allow_html=True)
    with m4: st.markdown(f'<div class="metric-card"><p class="metric-label">Active</p><p class="metric-val">{len(df[df["status"]=="Active"]) if not df.empty else 0}</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Chart Row
    c1, c2 = st.columns([3, 2])
    if not df.empty:
        with c1:
            st.markdown("#### Agreements by Country")
            fig = px.bar(df['country'].value_counts().reset_index(), x='country', y='count', color='country', color_discrete_sequence=px.colors.qualitative.Vivid)
            fig.update_layout(height=300, margin=dict(t=0,b=0,l=0,r=0), showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Category Split")
            fig2 = go.Figure(data=[go.Pie(labels=df['category'].unique(), values=df['category'].value_counts(), hole=.6, marker=dict(colors=['#8B5CF6', '#F59E0B']))])
            fig2.update_layout(height=300, margin=dict(t=0,b=0,l=0,r=0))
            st.plotly_chart(fig2, use_container_width=True)
    
    # Table
    st.markdown("#### Recent Records")
    if not df.empty:
        # Converting to HTML for badges
        html = "<table style='width:100%; border-collapse: collapse;'> <tr style='color:gray; border-bottom:1px solid #EEE;'><th>ID</th><th>Title</th><th>Partner</th><th>Category</th><th>Status</th></tr>"
        for _, r in df.head(5).iterrows():
            st_cls = "badge-active" if r['status'] == "Active" else "badge-expired"
            ct_cls = "badge-mou" if r['category'] == "MoU" else "badge-moa"
            html += f"<tr style='border-bottom:1px solid #F8FAFC;'><td>{r['id']}</td><td><b>{r['title']}</b></td><td>{r['partner']}</td><td><span class='badge {ct_cls}'>{r['category']}</span></td><td><span class='badge {st_cls}'>{r['status']}</span></td></tr>"
        st.markdown(html + "</table>", unsafe_allow_html=True)
    else:
        st.info("No records found. Use the 'Add' menu to insert data.")

# --- VIEW RECORDS ---
elif "View" in choice:
    st.title("📂 Repository View")
    df = get_data()
    st.dataframe(df, use_container_width=True, hide_index=True)

# --- ADD RECORD ---
elif "Add" in choice:
    st.title("➕ Add New Entry")
    with st.form("add_form"):
        col1, col2 = st.columns(2)
        with col1:
            rid = st.number_input("Record ID", step=1)
            rtitle = st.text_input("Agreement Title")
            rpartner = st.text_input("Partner Institution")
        with col2:
            rcountry = st.text_input("Country")
            rcat = st.selectbox("Category", ["MoU", "MoA"])
            rdur = st.text_input("Duration (e.g. 2024-2027)")
        rstatus = st.selectbox("Status", ["Active", "Expired"])
        
        if st.form_submit_button("Save Record"):
            try:
                cursor.execute("INSERT INTO records VALUES (?,?,?,?,?,?,?)", (rid, rtitle, rpartner, rcountry, rcat, rdur, rstatus))
                conn.commit()
                st.success("Record Saved!")
            except:
                st.error("ID already exists.")

# --- UPDATE RECORD ---
elif "Update" in choice:
    st.title("✏️ Update Entry")
    search_id = st.number_input("Enter Record ID to Modify", step=1)
    cursor.execute("SELECT * FROM records WHERE id=?", (search_id,))
    row = cursor.fetchone()
    
    if row:
        with st.form("up_form"):
            new_title = st.text_input("Title", value=row[1])
            new_partner = st.text_input("Partner", value=row[2])
            new_status = st.selectbox("Status", ["Active", "Expired"], index=0 if row[6]=="Active" else 1)
            if st.form_submit_button("Commit Changes"):
                cursor.execute("UPDATE records SET title=?, partner=?, status=? WHERE id=?", (new_title, new_partner, new_status, search_id))
                conn.commit()
                st.success("Updated!")
    else:
        st.warning("ID not found.")

# --- DELETE RECORD ---
elif "Delete" in choice:
    st.title("🗑️ Delete Entry")
    del_id = st.number_input("Enter Record ID to Delete", step=1)
    if st.button("Delete Permanently", type="primary"):
        cursor.execute("DELETE FROM records WHERE id=?", (del_id,))
        conn.commit()
        st.success("Record removed.")