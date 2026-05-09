import streamlit as st
import requests
from datetime import datetime
import random
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Absensi KPU HSS", layout="wide")

# Custom CSS untuk efek Maroon Glass & UI Modern
st.markdown("""
    <style>
    .main { background-color: #2e0505; }
    .stApp { background: linear-gradient(to bottom, #2e0505, #1a0404); }
    h1, h2, h3 { color: #ff9d00 !important; font-family: 'Segoe UI'; }
    .stButton>button { 
        background-color: #ff6a00; color: white; border-radius: 10px; 
        width: 100%; font-weight: bold; border: none; height: 3em;
    }
    .stButton>button:hover { background-color: #e65c00; border: none; color: white; }
    div[data-baseweb="select"] > div { background-color: #1a0404 !important; color: white !important; border: 1px solid #5e1515; }
    input { background-color: #1a0404 !important; color: white !important; border: 1px solid #ff9d00 !important; }
    textarea { background-color: #1a0404 !important; color: white !important; border: 1px solid #5e1515 !important; }
    .status-card { 
        background-color: #330808; padding: 15px; border-radius: 15px; 
        border: 1px solid #3d0a0a; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA PEGAWAI & URL ---
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

# --- LOGIKA DASHBOARD ---
st.title("🏛️ KPU KABUPATEN HULU SUNGAI SELATAN")
st.caption("O'lia Software Development v1.0 | Web responsive")

# --- FORM ABSENSI ---
with st.container():
    st.markdown("### 📝 Form Absensi Digital")
    c1, c2, c3 = st.columns([1, 2, 2])
    
    with c1:
        input_id = st.text_input("ID PEGAWAI", placeholder="Cth: 6")
    
    nama_pegawai = ""
    if input_id in DB_PEGAWAI:
        nama_pegawai = DB_PEGAWAI[input_id]['nama']
        with c2:
            st.markdown(f"<br><h4 style='color:white;'>{nama_pegawai}</h4>", unsafe_allow_html=True)
    
    with c3:
        jenis = st.selectbox("JENIS ABSENSI", ["Pilih Jenis", "Masuk", "Pulang", "Cuti", "Off Piket", "Izin"])

    # Input Dinamis
    status_khusus = ""
    tgl_mulai = tgl_selesai = ""
    uraian = output = ""

    if jenis == "Masuk":
        status_khusus = st.radio("Status Kehadiran", ["WFO", "WFH", "Dinas Luar", "Piket Pagi", "Piket Malam"], horizontal=True)
    elif jenis == "Cuti":
        col_t1, col_t2 = st.columns(2)
        tgl_mulai = col_t1.date_input("Mulai Cuti")
        tgl_selesai = col_t2.date_input("Sampai Cuti")
    elif jenis == "Pulang":
        col_u1, col_u2 = st.columns(2)
        uraian = col_u1.text_area("Uraian Tugas Hari Ini", height=100)
        output = col_u2.text_area("Output / Hasil Tugas", height=100)

    if st.button("KIRIM ABSENSI"):
        if input_id not in DB_PEGAWAI:
            st.error("ID Pegawai tidak ditemukan!")
        elif jenis == "Pilih Jenis":
            st.warning("Silakan pilih jenis absensi terlebih dahulu.")
        else:
            p = DB_PEGAWAI[input_id]
            now = datetime.now()
            data = {
                "sheetName": p["sheet"], "jenis": jenis, "nama": p["nama"],
                "nip": p["nip"], "unit": p["unit"], "status": status_khusus or jenis,
                "tanggal": now.strftime("%d/%m/%Y"), 
                "hari": ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][now.weekday()],
                "tglMulai": tgl_mulai.strftime("%d/%m/%Y") if tgl_mulai else "",
                "tglSelesai": tgl_selesai.strftime("%d/%m/%Y") if tgl_selesai else "",
                "uraian": uraian, "output": output
            }
            
            try:
                res = requests.post(URL_APPS_SCRIPT, params=data, timeout=15)
                st.success(f"Berhasil! {res.text}")
                st.info(f"💡 Motivasi: {random.choice(MOTIVASI)}")
                st.balloons()
            except:
                st.error("Gagal terhubung ke server Google.")

st.divider()

# --- MONITORING (REAL-TIME) ---
st.markdown("### 📊 Monitoring Kehadiran Hari Ini")

@st.cache_data(ttl=60) # Cache 60 detik agar tidak berat
def fetch_monitoring():
    try:
        response = requests.get(URL_APPS_SCRIPT, timeout=10)
        return response.json()
    except:
        return {}

monitor_data = fetch_monitoring()

if monitor_data:
    # Header Tabel
    h_id, h_nama, h_masuk, h_pulang, h_stat, h_ket = st.columns([1, 4, 2, 2, 2, 3])
    h_id.write("**ID**")
    h_nama.write("**NAMA PEGAWAI**")
    h_masuk.write("**MASUK**")
    h_pulang.write("**PULANG**")
    h_stat.write("**STATUS**")
    h_ket.write("**KETERANGAN**")

    for i in range(1, 31):
        p_id = str(i)
        if p_id in DB_PEGAWAI:
            p = DB_PEGAWAI[p_id]
            info = monitor_data.get(p["sheet"], {"jamMasuk": "-", "jamPulang": "-", "status": "-", "keterangan": "Belum Absen"})
            
            # Warna Baris Genap
            bg_color = "#330808" if i % 2 == 0 else "transparent"
            
            with st.container():
                st.markdown(f"""<div style='background-color:{bg_color}; padding:5px; border-radius:5px;'>""", unsafe_allow_html=True)
                c_id, c_nama, c_masuk, c_pulang, c_stat, c_ket = st.columns([1, 4, 2, 2, 2, 3])
                
                c_id.write(p_id)
                c_nama.write(f"**{p['nama']}**")
                c_masuk.write(f"**{info['jamMasuk']}**")
                c_pulang.write(f"**{info['jamPulang']}**")
                c_stat.write(info['status'])
                
                # Warna Keterangan
                ket = info['keterangan'].upper()
                color = "#00ff88" # Hijau
                if any(x in ket for x in ["IZIN", "CUTI", "OFF"]): color = "#ffff00"
                elif "DINAS" in ket: color = "#e0b0ff"
                elif "BELUM" in ket: color = "#ff4444"
                
                c_ket.markdown(f"<span style='color:{color}; font-weight:bold;'>{ket}</span>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("Data monitoring belum tersedia. Silakan refresh halaman.")
