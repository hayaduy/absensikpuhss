import streamlit as st
import requests
from datetime import datetime
import random

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Absensi KPU HSS - Center Pro", layout="wide")

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
    # --- PANTUN BANJAR ---
    "Ma-ambal itik di dalam kandang, itik dikurung di higa pahumaan. Bagawi sarius jangan mahadang, kaina bulik mambawa gajihan.",
    "Iwak karing diulah sangan, dimakan lawan nasi nang hangat. Amun handak jadi palangan, bagawi sarius jangan mangulir bangat.",
    "Ka pasar pargi mamukar lapat, jangan kada ingat mamukar saraba. Bagawi sarius biar hancap dapat, kaina di rumah mahadang kaluarga.",
    "Guring bakulambu takutan di-igut nyamuk, nyamuknya lari kana gubang. Mun bagawi jangan tapi bamamuk, kaina hancap tuha muha mangarubut, Bang!",
    "Iwak sapat iwak papuyu, dimasak karing nyaman rasanya. Bagawi mangat mambari jua, mudahan barakat gasan samuanya.",
    "Balah gumbili diulah kolak, gumbili putih matan pahumaan. Jangan koler jangan manulak, gawian KPU tugas nagaraan.",

    # --- KATA KATA KOCAK & RANDOM ---
    "Bagawi tu hancapi Wal, kaina amun talambat bulik, bini di rumah sudah mahadang lawan parang (parangai masam).",
    "ID sudah dikatik, absen sudah dikirim. Masalah rezeki, Allah sudah ma-atur, tapi amun kadada gawianna, apa nang handak diatur?",
    "Jangan tapi mangulir, kaina rezeki dipatuk hayam urang, ikam nang baisi hayamna urang nang bakulih taluna.",
    "Bagawi ikhlas tu bagus, tapi amun bagawi ikhlas sambal mangantuk, kaina hasilna 'halusinasi'.",
    "Kandangan rami lawan lapat, kita rami lawan gawian hancap. Semangat, Wal!",
    "Mun uyuh bawa mangopi, mun lapar bawa bamakan. Mun koler? Bawa istighfar, kaina dipecat bos hanyar tahu rasa!",
    "Dunia ni sandiwara haja jar, tapi amun gajihan kadada, sandiwara ni jadi film horor.",
    "Fokus ja lawan layar monitor, jangan fokus lawan monitor urang di higa. Kaina takana panyakit 'iri dengki hiri'.",
    "Gawi haja dulu, urusan sugih tu kaina. Nang panting wahini kawa nukar kuota gasan absen.",
    "KPU Melayani! Tapi jangan minta dilayani tarus, bagawi jua saurang!",
    "Absen sudah suksis, hati sudah tanang. Wahini waktunya mancari barakat, lain mancari panyakit hati.",
    "Ingat lah, bagawi tu mancari nafkah, lain mancari masalah lawan kakawanan di kantor.",
    "Amun muha sudah mahuyung, tandanya parlu banyu teh hangat wan guring sapalipisan.",
    "Jangan tapi 'pander ganal', kaina amun gawian kada tuntung, muha nang ganal panyasalan.",
    "Rezeki kada bakal tatukar lawan sandal jepit di masjid, tenang ja!",
    "Bagawi sarius tapi santai, kaya iwak di dalam banyu, kelihatanna tanang tapi ekorna bagarak tarus.",
    "Semangat pagi! Mudahan hari ini kadada drama 'server down' atau 'lampu mati'.",
    "Hidup ni perjuangan, amun handak nyaman guring ja di dalam kandang hayam, kadada nang mangiyau bagawi.",
    "Muha bungas kadada gunana amun koler bagawi, kaina diigut urang muha bungasna.",
    "Lakasi tuntungkan gawian, kaina kita mangopi di wadah Haji Amin!",
    "Bagawi tu kaya naik sapida, amun ampih bakayuh, kaina rabah. Jadi, kayuh tatarus!",
    "Jangan maurus urang nang kada maurus kita, fokus ja lawan tumpukan kartas di hadapan.",
    "Sabar itu baisi batas, tapi mun koler bagawi, bos nang baisi batas kasabaran.",
    "Bismillah hari ini, mudahan barakat, mudahan hancap tuntung, mudahan kawa bulik sungsung!",
    "Absen suksis! Mudahan motivasi ini mambari samangat, lain mambari mangantuk.",
    "Gawi bujur-bujur, jangan 'mencuri tulang'. Kaina tulang ikam nang dicuri kucing amun kadada gajihan buat nukar iwak.",
    "KPU HSS Jaya! Bagawi gumbira, hati himung, dompet kaina kandal jua.",
    "Hidup tu parlu aksi, lain pander haja kaya radio rusak.",
    "Ingat, gajihan mahadang di ujung bulan, koler wahini brarti mahadang panyasalan kaina.",
    "Jangan kada ingat tatawa, biar gawian sagunung, amun tatawa hati jadi ringan (tapi jangan tatawa saurang!).",
    "Mun rasa uyuh, bayangkan muha bini/laki di rumah nang handak minta nukarakan baju hanyar. Langsung samangat!",
    "Bagawi ikhlas karana Allah, tapi jangan lupa minta gajih lawan nagara jua.",
    "Hancapi bagawi, kaina amun sudah tuntung kita bawa bakisahan nang rami-rami.",
    "KPU Melayani, Rakyat Himung, Pegawaina Kenyang (Barakat nasi kotak).",
    "Jangan kalalu banyak 'curhat' di status WA, hancapi gawian tu kaina tuntung saurang.",
    "Maju tarus pantang mundur, mun mundur kaina kana tiang listrik di balakang.",
    "Barakat doa kuitan, gawian sakali ketik langsung tuntung. Mantap banar!",
    "Hari ini mudahan kadada nang pusing, amun pusing bawa maminum obat, jangan maminum banyu rawa.",
    "Tetap rendah hati, biar sudah naik pangkat jangan lali lawan kawan nang masih 'pangkat sarung'.",
    "Giat bagawi, rajin baibadah, kaina masuk surga sambil mambawa SK Pegawai.",
    "Jangan tapi mangulir, kaina gajihan ikam dipotong gasan nukar kopi kakawanan.",
    "Semangat Wal! Dunia mahadang aksi ikam nang harat-harat.",
    "Gawian banyak tu tanda dipercaya urang, amun kadada gawian tandanya ikam 'kadada gunana'. Pilih mana?",
    "Lakasi absen, lakasi gawi, lakasi bulik, lakasi bamakan. Hidup simpal haja!",
    "Hargai waktu kawan, jangan tapi rancak ba-janji palsu kaya calon legislatif.",
    "Mudahan hari ini barakat gasan kita barataan di KPU HSS. Merdeka!",
    "Gawi tuntung, dompet baisi, bini nagih, hati tatap ngeri-ngeri sedap.",
    "Ingat lah, di atas langit masih ada langit, di bawah meja ada 'jatah' (maksudna sampah, sapui lah!).",
    "Bagawi rapi, muha baisi aura cahaya (cahaya gajihan maksudna).",
    "Jangan tapi baperan mun dikiyau bos, kiyauan bos tu musik nang paling merdu gasan masa depan.",
    "Sukses tu kadada nang instan, mie instan haja parlu dimasak dulu banyu panasna.",
    "Kreatif tu mambantu gawian, lain mambantu urang jadi bingung.",
    "Bagawi sarius, panderan jujur, mudahan rezeki masuk kaur (banyak banget).",
    "Tetap samangat, kaina malam minggu kita bawa jalan-jalan ka siring!",
    "Jangan tapi koler, kaina muha ikam jadi kaya iwak karing nang dijemur kapanasan.",
    "Absen sudah, gawi sudah. Wahini waktunya mangopi sambal ma-awas monitor.",
    "Jaga katanangan, jangan panik mun ada audit. Hadapi lawan senyum pait.",
    "Dunia butuh dedikasi ikam, jangan dibari 'kolerisasi' tarus.",
    "KPU HSS Mantap! Gawi ikhlas, barakat sing banyakan. Aamiin!",
    "Jangan kada ingat mandi sungsung, biar muha segar pas dilihat bos.",
    "Bagawi tu niatkan ibadah, biar bulikna baisi pahala wan baisi rupiah.",
    "Gumbira baimbai, sukses baimbai. Hidup KPU HSS!",
    "Cari barakat jangan cari panyakit, bagawi sehat hidup makin nikmat.",
    "Jangan tapi mahulut urang, ulu-uluti ja gawian saurang kaina tuntung.",
    "Maju tatarus, rintangan itu tantangan, lain alasan gasan guring.",
    "Mudahan hari ini lancar, kadada hual, kadada pusing, nang ada cuma himung.",
    "Giat bagawi gasan nagara, niatkan tulus mambangun banua.",
    "Absen dudu, bagawi dudu, bulik dudu. Beres!",
    "Jangan koler Wal, kaina rezeki ikam lari ka wadah urang nang labih rajin.",
    "Semangat pagi KPU HSS! Gawi tuntung, hati sanang, perut kenyang.",
    "Hidup ni perjuangan, jangan gampang luhui di tangah jalan.",
    "Man jadda wajada, siapa nang mangatik absen pasti kawa bagawi!",
    "Rezeki halal mambawa barkah, bagawi rajin mambawa gembira.",
    "Tetap baiman, tatap bagawi, tatap samangat mambangun nagari.",
    "KPU Melayani, HSS Maju, Kita Samua Himung!"
    "Gawi haja dulu, masalah hasil tu kaina Allah nang maatur. Semangat, Wal!",
    "Jangan guring tarus, rezeki tu diigut urang kaina. Lakasi bagawi!",
    "KPU Melayani! Bagawi ikhlas, pahalanya sing banyakan, InsyaAllah.",
    "Biar uyuh, asal barakat. Jaga kesehatan, dangarakan jar mamah!",
    "Jangan tapi banyak hual, fokus haja lawan gawian di higa meja.",
    "Mun handak sugih, bagawi tabat-tabat. Mun handak harat, balajar tarus.",
    "Kada papa lambat, asal salamat wan gawian tuntung barataan.",
    "Hari ini harus labih baik pada samalam. Gas pol!",
    "Ingat, ada kaluarga nang mahadang di rumah. Bagawi nang bujur!",
    "Jujur tu modal utama, jangan tapi mambunguli urang kaina karma.",
    "Bismillah haja dulu, moga-moga barakat gasan sakalaurgaan.",
    "Sabar tu luas, mambari samangat tu wajib. Ayuja, pasti tuntung!",
    "Jangan maraju mun dikiyau bos, hadapi haja lawan senyum manis.",
    "Gawian banyak jangan dibawa pusing, bawa mangopi haja dulu.",
    "Integritas harga mati! Jaga marwah KPU HSS kita, Wal!",
    "Kada usah mambandingkan diri lawan urang lain, fokus ja lawan progres saurang.",
    "Man jadda wajada, siapa nang basungguh-sungguh pasti kawa!",
    "Jangan tapi takutan salah, nang panting wani mambaiki.",
    "Bagawi tu ibadah, niatkan ikhlas karana Allah Ta'ala.",
    "Kandangan baisi carita, kita bagawi gasan nagara.",
    "Amun balum tuntung, jangan bapadah uyuh dulu. Gas tatarus!",
    "Rezeki kada bakal tatukar, nang panting ikhtiar jangan bapagat.",
    "Sungsung bangun, sungsung rezeki. Jangan kalah lawan hayam!",
    "Tetap rendah hati, biar sudah harat jangan sombong lawan kakawanan.",
    "Gawian ngalih amun digawi baimbai jadi ringan. Jaga kakompakan!",
    "Jangan tapi bapikir nang kada-kada, fokus haja mambari nang panyamaian.",
    "Sukses tu kadada nang instan, bakulih uyuh dulu hanyar bakulih hasil.",
    "Masa depan tu cerah amun kita wani mamulai matan wahini.",
    "Gunakan waktu baik-baik, jangan tapi banyak 'te-pang' (santai kelamaan).",
    "Bagawi lawan hati, hasilna pasti mambari sanang hati.",
    "Jangan koler! Dunia mahadang dedikasi kita, Wal!",
    "Ikhlas tu kunci tanang, syukur tu kunci sanang.",
    "Barakat doa kuitan, gawian kita jadi ringan. Jangan kurang ajar!",
    "Jangan takutan gagal, takutan tu mun kada wani mancoba sama sakali.",
    "Fokus, tenang, tuntungkan. Mantap banar!",
    "Satiap langkah kita di KPU, mudahan jadi amal jariyah.",
    "Utamakan kualitas, biar hancap tapi bujur gawi-anya.",
    "Senyum dikit Wal, biar gawian banyak tapi hati tatap rami.",
    "Rezeki halal mambawa katanangan, cari nang barakat haja.",
    "Jaga lisan, jaga perbuatan, bagawi proyeksional (profesional).",
    "Handak sukses? Amalkan disiplin satiap hari.",
    "Dunia ni putaran haja, kadangkala di atas kadangkala di bawah. Sabar!",
    "Jangan marasa harat saurang, kita ni tim baimbaian.",
    "Pintar haja kada cukup mun kada jujur. Jaga amanah!",
    "Giat bagawi, rajin baibadah. Hidup bakal saimbang.",
    "Jangan tapi maurus urang, urusi gawian saurang haja dulu.",
    "Tekad kuat mambalah gunung. Semangat KPU HSS!",
    "Gunakan akal sahat, jangan emosi mun ada masalah.",
    "Hidup ni perjuangan, jangan luhui (lemah) parak garis finish.",
    "Tetap istiqomah dalam kabajikan, hasilnya pasti manis.",
    "Bagawi bujur-bujur, jangan tapi 'mencuri tulang' (malas-malasan).",
    "Kreatif tu gasan mamudahakan gawian, bukan gasan mangalihkan urang.",
    "Amun ada niat, pasti ada jalan. Jalan tatarus!",
    "KPU Melayani, Hati Sanang, Rakyat Tanang.",
    "Bersyukur tarus, Allah bakal manambah nikmat-Nya.",
    "Jangan kalalu baper mun dikritik, mambangun diri tu parlu.",
    "Hargai waktu kawan, jangan tapi maulur-ulur janji.",
    "Semangat pagi! Cari barakat, bukan cari masalah.",
    "Gawi ikhlas, jangan maharap pujian urang tarus.",
    "Amun rami baimbai, gawian nang ngalih jadi himung digawi.",
    "Jadilah inspirasi gasan kakawanan di kantor.",
    "Gunakan teknologi gasan kabaikan, jangan gasan mangulir.",
    "Jangan tapi 'pander haja' (bicara saja), bukti-akan lawan aksi nyata.",
    "Maju tarus, jangan mangeser ka balakang lagi.",
    "Sabar hadapi rintangan, itu bumbu gasan jadi sukses.",
    "Bagawi rapi, hasil mambari hati sanang.",
    "Ingat tujuan awal bagawi di sini, jaga samangatnya!",
    "Kadada kata talambat gasan mambaiki diri.",
    "Pancarkan aura positif, biar kawan-kawan rami jua.",
    "Gawi nang bujur, pander nang jujur.",
    "Hidup tu parlu aksi, bukan sekadar teori haja.",
    "Tetap semangat, weekend dait lagi (sudah dekat)!",
    "Istirahat parlu, tapi jangan 'istirahat tarus'.",
    "Gawi sabuting-sabuting, asalkan tuntung rapi.",
    "KPU Kuat, Demokrasi Sehat. Semangat HSS!",
    "Jangan tapi mangulir, kaina rezeki dipatuk hayam urang.",
    "Fokus lawan solusi, jangan tapi maulur-ulur masalah.",
    "Masa depan di tangan kita saurang, bukan jar urang.",
    "Hargai proses, nikmati hasil kaina di ujung.",
    "Satiap hari ada paluang baru, jangan dibuang sia-sia.",
    "Bagawi baimbai, sukses baimbai. Hidup KPU!",
    "Jangan gampang manyerah, hadapi lawan doa wan usaha.",
    "Tuntungkan gawian, hanyar santai mangopi.",
    "Berani tampil beda dalam kabaikan, itu hanyar harat.",
    "Jaga katanangan, jangan tapi panikan mun ada deadline.",
    "Hidup barkah matan bagawi nang sah-sah haja.",
    "Kaluarga bangga mun kita bagawi bujur-bujur.",
    "Jangan kada ingat badoa sabalum mamulai gawian.",
    "Tetap baiman, tetap bagawi, tetap samangat!",
    "KPU HSS Mantap! Gawi tuntung, hati himung."
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

