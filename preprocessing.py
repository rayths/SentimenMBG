import re
from tensorflow.keras.preprocessing.sequence import pad_sequences
from config import MAX_LEN

# ==================== KAMUS NORMALISASI ====================
NORM_DICT = {
    "yg": "yang", "blg": "bilang", "d": "di", "dket": "dekat", "deket": "dekat",
    "tak": "tidak", "tdk": "tidak", "ga": "tidak", "gak": "tidak", "gk": "tidak",
    "nggak": "tidak", "getu": "gitu", "duwit": "uang", "duit": "uang", "lh": "lah",
    "krn": "karena", "karna": "karena", "sdh": "sudah", "udh": "sudah",
    "blm": "belum", "dgn": "dengan", "dlm": "dalam", "jgn": "jangan", "pa": "apa",
    "bgt": "banget", "skrg": "sekarang", "sbelum": "sebelum", "bkn": "bukan",
    "utk": "untuk", "sy": "saya", "gue": "saya", "gw": "saya", "aku": "saya",
    "ku": "saya", "ndakjadi": "tidak jadi", "dobol": "bodoh", "bnyak": "banyak",
    "ngelesmu": "bohongmu", "bangss": "bangsa", "brp": "berapa", "nh": "nah",
    "km": "kamu", "lu": "kamu", "kta": "kita", "kalo": "kalau", "kl": "kalau",
    "berapq": "berapa", "tiap": "setiap", "mknya": "makanya", "edan": "gila",
    "kek": "kayak", "hrsnya": "harusnya", "peket": "paket", "tlol": "bodoh",
    "klau": "kalau", "klo": "kalau", "knp": "kenapa", "ksih": "kasih",
    "msh": "masih", "setop": "stop", "knmurid": "kemurid", "secuil": "sedikit",
    "kyk": "kayak", "spy": "supaya", "gmn": "gimana", "dah": "udah", "dl": "dulu",
    "sht": "sehat", "klu": "kalau", "bgus": "bagus", "krnpa": "kenapa",
    "jadivkepala": "jadi kepala", "slrh": "seluruh", "kepla": "kepala",
    "skolah": "sekolah", "bpk": "bapak", "smdgn": "sama dengan", "sing": "yang",
    "begonya": "bodohnya", "kluarganya": "keluarganya", "kya": "kayak",
    "merika": "mereka", "progrm": "program", "byk": "banyak", "cocog": "cocok",
    "bln": "bulan", "bp": "bapak", "tlng": "tolong", "dihntikn": "dihentikan",
    "tpi": "tapi", "tp": "tapi", "indo": "indonesia", "jd": "jadi", "bs": "bisa",
    "aja": "saja", "aj": "saja", "sj": "saja", "sja": "saja", "lbh": "lebih",
    "sm": "sama", "dr": "dari", "dri": "dari", "hrs": "harus", "pas": "saat",
    "tgl": "tanggal", "bnyk": "banyak", "mw": "mau", "tu": "itu",
    "samoai": "sampai", "knapa": "kenapa", "penerapnnya": "penerapannya",
    "cepolok": "ceplok", "semingu": "seminggu", "gimna": "gimana", "mf": "maaf",
    "doyan": "suka", "dg": "dengan", "rmh": "rumah", "umpetin": "disembunyikan",
    "anggean": "anggaran", "mubajir": "mubazir", "mlah": "malah", "lha": "lah",
    "cuannya": "uangnya", "dsar": "dasar", "mntal": "mental", "pjabat": "pejabat",
    "ngajarqw": "mengajarku", "mkn": "makan", "kenthang": "kentang", "iya": "ya",
    "trs": "terus", "koprupsi": "korupsi", "hrusnya": "harusnya", "bgtu": "begitu",
    "uda": "sudah", "mo": "mau", "engga": "tidak", "amburadul": "berantakan",
    "gpp": "tidak apa apa", "emang": "memang", "omprengx": "omprengnya",
    "sealot": "sekeras", "ajaa": "saja", "ntar": "nanti", "lgsg": "langsung",
    "bget": "banget", "nyari": "mencari", "bner": "benar", "ni": "ini",
    "mengdig": "mending", "mbgx": "mbgnya", "uagkan": "uangkan", "roar": "luar",
    "bagsa": "bangsa", "qt": "kita", "ubahla": "ubah lah", "ngmng": "berbicara",
    "doank": "saja", "vidio": "video", "cobak": "coba", "lgi": "lagi",
    "ortu": "orang tua", "itulah": "itu lah", "seharusx": "seharusnya",
    "cpt": "cepat", "ngeyel": "keras kepala", "pake": "pakai", "dpt": "dapat",
    "sblm": "sebelum", "ges": "teman teman", "bodih": "bodoh", "smoga": "semoga",
    "ajah": "saja", "wong": "orang", "yo": "ya", "iku": "itu", "makkin": "makin",
    "ramayi": "ramai", "giji": "gizi", "mantab": "mantap", "trus": "terus",
    "positfnya": "positifnya", "emng": "memang", "ank": "anak", "pda": "pada",
    "pucet": "pucat", "bat": "banget", "ky": "kayak", "pngen": "ingin",
    "ngeruk": "ambil", "akuu": "saya", "ny": "nya", "prbwo": "prabowo",
    "kagak": "tidak", "ngga": "tidak", "muke": "wajah", "nye": "nya",
    "rogram": "program", "cuan": "untung", "smw": "semua", "kyak": "kayak",
    "gtu": "gitu", "lwongan": "lowongan", "dikrm": "dikirim", "ne": "nya",
    "programx": "programnya", "spagety": "spageti", "gelem": "mau",
    "uwang": "uang", "kasi": "kasih", "bgm": "bagaimana",
    "cost": "pengeluaran", "gratisa": "gratis", "hargavl": "harga",
    "aing": "saya", "ngikutin": "mengikuti", "pegawe": "pegawai", "kaga": "tidak",
    "propokator": "provokator", "konslet": "korsleting", "nyampe": "sampai",
    "nemu": "menemukan", "kpl": "kepala", "nnti": "nanti", "sik": "sih",
    "nyalahin": "menyalahkan", "dipake": "dipakai", "masal": "massal",
    "pdhl": "padahal", "gua": "saya", "cm": "cuma", "bt": "buat", "utuk": "untuk",
    "dngan": "dengan", "nahhh": "nah", "competent": "kompeten", "peak": "bodoh",
    "ngicipi": "mencoba", "emak": "ibu", "emg": "memang", "slamanya": "selamanya",
    "smpe": "sampai", "kluarga": "keluarga", "ketolopan": "kebodohan",
    "trima": "terima", "disekolhan": "disekolahan", "kmi": "kami", "jln": "jalan",
    "tau": "mengerti", "tw": "mengerti", "pk": "pak", "pke": "pakai",
    "org": "orang", "mkan": "makan", "mbg": "makan bergizi gratis"
}

