# ==================== KONFIGURASI MODEL ====================
VOCAB_SIZE = 15000
MAX_LEN = 60
NUM_CLASSES = 3

# ==================== PATH MODEL & TOKENIZER ====================
MODEL_PATH = 'models/Best_Oversampled_Model.keras'
TOKENIZER_PATH = 'models/tokenizer.pickle'

# Fallback paths (jika tidak ada di folder models/)
MODEL_PATH_FALLBACK = 'Best_Oversampled_Model.keras'
TOKENIZER_PATH_FALLBACK = 'tokenizer.pickle'

# ==================== LABEL MAPPING ====================
LABEL_MAP = {0: "Negatif", 1: "Netral", 2: "Positif"}

LABEL_COLORS = {
    "Negatif": "#FF4B4B",   # Merah
    "Netral": "#808080",    # Abu-abu
    "Positif": "#00CC66"    # Hijau
}

LABEL_EMOJI = {
    "Negatif": "😠",
    "Netral": "😐", 
    "Positif": "😊"
}

# ==================== CONTOH KOMENTAR ====================
EXAMPLE_COMMENTS = [
    "Program MBG sangat membantu anak-anak Indonesia untuk mendapatkan gizi yang baik",
    "Saya ragu program ini bisa berjalan dengan baik, khawatir korupsi",
    "Semoga program makan bergizi gratis ini bisa berkelanjutan",
    "Program bagus tapi pelaksanaannya masih perlu diperbaiki",
    "Mantap program prabowo ini, anak sekolah jadi sehat semua",
    "Saya tidak merasakan manfaat dari program ini"
]
