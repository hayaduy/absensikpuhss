import streamlit as st
import requests
from datetime import datetime
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Absensi KPU HSS - V.1.4", layout="wide")

# --- DATABASE & CONFIG ---
URL_APPS_SCRIPT = "https://script.google.com/macros/s/AKfycbwLk_OWo1_BaJYaIpQvd78irmthnaHmNlMgII-HI1NrqzFIO-3uNXXoN7tqBm0-95-rIg/exec"

DB_PEGAWAI = {
    "1": {"nama": "Suwanto", "sheet": "Suwanto", "nip": "19720521 200912 1 001", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "2": {"nama": "Wawan Setiawan", "sheet": "Wawan Setiawan", "nip": "19860601 201012 1 004", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "3": {"nama": "Ineke Setiyaningsih", "sheet": "Ineke Setiyaningsih", "nip": "19831003 200912 2 001", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "4": {"nama": "Farah Agustina Setiawati", "sheet": "Farah Agustina Setiawati", "nip": "19840828 201012 2 003", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "5": {"nama": "Rusma Ariati", "sheet": "Rusma Ariati", "nip": "19840621 201101 2 013", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "6": {"nama": "Ahmad Erwan Rifani", "sheet": "Ahmad Erwan Rifani", "nip": "19830829 200811 1 001", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "7": {"nama": "Syaiful Anwar", "sheet": "Syaiful Anwar", "nip": "19741127 200710 1 001", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "8": {"nama": "Zainal Hilmi Yustan", "sheet": "Zainal Hilmi Yustan", "nip": "19821025 200701 1 003", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "9": {"nama": "Najmi Hidayati", "sheet": "Najmi Hidayati", "nip": "19850608 200701 2 003", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "10": {"nama": "Jainal Abidin", "sheet": "Jainal Abidin", "nip": "19820712 200910 1 001", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "11": {"nama": "Suci Lestari", "sheet": "Suci Lestari", "nip": "19850108 201012 2 006", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "12": {"nama": "Athaya Insyira Khairani", "sheet": "Athaya Insyira Khairani", "nip": "20010712 202506 2 017", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "13": {"nama": "Muhammad Ibnu Fahmi", "sheet": "Muhammad Ibnu Fahmi", "nip": "20010608 202506 1 007", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "14": {"nama": "Alfian Ridhani", "sheet": "Alfian Ridhani", "nip": "19950903 202506 1 005", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "15": {"nama": "Muhammad Aldi Hudaifi", "sheet": "Muhammad Aldi Hudaifi", "nip": "20010121 202506 1 007", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "16": {"nama": "Firda Aulia", "sheet": "Firda Aulia", "nip": "20020415 202506 2 007", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "17": {"nama": "Sya'bani Rona Baika", "sheet": "Sya'bani Rona Baika", "nip": "19920207 202421 2 044", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "18": {"nama": "Apriadi Rakhman", "sheet": "Apriadi Rakhman", "nip": "19890422 202421 1 013", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "19": {"nama": "M Satria Maipadly", "sheet": "M Satria Maipadly", "nip": "19890526 202421 1 016", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "20": {"nama": "Basuki Rahmat", "sheet": "Basuki Rahmat", "nip": "19770502 202421 1 007", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "21": {"nama": "Sulaiman", "sheet": "Sulaiman", "nip": "19841122 202421 1 010", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "22": {"nama": "Saldoz Yedi", "sheet": "Saldoz Yedi", "nip": "19800811 202521 1 019", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "23": {"nama": "Mastoni Ridani", "sheet": "Mastoni Ridani", "nip": "19910601 202521 1 018", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "24": {"nama": "Suriadi", "sheet": "Suriadi", "nip": "19980302 202521 1 005", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "25": {"nama": "Ami Aspihani", "sheet": "Ami Aspihani", "nip": "19820404 202521 1 031", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "26": {"nama": "Abdurrahman", "sheet": "Abdurrahman", "nip": "19881012 202521 1 031", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "27": {"nama": "Emaliani", "sheet": "Emaliani", "nip": "19890622 202521 2 027", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "28": {"nama": "Muhammad Hafiz Rijani", "sheet": "Muhammad Hafiz Rijani", "nip": "19960321 202521 1 031", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "29": {"nama": "Saiful Fahmi", "sheet": "Saiful Fahmi", "nip": "19950617 202521 1 036", "unit": "KPU KAB. HULU SUNGAI SELATAN"},
    "30": {"nama": "Nadianti", "sheet": "Nadianti", "nip": "19990606 202521 2 036", "unit": "KPU KAB. HULU SUNGAI SELATAN"}
}

MOTIVASI = [
    "Kadada nang labih manis selain lihum pian hari ini.",
    "Biar dunya baputar hancap, hati ulun tatap diam di wadah pian haja.",
    "Apa nang labih manis: dodol Kandangan kah lihum manis sidin?",
    "Dasar lain mun sudah gajihan nih, tihang listrik gin dilihumi",
    "Kira-kira pian baisi rahasia lah? Rahasia ulun cuma sabuting: ulun sayang lawan pian.",
    "Jangan tamakan janji, sidin bahanu ada wisanya",
    "Pian ni kaya wadai bingka, manisnya pas, maulah ulun handak tarus.",
    "Jangan tapi dipikirakan banar gawian tu, kaina hancap tuha muha kaya iwak karing talambat diangkat."
]

# --- CSS MEWAH ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #4d0a0a 0%, #1a0404 100%); }
    div[data-testid="stVerticalBlockBorder"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 20px !important;
    }
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea, .stDateInput input {
        background-color: rgba(0, 0, 0, 0.4) !important;
        color: #ffd700 !important;
        border: 1px solid #5e1515 !important;
        border-radius: 12px !important;
    }
    .stButton { display: flex; justify-content: center; }
    .stButton>button {
        background: linear-gradient(135deg, #ff8c00 0%, #d42020 100%) !important;
        color: white !important; font-weight: 800 !important;
        text-transform: uppercase !important; border-radius: 12px !important;
        padding: 10px 30px !important; border: none !important;
        box-shadow: 0 4px 15px rgba(212, 32, 32, 0.4) !important;
    }
    .stButton>button:disabled { background: #333 !important; color: #666 !important; }
    .mon-title { text-align: center; color: #ffd700; font-size: 24px; font-weight: 800; margin-top: 40px; }
    .mobile-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255, 215, 0, 0.15); border-radius: 15px; padding: 15px; margin-bottom: 10px; }
    .card-title { color: #ffd700; font-weight: bold; border-bottom: 1px solid rgba(255,215,0,0.2); padding-bottom: 5px; margin-bottom: 8px; }
    .card-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; }
    .card-label { color: #a87b7b; font-size: 10px; text-transform: uppercase; }
    .card-val { color: #ffffff; font-weight: bold; font-size: 13px; }
    h1 { color: #ffd700 !important; text-align: center; font-weight: 900 !important; margin-bottom: 0px !important; }
    .software-credit { text-align: center; color: #8a5a5a; font-size: 14px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI DIALOG ---
@st.dialog(" ")
def show_motivation(nama_orang):
    quote = random.choice(MOTIVASI)
    st.markdown(f"""
        <div style="text-align: center; background: radial-gradient(#6e1a1a, #2b0606); padding: 20px; border-radius: 15px; border: 2px solid #ffd700;">
            <h2 style="color: #ffd700; margin-bottom: 5px;">BERHASIL! 🎊</h2>
            <h3 style="color: white; border:none;">{nama_orang}</h3>
            <hr style="border-color: rgba(255,215,0,0.3);">
            <p style="font-size: 18px; font-style: italic; color: #fff;">"{quote}"</p>
        </div>
    """, unsafe_allow_html=True)
    _, mid_c, _ = st.columns([1, 2, 1])
    with mid_c:
        if st.button("Selesai", use_container_width=True):
            st.rerun()

# --- FETCH DATA MONITORING ---
@st.cache_data(ttl=30)
def get_mon_data():
    try:
        return requests.get(URL_APPS_SCRIPT, timeout=10).json()
    except:
        return {}

mon_data = get_mon_data()

# --- LOGIKA WAKTU ---
now = datetime.now()
hari_ini = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][now.weekday()]
is_weekend = now.weekday() >= 5 

# --- HEADER ---
st.markdown("<h1>KPU KABUPATEN HULU SUNGAI SELATAN</h1>", unsafe_allow_html=True)
st.markdown("<p class='software-credit'>O'lia Software Development V.1.4</p>", unsafe_allow_html=True)

# --- FORM ---
with st.container(border=True):
    v_id = st.text_input("🆔 ID PEGAWAI", placeholder="Masukkan ID...")
    pegawai = DB_PEGAWAI.get(v_id)
    
    if pegawai:
        st.markdown(f"<div style='background:rgba(255,215,0,0.1); padding:10px; border-radius:10px; border-left:4px solid #ffd700; color:white; margin-bottom:15px;'><b>Nama Pegawai:</b> {pegawai['nama']}</div>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        jenis = st.selectbox("📅 JENIS ABSENSI", ["Masuk", "Pulang", "Cuti", "Izin", "Off"])
    
    status_val = ""
    tgl_mulai = None
    tgl_selesai = None
    
    with col_b:
        if jenis == "Masuk":
            status_val = st.selectbox("📍 STATUS KEHADIRAN", ["WFO", "WFH", "Dinas Luar", "Piket Pagi", "Piket Malam"])
        elif jenis == "Cuti":
            # Perbaikan: Input tanggal Mulai dan Sampai
            c1, c2 = st.columns(2)
            tgl_mulai = c1.date_input("Mulai")
            tgl_selesai = c2.date_input("Sampai")
        else:
            st.markdown("<br>", unsafe_allow_html=True)

    uraian = output = ""
    if jenis == "Pulang":
        uraian = st.text_area("📋 URAIAN TUGAS")
        output = st.text_area("📦 OUTPUT")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- LOGIKA VALIDASI HARI LIBUR & PIKET ---
    can_send = True
    libur_msg = ""
    
    if is_weekend and pegawai:
        u_info = mon_data.get(pegawai["sheet"], {})
        is_piket_now = "PIKET" in str(u_info.get("status", "")).upper()

        if jenis == "Masuk":
            if status_val not in ["Piket Pagi", "Piket Malam"]:
                can_send = False
                libur_msg = f"Hari ini {hari_ini} (Libur). Absen MASUK hanya diperbolehkan untuk Piket."
        elif jenis == "Pulang":
            if not is_piket_now:
                can_send = False
                libur_msg = "Anda belum absen MASUK PIKET hari ini."
        elif jenis in ["Cuti", "Off", "Izin"]:
            can_send = True
        else:
            can_send = False
            libur_msg = "Hari libur. Hanya absensi Piket, Cuti, atau Off yang diizinkan."

    if not can_send and v_id:
        st.warning(libur_msg)

    # TOMBOL KIRIM
    left_c, center_c, right_c = st.columns([1, 2, 1])
    with center_c:
        if st.button("KIRIM DATA ABSENSI", use_container_width=True, disabled=not can_send):
            if pegawai:
                payload = {
                    "sheetName": pegawai["sheet"], "jenis": jenis, "nama": pegawai["nama"],
                    "nip": pegawai["nip"], "unit": pegawai["unit"], "status": status_val if jenis == "Masuk" else jenis,
                    "tanggal": now.strftime("%d/%m/%Y"), "hari": hari_ini,
                    "tglMulai": tgl_mulai.strftime("%d/%m/%Y") if tgl_mulai else "",
                    "tglSelesai": tgl_selesai.strftime("%d/%m/%Y") if tgl_selesai else "",
                    "uraian": uraian, "output": output
                }
                try:
                    requests.post(URL_APPS_SCRIPT, params=payload, timeout=15)
                    st.balloons()
                    show_motivation(pegawai['nama'])
                except: st.error("Gagal terhubung ke Google Spreadsheet!")
            else: st.error("ID Pegawai Salah!")

# --- MONITORING ---
st.markdown("<div class='mon-title'>MONITORING KEHADIRAN HARI INI</div>", unsafe_allow_html=True)
try:
    for pid in range(1, 31):
        sid = str(pid)
        if sid in DB_PEGAWAI:
            p = DB_PEGAWAI[sid]
            inf = mon_data.get(p["sheet"], {"jamMasuk": "-", "jamPulang": "-", "status": "-", "keterangan": "Belum Absen"})
            ket = inf['keterangan'].upper()
            k_clr = "#00ff88" if "HADIR" in ket else "#ff4444"
            if any(x in ket for x in ["CUTI", "IZIN", "OFF", "LIBUR"]): k_clr = "#ffff00"
            st.markdown(f"""<div class="mobile-card"><div class="card-title">{sid}. {p['nama']}</div><div class="card-grid"><div><div class="card-label">Masuk</div><div class="card-val">{inf['jamMasuk']}</div></div><div><div class="card-label">Pulang</div><div class="card-val">{inf['jamPulang']}</div></div><div><div class="card-label">Status</div><div class="card-val">{inf['status']}</div></div><div><div class="card-label">Ket</div><div style="color:{k_clr}; font-size:12px; font-weight:bold;">{ket}</div></div></div></div>""", unsafe_allow_html=True)
except: st.info("Memproses data...")
