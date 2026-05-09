import streamlit as st
import requests
from datetime import datetime
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Absensi KPU HSS - Elegant Pro", layout="wide")

# --- DATABASE ---
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
    "Kerja keras tidak akan mengkhianati hasil. Semangat, Bang!",
    "Jangan menunggu sukses untuk bersyukur, bersyukurlah maka sukses akan datang.",
    "Bekerjalah dengan ikhlas, karena Tuhan tidak pernah tidur melihat lelahmu.",
    "KPU Melayani! Terima kasih atas dedikasi Anda hari ini.",
    "Sukses adalah guru yang buruk. Ia menggoda orang cerdas untuk berpikir mereka tak bisa gagal.",
    "Hanya mereka yang berani gagal total yang dapat meraih keberhasilan besar.",
    "Kesuksesan bukan kunci kebahagiaan. Kebahagiaan adalah kunci kesuksesan.",
    "Lakukan hari ini apa yang orang lain tidak lakukan, agar besok kau bisa mendapatkan apa yang orang lain tak dapatkan.",
    "Masa depan adalah milik mereka yang percaya pada keindahan mimpi mereka.",
    "Awal yang sulit biasanya mengarah ke tujuan yang indah.",
    "Disiplin adalah jembatan antara cita-cita dan pencapaian.",
    "Kunci sukses adalah fokus pada tujuan, bukan pada rintangan.",
    "Jangan berhenti saat lelah. Berhentilah saat selesai.",
    "Hargai setiap detik waktu, karena ia takkan pernah kembali.",
    "Hidup bukan tentang menemukan dirimu, tapi tentang membangun dirimu.",
    "Jangan membandingkan bab pertama hidupmu dengan bab kedua puluh orang lain.",
    "Energi dan ketekunan mengalahkan segalanya.",
    "Kesempatan biasanya menyamar sebagai kerja keras.",
    "Kegagalan adalah satu-satunya kesempatan untuk memulai lagi dengan lebih cerdas.",
    "Mimpi tidak akan berhasil kecuali jika kamu melakukannya.",
    "Berbuat baiklah tanpa alasan, dan jangan mengharap balasan.",
    "Tujuan hidup kita adalah menjadi bahagia. Semangat hari ini!",
    "Waktu kamu terbatas, jangan habiskan untuk menjalani hidup orang lain.",
    "Satu-satunya cara melakukan pekerjaan hebat adalah dengan mencintai apa yang kamu lakukan.",
    "Percaya kamu bisa, dan kamu sudah setengah jalan menuju sukses.",
    "Keberuntungan adalah pertemuan antara persiapan dan kesempatan.",
    "Teruslah bergerak maju, rintangan hanyalah bumbu dalam perjalanan.",
    "Kemenangan terbesar adalah kemenangan atas diri sendiri.",
    "Integritas adalah memilih jalan yang benar, bukan jalan yang mudah.",
    "Jangan hanya berharap, mulailah bekerja!",
    "Hasil yang besar membutuhkan kesabaran yang besar pula.",
    "Ubah tantangan menjadi peluang hari ini.",
    "Kebahagiaan bukan sesuatu yang sudah jadi, ia berasal dari tindakanmu sendiri.",
    "Segala sesuatu yang dapat dibayangkan adalah nyata jika kita berusaha.",
    "Keberanian adalah ketakutan yang telah didoakan.",
    "Semangat pagi! Dunia menunggumu untuk memberikan kontribusi terbaik.",
    "Jangan biarkan kemarin mengambil terlalu banyak dari hari ini.",
    "Lakukan pekerjaanmu seolah-olah kamu tidak butuh uang.",
    "Satu pikiran positif di pagi hari bisa mengubah seluruh harimu.",
    "Sukses tidak datang kepadamu, kamu yang harus menjemputnya.",
    "Jangan takut berjalan lambat, takutlah jika hanya berdiri diam.",
    "Setiap langkah kecil membawamu lebih dekat ke impian besar.",
    "Rezeki sudah diatur, tugas kita adalah menjemputnya dengan cara yang halal.",
    "Jangan menyerah, permulaan selalu menjadi yang tersulit.",
    "Jadilah pribadi yang bermanfaat bagi orang di sekitarmu.",
    "Fokus pada solusi, bukan hanya pada masalah.",
    "Masa depanmu ditentukan oleh apa yang kamu lakukan hari ini.",
    "Hanya dengan bekerja sama, kita bisa mencapai hal-hal luar biasa.",
    "Ketekunan adalah kunci yang membuka pintu keberhasilan.",
    "Nikmati prosesnya, hasil akan mengikuti pada waktunya.",
    "Kualitas pekerjaanmu mencerminkan kualitas dirimu.",
    "Berikan yang terbaik hari ini, agar tidak ada penyesalan esok hari.",
    "Keikhlasan dalam bekerja akan mendatangkan ketenangan hati.",
    "Teruslah bermimpi, tapi jangan lupa bangun dan bekerja keras.",
    "Jadikan pekerjaan sebagai ladang ibadah bagi kita semua.",
    "Jangan pernah meremehkan kekuatan niat yang tulus.",
    "Setiap masalah punya tanggal kadaluarsa, tetap semangat!",
    "Kebersamaan adalah kekuatan kita di KPU HSS.",
    "Berani bermimpi besar, berani bekerja keras.",
    "Kesuksesan adalah kumpulan dari kemenangan-kemenangan kecil setiap hari.",
    "Jangan biarkan kegagalan kemarin menghalangi kesuksesan besok.",
    "Hari ini adalah kesempatan baru untuk menjadi lebih baik.",
    "Jangan mengeluh, syukuri apa yang masih kita miliki saat ini.",
    "Tetap rendah hati saat sukses, tetap kuat saat sulit.",
    "Pekerjaan hebat dibangun dengan ketekunan, bukan kekuatan semata.",
    "Selesaikan apa yang kamu mulai dengan penuh tanggung jawab.",
    "Jadilah inspirasi bagi rekan kerjamu hari ini.",
    "Kejujuran adalah modal utama dalam bekerja.",
    "Tersenyumlah, dunia akan terasa lebih ringan.",
    "Lakukan sesuatu yang akan membuat dirimu di masa depan berterima kasih.",
    "Kesabaran adalah pahit, tapi buahnya sangat manis.",
    "Jangan takut salah, takutlah jika tidak belajar dari kesalahan.",
    "Fokus pada progres, bukan hanya pada kesempurnaan.",
    "Setiap hari adalah lembaran baru untuk menulis cerita suksesmu.",
    "Keberanian bukan berarti tidak takut, tapi bertindak meski takut.",
    "Hargai rekan kerjamu, tim yang kuat dimulai dari saling menghargai.",
    "Jangan lupakan tujuan awalmu bekerja.",
    "Komitmen adalah apa yang mengubah janji menjadi kenyataan.",
    "Semangat melayani masyarakat dengan sepenuh hati!",
    "Jaga kesehatan, tubuh yang sehat adalah modal utama produktivitas.",
    "Ketenangan adalah kunci untuk mengambil keputusan yang tepat.",
    "Tantangan hari ini adalah latihan untuk kesuksesan hari esok.",
    "Jangan tunda pekerjaan yang bisa diselesaikan hari ini.",
    "Gunakan waktumu dengan bijak, setiap detik berharga.",
    "Yakinlah, kerja kerasmu akan membuahkan hasil manis nantinya.",
    "Saling mendukung adalah kunci sukses sebuah organisasi.",
    "Tetap semangat, weekend sudah menanti di depan mata!",
    "Istirahatlah jika lelah, tapi jangan pernah menyerah.",
    "Dunia membutuhkan dedikasimu, jangan lelah berbuat baik.",
    "Tuhan bersama orang-orang yang bersungguh-sungguh dalam kebaikan."
]