# --- CSS MEWAH & CENTER ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #4d0a0a 0%, #1a0404 100%); }
    
    div[data-testid="stVerticalBlockBorder"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        border-radius: 20px !important;
    }

    /* Input & Selectbox */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
        background-color: rgba(0, 0, 0, 0.4) !important;
        color: #ffd700 !important;
        border: 1px solid #5e1515 !important;
        border-radius: 12px !important;
    }

    /* TOMBOL CENTER STYLE */
    .stButton {
        display: flex;
        justify-content: center;
    }

    .stButton>button {
        background: linear-gradient(135deg, #ff8c00 0%, #d42020 100%) !important;
        color: white !important;
        font-weight: 800 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        border-radius: 12px !important;
        padding: 10px 30px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(212, 32, 32, 0.4) !important;
    }

    .mon-title {
        text-align: center;
        color: #ffd700;
        font-size: 24px;
        font-weight: 800;
        margin-top: 40px;
    }

    .mobile-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255, 215, 0, 0.15);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
    }
    
    .card-title { color: #ffd700; font-weight: bold; border-bottom: 1px solid rgba(255,215,0,0.2); padding-bottom: 5px; margin-bottom: 8px; }
    .card-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; }
    .card-label { color: #a87b7b; font-size: 10px; text-transform: uppercase; }
    .card-val { color: #ffffff; font-weight: bold; font-size: 13px; }
    
    h1 { color: #ffd700 !important; text-align: center; font-weight: 900 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- POP UP DIALOG ---
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
    # Tombol Tutup di dalam Dialog juga di Tengah
    _, mid_c, _ = st.columns([1, 2, 1])
    with mid_c:
        if st.button("Selesai", use_container_width=True):
            st.rerun()

# --- CONTENT ---
st.markdown("<h1>KPU KABUPATEN HULU SUNGAI SELATAN</h1>", unsafe_allow_html=True)

with st.container(border=True):
    v_id = st.text_input("🆔 ID PEGAWAI", placeholder="Masukkan ID...")
    
    if v_id in DB_PEGAWAI:
        st.markdown(f"<div style='background:rgba(255,215,0,0.1); padding:10px; border-radius:10px; border-left:4px solid #ffd700; color:white; margin-bottom:15px;'><b>Nama:</b> {DB_PEGAWAI[v_id]['nama']}</div>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        jenis = st.selectbox("📅 JENIS ABSENSI", ["Masuk", "Pulang", "Cuti", "Izin", "Off"])
    
    status_val = ""
    tgl_mulai = None
    with col_b:
        if jenis == "Masuk":
            status_val = st.selectbox("📍 STATUS KEHADIRAN", ["WFO", "WFH", "Dinas Luar", "Piket Pagi", "Piket Malam"])
        elif jenis == "Cuti":
            tgl_mulai = st.date_input("Mulai")
        else:
            st.markdown("<br>", unsafe_allow_html=True)

    uraian = output = ""
    if jenis == "Pulang":
        uraian = st.text_area("📋 URAIAN TUGAS")
        output = st.text_area("📦 OUTPUT")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # MELETAKKAN TOMBOL DI TENGAH
    left_c, center_c, right_c = st.columns([1, 2, 1])
    with center_c:
        if st.button("KIRIM DATA ABSENSI", use_container_width=True):
            if v_id in DB_PEGAWAI:
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
                    st.error("Gagal!")
            else:
                st.error("ID tidak valid!")

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
                        <div><div class="card-label">Ket</div><div style="color:{k_clr}; font-size:12px; font-weight:bold;">{ket}</div></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
except:
    st.info("Menyinkronkan data...")
