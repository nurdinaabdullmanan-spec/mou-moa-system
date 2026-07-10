import plotly.express as px
import streamlit as st
import sqlite3
import pandas as pd
import base64
import os
from datetime import datetime

st.set_page_config(
    page_title="Sistem Pengurusan Rekod Kolaborasi MoU/MoA",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

conn = sqlite3.connect("mou_moa_db.db", check_same_thread=False)
cursor = conn.cursor()

# Cipta jadual sistem
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS collaboration_data (
    id INTEGER PRIMARY KEY,
    title TEXT,
    duration TEXT,
    department TEXT,
    partner TEXT,
    country TEXT,
    category TEXT
)
""")
conn.commit()

# Ini bagi mengelakkan paparan kosong yang bosan pada kali pertama sistem dibuka
cursor.execute("SELECT COUNT(*) FROM users")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", ("admin", "staf@uitm.edu.my", "admin"))
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM collaboration_data")
if cursor.fetchone()[0] == 0:
    demo_records = [
        (1, "MoU Kerjasama Penyelidikan Kecerdasan Buatan (AI) Global", "5 Tahun", "Fakulti Sains Komputer & Matematik", "Intel Microelectronics", "Amerika Syarikat", "Memorandum of Understanding (MoU)"),
        (2, "MoA Pembangunan Hab Teknologi Tenaga Hijau", "3 Tahun", "Fakulti Kejuruteraan Kimia", "PETRONAS", "Malaysia", "Agreement for MyRA Purpose"),
        (3, "MoU Program Pertukaran Sarjana & Penyelidik Kanan", "3 Tahun", "Fakulti Pengurusan Perniagaan", "Kyoto University", "Jepun", "Memorandum of Understanding (MoU)"),
        (4, "MoA Pemindahan Teknologi Pintar IoT Pertanian", "2 Tahun", "Fakulti Kejuruteraan Elektrik", "Huawei Technologies Co. Ltd.", "China", "Agreement for MyRA Purpose"),
        (5, "MoU Konsortium Kajian Klinikal & Sains Farmaseutikal", "5 Tahun", "Fakulti Farmasi", "AstraZeneca PLC", "United Kingdom", "Memorandum of Understanding (MoU)")
    ]
    cursor.executemany("INSERT INTO collaboration_data VALUES (?, ?, ?, ?, ?, ?, ?)", demo_records)
    conn.commit()

def get_local_logo_base64(file_path="Logo.png"):
    if os.path.exists(file_path):
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"
    else:
        # Jika fail tempatan tiada, gunakan logo UiTM rasmi daripada pelayan web
        return "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/UiTM_Logo.png/640px-UiTM_Logo.png"

UITM_LOGO_SRC = get_local_logo_base64()

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
    
    /* REKA BENTUK ULTRA-PREMIUM CYBER DARK DENGAN KESAN METALLIC */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #060511 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(124, 58, 237, 0.15) 0px, transparent 50%), 
            radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.12) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(79, 70, 229, 0.08) 0px, transparent 60%),
            linear-gradient(180deg, #060511 0%, #0c0a21 100%) !important;
        background-attachment: fixed;
        color: #f1f5f9 !important;
    }}

    /* Sembunyikan elemen lalai Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* MENU SISI (SIDEBAR) - GLASSMORPHISM BERKILAU */
    section[data-testid="stSidebar"] {{
        background: rgba(10, 8, 28, 0.8) !important;
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }}
    
    div[role="radiogroup"] label input[type="radio"],
    div[role="radiogroup"] label > div:first-child {{
        display: none !important;
    }}

    /* REKA BUTANG MENU SIDEBAR */
    div[role="radiogroup"] label {{
        display: flex !important;
        align-items: center !important;
        padding: 14px 22px !important;
        margin-bottom: 10px !important;
        border-radius: 16px !important;
        background: rgba(255, 255, 255, 0.02) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        cursor: pointer;
        border: 1px solid rgba(255, 255, 255, 0.03) !important;
    }}

    div[role="radiogroup"] label p {{
        color: #94a3b8 !important; 
        font-size: 14px !important;
        font-weight: 600 !important;
        margin-left: 0px !important;
        font-family: 'Poppins', sans-serif !important;
    }}

    div[role="radiogroup"] label:hover {{
        background: rgba(124, 58, 237, 0.1) !important;
        border-color: rgba(124, 58, 237, 0.3) !important;
        transform: translateX(8px);
        box-shadow: 0 5px 15px rgba(124, 58, 237, 0.15);
    }}

    div[role="radiogroup"] label[data-selected="true"] {{
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important; 
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }}

    div[role="radiogroup"] label[data-selected="true"] p {{
        color: #ffffff !important; 
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}

    /* KAD ANALITIK & GRID - METRIK METALLIC */
    .metric-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 35px; }}
    .metric-card {{
        background: rgba(15, 12, 38, 0.7); 
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 24px; 
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08); 
        display: flex; align-items: center; gap: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25);
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.4s ease, box-shadow 0.4s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(124, 58, 237, 0.25);
        border-color: rgba(124, 58, 237, 0.4) !important;
    }}
    .metric-icon-box {{
        width: 65px; height: 65px; border-radius: 18px;
        display: flex; justify-content: center; align-items: center; font-size: 30px;
        box-shadow: inset 0 2px 4px rgba(255,255,255,0.1);
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }}
    
    .metric-info h3 {{ margin: 0; font-size: 32px; color: #ffffff; font-weight: 800; line-height: 1.2; letter-spacing: -1px; }}
    .metric-info p {{ margin: 0; font-size: 12px; color: #94a3b8; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }}
    
    /* KAD KANDUNGAN UTAMA (GLASS CARD DENGAN KILAUAN NEON) */
    .content-card {{
        background: rgba(15, 12, 38, 0.55) !important; 
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 24px; padding: 35px; 
        border: 1px solid rgba(255, 255, 255, 0.06);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        margin-bottom: 25px;
        transition: all 0.4s ease;
    }}
    .content-card:hover {{
        border-color: rgba(124, 58, 237, 0.15);
        box-shadow: 0 25px 60px rgba(124, 58, 237, 0.08);
    }}

    /* BUTANG PREMIUM DENGAN GLOW ANIMASI */
    .stButton > button, 
    button[kind="primary"], 
    button[kind="secondary"] {{
        border-radius: 50px !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.8px;
        padding: 14px 32px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.3) !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}

    .stButton > button:hover, 
    button[kind="primary"]:hover, 
    button[kind="secondary"]:hover {{
        transform: translateY(-4px) scale(1.03);
        box-shadow: 0 15px 35px rgba(124, 58, 237, 0.5) !important;
        border-color: rgba(255,255,255,0.3) !important;
    }}

    /* LOGO DAN ELEMEN GRAFIK GLOWING */
    .uitm-logo {{
        filter: drop-shadow(0px 10px 25px rgba(124, 58, 237, 0.3));
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .uitm-logo:hover {{
        transform: scale(1.06) rotate(1deg);
    }}

    /* GAYA BORANG & RUANG MASUKKAN (INPUT CONTROLS) */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        border-radius: 16px !important; 
        border: 2px solid rgba(255, 255, 255, 0.08) !important;
        background-color: rgba(10, 8, 28, 0.8) !important; 
        color: #ffffff !important; 
        padding: 14px 20px !important;
        font-family: 'Quicksand', sans-serif !important;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: #7c3aed !important;
        box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.2) !important;
        background-color: rgba(10, 8, 28, 0.95) !important;
    }}
    
    /* GAYA JADUAL MAKLUMAT ELEGAN (TABLE) */
    .table-container {{
        width: 100%; overflow-x: auto; border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.08); margin-top: 15px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }}
    .styled-table {{
        width: 100%; border-collapse: collapse; margin: 0;
        font-size: 14px; font-family: 'Quicksand', sans-serif; 
        background-color: rgba(15, 12, 38, 0.6);
    }}
    .styled-table thead tr {{
        background: linear-gradient(90deg, #120e2e 0%, #1a1540 100%); 
        color: #ffffff; text-align: left;
        border-bottom: 2px solid rgba(124, 58, 237, 0.3);
    }}
    .styled-table th {{ 
        padding: 20px 24px; font-family: 'Poppins', sans-serif; 
        font-weight: 700; white-space: nowrap; 
    }}
    .styled-table td {{ 
        padding: 18px 24px; border-bottom: 1px solid rgba(255,255,255,0.04); color: #cbd5e1; font-weight: 600; 
    }}
    .styled-table tbody tr {{ transition: background-color 0.3s ease; }}
    .styled-table tbody tr:hover {{ background-color: rgba(124, 58, 237, 0.1); cursor: pointer; }}

    /* GRADIENT TEXT */
    .glow-text {{
        background: linear-gradient(135deg, #ffffff 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }}
    .gold-text {{
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
</style>

<!-- GLOWING BACKGROUND ORBS (MEMBUATKAN DESIGN WOW DAN DINAMIK) -->
<div style="position: fixed; top: -10%; left: -10%; width: 50vw; height: 50vw; background: radial-gradient(circle, rgba(124, 58, 237, 0.18) 0%, rgba(124, 58, 237, 0) 70%); border-radius: 50%; z-index: -1; pointer-events: none; filter: blur(120px);"></div>
<div style="position: fixed; bottom: -10%; right: -10%; width: 55vw; height: 55vw; background: radial-gradient(circle, rgba(16, 185, 129, 0.14) 0%, rgba(16, 185, 129, 0) 70%); border-radius: 50%; z-index: -1; pointer-events: none; filter: blur(140px);"></div>
<div style="position: fixed; top: 35%; right: 15%; width: 40vw; height: 40vw; background: radial-gradient(circle, rgba(99, 102, 241, 0.12) 0%, rgba(99, 102, 241, 0) 70%); border-radius: 50%; z-index: -1; pointer-events: none; filter: blur(110px);"></div>
""", unsafe_allow_html=True)

