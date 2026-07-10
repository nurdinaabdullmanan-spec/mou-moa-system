import plotly.express as px
import streamlit as st
import sqlite3
import pandas as pd
import base64
import os
from datetime import datetime

# ======================================================
# KONFIGURASI HALAMAN (PAGE CONFIG)
# ======================================================
st.set_page_config(
    page_title="Sistem Pengurusan Rekod Kolaborasi MoU/MoA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# SAMBUNGAN PANGKALAN DATA (DATABASE CONNECTION)
# ======================================================
conn = sqlite3.connect("mou_moa_db.db", check_same_thread=False)
cursor = conn.cursor()

# CIPTA JADUAL JIKA BELUM WUJUD
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
# REKA BENTUK UI GRED TINGGI (GRID GEOMETRI & GLASSMORPHISM)
# ======================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Quicksand:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Quicksand', sans-serif;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Poppins', sans-serif !important;
        letter-spacing: -0.5px;
    }}
    
    /* LATAR BELAKANG GEOMETRI DENGAN GRID TITIK KORPORAT */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #f5f3fa !important;
        background-image: 
            radial-gradient(rgba(124, 58, 237, 0.08) 2px, transparent 2px), 
            radial-gradient(rgba(16, 185, 129, 0.06) 2px, transparent 2px),
            linear-gradient(135deg, #f3f0fa 0%, #eef2ff 100%) !important;
        background-size: 40px 40px, 30px 30px, 100% 100%;
        background-position: 0 0, 20px 20px, 0 0;
        background-attachment: fixed;
        color: #1e293b !important;
    }}

    /* Sembunyikan Menu Lalai */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* MENU NAVIGASI KIRI (SIDEBAR) - KESAN FROSTED GLASS */
    section[data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.55) !important;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-right: 1px solid rgba(255, 255, 255, 0.7) !important;
    }}
    
    div[role="radiogroup"] label input[type="radio"],
    div[role="radiogroup"] label > div:first-child {{
        display: none !important;
    }}

    div[role="radiogroup"] label {{
        display: flex !important;
        align-items: center !important;
        padding: 14px 20px !important;
        margin-bottom: 8px !important;
        border-radius: 14px !important;
        background: transparent !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        border: 1px solid transparent !important;
    }}

    div[role="radiogroup"] label p {{
        color: #475569 !important; 
        font-size: 15px !important;
        font-weight: 600 !important;
        margin-left: 0px !important;
        font-family: 'Poppins', sans-serif !important;
    }}

    div[role="radiogroup"] label:hover {{
        background: rgba(255, 255, 255, 0.95) !important;
        transform: translateX(6px);
        box-shadow: 0 8px 20px rgba(124, 58, 237, 0.05);
    }}

    div[role="radiogroup"] label[data-selected="true"] {{
        background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important; 
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.35) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }}

    div[role="radiogroup"] label[data-selected="true"] p {{
        color: #ffffff !important; 
        font-weight: 700 !important;
    }}

    /* KAD METRIK - FLOATING GLASS EFFECT */
    .metric-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 35px; }}
    .metric-card {{
        background: rgba(255, 255, 255, 0.75); 
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 24px; 
        border-radius: 22px;
        border: 1px solid rgba(255, 255, 255, 0.9); 
        display: flex; align-items: center; gap: 18px;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.03);
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 45px rgba(124, 58, 237, 0.15);
    }}
    .metric-icon-box {{
        width: 60px; height: 60px; border-radius: 16px;
        display: flex; justify-content: center; align-items: center; font-size: 28px;
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);
    }}
    
    .metric-info h3 {{ margin: 0; font-size: 28px; color: #0f172a; font-weight: 800; line-height: 1.2; }}
    .metric-info p {{ margin: 0; font-size: 13px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }}
    
    /* KAD KANDUNGAN UTAMA (GLASS CARD) */
    .content-card {{
        background: rgba(255, 255, 255, 0.7) !important; 
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px; padding: 32px; 
        border: 1px solid rgba(255, 255, 255, 0.9);
        box-shadow: 0 15px 40px rgba(31, 38, 135, 0.03);
        margin-bottom: 24px;
        transition: all 0.3s ease;
    }}
    .content-card:hover {{
        box-shadow: 0 20px 50px rgba(31, 38, 135, 0.06);
    }}

    /* BUTANG UTAMA - PILL GRADIENT */
    .stButton > button, 
    button[kind="primary"], 
    button[kind="secondary"] {{
        border-radius: 50px !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        padding: 12px 30px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.25) !important;
    }}

    .stButton > button:hover, 
    button[kind="primary"]:hover, 
    button[kind="secondary"]:hover {{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 30px rgba(124, 58, 237, 0.4) !important;
        color: #ffffff !important;
    }}

    /* ISI BORANG DAN INPUT */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        border-radius: 14px !important; 
        border: 2px solid #e2e8f0 !important;
        background-color: rgba(255, 255, 255, 0.95) !important; 
        color: #1e293b !important; 
        padding: 12px 18px !important;
        font-family: 'Quicksand', sans-serif !important;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.15) !important;
    }}
    
    /* JADUAL REKOD */
    .table-container {{
        width: 100%; overflow-x: auto; border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.9); margin-top: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.02);
    }}
    .styled-table {{
        width: 100%; border-collapse: collapse; margin: 0;
        font-size: 14px; font-family: 'Quicksand', sans-serif; 
        background-color: rgba(255,255,255,0.9);
    }}
    .styled-table thead tr {{
        background: linear-gradient(90deg, #f8fafc 0%, #f1f5f9 100%); 
        color: #1e293b; text-align: left;
    }}
    .styled-table th {{ 
        padding: 18px 24px; font-family: 'Poppins', sans-serif; 
        font-weight: 600; border-bottom: 2px solid #cbd5e1; white-space: nowrap; 
    }}
    .styled-table td {{ 
        padding: 16px 24px; border-bottom: 1px solid #f1f5f9; color: #475569; font-weight: 600; 
    }}
    .styled-table tbody tr {{ transition: background-color 0.2s ease; }}
    .styled-table tbody tr:hover {{ background-color: #f5f3fa; cursor: pointer; }}

    /* LOGO BLENDING */
    .uitm-logo {{
        mix-blend-mode: multiply;
        filter: drop-shadow(0px 8px 16px rgba(124, 58, 237, 0.15));
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .uitm-logo:hover {{
        transform: scale(1.05) rotate(1deg);
    }}
</style>

<!-- BEBOLA CAHAYA TERAPUNG DI LATAR BELAKANG (WOW FACTOR) -->
<div style="position: fixed; top: -10%; left: -10%; width: 45vw; height: 45vw; background: radial-gradient(circle, rgba(124, 58, 237, 0.14) 0%, rgba(124, 58, 237, 0) 70%); border-radius: 50%; z-index: -1; pointer-events: none; filter: blur(100px);"></div>
<div style="position: fixed; bottom: -10%; right: -10%; width: 50vw; height: 50vw; background: radial-gradient(circle, rgba(16, 185, 129, 0.11) 0%, rgba(16, 185, 129, 0) 70%); border-radius: 50%; z-index: -1; pointer-events: none; filter: blur(120px);"></div>
<div style="position: fixed; top: 35%; right: 10%; width: 35vw; height: 35vw; background: radial-gradient(circle, rgba(236, 72, 153, 0.07) 0%, rgba(236, 72, 153, 0) 70%); border-radius: 50%; z-index: -1; pointer-events: none; filter: blur(110px);"></div>
""", unsafe_allow_html=True)

# ======================================================
# KONTROLLER NAVIGASI (SESSION STATE)
# ======================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Papan Pemuka"

def switch_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ======================================================
# GERBANG MASUK (LOGIN / DAFTAR / RESET) - DIBAHASA MELAYUKAN
# ======================================================
if not st.session_state.logged_in:
    spacer_left, center_col, spacer_right = st.columns([1, 1.5, 1])
    
    with center_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; padding: 16px 0;">
            <img src="{UITM_LOGO_SRC}" class="uitm-logo" alt="UiTM Logo" style="width: 280px;">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align:center; width:100%; margin-bottom: 30px;'>
            <h2 style='color:#0f172a !important; margin-bottom: 5px; font-weight: 800; font-size: 32px !important;'>
                Sistem Pengurusan Rekod
            </h2>
            <p style='color: #64748b; font-size: 15px; margin-top: 0; font-weight: 700; letter-spacing: 1px;'>UiTM KAMPUS PERMATANG PAUH</p>
        </div>
        """, unsafe_allow_html=True)
        
        auth = st.selectbox("Akses Autentikasi Selamat", ["Log Masuk", "Daftar Akaun Baru", "Set Semula Kata Laluan"])

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        if auth == "Log Masuk":
            st.markdown("<h3 style='margin-bottom: 25px; font-size: 22px !important; color: #5b21b6 !important;'>🔑 Log Masuk Portal</h3>", unsafe_allow_html=True)
            username = st.text_input("Nama Pengguna Korporat")
            password = st.text_input("Kata Laluan Akaun", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sahkan Sesi Masuk", use_container_width=True):
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
                user = cursor.fetchone()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Sesi berjaya disahkan. Membuka sistem...")
                    st.rerun()
                else:
                    st.error("Ralat: Kunci autentikasi pangkalan data tidak sah.")

        elif auth == "Daftar Akaun Baru":
            st.markdown("<h3 style='margin-bottom: 25px; font-size: 22px !important; color: #5b21b6 !important;'>📝 Daftar Akaun Kakitangan</h3>", unsafe_allow_html=True)
            new_username = st.text_input("Nama Pengguna Pilihan")
            new_email = st.text_input("Alamat E-mel Rasmi Staf")
            new_password = st.text_input("Kata Laluan Selamat", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Daftar Maklumat Akaun", use_container_width=True):
                cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (new_username, new_email, new_password))
                conn.commit()
                st.success("Akaun berjaya didaftarkan ke dalam pangkalan data.")

        elif auth == "Set Semula Kata Laluan":
            st.markdown("<h3 style='margin-bottom: 25px; font-size: 22px !important; color: #5b21b6 !important;'>🔄 Set Semula Kredensial</h3>", unsafe_allow_html=True)
            email = st.text_input("Profil E-mel Terdaftar")
            new_password = st.text_input("Kata Laluan Baharu", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Kemaskini Kata Laluan", use_container_width=True):
                cursor.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
                conn.commit()
                st.success("Kata laluan baharu berjaya dikemaskini.")
                
        st.markdown('</div>', unsafe_allow_html=True)


# ======================================================
# RUANG KERJA UTAMA - DIBAHASA MELAYUKAN
# ======================================================
else:
    current_date = datetime.now().strftime("%d %B %Y")

    # PAPARAN MENU SISI (SIDEBAR UI)
    st.sidebar.markdown(f"""
        <div style="text-align:center; margin-bottom: 30px; padding-top: 10px;">
            <img src="{UITM_LOGO_SRC}" class="uitm-logo" style="width:140px; margin-bottom:15px;" alt="UiTM Logo">
            <h3 style="color:#0f172a; font-size:18px; font-weight:800; margin:0;">UiTM Permatang Pauh</h3>
            <p style="color:#64748b; font-size:12px; margin-top:4px; font-weight:700; line-height:1.4;">Sistem Pengurusan Rekod<br>Kolaborasi MoU/MoA</p>
        </div>
        """, unsafe_allow_html=True)

    menu_options = [
        "🏠 Papan Pemuka", 
        "📂 Lihat Semua Rekod", 
        "➕ Tambah Rekod Baharu", 
        "📝 Kemaskini Rekod", 
        "🗑️ Padam Rekod"
    ]
    
    clean_menu_options = [m.split(" ", 1)[1] for m in menu_options]
    
    current_index = 0
    if st.session_state.current_page in clean_menu_options:
        current_index = clean_menu_options.index(st.session_state.current_page)
    elif st.session_state.current_page == "Papan Pemuka":
         current_index = 0
            
    selected_menu = st.sidebar.radio(
        "NAVIGASI",
        menu_options,
        index=current_index,
        label_visibility="collapsed"
    )
    
    selected_page_name = selected_menu.split(" ", 1)[1]
    if selected_page_name != st.session_state.current_page:
        st.session_state.current_page = selected_page_name
        st.rerun()

    st.sidebar.markdown("<hr style='margin: 30px 0 20px 0; border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(0,0,0,0.1), transparent);'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='font-size:11px; color:#94a3b8; font-weight:700; text-transform:uppercase; letter-spacing: 1px;'>Sesi Aktif</p>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <div style='background: rgba(124, 58, 237, 0.05); padding: 12px; border-radius: 12px; margin-bottom: 20px; border: 1px solid rgba(124, 58, 237, 0.1);'>
        <p style='color:#334155; font-size:15px; margin:0; font-family: "Poppins", sans-serif;'>👤 <b>{st.session_state.username}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Log Keluar Sesi", key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # Baca Aliran Jadual Teras (Dipaparkan dalam Bahasa Melayu)
    cursor.execute("SELECT * FROM collaboration_data ORDER BY id ASC")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Tajuk Perjanjian", "Tempoh", "Jabatan/Fakulti", "Rakan Kolaborasi", "Negara", "Kategori"])

    # ------------------------------------------------------
    # MODUL: PAPAN PEMUKA (DASHBOARD)
    # ------------------------------------------------------
    if st.session_state.current_page == "Papan Pemuka":
        col_greet, col_date = st.columns([3, 1])
        with col_greet:
            st.markdown(f"""
            <h1 style='color:#0f172a; margin-bottom: 8px; font-weight:800; font-size: 34px;'>Selamat Petang, {st.session_state.username}! 👋</h1>
            <p style='color:#64748b; font-size:16px; margin-top:0; font-weight:600;'>Berikut adalah ringkasan analisis data kolaborasi MoU/MoA terkini.</p>
            """, unsafe_allow_html=True)
        with col_date:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.85); backdrop-filter:blur(10px); padding:12px 20px; border-radius:16px; border:1px solid rgba(255,255,255,0.9); display:flex; align-items:center; gap:15px; float:right; box-shadow: 0 8px 20px rgba(0,0,0,0.03);'>
                <div style='background: #f3e8ff; width: 40px; height: 40px; border-radius: 10px; display: flex; justify-content: center; align-items: center; font-size:20px;'>📅</div>
                <div>
                    <div style='font-size:11px; color:#64748b; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;'>Tarikh Hari Ini</div>
                    <div style='font-size:14px; font-weight:700; color:#1e293b;'>{current_date}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        valid_categories = ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"]
        df_filtered = df[df["Kategori"].isin(valid_categories)]
        
        total_records = len(df)
        total_country = df["Negara"].nunique() if total_records > 0 else 0
        total_category = 2 
        active_agreements = len(df)

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card" style="border-bottom: 4px solid #8b5cf6;">
                <div class="metric-icon-box" style="background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%); color:#8b5cf6;">📄</div>
                <div class="metric-info">
                    <h3>{total_records}</h3>
                    <p style="color: #6d28d9;">Jumlah Dokumen</p>
                </div>
            </div>
            <div class="metric-card" style="border-bottom: 4px solid #10b981;">
                <div class="metric-icon-box" style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); color:#10b981;">🌐</div>
                <div class="metric-info">
                    <h3>{total_country}</h3>
                    <p style="color: #059669;">Negara Terlibat</p>
                </div>
            </div>
            <div class="metric-card" style="border-bottom: 4px solid #f59e0b;">
                <div class="metric-icon-box" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); color:#f59e0b;">🤝</div>
                <div class="metric-info">
                    <h3>{total_category}</h3>
                    <p style="color: #d97706;">Kategori Teras</p>
                </div>
            </div>
            <div class="metric-card" style="border-bottom: 4px solid #ef4444;">
                <div class="metric-icon-box" style="background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); color:#ef4444;">📂</div>
                <div class="metric-info">
                    <h3>{active_agreements}</h3>
                    <p style="color: #dc2626;">Rekod Aktif</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 20px; color:#0f172a; margin-bottom: 20px;'>🌍 Perjanjian Mengikut Negara</h3>", unsafe_allow_html=True)
            if total_records > 0:
                country_chart = df["Negara"].value_counts().reset_index()
                country_chart.columns = ["Negara", "Jumlah"]
                fig1 = px.bar(country_chart, x="Negara", y="Jumlah", text_auto=True, 
                              color="Negara", color_discrete_sequence=px.colors.qualitative.Pastel)
                fig1.update_layout(showlegend=False, margin=dict(t=10, b=10, l=0, r=0), height=320, 
                                   plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                                   font=dict(family="Quicksand"))
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("Tiada data negara untuk dipetakan.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_chart2:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 20px; color:#0f172a; margin-bottom: 20px;'>📊 Perjanjian Mengikut Kategori</h3>", unsafe_allow_html=True)
            
            if total_records > 0:
                cat_data = df["Kategori"].value_counts().reindex(
                    ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"], 
                    fill_value=0
                ).reset_index()
                cat_data.columns = ["Kategori", "Jumlah"]
                
                fig2 = px.pie(cat_data, values="Jumlah", names="Kategori", hole=0.6, 
                              color_discrete_sequence=["#8b5cf6", "#10b981"]) 
                
                fig2.update_layout(margin=dict(t=10, b=10, l=0, r=0), height=320,
                                   paper_bgcolor="rgba(0,0,0,0)", font=dict(family="Quicksand"),
                                   legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Tiada data kategori untuk dipaparkan.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 20px; color:#0f172a; margin-bottom: 20px;'>⚡ Rekod Baharu Ditambah</h3>", unsafe_allow_html=True)
        
        if len(df) > 0:
            st.markdown(f"""
            <div class="table-container">
                {df.tail(5).to_html(index=False, classes="styled-table", escape=False)}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Tiada rekod terkini untuk dipaparkan.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODUL: LIHAT REKOD (VIEW DATA)
    # ------------------------------------------------------
    elif st.session_state.current_page == "Lihat Semua Rekod":
        st.markdown("<h1 style='color:#0f172a; margin-bottom: 20px;'>📂 Repositori Data Utama</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        search = st.text_input("🔍 Cari Rekod (Masukkan Tajuk, Rakan Kolaborasi atau Negara)", placeholder="Taip di sini untuk mencari...")

        if search:
            sql = "SELECT * FROM collaboration_data WHERE title LIKE ? OR partner LIKE ? OR country LIKE ?"
            cursor.execute(sql, (f"%{search}%", f"%{search}%", f"%{search}%"))
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=["ID", "Tajuk Perjanjian", "Tempoh", "Jabatan/Fakulti", "Rakan Kolaborasi", "Negara", "Kategori"])

        if len(df) > 0:
            html_table = df.to_html(index=False, classes="styled-table", escape=False)
            st.markdown(f'<div class="table-container">{html_table}</div>', unsafe_allow_html=True)
        else:
            st.info("Tiada data ditemui dalam repositori yang sepadan dengan carian anda.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_spacer, col_btn_cancel = st.columns([8, 2])
        with col_btn_cancel:
            if st.button("← Papan Pemuka", key="back_view", use_container_width=True):
                switch_page("Papan Pemuka")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODUL: TAMBAH REKOD (ADD DATA)
    # ------------------------------------------------------
    elif st.session_state.current_page == "Tambah Rekod Baharu":
        st.markdown("<h1 style='color:#0f172a; margin-bottom: 20px;'>➕ Daftar Rekod Kolaborasi Baharu</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        st.markdown("<h4 style='color:#5b21b6; margin-bottom: 15px;'>📄 Butiran Dokumen Perjanjian</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            id_in = st.number_input("Tetapkan ID Rekod", min_value=1, step=1, format="%d")
            category = st.selectbox("Kategori Teras Perjanjian", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"])
        with col2:
            title = st.text_input("Tajuk Perjanjian")
            duration = st.text_input("Tempoh Aktif (Cth: 3 Tahun)")

        st.markdown("<hr style='border: 1px dashed rgba(0,0,0,0.1); margin:25px 0;'>", unsafe_allow_html=True)

        st.markdown("<h4 style='color:#5b21b6; margin-bottom: 15px;'>🤝 Maklumat Rakan Kolaborasi</h4>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            department = st.text_input("Jabatan / Fakulti Pelaksana")
            country = st.text_input("Lokasi Negara")
        with col4:
            partner = st.text_input("Institusi Rakan Luar")

        st.markdown("<hr style='border: 1px solid rgba(0,0,0,0.05); margin:30px 0 20px 0;'>", unsafe_allow_html=True)

        col_btn_save, col_spacer, col_btn_cancel = st.columns([2.5, 5, 2.5])
        
        with col_btn_save:
            if st.button("💾 Simpan Rekod Selamat", use_container_width=True):
                cursor.execute("INSERT INTO collaboration_data (id, title, duration, department, partner, country, category) VALUES (?,?,?,?,?,?,?)",
                               (int(id_in), title, duration, department, partner, country, category))
                conn.commit()
                st.success("Rekod perundangan baharu berjaya disimpan ke dalam pangkalan data.")
                switch_page("Lihat Semua Rekod")
                
        with col_btn_cancel:
            if st.button("❌ Batal & Kembali", key="back_add", use_container_width=True):
                switch_page("Papan Pemuka")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODUL: KEMASKINI REKOD (UPDATE DATA)
    # ------------------------------------------------------
    elif st.session_state.current_page == "Kemaskini Rekod":
        st.markdown("<h1 style='color:#0f172a; margin-bottom: 20px;'>📝 Kemaskini Rekod Sedia Ada</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        uid = st.number_input("ID Rekod Sasaran untuk Dikemaskini", min_value=1, step=1, format="%d")
        cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(uid),))
        result = cursor.fetchone()

        if result:
            st.markdown("<hr style='border: 1px dashed rgba(0,0,0,0.1); margin:25px 0;'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Pernyataan Tajuk Perjanjian", result[1])
                duration = st.text_input("Tempoh Jangka Hayat Aktif", result[2])
                department = st.text_input("Jabatan Pelaksana", result[3])
            with col2:
                partner = st.text_input("Institusi Rakan Luar", result[4])
                country = st.text_input("Lokasi Negara", result[5])
                category = st.selectbox("Penetapan Kategori Teras Perjanjian", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"], 
                                        index=["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"].index(result[6]) if result[6] in ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"] else 0)

            st.markdown("<br>", unsafe_allow_html=True)
            
            col_btn_update, col_spacer, col_btn_cancel = st.columns([2.5, 5, 2.5])
            
            with col_btn_update:
                if st.button("🔄 Kemaskini Perubahan", use_container_width=True):
                    cursor.execute("UPDATE collaboration_data SET title=?, duration=?, department=?, partner=?, country=?, category=? WHERE id=?",
                                   (title, duration, department, partner, country, category, int(uid)))
                    conn.commit()
                    st.success("Sesi rekod berjaya dikemaskini dan diselaraskan.")
                    switch_page("Lihat Semua Rekod")
                    
            with col_btn_cancel:
                if st.button("❌ Batal & Kembali", key="back_update", use_container_width=True):
                    switch_page("Papan Pemuka")
                
        else:
            st.warning("Makluman: ID Sasaran tidak wujud dalam sistem pangkalan data. Sila sahkan semula.")
            st.markdown("<br>", unsafe_allow_html=True)
            col_spacer, col_btn_cancel = st.columns([8, 2])
            with col_btn_cancel:
                if st.button("← Kembali", key="back_update_fail", use_container_width=True):
                    switch_page("Papan Pemuka")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODUL: PADAM REKOD (DELETE DATA)
    # ------------------------------------------------------
    elif st.session_state.current_page == "Padam Rekod":
        st.markdown("<h1 style='color:#0f172a; margin-bottom: 20px;'>🗑️ Padam Rekod Kolaborasi</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        del_id = st.number_input("ID Rekod Sasaran untuk Dipadam", min_value=1, step=1, format="%d")
        
        st.markdown("""
        <div style='background: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; border-radius: 8px; margin-top: 15px;'>
            <p style='color: #991b1b; margin: 0; font-weight: 700;'>💣 Amaran Kritikal: Tindakan pemadaman rekod adalah kekal dan tidak boleh dikembalikan.</p>
        </div>
        """, unsafe_allow_html=True)

        @st.dialog("⚠️ Sahkan Pemadaman Kekal")
        def confirm_delete_dialog(record_id):
            st.warning(f"Adakah anda pasti mahu memadamkan Rekod ID {record_id} secara kekal?")
            st.write("Tindakan ini akan memadamkan data serta-merta daripada pangkalan data.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_yes, col_spacer_dialog, col_cancel = st.columns([4, 2, 4])
            
            with col_yes:
                if st.button("Ya, Padam Sekarang", use_container_width=True):
                    cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(record_id),))
                    if cursor.fetchone():
                        cursor.execute("DELETE FROM collaboration_data WHERE id=?", (int(record_id),))
                        conn.commit()
                        st.success(f"Rekod ID {record_id} berjaya dipadamkan.")
                        switch_page("Lihat Semua Rekod")
                    else:
                        st.error("Kegagalan Pemadaman: ID Sasaran tidak ditemui.")
            
            with col_cancel:
                if st.button("Batal Operasi", key="dialog_cancel", use_container_width=True):
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_btn_del, col_spacer, col_btn_cancel = st.columns([3, 4, 3])
        
        with col_btn_del:
            if st.button("🚨 Sahkan & Padam Rekod", use_container_width=True):
                confirm_delete_dialog(del_id)
                
        with col_btn_cancel:
            if st.button("❌ Batal & Kembali", key="back_delete", use_container_width=True):
                switch_page("Papan Pemuka")
            
        st.markdown('</div>', unsafe_allow_html=True)