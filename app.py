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
    "Jangan tapi dipikirakan banar gawian tu, kaina hancap tuha muha kaya iwak karing talambat diangkat.",
    "Rezeki tu kaya jodoh, dicari ngalih, dihadang kada datang. Ayuja, nang panting sudah absen!",
    "Adakah urang nang maulah ikam lihum saurangan pas malihat layar HP?",
    "Sudahkah mambari habar 'sudah bamakan kah' lawan urang nang di hati?",
    "Kira-kira, sapa urang nang pertama kali ikam ingat pas bangun guring tadi?",
    "Apa nang labih nyaman: mandangar suara banyu hujan kah suara sidin?",
    "Sudahkah mahulut-i kawan nang lagi kasmaran sapanjangan hari ini?",
    "Kira-kira, adakah lagu nang maulah ikam kaganangan lawan seseorang?",
    "Apa nang labih manis: dodol Kandangan kah lihum manis sidin?",
    "Sudahkah mamanderi hal nang indah-indah lawan urang nang disayang?",
    "Hal apa nang paling maulah hati 'marikit' pas malihat sidin lihum?",
    "Kira-kira, adakah niat handak manukari wadai sagan urang nang spesial?",
    "Sudahkah manukuni habar urang nang paling ikam takuti kaina kaganangan?",
    "Apa kabaikan sidin nang paling maulah ikam tarasa 'paling beruntung'?",
    "Kira-kira, wadai apa nang paling pas dimakan badua sambal bakisahan?",
    "Sudahkah marasa tanang pas tahu sidin baik-baik haja di sana?",
    "Apa nang labih rami: bajalanan badua ka pasar kah ka pinggir sungai?",
    "Kira-kira, sapa kawan nang paling tahu rahasia cinta ikam wahini?",
    "Sudahkah mambari pujian 'bungas banar ikam hari ini' lawan sidin?",
    "Apa nang maulah hati tarasa dingin pas lagi parak lawan urang nang dicintai?",
    "Kira-kira, mun ada waktu luang, handak mambawa sidin bajalan ka mana?",
    "Sudahkah manikmati kadiaman nang indah sambal mangingat sidin?",
    "Apa hal receh matan sidin nang maulah ikam kada kawa ampih lihum?",
    "Kira-kira, warna baju apa nang paling katuju amun dipakai ulih sidin?",
    "Sudahkah manyapa 'semangat sayang' sungsung tadi sabalum absen?",
    "Apa nang labih nyaman: minum teh es badua kah es campur baimbaian?",
    "Kira-kira, carita cinta apa nang paling rami dipandirakan lawan kawan?",
    "Sudahkah merapikan muha di cermin sungsung tadi sagan manamu-i sidin?",
    "Hal apa nang maulah kita marasa rami banar kasmaran di banua urang?",
    "Kira-kira, mun ada rezeki labih, handak manukari hadiah apa sagan sidin?",
    "Sudahkah mahirup udara segar sambal mambayangkan masa depan badua?",
    "Apa nang maulah kita marasa 'hidup' banar pas tangan dijapa ulih sidin?",
    "Kira-kira, pantun cinta apa nang handak disambat sagan sidin kaina?",
    "Sudahkah basantai sapalipisan sambil mahayal ba-ulur tangan lawan sidin?",
    "Apa kenangan paling manis pas pertama kali batamu lawan sidin bahari?",
    "Kira-kira, mun main bal, handak dilihum ulih sidin matan pinggir lapangan?",
    "Sudahkah manakuni habar sidin nang mungkin lagi mahadang kiyauan?",
    "Apa hal sederhana nang maulah dunya tarasa penuh bunga hari ini?",
    "Kira-kira, amun kaganangan, banyu apa nang paling hancap maulah hati segar?",
    "Sudahkah manyiapakan carita rami sagan dikisahakan lawan sidin pas istirahat?",
    "Apa nang labih asik: bakisah cinta di warung kah atawa di teras rumah sidin?",
    "Kira-kira, aroma minyak harum sidin nang mana nang paling mangingat?",
    "Sudahkah malihat poto sidin di galeri HP sagan mambuang rasa rindu?",
    "Apa hal nang paling maulah ikam marasa 'paling disayang' ulih sidin?",
    "Kira-kira, amun bajalanan badua, handak ka Loksado kah ka pantai?",
    "Sudahkah mambarasihi kendaraan sagan mambawa sidin jalan sore kaina?",
    "Apa satu kata cinta nang handak disambat sagan sidin hari ini?",
    "Kira-kira, gaya rambut sidin nang mana nang paling maulah hati dag-dig-dug?",
    "Sudahkah manyisihakan waktu sagan manalipun sidin walau cuma sapalipisan?",
    "Apa nang maulah kita marasa 'bersyukur' baisi pasangan nang sabar banar?",
    "Kira-kira, amun nukar pentol badua, labih nyaman pakai saos kah kecap?",
    "Sudahkah mangingat amun cinta tu parlu dijaga kaya manjaga tanaman?",
    "Apa hal nang maulah kita marasa bangga baisi sidin nang urang banua jua?",
    "Kira-kira, sapaan apa nang paling mambari samangat matan suara sidin?",
    "Sudahkah ba-istirahat dudu sambil mangingat kenangan manis malam tadi?",
    "Apa nang labih rami: bamainan mata kah atawa bamainan lihum cinta?",
    "Kira-kira, buah tangan apa nang paling maulah sidin lihum gumbira?",
    "Sudahkah bapikir handak mambari kabaikan cinta apa sagan sidin hari ini?",
    "Apa nang maulah kita tatap handak lihum pas sidin manyambati kita?",
    "Kira-kira, amun ba-isi waktu luang, handak bajanji jalan kah bakisah?",
    "Sudahkah manjaga katanangan hati pas sidin lagi sibuk wan gawian saurangan?",
    "Apa hal nang maulah ikam marasa 'paling sahat' pas sidin parak di higa?",
    "Kira-kira, iwak masak habang apa nang paling sidin katuju amun kita bawakan?",
    "Sudahkah mambari samangat 'Ikam harat banar' lawan sidin hari ini?",
    "Apa nang labih asik: mandangar sidin banyanyi kah mandangar sidin banyaring?",
    "Kira-kira, mun bajalan ka pasar badua, barang apa nang paling sidin cari?",
    "Sudahkah manikmati satiap detik pas sidin manyuapi makan sungsung tadi?",
    "Apa hal nang maulah ikam marasa 'paling harat' di mata sidin hari ini?",
    "Kira-kira, amun baisi duit banyakan, handak mambawa sidin makan ka mana?",
    "Sudahkah manakuni parasaan sidin sapanjangan malalui hari nang cerah ni?",
    "Kira-kira, carita lucu sidin nang mana nang paling ma-ulah hati lihum?",
    "Sudahkah marasa cukup tanang sagan malalui hari sungsung mahadang sidin?",
    "Apa hal nang maulah kita katuju banar lawan lihum sidin pas sore hari?",
    "Kira-kira, sapa urang nang paling handak kita bawakan katupat Kandangan?",
    "Akaiii, rabah waluh",
    "Jangan tamakan janji,sidin bahanu ada wisanya",
    "Apa nang labih rami: ma-awas sidin bagawi kah ma-awas sidin guring?",
    "Kadada nang lebih manis selain senyuman pian",
    "Kadada nang labih manis selain lihum pian hari ini.",
    "Dasar lain mun sudah gajihan nih, tihang listrik gin dilihumi",
    "Biar dodol Kandangan manis rasanya, tatap kalah lawan manisnya lihum pian.",
    "Ikan sepat ikan papuyu, napa daya hati ulun sudah manyangkut di pian jua.",
    "Amun pian naya gula, ulun rila jadi samutnya nang handak parak tatarus.",
    "Kandangan rami lawan ketupatnya, hati ulun rami lawan bayangan pian di dalamnya.",
    "Biar hari panas manggantang, malihat pian lewat langsung tarasa dingin hati ulun.",
    "Pian ni kaya wadai bingka, manisnya pas, maulah ulun handak tarus.",
    "Adakah urang nang labih bungas matan pian? Kayanya kadada lagi di dunya ni.",
    "Sudahkah pian lihum hari ini? Soalnya lihum pian tu energi gasan ulun.",
    "Biar dunya baputar hancap, hati ulun tatap diam di wadah pian haja.",
    "Pian ni kaya banyu teh hangat, mambari tanang pas hati ulun lagi sungsung.",
    "Kira-kira pian baisi peta lah? Soalnya ulun sasat di dalam hati pian.",
    "Jangan tapi rancak lihum, kaina samut banyakan mahurung pian karana kalaluan manis.",
    "Biar ulun kada sugih harta, nang panting ulun sugih kasih sayang gasan pian.",
    "Apa nang labih indah matan matahari timbul? Jawabannya: pas pian bangun guring.",
    "Pian ni kaya lapat, mambungkus rapat rasa sayang ulun sagan pian saurangan.",
    "Adakah obat sagan kaganangan? Soalnya ulun kaganangan lawan pian satiap detik.",
    "Biar iwak karing masin rasanya, amun makanna lawan pian tatap tarasa manis.",
    "Pian ni kaya sasirangan, motifnya indah, maulah hati ulun katarikan tatarus.",
    "Sudahkah pian tahu amun pian tu alasan ulun samangat barangkat sungsung?",
    "Kira-kira pian baisi lem lah? Soalnya ulun handak marikit tatarus di higa pian.",
    "Biar urang manyambat ulun gila, nang panting ulun gila karana cinta lawan pian.",
    "Pian ni kaya banyu sungai barito, mangalir tatarus kasih sayang ulun kadada ampihna.",
    "Apa kabaar bidadari dunya? Mudahan tatarus lihum gasan ulun hari ini.",
    "Kira-kira amun ulun dadi raja, pian rila lah jadi ratunya di hati ulun?",
    "Pian ni kaya wadai apam, amun dimakan mambari kanyangan, amun dilihumi mambari katanangan.",
    "Jangan tapi jauh-jauh, kaina ulun sasat mancari jalan bulik ka hati pian.",
    "Biar bintang banyakan di langit, tatap pian nang paling mancahaya di mata ulun.",
    "Pian ni kaya pantun Banjar, rami didangar, maulah lihum kadada ampihna.",
    "Apa nang maulah hari ini cerah? Jawabannya: karana ada pian di higa ulun.",
    "Kira-kira pian baisi kunci lah? Soalnya hati ulun sudah takunci sagan pian haja.",
    "Biar jalan ka Loksado banyulak, ulun rila malaluinya amun tujuannya wadah pian.",
    "Pian ni kaya banyu kalapa sungsung, segar rasanya, maulah hati tarasa muda tatarus.",
    "Jangan sadih Wal, pian tu permata nang paling harat nang suah ulun tamui.",
    "Apa nang labih harum matan kambang melati? Jawabannya: aroma dangan pian parak ulun.",
    "Kira-kira pian baisi cermin lah? Ulun handak malihat masa depan ulun di mata pian.",
    "Pian ni kaya nasi kuning, sungsung dicari, maulah samangat mamulai hari.",
    "Jangan takutan sasat, ulun rila jadi kompas sagan jalan hidup pian sapanjangan.",
    "Biar dunya ni sasak, tatap ada ruang nang luas sagan pian di dalam hati ulun.",
    "Pian ni kaya wadai cincin, bulat cintanya, kadada ujung wan pangkalnya sagan pian.",
    "Apa nang labih rami matan pasar terapung? Jawabannya: pas kita badua bakisahan rami.",
    "Kira-kira pian baisi bantal lah? Hati ulun handak basandat dudu di higa pian.",
    "Pian ni kaya iwak haruan, ganal manfaatnya, labih ganal lagi rasa sayang ulun.",
    "Jangan tapi banyaring pander, kaina urang tahu amun pian tu ampun ulun sa-urangan.",
    "Apa nang labih tanang matan malam sunyi? Jawabannya: pas ulun mangingat lihum pian.",
    "Kira-kira pian katuju cokelat kah? Soalnya lihum pian labih manis matan itu.",
    "Pian ni kaya lampu jalan, mambari tarang pas dunya ulun lagi kadap.",
    "Jangan tapi rancak mangantuk, kaina pian kada malihat amun ulun lagi ma-awas pian.",
    "Apa nang labih hebat matan pahlawan? Jawabannya: pian nang kawa manakluk-akan hati ulun.",
    "Kira-kira pian baisi kacamata lah? Ulun silau malihat kbungasan pian hari ini.",
    "Pian ni kaya banyu hujan, mambari sejuk pas hati ulun lagi kapanasan.",
    "Jangan sadih, lihum pian tu obat nang paling ampuh sagan samua panyakit hati ulun.",
    "Apa nang labih akrab matan parakawanan? Jawabannya: kita badua nang handak baimbaian tatarus.",
    "Kira-kira pian baisi payung lah? Ulun handak manjaga pian matan badai dunya.",
    "Pian ni kaya wadai klemben, lembut hatinya, maulah ulun sayang tatarus.",
    "Jangan tapi ma-urus urang lain, urusi ja hati ulun nang sudah jadi ampun pian ni.",
    "Apa nang labih nyaman matan guring sungsung? Jawabannya: mandangar suara pian manyapa.",
    "Kira-kira pian baisi jam tangan lah? Supaya pian tahu waktu sagan manyayangi ulun.",
    "Pian ni kaya jembatan rumpiang, manghubung-akan mimpi ulun lawan kanyataan.",
    "Jangan takutan, ulun tatap di balakang pian sagan mambari samangat satiap hari.",
    "Apa nang labih segar matan limau kuit? Jawabannya: pas pian manyambat ngaran ulun.",
    "Kira-kira pian baisi pulpen lah? Ulun handak manulis ngaran kita badua di langit.",
    "Pian ni kaya wadai rangai, gurih panderannya, maulah ulun katuju tatarus.",
    "Jangan tapi koler lihum, kaina dunya tarasa kadap amun pian banyanyat haja.",
    "Apa nang labih luas matan pahumaan? Jawabannya: rasa rindu ulun sagan pian.",
    "Kira-kira pian baisi sapatu lah? Handak ulun bawa bajalanan ka pelaminan kaina.",
    "Pian ni kaya banyu teh manis, amun kadada pian, hidup ulun tarasa kelat.",
    "Jangan tapi pusing, sandatakan ja kapala pian ka bahu ulun nang kuat ni.",
    "Apa nang labih indah matan pelangi? Jawabannya: garis lihum di muha pian.",
    "Kira-kira pian baisi rahasia lah? Rahasia ulun cuma sabuting: ulun sayang lawan pian.",
    "Pian ni kaya puhun rambutan, manis buahnya, maulah urang handak mamutik tatarus.",
    "Jangan tapi rancak maraju, kaina bungas pian hilang dimakan om saldoz.",
    "Amun paman galon datang, telponi om saldoz",
    "Apa nang labih rami matan bakisahan? Jawabannya: pas kita barencana sagan masa depan.",
    "Kira-kira pian baisi dompet lah? Ulun handak manyimpan poto pian di dalamnya tatarus.",
    "Pian ni kaya iwak papuyu sangan, garing panderannya, maulah parut hati ulun lapar cinta.",
    "Jangan takutan garing, lihum pian tu vitamin nang paling harat sagan ulun.",
    "Apa nang labih harum matan parpuman? Jawabannya: aroma kasih sayang matan pian.",
    "Kira-kira pian baisi buku lah? Ulun handak manjadi bagian matan carita hidup pian.",
    "Jangan tapi rancak bajalan sa-urangan, kaina urang sangka pian bidadari sasat.",
    "Apa nang labih syahdu matan suara biola? atau pas pian mangiyau ngaran ulun kah.",
    "Kira-kira pian baisi kancing lah?.",
    "Pian ni kaya wadai lupis, marikit cintanya, kadada nang kawa mamisahkan.",
    "Jangan tapi takutan lawan malam, ulun rila jadi bintang nang manemani pian guring.",
    "Apa nang labih mantap matan soto Banjar? Jawabannya: pas kita makan baimbaian badua.",
    "Kira-kira pian baisi payung lah? Handak ulun pakai sagan malindungi pian matan panasna dunya.",
    "Pian ni kaya embun pagi, segar malihatnya, maulah samangat mamulai hari nang pina pina babanyuan.",
    "Jangan tapi koler bagawi, bayangkan kaina kita nukar baju pangantin baimbaian hen.",
    "Apa nang labih abadi matan sajarahkah atau rasa sayang ulun sagan pian sapanjangan.",
    "Kira-kira pian lihum lah mambaca ini? Mun iya, brarti ulun suksis maulah hari pian sanang."
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