# ======================================================
# KONTROLLER NAVIGASI HALAMAN (SESSION STATE)
# ======================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "Papan Pemuka"

def switch_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()

# ======================================================
# GERBANG AUTENTIKASI UTAMA (LOGIN / DAFTAR / RESET)
# ======================================================
if not st.session_state.logged_in:
    spacer_left, center_col, spacer_right = st.columns([1, 1.4, 1])
    
    with center_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <img src="{UITM_LOGO_SRC}" class="uitm-logo" alt="UiTM Logo" style="width: 290px;">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align:center; width:100%; margin-bottom: 35px;'>
            <h1 class='glow-text' style='margin-bottom: 5px; font-size: 34px !important;'>
                SISTEM PENGURUSAN REKOD
            </h1>
            <p class='gold-text' style='font-size: 16px; margin-top: 0; font-weight: 800; letter-spacing: 2px;'>UiTM KAMPUS PERMATANG PAUH</p>
        </div>
        """, unsafe_allow_html=True)
        
        auth = st.selectbox("Akses Autentikasi Pengguna", ["Sesi Log Masuk Portal", "Daftar Akaun Kakitangan Baru", "Tukar Kata Laluan Sedia Ada"])

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        if auth == "Sesi Log Masuk Portal":
            st.markdown("<h3 style='margin-bottom: 25px; font-size: 22px !important; color: #a78bfa !important;'>🔑 Log Masuk Keselamatan</h3>", unsafe_allow_html=True)
            username = st.text_input("Nama Pengguna Rasmi")
            password = st.text_input("Kata Laluan Kunci Masuk", type="password")

            # Paparan pembantu akaun demo eksklusif
            st.markdown("""
            <div style="background: rgba(124, 58, 237, 0.08); border-left: 3px solid #7c3aed; padding: 12px; border-radius: 8px; margin-top: 15px; font-size: 13px;">
                💡 <b>Sesi Percubaan Segera:</b> Gunakan Nama Pengguna: <code style="color:#a78bfa">admin</code> dan Kata Laluan: <code style="color:#a78bfa">admin</code>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Sahkan & Jalankan Sesi", use_container_width=True):
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
                user = cursor.fetchone()
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Sesi disahkan! Membuka pangkalan data utama...")
                    st.rerun()
                else:
                    st.error("Ralat: Kunci keselamatan atau nama pengguna tidak ditemui.")

        elif auth == "Daftar Akaun Kakitangan Baru":
            st.markdown("<h3 style='margin-bottom: 25px; font-size: 22px !important; color: #a78bfa !important;'>📝 Daftar Akaun Staf</h3>", unsafe_allow_html=True)
            new_username = st.text_input("Nama Pengguna Dipilih")
            new_email = st.text_input("E-mel Rasmi UiTM (@uitm.edu.my)")
            new_password = st.text_input("Kata Laluan Selamat", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Hantar Permohonan Akaun", use_container_width=True):
                try:
                    cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (new_username, new_email, new_password))
                    conn.commit()
                    st.success("Selesai! Akaun anda kini telah disimpan di dalam sistem.")
                except sqlite3.IntegrityError:
                    st.error("Ralat: Nama pengguna tersebut sudah berdaftar di dalam pangkalan data.")

        elif auth == "Tukar Kata Laluan Sedia Ada":
            st.markdown("<h3 style='margin-bottom: 25px; font-size: 22px !important; color: #a78bfa !important;'>🔄 Kemaskini Kata Laluan</h3>", unsafe_allow_html=True)
            email = st.text_input("Profil Alamat E-mel Berdaftar")
            new_password = st.text_input("Kata Laluan Baharu Pilihan", type="password")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Tulis Semula Sesi Enkripsi", use_container_width=True):
                cursor.execute("SELECT * FROM users WHERE email=?", (email,))
                if cursor.fetchone():
                    cursor.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
                    conn.commit()
                    st.success("Kata laluan baharu anda telah dikemaskini dan diselaraskan.")
                else:
                    st.error("E-mel tidak ditemui dalam rekod pangkalan data pengguna.")
                
        st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# KONSOL PENGURUSAN UTAMA (WORKSPACE)