# ==================== STOPWORDS ====================
STOP_WORDS = set([
    "yang", "di", "ke", "dari", "dan", "atau", "ini", "itu", "juga", "nya", "saya",
    "aku", "kamu", "dia", "kita", "mereka", "pada", "dengan", "adalah", "yaitu",
    "karena", "untuk", "bagi", "bisa", "akan", "sudah", "lagi", "masih", "oleh",
    "saja", "kah", "pun", "ada", "jadi", "kalau", "tapi", "namun", "kok", "sih",
    "deh", "dong", "lah", "mah", "kan", "ya", "yak", "yuk", "tuh", "nih", "wah",
    "wow", "biar", "agar", "supaya", "lalu", "kemudian", "setelah", "sebelum", "lo",
    "saat", "ketika", "seperti", "bagaikan", "antara", "terhadap", "tentang", "si",
    "nah", "oh", "kayak", "lahh", "inimahh", "nyaa", "loh", "yah", "nahh", "jir",
    "njir", "dehh", "se", "waw", "wooow",
    "secara", "dalam", "luar", "atas", "bawah", "depan", "belakang", "sana", "sini"
])


class TextPreprocessor:
    """
    Kelas untuk preprocessing teks dengan pipeline yang konsisten
    """
    
    def __init__(self, norm_dict=None, stop_words=None):
        """
        Inisialisasi preprocessor dengan kamus normalisasi dan stopwords
        
        Args:
            norm_dict: Dictionary untuk normalisasi kata (default: NORM_DICT)
            stop_words: Set stopwords (default: STOP_WORDS)
        """
        self.norm_dict = norm_dict if norm_dict is not None else NORM_DICT
        self.stop_words = stop_words if stop_words is not None else STOP_WORDS
    
    def case_folding(self, text: str) -> str:
        """
        Langkah 1: Mengubah teks menjadi huruf kecil
        
        Args:
            text: Teks input
            
        Returns:
            Teks dalam huruf kecil
        """
        return str(text).lower()
    
    def remove_urls(self, text: str) -> str:
        """
        Langkah 2a: Menghapus URL dari teks
        
        Args:
            text: Teks input
            
        Returns:
            Teks tanpa URL
        """
        return re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    def remove_mentions_hashtags(self, text: str) -> str:
        """
        Langkah 2b: Menghapus @username dan #hashtag
        
        Args:
            text: Teks input
            
        Returns:
            Teks tanpa mention dan hashtag
        """
        return re.sub(r'@\w+|#\w+', '', text)
    
    def remove_non_alpha(self, text: str) -> str:
        """
        Langkah 3: Menghapus angka dan tanda baca (hanya sisakan huruf a-z dan spasi)
        
        Args:
            text: Teks input
            
        Returns:
            Teks hanya berisi huruf dan spasi
        """
        return re.sub(r'[^a-z\s]', ' ', text)
    
    def remove_extra_whitespace(self, text: str) -> str:
        """
        Langkah 4: Menghapus spasi berlebih
        
        Args:
            text: Teks input
            
        Returns:
            Teks dengan spasi yang dinormalisasi
        """
        return re.sub(r'\s+', ' ', text).strip()
    
    def normalize_slang(self, text: str) -> str:
        """
        Langkah 5: Normalisasi singkatan dan kata tidak baku
        
        Args:
            text: Teks input
            
        Returns:
            Teks dengan kata-kata yang sudah dinormalisasi
        """
        words = text.split()
        normalized_words = [self.norm_dict.get(word, word) for word in words]
        return " ".join(normalized_words)
    
    def remove_stopwords(self, text: str) -> str:
        """
        Langkah 6: Menghapus stopwords
        
        Args:
            text: Teks input
            
        Returns:
            Teks tanpa stopwords
        """
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        return " ".join(filtered_words)
    
    def remove_short_words(self, text: str, min_length: int = 2) -> str:
        """
        Langkah 7: Menghapus kata pendek
        
        Args:
            text: Teks input
            min_length: Panjang minimum kata (default: 2)
            
        Returns:
            Teks tanpa kata pendek
        """
        words = text.split()
        filtered_words = [word for word in words if len(word) >= min_length]
        return " ".join(filtered_words)
    
    def preprocess(self, text: str) -> str:
        """
        Menjalankan seluruh pipeline preprocessing
        
        Args:
            text: Teks input mentah
            
        Returns:
            Teks yang sudah diproses
        """
        # Langkah 1: Case Folding
        text = self.case_folding(text)
        
        # Langkah 2: Hapus URL, Username, Hashtag
        text = self.remove_urls(text)
        text = self.remove_mentions_hashtags(text)
        
        # Langkah 3: Hapus Angka dan Tanda Baca
        text = self.remove_non_alpha(text)
        
        # Langkah 4: Hapus spasi berlebih
        text = self.remove_extra_whitespace(text)
        
        # Langkah 5: Normalisasi Singkatan
        text = self.normalize_slang(text)
        
        # Langkah 6: Hapus Stopwords
        text = self.remove_stopwords(text)
        
        # Langkah 7: Hapus Kata Pendek
        text = self.remove_short_words(text)
        
        return text
    
    def get_preprocessing_steps(self, text: str) -> dict:
        """
        Mengembalikan hasil setiap langkah preprocessing untuk debugging/visualisasi
        
        Args:
            text: Teks input mentah
            
        Returns:
            Dictionary berisi hasil setiap langkah
        """
        steps = {}
        
        # Original
        steps['0_original'] = text
        
        # Langkah 1: Case Folding
        text = self.case_folding(text)
        steps['1_case_folding'] = text
        
        # Langkah 2: Hapus URL, Username, Hashtag
        text = self.remove_urls(text)
        text = self.remove_mentions_hashtags(text)
        steps['2_remove_url_mention_hashtag'] = text
        
        # Langkah 3: Hapus Angka dan Tanda Baca
        text = self.remove_non_alpha(text)
        steps['3_remove_non_alpha'] = text
        
        # Langkah 4: Hapus spasi berlebih
        text = self.remove_extra_whitespace(text)
        steps['4_remove_extra_whitespace'] = text
        
        # Langkah 5: Normalisasi Singkatan
        text = self.normalize_slang(text)
        steps['5_normalize_slang'] = text
        
        # Langkah 6: Hapus Stopwords
        text = self.remove_stopwords(text)
        steps['6_remove_stopwords'] = text
        
        # Langkah 7: Hapus Kata Pendek
        text = self.remove_short_words(text)
        steps['7_remove_short_words'] = text
        
        # Final
        steps['final'] = text
        
        return steps


def tokenize_and_pad(text: str, tokenizer, max_len: int = MAX_LEN):
    """
    Tokenisasi dan padding sequence
    
    Args:
        text: Teks yang sudah dipreprocess
        tokenizer: Keras Tokenizer object
        max_len: Panjang maksimal sequence
        
    Returns:
        Numpy array dengan shape (1, max_len)
    """
    sequences = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequences, maxlen=max_len, padding='post', truncating='post')
    return padded


# Instance default preprocessor
default_preprocessor = TextPreprocessor()


def clean_text(text: str) -> str:
    """
    Fungsi wrapper untuk kompatibilitas dengan kode lama
    
    Args:
        text: Teks input mentah
        
    Returns:
        Teks yang sudah diproses
    """
    return default_preprocessor.preprocess(text)
