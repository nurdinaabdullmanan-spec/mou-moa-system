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

# Pengisian Data Demo Secara Automatik (Untuk mengelakkan sistem nampak kosong)
cursor.execute("SELECT COUNT(*) FROM users")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", ("admin", "staf@uitm.edu.my", "admin"))
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM collaboration_data")
if cursor.fetchone()[0] == 0:
    demo_records = [
        (1, "MoU Penyelidikan Kecerdasan Buatan (AI) Global", "5 Tahun", "Fakulti Sains Komputer & Matematik", "Intel Microelectronics", "Amerika Syarikat", "Memorandum of Understanding (MoU)"),
        (2, "MoA Pembangunan Hab Teknologi Tenaga Hijau", "3 Tahun", "Fakulti Kejuruteraan Kimia", "PETRONAS", "Malaysia", "Agreement for MyRA Purpose"),
        (3, "MoU Program Pertukaran Sarjana & Penyelidik Kanan", "3 Tahun", "Fakulti Pengurusan Perniagaan", "Kyoto University", "Jepun", "Memorandum of Understanding (MoU)"),
        (4, "MoA Pemindahan Teknologi Pintar IoT Pertanian", "2 Tahun", "Fakulti Kejuruteraan Elektrik", "Huawei Technologies Co. Ltd.", "China", "Agreement for MyRA Purpose"),
        (5, "MoU Konsortium Kajian Klinikal & Sains Farmaseutikal", "5 Tahun", "Fakulti Farmasi", "AstraZeneca PLC", "United Kingdom", "Memorandum of Understanding (MoU)")
    ]
    cursor.executemany("INSERT INTO collaboration_data VALUES (?, ?, ?, ?, ?, ?, ?)", demo_records)
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
# REKA BENTUK UI KORPORAT "CLEAN & PRO" (LIGHT MODE WOW)
# ======================================================
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        letter-spacing: -0.5px;
    }}
    
    /* LATAR BELAKANG CLEAN & PRO DENGAN CORAK GRID GEOMETRI HALUS */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #f8fafc !important;
        background-image: radial-gradient(#cbd5e1 1.5px, transparent 1.5px) !important;
        background-size: 26px 26px !important;
        color: #1e293b !important;
    }}

    /* Sembunyikan elemen lalai Streamlit */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* MENU SISI (SIDEBAR) BERSALUT PUTIH KORPORAT */
    section[data-testid="stSidebar"] {{
        background: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
        box-shadow: 4px 0 20px rgba(0,0,0,0.03);
    }}
    
    div[role="radiogroup"] label input[type="radio"],
    div[role="radiogroup"] label > div:first-child {{
        display: none !important;
    }}

    /* REKA BUTANG MENU SIDEBAR */
    div[role="radiogroup"] label {{
        display: flex !important;
        align-items: center !important;
        padding: 12px 18px !important;
        margin-bottom: 8px !important;
        border-radius: 12px !important;
        background: transparent !important;
        transition: all 0.25s ease;
        cursor: pointer;
        border: 1px solid transparent !important;
    }}

    div[role="radiogroup"] label p {{
        color: #64748b !important; 
        font-size: 14px !important;
        font-weight: 600 !important;
        margin-left: 0px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}

    div[role="radiogroup"] label:hover {{
        background: #f1f5f9 !important;
        transform: translateX(5px);
    }}

    div[role="radiogroup"] label[data-selected="true"] {{
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important; 
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.25) !important;
    }}

    div[role="radiogroup"] label[data-selected="true"] p {{
        color: #ffffff !important; 
        font-weight: 700 !important;
    }}

    /* KAD METRIK (CLEAN, KEMAS, DAN TERAPUNG) */
    .metric-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }}
    .metric-card {{
        background: #ffffff; 
        padding: 24px; 
        border-radius: 16px;
        border: 1px solid #e2e8f0; 
        display: flex; align-items: center; gap: 16px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.08);
        border-color: #cbd5e1;
    }}
    .metric-icon-box {{
        width: 55px; height: 55px; border-radius: 14px;
        display: flex; justify-content: center; align-items: center; font-size: 26px;
    }}
    
    .metric-info h3 {{ margin: 0; font-size: 26px; color: #0f172a; font-weight: 800; line-height: 1.2; }}
    .metric-info p {{ margin: 0; font-size: 12px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }}
    
    /* KAD KANDUNGAN UTAMA (CLEAN WHITE) */
    .content-card {{
        background: #ffffff !important; 
        border-radius: 16px; padding: 30px; 
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
        margin-bottom: 24px;
        transition: box-shadow 0.3s ease;
    }}
    .content-card:hover {{
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.06);
    }}

    /* BUTANG KORPORAT (BIRU GELAP) */
    .stButton > button, 
    button[kind="primary"], 
    button[kind="secondary"] {{
        border-radius: 10px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px;
        padding: 12px 28px !important;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.25) !important;
    }}

    .stButton > button:hover, 
    button[kind="primary"]:hover, 
    button[kind="secondary"]:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4) !important;
        color: #ffffff !important;
    }}

    /* GAYA BORANG & RUANG MASUKKAN (INPUT CONTROLS) */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
        border-radius: 10px !important; 
        border: 1.5px solid #cbd5e1 !important;
        background-color: #f8fafc !important; 
        color: #1e293b !important; 
        padding: 12px 16px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500;
        transition: all 0.2s ease;
    }}
    .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
        background-color: #ffffff !important;
    }}
    
    /* GAYA JADUAL MAKLUMAT ELEGAN (TABLE) */
    .table-container {{
        width: 100%; overflow-x: auto; border-radius: 12px;
        border: 1px solid #e2e8f0; margin-top: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }}
    .styled-table {{
        width: 100%; border-collapse: collapse; margin: 0;
        font-size: 14px; font-family: 'Inter', sans-serif; 
        background-color: #ffffff;
    }}
    .styled-table thead tr {{
        background: #f1f5f9; 
        color: #334155; text-align: left;
        border-bottom: 2px solid #cbd5e1;
    }}
    .styled-table th {{ 
        padding: 16px 24px; font-family: 'Plus Jakarta Sans', sans-serif; 
        font-weight: 700; white-space: nowrap; 
    }}
    .styled-table td {{ 
        padding: 16px 24px; border-bottom: 1px solid #f1f5f9; color: #475569; font-weight: 500; 
    }}
    .styled-table tbody tr {{ transition: background-color 0.2s ease; }}
    .styled-table tbody tr:hover {{ background-color: #f8fafc; cursor: pointer; }}

    /* LOGO DAN ELEMEN GRAFIK */
    .uitm-logo {{
        filter: drop-shadow(0px 8px 15px rgba(0, 0, 0, 0.08));
        transition: transform 0.3s ease;
    }}
    .uitm-logo:hover {{
        transform: scale(1.03);
    }}

    /* GRADIENT TEXT KORPORAT */
    .corp-text {{
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }}
</style>
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
    spacer_left, center_col, spacer_right = st.columns([1, 1.2, 1])
    
    with center_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <img src="{UITM_LOGO_SRC}" class="uitm-logo" alt="UiTM Logo" style="width: 270px;">
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align:center; width:100%; margin-bottom: 35px;'>
            <h1 class='corp-text' style='margin-bottom: 5px; font-size: 32px !important;'>
                SISTEM PENGURUSAN REKOD
            </h1>
            <p style='color:#64748b; font-size: 15px; margin-top: 0; font-weight: 700; letter-spacing: 1.5px;'>UiTM KAMPUS PERMATANG PAUH</p>
        </div>
        """, unsafe_allow_html=True)
        
        auth = st.selectbox("Pilih Tindakan Akses", ["Sesi Log Masuk Portal", "Daftar Akaun Kakitangan Baru", "Tukar Kata Laluan Sedia Ada"])

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        if auth == "Sesi Log Masuk Portal":
            st.markdown("<h3 style='margin-bottom: 25px; font-size: 20px !important; color: #1e3a8a !important;'>🔑 Log Masuk Keselamatan</h3>", unsafe_allow_html=True)
            username = st.text_input("Nama Pengguna Rasmi")
            password = st.text_input("Kata Laluan", type="password")

            # Paparan pembantu akaun demo eksklusif
            st.markdown("""
            <div style="background: #eff6ff; border-left: 3px solid #3b82f6; padding: 12px; border-radius: 8px; margin-top: 15px; font-size: 13px; color: #1e3a8a;">
                💡 <b>Sesi Percubaan Segera:</b> Gunakan Username: <code style="color:#2563eb; background:transparent;">admin</code> | Password: <code style="color:#2563eb; background:transparent;">admin</code>
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
            st.markdown("<h3 style='margin-bottom: 25px; font-size: 20px !important; color: #1e3a8a !important;'>📝 Daftar Akaun Staf</h3>", unsafe_allow_html=True)
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
            st.markdown("<h3 style='margin-bottom: 25px; font-size: 20px !important; color: #1e3a8a !important;'>🔄 Kemaskini Kata Laluan</h3>", unsafe_allow_html=True)
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

    # SIDEBAR UTAMA - CLEAN & KORPORAT
    st.sidebar.markdown(f"""
        <div style="text-align:center; margin-bottom: 30px; padding-top: 15px;">
            <img src="{UITM_LOGO_SRC}" class="uitm-logo" style="width:145px; margin-bottom:15px;" alt="UiTM Logo">
            <h3 style="color:#0f172a; font-size:16px; font-weight:800; margin:0; letter-spacing:-0.5px;">UiTM Permatang Pauh</h3>
            <p style="color:#64748b; font-size:11px; margin-top:5px; line-height:1.4; font-weight:700; text-transform: uppercase; letter-spacing: 0.5px;">Sistem Pengurusan Rekod<br>Kolaborasi MoU/MoA</p>
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

    st.sidebar.markdown("<hr style='margin: 25px 0; border: none; height: 1px; background: #e2e8f0;'>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='font-size:11px; color:#94a3b8; font-weight:800; text-transform:uppercase; letter-spacing: 1px;'>PENGGUNA AKTIF</p>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <div style='background: #f8fafc; padding: 14px; border-radius: 12px; margin-bottom: 25px; border: 1px solid #e2e8f0; text-align:center;'>
        <p style='color:#0f172a; font-size:14px; margin:0; font-family: "Plus Jakarta Sans", sans-serif; font-weight:700;'>👤 {st.session_state.username}</p>
        <span style="font-size:10px; color:#10b981; font-weight:800; letter-spacing:1px; text-transform:uppercase;">● Atas Talian</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Tamatkan Sesi Selamat", key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # Membaca data terkini daripada pangkalan data
    cursor.execute("SELECT * FROM collaboration_data ORDER BY id ASC")
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["ID", "Tajuk Perjanjian", "Tempoh Kuat Kuasa", "Bahagian/Fakulti", "Rakan Kerjasama", "Negara", "Kategori"])

    # ------------------------------------------------------
    # MODUL: PAPAN PEMUKA (CLEAN EXECUTIVE DASHBOARD)
    # ------------------------------------------------------
    if st.session_state.current_page == "Papan Pemuka":
        col_greet, col_date = st.columns([2.8, 1.2])
        with col_greet:
            st.markdown(f"""
            <h1 class='corp-text' style='margin-bottom: 5px; font-size:36px;'>Selamat Datang, {st.session_state.username}! 👋</h1>
            <p style='color:#64748b; font-size:16px; margin-top:0; font-weight:500;'>Analitik Sesi Pintar: Ringkasan data pengurusan kolaborasi rasmi kampus.</p>
            """, unsafe_allow_html=True)
        with col_date:
            st.markdown(f"""
            <div style='background:#ffffff; padding:14px 22px; border-radius:16px; border:1px solid #e2e8f0; display:flex; align-items:center; gap:15px; float:right; box-shadow: 0 4px 6px rgba(0,0,0,0.02);'>
                <div style='background: #eff6ff; color:#2563eb; width: 45px; height: 45px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size:22px;'>📅</div>
                <div>
                    <div style='font-size:10px; color:#64748b; font-weight:700; text-transform:uppercase; letter-spacing:1px;'>Tarikh Semasa</div>
                    <div style='font-size:15px; font-weight:800; color:#0f172a;'>{current_date}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Analisis Ringkasan data
        total_records = len(df)
        total_country = df["Negara"].nunique() if total_records > 0 else 0
        total_category = 2 
        active_agreements = len(df)

        # METRIK GRID (CLEAN & KORPORAT)
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card" style="border-bottom: 4px solid #2563eb;">
                <div class="metric-icon-box" style="background: #eff6ff; color:#2563eb;">📄</div>
                <div class="metric-info">
                    <h3>{total_records}</h3>
                    <p>Jumlah Dokumen</p>
                </div>
            </div>
            <div class="metric-card" style="border-bottom: 4px solid #059669;">
                <div class="metric-icon-box" style="background: #ecfdf5; color:#059669;">🌐</div>
                <div class="metric-info">
                    <h3>{total_country}</h3>
                    <p>Negara Rakan</p>
                </div>
            </div>
            <div class="metric-card" style="border-bottom: 4px solid #d97706;">
                <div class="metric-icon-box" style="background: #fffbeb; color:#d97706;">🤝</div>
                <div class="metric-info">
                    <h3>{total_category}</h3>
                    <p>Kategori Utama</p>
                </div>
            </div>
            <div class="metric-card" style="border-bottom: 4px solid #dc2626;">
                <div class="metric-icon-box" style="background: #fef2f2; color:#dc2626;">📂</div>
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
            st.markdown("<h3 style='font-size: 20px; color:#0f172a; margin-bottom: 20px; font-weight:700;'>🌍 Pembahagian Mengikut Negara Rakan</h3>", unsafe_allow_html=True)
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
                    font=dict(family="Inter", color="#475569"),
                    xaxis=dict(gridcolor="#f1f5f9", title_font=dict(size=14), tickfont=dict(size=12)),
                    yaxis=dict(gridcolor="#f1f5f9", title_font=dict(size=14), tickfont=dict(size=12))
                )
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("Tiada data ditemui untuk analisis pembahagian.")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_chart2:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 20px; color:#0f172a; margin-bottom: 20px; font-weight:700;'>📊 Agihan Mengikut Kategori Perjanjian</h3>", unsafe_allow_html=True)
            
            if total_records > 0:
                cat_data = df["Kategori"].value_counts().reindex(
                    ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"], 
                    fill_value=0
                ).reset_index()
                cat_data.columns = ["Kategori", "Jumlah"]
                
                fig2 = px.pie(cat_data, values="Jumlah", names="Kategori", hole=0.5, 
                              color_discrete_sequence=["#3b82f6", "#10b981"]) 
                
                fig2.update_layout(
                    margin=dict(t=10, b=10, l=0, r=0), 
                    height=320,
                    paper_bgcolor="rgba(0,0,0,0)", 
                    font=dict(family="Inter", color="#475569"),
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(size=11))
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Tiada data kategori yang dapat dianalisis.")
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 20px; color:#0f172a; margin-bottom: 20px; font-weight:700;'>⚡ Log Aktiviti: 5 Rekod Pendaftaran Terkini</h3>", unsafe_allow_html=True)
        
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
    elif st.session_state.current_page == "Paparan Rekod Global":
        st.markdown("<h1 class='corp-text' style='margin-bottom: 20px;'>📂 Repositori Pengurusan Data Utama</h1>", unsafe_allow_html=True)

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
    elif st.session_state.current_page == "Daftar Rekod Baru":
        st.markdown("<h1 class='corp-text' style='margin-bottom: 20px;'>➕ Pendaftaran Rekod Baharu</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        
        st.markdown("<h4 style='color:#1e3a8a; margin-bottom: 15px; font-weight:700;'>📄 Butiran Dokumen Perundangan</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            id_in = st.number_input("Tentukan ID Rekod Unik", min_value=1, step=1, format="%d")
            category = st.selectbox("Kategori Struktur Perjanjian", ["Memorandum of Understanding (MoU)", "Agreement for MyRA Purpose"])
        with col2:
            title = st.text_input("Tajuk Perjanjian Rasmi")
            duration = st.text_input("Tempoh Kuat Kuasa (Cth: 3 Tahun)")

        st.markdown("<hr style='border: 1px dashed #e2e8f0; margin:25px 0;'>", unsafe_allow_html=True)

        st.markdown("<h4 style='color:#1e3a8a; margin-bottom: 15px; font-weight:700;'>🤝 Profil Rakan Kolaborasi</h4>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)
        with col3:
            department = st.text_input("Bahagian / Fakulti Peneraju")
            country = st.text_input("Negara Lokasi Rakan")
        with col4:
            partner = st.text_input("Nama Entiti Rakan Kerjasama")

        st.markdown("<hr style='border: 1px solid #e2e8f0; margin:30px 0 20px 0;'>", unsafe_allow_html=True)

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
    elif st.session_state.current_page == "Kemas Kini Rekod":
        st.markdown("<h1 class='corp-text' style='margin-bottom: 20px;'>📝 Ubah Suai Profil Rekod Sedia Ada</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        uid = st.number_input("Masukkan ID Rekod yang Ingin Diubah", min_value=1, step=1, format="%d")
        cursor.execute("SELECT * FROM collaboration_data WHERE id=?", (int(uid),))
        result = cursor.fetchone()

        if result:
            st.markdown("<hr style='border: 1px dashed #e2e8f0; margin:25px 0;'>", unsafe_allow_html=True)
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
    elif st.session_state.current_page == "Pelupusan Rekod":
        st.markdown("<h1 class='corp-text' style='margin-bottom: 20px;'>🗑️ Pelupusan Fail Rekod Kolaborasi</h1>", unsafe_allow_html=True)

        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        del_id = st.number_input("Masukkan ID Rekod Sasaran Pemadaman", min_value=1, step=1, format="%d")
        
        st.markdown("""
        <div style='background: #fef2f2; border-left: 4px solid #ef4444; padding: 18px; border-radius: 12px; margin-top: 20px; margin-bottom: 10px;'>
            <p style='color: #b91c1c; margin: 0; font-weight: 700; font-size:15px;'>🚨 AMARAN KRITIKAL: Pemadaman adalah kekal dan tidak boleh dipulihkan semula.</p>
        </div>
        """, unsafe_allow_html=True)

        @st.dialog("⚠️ Pengesahan Pemadaman Muktamad")
        def confirm_delete_dialog(record_id):
            st.markdown(f"<h4 style='color:#b91c1c;'>Adakah anda pasti untuk melupuskan Rekod ID {record_id}?</h4>", unsafe_allow_html=True)
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