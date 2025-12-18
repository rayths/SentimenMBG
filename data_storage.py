import os
import csv
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
import streamlit as st

# ==================== KONFIGURASI ====================
DATA_DIR = "data"
LOCAL_CSV_FILE = os.path.join(DATA_DIR, "sentiment_history.csv")
FEEDBACK_CSV_FILE = os.path.join(DATA_DIR, "user_feedback.csv")

# CSV Headers
HISTORY_HEADERS = [
    "timestamp", "original_text", "cleaned_text", "predicted_label", 
    "confidence", "prob_negatif", "prob_netral", "prob_positif"
]

FEEDBACK_HEADERS = [
    "timestamp", "original_text", "predicted_label", "is_correct", 
    "correct_label", "feedback_comment"
]


# ==================== UTILITY FUNCTIONS ====================
def ensure_data_directory():
    """Memastikan direktori data ada"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def get_timestamp():
    """Mendapatkan timestamp saat ini"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ==================== LOCAL CSV STORAGE ====================
class LocalCSVStorage:
    """
    Penyimpanan lokal menggunakan CSV
    Cocok untuk development dan testing
    """
    
    @staticmethod
    def save_prediction(
        original_text: str,
        cleaned_text: str,
        result: Dict[str, Any]
    ) -> bool:
        """
        Menyimpan hasil prediksi ke CSV
        
        Args:
            original_text: Teks asli dari user
            cleaned_text: Teks setelah preprocessing
            result: Hasil prediksi dari model
            
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            ensure_data_directory()
            
            # Cek apakah file sudah ada
            file_exists = os.path.exists(LOCAL_CSV_FILE)
            
            with open(LOCAL_CSV_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Tulis header jika file baru
                if not file_exists:
                    writer.writerow(HISTORY_HEADERS)
                
                # Tulis data
                writer.writerow([
                    get_timestamp(),
                    original_text,
                    cleaned_text,
                    result['label'],
                    f"{result['confidence']:.2f}",
                    f"{result['probabilities']['Negatif']:.2f}",
                    f"{result['probabilities']['Netral']:.2f}",
                    f"{result['probabilities']['Positif']:.2f}"
                ])
            
            return True
        except Exception as e:
            st.warning(f"Gagal menyimpan ke CSV: {e}")
            return False
    
    @staticmethod
    def save_feedback(
        original_text: str,
        predicted_label: str,
        is_correct: bool,
        correct_label: Optional[str] = None,
        feedback_comment: str = ""
    ) -> bool:
        """
        Menyimpan feedback user ke CSV
        
        Args:
            original_text: Teks yang dianalisis
            predicted_label: Label hasil prediksi
            is_correct: Apakah prediksi benar
            correct_label: Label yang benar (jika prediksi salah)
            feedback_comment: Komentar tambahan dari user
            
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            ensure_data_directory()
            
            file_exists = os.path.exists(FEEDBACK_CSV_FILE)
            
            with open(FEEDBACK_CSV_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                if not file_exists:
                    writer.writerow(FEEDBACK_HEADERS)
                
                writer.writerow([
                    get_timestamp(),
                    original_text,
                    predicted_label,
                    "Ya" if is_correct else "Tidak",
                    correct_label or "-",
                    feedback_comment
                ])
            
            return True
        except Exception as e:
            st.warning(f"Gagal menyimpan feedback: {e}")
            return False
    
    @staticmethod
    def get_history(limit: int = 100) -> List[Dict]:
        """
        Mengambil history prediksi
        
        Args:
            limit: Jumlah maksimal data yang diambil
            
        Returns:
            List of dictionaries berisi history
        """
        try:
            if not os.path.exists(LOCAL_CSV_FILE):
                return []
            
            with open(LOCAL_CSV_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                history = list(reader)
            
            # Return data terbaru
            return history[-limit:][::-1]  # Reverse untuk terbaru di atas
        except Exception as e:
            st.warning(f"Gagal membaca history: {e}")
            return []
    
    @staticmethod
    def get_feedback_stats() -> Dict[str, Any]:
        """
        Mengambil statistik feedback
        
        Returns:
            Dictionary berisi statistik feedback
        """
        try:
            if not os.path.exists(FEEDBACK_CSV_FILE):
                return {"total": 0, "correct": 0, "incorrect": 0, "accuracy": 0}
            
            with open(FEEDBACK_CSV_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                feedbacks = list(reader)
            
            total = len(feedbacks)
            correct = sum(1 for f in feedbacks if f.get('is_correct') == 'Ya')
            incorrect = total - correct
            accuracy = (correct / total * 100) if total > 0 else 0
            
            return {
                "total": total,
                "correct": correct,
                "incorrect": incorrect,
                "accuracy": round(accuracy, 2)
            }
        except Exception as e:
            return {"total": 0, "correct": 0, "incorrect": 0, "accuracy": 0}


# ==================== GOOGLE SHEETS STORAGE (FOR DEPLOYMENT) ====================
class GoogleSheetsStorage:
    """
    Penyimpanan menggunakan Google Sheets
    Cocok untuk deployment di Streamlit Cloud
    
    Setup:
    1. Buat Google Cloud Project
    2. Enable Google Sheets API
    3. Buat Service Account dan download credentials JSON
    4. Share Google Sheet dengan email service account
    5. Simpan credentials di Streamlit Secrets
    """
    
    def __init__(self):
        self.client = None
        self.sheet = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Google Sheets connection"""
        try:
            # Check if gspread is available
            import gspread
            from google.oauth2.service_account import Credentials
            
            # Check if secrets are configured
            if "gcp_service_account" not in st.secrets:
                return
            
            # Setup credentials
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            
            credentials = Credentials.from_service_account_info(
                st.secrets["gcp_service_account"],
                scopes=scopes
            )
            
            self.client = gspread.authorize(credentials)
            
            # Open spreadsheet
            if "spreadsheet_url" in st.secrets:
                self.sheet = self.client.open_by_url(st.secrets["spreadsheet_url"])
            
        except ImportError:
            pass  # gspread not installed
        except Exception as e:
            st.warning(f"Google Sheets tidak tersedia: {e}")
    
    def is_available(self) -> bool:
        """Check if Google Sheets is configured"""
        return self.sheet is not None
    
    def save_prediction(
        self,
        original_text: str,
        cleaned_text: str,
        result: Dict[str, Any]
    ) -> bool:
        """Save prediction to Google Sheets"""
        if not self.is_available():
            return False
        
        try:
            worksheet = self.sheet.worksheet("predictions")
            
            worksheet.append_row([
                get_timestamp(),
                original_text,
                cleaned_text,
                result['label'],
                f"{result['confidence']:.2f}",
                f"{result['probabilities']['Negatif']:.2f}",
                f"{result['probabilities']['Netral']:.2f}",
                f"{result['probabilities']['Positif']:.2f}"
            ])
            
            return True
        except Exception as e:
            st.warning(f"Gagal menyimpan ke Google Sheets: {e}")
            return False
    
    def save_feedback(
        self,
        original_text: str,
        predicted_label: str,
        is_correct: bool,
        correct_label: Optional[str] = None,
        feedback_comment: str = ""
    ) -> bool:
        """Save feedback to Google Sheets"""
        if not self.is_available():
            return False
        
        try:
            worksheet = self.sheet.worksheet("feedback")
            
            worksheet.append_row([
                get_timestamp(),
                original_text,
                predicted_label,
                "Ya" if is_correct else "Tidak",
                correct_label or "-",
                feedback_comment
            ])
            
            return True
        except Exception as e:
            st.warning(f"Gagal menyimpan feedback ke Google Sheets: {e}")
            return False


# ==================== DATA MANAGER (UNIFIED INTERFACE) ====================
class DataManager:
    """
    Manager untuk mengelola penyimpanan data
    Otomatis memilih storage yang tersedia
    """
    
    def __init__(self):
        self.local_storage = LocalCSVStorage()
        self.cloud_storage = GoogleSheetsStorage()
    
    def save_prediction(
        self,
        original_text: str,
        cleaned_text: str,
        result: Dict[str, Any]
    ) -> bool:
        """
        Menyimpan prediksi ke storage yang tersedia
        Prioritas: Google Sheets > Local CSV
        """
        # Try cloud storage first (for deployment)
        if self.cloud_storage.is_available():
            return self.cloud_storage.save_prediction(original_text, cleaned_text, result)
        
        # Fallback to local storage
        return self.local_storage.save_prediction(original_text, cleaned_text, result)
    
    def save_feedback(
        self,
        original_text: str,
        predicted_label: str,
        is_correct: bool,
        correct_label: Optional[str] = None,
        feedback_comment: str = ""
    ) -> bool:
        """
        Menyimpan feedback ke storage yang tersedia
        """
        # Try cloud storage first
        if self.cloud_storage.is_available():
            return self.cloud_storage.save_feedback(
                original_text, predicted_label, is_correct, correct_label, feedback_comment
            )
        
        # Fallback to local storage
        return self.local_storage.save_feedback(
            original_text, predicted_label, is_correct, correct_label, feedback_comment
        )
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        """Mengambil history prediksi"""
        return self.local_storage.get_history(limit)
    
    def get_feedback_stats(self) -> Dict[str, Any]:
        """Mengambil statistik feedback"""
        return self.local_storage.get_feedback_stats()
    
    def get_storage_type(self) -> str:
        """Mendapatkan jenis storage yang aktif"""
        if self.cloud_storage.is_available():
            return "Google Sheets (Cloud)"
        return "Local CSV"


# ==================== SINGLETON INSTANCE ====================
@st.cache_resource
def get_data_manager() -> DataManager:
    """Get singleton instance of DataManager"""
    return DataManager()
