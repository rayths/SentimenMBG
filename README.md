# 🍽️ Analisis Sentimen Program Makan Bergizi Gratis (MBG)

Aplikasi web untuk menganalisis sentimen opini publik terhadap program **Makan Bergizi Gratis (MBG)** menggunakan model Deep Learning Bi-GRU.

## 📋 Fitur

- ✅ Analisis sentimen real-time (Positif, Netral, Negatif)
- ✅ Preprocessing teks otomatis (cleaning, normalisasi, stopword removal)
- ✅ Visualisasi probabilitas dengan bar chart interaktif
- ✅ Word cloud dari teks input
- ✅ Confidence score untuk setiap prediksi
- ✅ Detail langkah-langkah preprocessing
- ✅ Contoh komentar yang bisa langsung digunakan
- ✅ UI/UX responsif (mendukung Dark & Light theme)
- ✅ Modular code architecture
- ✅ **Penyimpanan data** - Menyimpan history prediksi ke CSV/Google Sheets
- ✅ **Sistem feedback** - User dapat memberikan feedback untuk meningkatkan model
- ✅ **Cloud-ready** - Siap deploy ke Streamlit Cloud dengan penyimpanan persisten

## 🛠️ Instalasi

### 1. Clone atau Download Repository

```bash
cd SentimenMBG
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Siapkan Model dan Tokenizer

Pastikan file berikut tersedia di folder `models/`:

```
models/
├── Best_Oversampled_Model.keras    # Model Bi-GRU
├── tokenizer.pickle                # Tokenizer Keras
└── history_os.pickle               # Training history (opsional)
```

## 🚀 Menjalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada alamat: `http://localhost:8501`

## 📁 Struktur Proyek

```
SentimenMBG/
├── app.py                  # Entry point aplikasi Streamlit
├── config.py               # Konfigurasi konstanta dan variabel
├── preprocessing.py        # Modul preprocessing teks
├── model_utils.py          # Utilitas loading model dan prediksi
├── ui_components.py        # Komponen UI Streamlit
├── data_storage.py         # Modul penyimpanan data (CSV & Google Sheets)
├── requirements.txt        # Daftar dependencies
├── README.md               # Dokumentasi
├── DEPLOYMENT.md           # Panduan deployment ke Streamlit Cloud
├── .gitignore              # File yang diabaikan git
├── data/                   # Folder penyimpanan data lokal
│   ├── .gitkeep
│   ├── sentiment_history.csv   # History prediksi (auto-generated)
│   └── user_feedback.csv       # Feedback user (auto-generated)
└── models/
    ├── Best_Oversampled_Model.keras    # Model Bi-GRU terlatih
    ├── tokenizer.pickle                # Tokenizer Keras
    └── history_os.pickle               # Training history
```

## 📊 Alur Preprocessing

Aplikasi menggunakan pipeline preprocessing yang sama dengan saat training:

1. **Case Folding** - Mengubah teks ke huruf kecil
2. **Cleaning** - Menghapus URL, @username, #hashtag
3. **Hapus Karakter Non-Alfabet** - Hanya menyisakan huruf a-z dan spasi
4. **Hapus Spasi Berlebih** - Menormalkan whitespace
5. **Normalisasi Singkatan** - Mengubah singkatan ke bentuk baku (yg → yang, gak → tidak, mbg → makan bergizi gratis, dll)
6. **Stopword Removal** - Menghapus kata umum (yang, di, ke, dari, dll)
7. **Hapus Kata Pendek** - Menghapus kata dengan panjang ≤ 1 karakter
8. **Tokenisasi** - Mengubah teks ke sequence angka (vocab_size=15000)
9. **Padding** - Menyamakan panjang sequence (maxlen=60, padding='post', truncating='post')

## 🏷️ Label Sentimen

| Label | Emoji | Deskripsi |
|-------|-------|-----------|
| Positif | 😊 🟢 | Opini mendukung/positif terhadap program MBG |
| Netral | 😐 ⚪ | Opini netral/tidak memihak |
| Negatif | 😠 🔴 | Opini menentang/negatif terhadap program MBG |

## 🔧 Konfigurasi

Konfigurasi dapat diubah di file `config.py`:

```python
VOCAB_SIZE = 15000                      # Ukuran vocabulary
MAX_LEN = 60                            # Panjang maksimal sequence
NUM_CLASSES = 3                         # Jumlah kelas sentimen
LABEL_MAP = {0: "Negatif", 1: "Netral", 2: "Positif"}
```

## 📝 Contoh Penggunaan

1. Buka aplikasi di browser
2. Masukkan komentar tentang program MBG, contoh:
   - "Program MBG sangat membantu anak-anak Indonesia untuk mendapatkan gizi yang baik"
   - "Saya ragu program ini bisa berjalan dengan baik, khawatir korupsi"
   - "Semoga program makan bergizi gratis ini bisa berkelanjutan"
3. Atau klik tombol "Contoh" untuk menggunakan contoh komentar
4. Klik tombol "🔍 Analisis Sentimen"
5. Lihat hasil prediksi dan visualisasi

## 🤖 Teknologi yang Digunakan

- **Python 3.10+** - Bahasa pemrograman
- **TensorFlow/Keras** - Framework Deep Learning
- **Streamlit** - Web Framework
- **Plotly** - Visualisasi interaktif
- **WordCloud** - Visualisasi kata
- **Bidirectional GRU** - Arsitektur model

## 🏗️ Arsitektur Modul

| Modul | Deskripsi |
|-------|-----------|
| `app.py` | Entry point utama, orchestration aplikasi |
| `config.py` | Konstanta, paths, label mapping, contoh komentar |
| `preprocessing.py` | `TextPreprocessor` class dengan pipeline preprocessing |
| `model_utils.py` | `SentimentAnalyzer` class untuk prediksi |
| `ui_components.py` | Fungsi-fungsi render UI Streamlit |
| `data_storage.py` | `DataManager` class untuk penyimpanan data |

## 💾 Penyimpanan Data

Aplikasi menyimpan data dalam 2 file:

1. **sentiment_history.csv** - History semua prediksi
   - Timestamp, teks original, teks cleaned, label, confidence, probabilitas

2. **user_feedback.csv** - Feedback dari user
   - Timestamp, teks, prediksi, apakah benar, label yang benar, komentar

### Untuk Development (Local)
Data disimpan di folder `data/` dalam format CSV.

### Untuk Production (Streamlit Cloud)
Gunakan Google Sheets untuk penyimpanan persisten. Lihat [DEPLOYMENT.md](DEPLOYMENT.md) untuk panduan lengkap.

## 👥 Tim Pengembang

**Tugas Besar Deep Learning - Kelompok 9**  
- 👤 [Raid Muhammad Naufal](https://github.com/rayths)
- 👤 [Najla Juwairia](https://github.com/najlajuwa)
- 👤 [Tessa Kania Sagala](https://github.com/username3)

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademik.

---

**© 2025 - Analisis Sentimen MBG Kelompok 9 | Deep Learning Project**
