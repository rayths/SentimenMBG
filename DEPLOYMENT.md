# 🚀 Panduan Deployment ke Streamlit Cloud

## 📋 Persiapan

### 1. Push ke GitHub
Pastikan semua file sudah di-push ke repository GitHub Anda.

### 2. Daftar di Streamlit Cloud
- Kunjungi [share.streamlit.io](https://share.streamlit.io)
- Login dengan akun GitHub

## 🔐 Setup Google Sheets untuk Penyimpanan Data Persisten

Karena filesystem Streamlit Cloud bersifat ephemeral (tidak permanen), data yang disimpan di CSV lokal akan hilang saat app restart. Gunakan Google Sheets untuk penyimpanan permanen.

### Langkah 1: Buat Google Cloud Project

1. Kunjungi [Google Cloud Console](https://console.cloud.google.com)
2. Buat project baru atau pilih project yang ada
3. Enable **Google Sheets API**:
   - Pergi ke "APIs & Services" > "Library"
   - Cari "Google Sheets API"
   - Klik "Enable"

### Langkah 2: Buat Service Account

1. Di Google Cloud Console, pergi ke "APIs & Services" > "Credentials"
2. Klik "Create Credentials" > "Service Account"
3. Isi nama service account (contoh: `streamlit-app`)
4. Klik "Create and Continue"
5. Skip role assignment, klik "Continue"
6. Klik "Done"

### Langkah 3: Download Credentials

1. Klik service account yang baru dibuat
2. Pergi ke tab "Keys"
3. Klik "Add Key" > "Create new key"
4. Pilih "JSON" dan klik "Create"
5. File JSON akan ter-download, **simpan dengan aman!**

### Langkah 4: Buat Google Spreadsheet

1. Buat Google Spreadsheet baru di [sheets.google.com](https://sheets.google.com)
2. Beri nama (contoh: "MBG Sentiment Data")
3. Buat 2 sheet:
   - Sheet 1: Rename ke `predictions`
   - Sheet 2: Buat sheet baru, rename ke `feedback`
4. Di sheet `predictions`, tambahkan header di row 1:
   ```
   timestamp | original_text | cleaned_text | predicted_label | confidence | prob_negatif | prob_netral | prob_positif
   ```
5. Di sheet `feedback`, tambahkan header di row 1:
   ```
   timestamp | original_text | predicted_label | is_correct | correct_label | feedback_comment
   ```

### Langkah 5: Share Spreadsheet ke Service Account

1. Buka file JSON credentials yang di-download
2. Cari field `client_email` (contoh: `streamlit-app@project-id.iam.gserviceaccount.com`)
3. Di Google Spreadsheet, klik "Share"
4. Paste email service account tersebut
5. Pilih "Editor" dan klik "Send"
6. Copy URL spreadsheet untuk digunakan nanti

### Langkah 6: Setup Streamlit Secrets

1. Di Streamlit Cloud, buka app Anda
2. Klik "⚙️ Settings" > "Secrets"
3. Tambahkan secrets dalam format TOML:

```toml
# Streamlit Secrets Configuration

# URL Google Spreadsheet
spreadsheet_url = "https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit"

# Google Cloud Service Account Credentials
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@project-id.iam.gserviceaccount.com"
client_id = "123456789"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."
```

> **⚠️ PENTING:** Salin semua field dari file JSON credentials ke dalam `[gcp_service_account]`

### Langkah 7: Install Dependencies

Pastikan `gspread` dan `google-auth` ada di `requirements.txt`:

```
gspread>=5.0.0
google-auth>=2.0.0
```

## 🔄 Deploy Aplikasi

1. Di Streamlit Cloud, klik "New app"
2. Pilih repository GitHub Anda
3. Pilih branch (biasanya `main`)
4. Masukkan path ke `app.py`
5. Klik "Deploy"

## ✅ Verifikasi

1. Buka aplikasi yang sudah di-deploy
2. Lakukan analisis sentimen
3. Cek Google Spreadsheet, data harus tersimpan di sheet `predictions`
4. Berikan feedback
5. Cek sheet `feedback`, data feedback harus tersimpan

## 🔧 Troubleshooting

### Error: "gspread not found"
- Pastikan `gspread` ada di `requirements.txt`
- Restart aplikasi

### Error: "Permission denied"
- Pastikan spreadsheet sudah di-share ke service account email
- Pastikan service account memiliki role "Editor"

### Error: "Worksheet not found"
- Pastikan nama sheet persis `predictions` dan `feedback` (case-sensitive)

### Data tidak tersimpan
- Cek Streamlit logs untuk error detail
- Verifikasi semua secrets sudah diisi dengan benar

## 📝 Catatan Penting

- **Jangan commit file credentials JSON ke repository!**
- Gunakan `.gitignore` untuk exclude file sensitif
- Secrets di Streamlit Cloud aman dan terenkripsi
- Data di Google Sheets bisa di-export ke CSV/Excel kapan saja

## 🆓 Alternatif Gratis Lainnya

Jika tidak ingin setup Google Sheets, alternatif lain:

1. **Supabase** - PostgreSQL database gratis
2. **PlanetScale** - MySQL database gratis
3. **MongoDB Atlas** - NoSQL database gratis
4. **Airtable** - Spreadsheet-database hybrid

---

**© 2025 - Analisis Sentimen MBG | Deployment Guide**