# ======================================================
else:
    current_date = datetime.now().strftime("%d %B %Y")

    # SIDEBAR UTAMA - SANGAT WOW
    st.sidebar.markdown(f"""
        <div style="text-align:center; margin-bottom: 30px; padding-top: 15px;">
            <img src="{UITM_LOGO_SRC}" class="uitm-logo" style="width:160px; margin-bottom:15px;" alt="UiTM Logo">
            <h3 style="color:#ffffff; font-size:18px; font-weight:800; margin:0; letter-spacing:-0.5px;">UiTM Permatang Pauh</h3>
            <p style="color:#94a3b8; font-size:11px; margin-top:5px; line-height:1.4; font-weight:600; text-transform: uppercase; letter-spacing: 0.5px;">Sistem Pengurusan Rekod<br>Kolaborasi MoU/MoA</p>
        </div>
        """, unsafe_allow_html=True)

    menu_options = [
        "🏠 Papan Pemuka", 
        "📂 Paparan Rekod Global", 
        "➕ Daftar Rekod Baru", 
        "📝 Kemas Kini Rekod", 
        "🗑️ Pelupusan Rekod"
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

    st.sidebar.markdown("<hr style='margin: 25px 0; border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='font-size:11px; color:#64748b; font-weight:800; text-transform:uppercase; letter-spacing: 1px;'>PENGGUNA AKTIF</p>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <div style='background: rgba(124, 58, 237, 0.1); padding: 14px; border-radius: 16px; margin-bottom: 25px; border: 1px solid rgba(124, 58, 237, 0.2); text-align:center;'>
        <p style='color:#ffffff; font-size:15px; margin:0; font-family: "Poppins", sans-serif; font-weight:700;'>👤 {st.session_state.username}</p>
        <span style="font-size:10px; color:#10b981; font-weight:800; letter-spacing:1px; text-transform:uppercase;">● Atas Talian</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Tamatkan Sesi Serta Merta", key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # Membaca data terkini daripada pangkalan data
    cursor.execute("SELECT * FROM collaboration_data ORDER BY id ASC")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Tajuk Perjanjian", "Tempoh Kuat Kuasa", "Bahagian/Fakulti", "Rakan Kerjasama", "Negara", "Kategori"])

    # ------------------------------------------------------
    # MODUL: PAPAN PEMUKA (EXECUTIVE DASHBOARD) - WOW
    # ------------------------------------------------------
    if st.session_state.current_page == "Papan Pemuka":
        col_greet, col_date = st.columns([2.8, 1.2])
        with col_greet:
            st.markdown(f"""
            <h1 class='glow-text' style='margin-bottom: 5px; font-size:38px;'>Selamat Datang, {st.session_state.username}! 👋</h1>
            <p style='color:#94a3b8; font-size:16px; margin-top:0; font-weight:600;'>Analitik Sesi Pintar: Ringkasan data pengurusan kolaborasi rasmi kampus.</p>
            """, unsafe_allow_html=True)
        with col_date:
            st.markdown(f"""
            <div style='background:rgba(15, 12, 38, 0.6); backdrop-filter:blur(15px); padding:14px 22px; border-radius:20px; border:1px solid rgba(255,255,255,0.08); display:flex; align-items:center; gap:15px; float:right; box-shadow: 0 10px 30px rgba(0,0,0,0.2);'>
                <div style='background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%); width: 45px; height: 45px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size:22px;'>📅</div>
                <div>
                    <div style='font-size:10px; color:#94a3b8; font-weight:700; text-transform:uppercase; letter-spacing:1px;'>Tarikh Semasa</div>
                    <div style='font-size:15px; font-weight:800; color:#ffffff;'>{current_date}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Analisis Ringkasan data
        total_records = len(df)
        total_country = df["Negara"].nunique() if total_records > 0 else 0
        total_category = 2 
        active_agreements = len(df)

        # METRIK GRID YANG WOW & GLOWING
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card" style="border-bottom: 4px solid #7c3aed;">
                <div class="metric-icon-box" style="background: linear-gradient(135deg, #2e1065 0%, #7c3aed 100%); color:#ffffff;">📄</div>
                <div class="metric-info">
                    <h3>{total_records}</h3>
                    <p>Jumlah Dokumen</p>
                </div>
            </div>
            <div class="metric-card" style="border-bottom: 4px solid #10b981;">
                <div class="metric-icon-box" style="background: linear-gradient(135deg, #064e3b 0%, #10b981 100%); color:#ffffff;">🌐</div>
                <div class="metric-info">
                    <h3>{total_country}</h3>
                    <p>Negara Rakan</p>
                </div>
            </div>
            <div class="metric-card" style="border-bottom: 4px solid #f59e0b;">
                <div class="metric-icon-box" style="background: linear-gradient(135deg, #78350f 0%, #f59e0b 100%); color:#ffffff;">🤝</div>
                <div class="metric-info">
                    <h3>{total_category}</h3>
                    <p>Kategori Utama</p>
                </div>
            </div>
            <div class="metric-card" style="border-bottom: 4px solid #ef4444;">
                <div class="metric-icon-box" style="background: linear-gradient(135deg, #7f1d1d 0%, #ef4444 100%); color:#ffffff;">📂</div>
                <div class="metric-info">
                    <h3>{active_agreements}</h3>
                    <p>Rekod Aktif</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 20px; color:#ffffff; margin-bottom: 20px; font-weight:700;'>🌍 Pembahagian Mengikut Negara Rakan</h3>", unsafe_allow_html=True)
            if total_records > 0:
                country_chart = df["Negara"].value_counts().reset_index()
                country_chart.columns = ["Negara", "Jumlah"]
                fig1 = px.bar(country_chart, x="Negara", y="Jumlah", text_auto=True, 
                              color="Negara", color_discrete_sequence=px.colors.qualitative.Pastel)
                fig1.update_layout(
                    showlegend=False, 
                    margin=dict(t=10, b=10, l=0, r=0), 
                    height=320, 
                    plot_bgcolor="rgba(0,0,0,0)", 
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Quicksand", color="#f1f5f9"),
                    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title_font=dict(size=14), tickfont=dict(size=12)),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title_font=dict(size=14), tickfont=dict(size=12))
                )
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("Tiada data ditemui untuk analisis pembahagian.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_chart2:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 20px; color:#ffffff; margin-bottom: 20px; font-weight:700;'>📊 Agihan Mengikut Kategori Perjanjian</h3>", unsafe_allow_html=True)
            
            if total_records > 0:
                cat_data = df["Kategori"].value_counts().reindex(
                    ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"], 
                    fill_value=0
                ).reset_index()
                cat_data.columns = ["Kategori", "Jumlah"]
                
                fig2 = px.pie(cat_data, values="Jumlah", names="Kategori", hole=0.6, 
                              color_discrete_sequence=["#8b5cf6", "#10b981"]) 
                
                fig2.update_layout(
                    margin=dict(t=10, b=10, l=0, r=0), 
                    height=320,
                    paper_bgcolor="rgba(0,0,0,0)", 
                    font=dict(family="Quicksand", color="#f1f5f9"),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=11))
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Tiada data kategori yang dapat dianalisis.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 20px; color:#ffffff; margin-bottom: 20px; font-weight:700;'>⚡ Log Aktiviti: 5 Rekod Pendaftaran Terkini</h3>", unsafe_allow_html=True)
        
        if len(df) > 0:
            st.markdown(f"""
            <div class="table-container">
                {df.tail(5).to_html(index=False, classes="styled-table", escape=False)}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Tiada log kemasukan maklumat terkini.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODUL: PAPARAN REKOD GLOBAL
    # ------------------------------------------------------
    elif st.session_state.current_page == "View All Records" or st.session_state.current_page == "Paparan Rekod Global":
        st.markdown("<h1 class='glow-text' style='margin-bottom: 20px;'>📂 Repositori Pengurusan Data Utama</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        search = st.text_input("🔍 Penapis Pintar (Masukkan Tajuk Perjanjian, Nama Rakan atau Negara)", placeholder="Taip maklumat carian di sini...")

        if search:
            sql = "SELECT * FROM collaboration_data WHERE title LIKE ? OR partner LIKE ? OR country LIKE ?"
            cursor.execute(sql, (f"%{search}%", f"%{search}%", f"%{search}%"))
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=["ID", "Tajuk Perjanjian", "Tempoh Kuat Kuasa", "Bahagian/Fakulti", "Rakan Kerjasama", "Negara", "Kategori"])

        if len(df) > 0:
            html_table = df.to_html(index=False, classes="styled-table", escape=False)
            st.markdown(f'<div class="table-container">{html_table}</div>', unsafe_allow_html=True)
        else:
            st.info("Maaf, tiada rekod kolaborasi ditemui dalam pengkalan data yang sepadan dengan kriteria carian.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_spacer, col_btn_cancel = st.columns([8, 2])
        with col_btn_cancel:
            if st.button("← Kembali", key="back_view", use_container_width=True):
                switch_page("Papan Pemuka")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODUL: DAFTAR REKOD BARU
    # ------------------------------------------------------
    elif st.session_state.current_page == "Add New Record" or st.session_state.current_page == "Daftar Rekod Baru":
        st.markdown("<h1 class='glow-text' style='margin-bottom: 20px;'>➕ Pendaftaran Rekod Baharu</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        st.markdown("<h4 style='color:#a78bfa; margin-bottom: 15px; font-weight:700;'>📄 Butiran Dokumen Perundangan</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            id_in = st.number_input("Tentukan ID Rekod Unik", min_value=1, step=1, format="%d")
            category = st.selectbox("Kategori Struktur Perjanjian", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"])
        with col2:
            title = st.text_input("Tajuk Perjanjian Rasmi")
            duration = st.text_input("Tempoh Kuat Kuasa (Cth: 3 Tahun)")

        st.markdown("<hr style='border: 1px dashed rgba(255,255,255,0.08); margin:25px 0;'>", unsafe_allow_html=True)

        st.markdown("<h4 style='color:#a78bfa; margin-bottom: 15px; font-weight:700;'>🤝 Profil Rakan Kolaborasi</h4>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            department = st.text_input("Bahagian / Fakulti Peneraju")
            country = st.text_input("Negara Lokasi Rakan")
        with col4:
            partner = st.text_input("Nama Entiti Rakan Kerjasama")

        st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.05); margin:30px 0 20px 0;'>", unsafe_allow_html=True)

        col_btn_save, col_spacer, col_btn_cancel = st.columns([3, 4.5, 2.5])
        
        with col_btn_save:
            if st.button("💾 Simpan Rekod Baharu", use_container_width=True):
                try:
                    cursor.execute("INSERT INTO collaboration_data (id, title, duration, department, partner, country, category) VALUES (?,?,?,?,?,?,?)",
                                   (int(id_in), title, duration, department, partner, country, category))
                    conn.commit()
                    st.success("Selesai! Rekod kolaborasi baharu ini berjaya dimasukkan ke dalam SQL cluster.")
                    switch_page("Paparan Rekod Global")
                except sqlite3.IntegrityError:
                    st.error("Ralat: ID Rekod Unik tersebut sudah wujud. Sila pilih ID lain.")
                
        with col_btn_cancel:
            if st.button("❌ Batal Operasi", key="back_add", use_container_width=True):
                switch_page("Papan Pemuka")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODUL: KEMAS KINI REKOD
    # ------------------------------------------------------
    elif st.session_state.current_page == "Update Record" or st.session_state.current_page == "Kemas Kini Rekod":
        st.markdown("<h1 class='glow-text' style='margin-bottom: 20px;'>📝 Ubah Suai Profil Rekod Sedia Ada</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        uid = st.number_input("Masukkan ID Rekod yang Ingin Diubah", min_value=1, step=1, format="%d")
        cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(uid),))
        result = cursor.fetchone()

        if result:
            st.markdown("<hr style='border: 1px dashed rgba(255,255,255,0.08); margin:25px 0;'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                title = st.text_input("Tajuk Perjanjian Baharu", result[1])
                duration = st.text_input("Tempoh Kuat Kuasa Kemaskini", result[2])
                department = st.text_input("Bahagian / Fakulti Peneraju", result[3])
            with col2:
                partner = st.text_input("Nama Entiti Rakan Kerjasama", result[4])
                country = st.text_input("Negara Lokasi Rakan", result[5])
                category = st.selectbox("Kategori Struktur Perjanjian", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"], 
                                        index=["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"].index(result[6]) if result[6] in ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"] else 0)

            st.markdown("<br>", unsafe_allow_html=True)
            
            col_btn_update, col_spacer, col_btn_cancel = st.columns([3, 4.5, 2.5])
            
            with col_btn_update:
                if st.button("🔄 Kemaskini Perubahan", use_container_width=True):
                    cursor.execute("UPDATE collaboration_data SET title=?, duration=?, department=?, partner=?, country=?, category=? WHERE id=?",
                                   (title, duration, department, partner, country, category, int(uid)))
                    conn.commit()
                    st.success("Keberhasilan: Rekod kolaborasi ini telah berjaya diselaraskan.")
                    switch_page("Paparan Rekod Global")
                    
            with col_btn_cancel:
                if st.button("❌ Batal & Kembali", key="back_update", use_container_width=True):
                    switch_page("Papan Pemuka")
                
        else:
            st.warning("Pemberitahuan: ID Sasaran rujukan tidak ditemui di dalam pangkalan data.")
            st.markdown("<br>", unsafe_allow_html=True)
            col_spacer, col_btn_cancel = st.columns([8, 2])
            with col_btn_cancel:
                if st.button("← Kembali", key="back_update_fail", use_container_width=True):
                    switch_page("Papan Pemuka")
            
        st.markdown('</div>', unsafe_allow_html=True)

    # ------------------------------------------------------
    # MODUL: PELUPUSAN REKOD
    # ------------------------------------------------------
    elif st.session_state.current_page == "Delete Record" or st.session_state.current_page == "Pelupusan Rekod":
        st.markdown("<h1 class='glow-text' style='margin-bottom: 20px;'>🗑️ Pelupusan Fail Rekod Kolaborasi</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        del_id = st.number_input("Masukkan ID Rekod Sasaran Pemadaman", min_value=1, step=1, format="%d")
        
        st.markdown("""
        <div style='background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; padding: 18px; border-radius: 12px; margin-top: 20px; margin-bottom: 10px;'>
            <p style='color: #fca5a5; margin: 0; font-weight: 700; font-size:15px;'>🚨 AMARAN KRITIKAL: Pemadaman adalah kekal dan tidak boleh dipulihkan semula.</p>
        </div>
        """, unsafe_allow_html=True)

        @st.dialog("⚠️ Pengesahan Pemadaman Muktamad")
        def confirm_delete_dialog(record_id):
            st.markdown(f"<h4 style='color:#fca5a5;'>Adakah anda pasti untuk melupuskan Rekod ID {record_id}?</h4>", unsafe_allow_html=True)
            st.write("Semua fail maklumat kolaborasi ini akan disingkirkan secara kekal serta-merta.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_yes, col_spacer_dialog, col_cancel = st.columns([4, 2, 4])
            
            with col_yes:
                if st.button("Ya, Padam Sekarang", use_container_width=True):
                    cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(record_id),))
                    if cursor.fetchone():
                        cursor.execute("DELETE FROM collaboration_data WHERE id=?", (int(record_id),))
                        conn.commit()
                        st.success(f"Rekod ID {record_id} berjaya dilupuskan dengan selamat.")
                        switch_page("Paparan Rekod Global")
                    else:
                        st.error("Ralat Pelupusan: ID Sasaran tidak ditemui.")
            
            with col_cancel:
                if st.button("Batal Sesi", key="dialog_cancel", use_container_width=True):
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_btn_del, col_spacer, col_btn_cancel = st.columns([3, 4.5, 2.5])
        
        with col_btn_del:
            if st.button("🚨 Jalankan Pelupusan", use_container_width=True):
                confirm_delete_dialog(del_id)
                
        with col_btn_cancel:
            if st.button("❌ Batal & Kembali", key="back_delete", use_container_width=True):
                switch_page("Papan Pemuka")
            
        st.markdown('</div>', unsafe_allow_html=True)