# --- CSS MERIAH & PROFESIONAL ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #4d0a0a 0%, #1a0404 100%); }
    
    /* Container Mewah */
    div[data-testid="stVerticalBlockBorder"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6) !important;
    }

    /* Input Styling */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.4) !important;
        color: #ffd700 !important;
        border: 1px solid #5e1515 !important;
        border-radius: 12px !important;
    }

    /* Tombol Kirim Proporsional & Meriah */
    .stButton>button {
        background: linear-gradient(135deg, #ff8c00 0%, #d42020 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px 25px !important;
        width: auto !important;
        margin: 0 auto !important;
        display: block !important;
        box-shadow: 0 4px 15px rgba(212, 32, 32, 0.4) !important;
    }

    /* Monitoring Title */
    .mon-title {
        text-align: center;
        color: #ffd700;
        font-size: 24px;
        font-weight: 800;
        margin: 40px 0 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* Card Monitoring Mobile */
    .mobile-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
        border: 1px solid rgba(255, 215, 0, 0.15);
        border-radius: 15px;
        padding: 18px;
        margin-bottom: 12px;
    }
    
    .card-title { color: #ffd700; font-weight: bold; font-size: 17px; border-bottom: 1px solid rgba(255,215,0,0.2); padding-bottom: 5px; margin-bottom: 10px; }
    .card-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    .card-label { color: #a87b7b; font-size: 11px; text-transform: uppercase; font-weight: 600; }
    .card-val { color: #ffffff; font-weight: bold; font-size: 14px; }
    
    h1 { color: #ffd700 !important; text-align: center; font-size: 26px !important; font-weight: 900 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- POP UP MOTIVASI MERIAH ---
@st.dialog(" ")
def show_motivation(nama_orang):
    quote = random.choice(MOTIVASI)
    st.markdown(f"""
        <div style="text-align: center; background: radial-gradient(#6e1a1a, #2b0606); padding: 20px; border-radius: 15px; border: 2px solid #ffd700;">
            <h2 style="color: #ffd700; margin-bottom: 5px;">BERHASIL! 🎊</h2>
            <h4 style="color: white; border:none;">Terima Kasih</h4>
            <h3 style="color: #ffd700; border:none; margin-top:-10px;">{nama_orang}</h3>
            <hr style="border-color: rgba(255,215,0,0.3);">
            <p style="font-size: 20px; font-style: italic; color: #fff; line-height: 1.4;">"{quote}"</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Selesai & Kembali", use_container_width=True):
        st.rerun()

# --- HEADER ---
st.markdown("<h1>KPU KABUPATEN HULU SUNGAI SELATAN</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#a87b7b; margin-top:-15px;'>Sistem Absensi Digital Mandiri</p>", unsafe_allow_html=True)

# --- FORM UTAMA ---
with st.container(border=True):
    v_id = st.text_input("ID PEGAWAI", placeholder="Ketik ID...")
    
    if v_id in DB_PEGAWAI:
        st.markdown(f"<div style='background:rgba(255,215,0,0.1); padding:10px; border-radius:10px; border-left:4px solid #ffd700; color:white;'><b>Nama:</b> {DB_PEGAWAI[v_id]['nama']}</div>", unsafe_allow_html=True)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        jenis = st.selectbox("JENIS ABSENSI", ["Masuk", "Pulang", "Cuti", "Izin", "Off"])
    
    status_val = ""
    tgl_mulai = tgl_selesai = None
    
    with col_f2:
        if jenis == "Masuk":
            # Perubahan ke Dropdown sesuai permintaan Bang
            status_val = st.selectbox("STATUS KEHADIRAN", ["WFO", "WFH", "Dinas Luar", "Piket Pagi", "Piket Malam"])
        elif jenis == "Cuti":
            tgl_mulai = st.date_input("Mulai")
        else:
            st.markdown("<br>", unsafe_allow_html=True)

    uraian = output = ""
    if jenis == "Pulang":
        uraian = st.text_area("URAIAN TUGAS", placeholder="Apa yang Anda kerjakan hari ini?")
        output = st.text_area("HASIL / OUTPUT", placeholder="Hasil dari pekerjaan tersebut...")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("KIRIM DATA ABSENSI"):
        if v_id not in DB_PEGAWAI:
            st.error("ID tidak terdaftar!")
        else:
            p = DB_PEGAWAI[v_id]
            payload = {
                "sheetName": p["sheet"], "jenis": jenis, "nama": p["nama"],
                "nip": p["nip"], "unit": p["unit"], "status": status_val if jenis == "Masuk" else jenis,
                "tanggal": datetime.now().strftime("%d/%m/%Y"),
                "tglMulai": tgl_mulai.strftime("%d/%m/%Y") if tgl_mulai else "",
                "uraian": uraian, "output": output
            }
            try:
                requests.post(URL_APPS_SCRIPT, params=payload, timeout=15)
                st.balloons()
                show_motivation(p['nama'])
            except:
                st.error("Gagal terhubung ke sistem!")

# --- MONITORING ---
st.markdown("<div class='mon-title'>MONITORING KEHADIRAN HARI INI</div>", unsafe_allow_html=True)

try:
    mon_res = requests.get(URL_APPS_SCRIPT, timeout=10).json()
    
    for i in range(1, 31):
        pid = str(i)
        if pid in DB_PEGAWAI:
            p = DB_PEGAWAI[pid]
            inf = mon_res.get(p["sheet"], {"jamMasuk": "-", "jamPulang": "-", "status": "-", "keterangan": "Belum Absen"})
            
            ket = inf['keterangan'].upper()
            k_clr = "#00ff88" if "HADIR" in ket else "#ff4444"
            if any(x in ket for x in ["CUTI", "IZIN", "OFF"]): k_clr = "#ffff00"

            st.markdown(f"""
                <div class="mobile-card">
                    <div class="card-title">{pid}. {p['nama']}</div>
                    <div class="card-grid">
                        <div><div class="card-label">Masuk</div><div class="card-val">{inf['jamMasuk']}</div></div>
                        <div><div class="card-label">Pulang</div><div class="card-val">{inf['jamPulang']}</div></div>
                        <div><div class="card-label">Status</div><div class="card-val">{inf['status']}</div></div>
                        <div><div class="card-label">Ket</div><div style="color:{k_clr}; font-weight:bold; font-size:13px;">{ket}</div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
except:
    st.info("Menyinkronkan data...")
