import pickle
import numpy as np
import tensorflow as tf
from typing import Tuple, Optional, Dict, Any

from config import (
    MODEL_PATH, 
    TOKENIZER_PATH, 
    MODEL_PATH_FALLBACK, 
    TOKENIZER_PATH_FALLBACK,
    LABEL_MAP
)
from preprocessing import TextPreprocessor, tokenize_and_pad


class SentimentAnalyzer:
    """
    Kelas untuk analisis sentimen menggunakan model Bi-GRU
    """
    
    def __init__(self, model=None, tokenizer=None, preprocessor=None):
        """
        Inisialisasi SentimentAnalyzer
        
        Args:
            model: Model Keras yang sudah diload (opsional)
            tokenizer: Tokenizer Keras yang sudah diload (opsional)
            preprocessor: Instance TextPreprocessor (opsional)
        """
        self.model = model
        self.tokenizer = tokenizer
        self.preprocessor = preprocessor if preprocessor else TextPreprocessor()
        self.label_map = LABEL_MAP
    
    def load_model(self, model_path: str = MODEL_PATH) -> bool:
        """
        Memuat model dari file
        
        Args:
            model_path: Path ke file model .keras
            
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            self.model = tf.keras.models.load_model(model_path)
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def load_tokenizer(self, tokenizer_path: str = TOKENIZER_PATH) -> bool:
        """
        Memuat tokenizer dari file pickle
        
        Args:
            tokenizer_path: Path ke file tokenizer .pickle
            
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            with open(tokenizer_path, 'rb') as handle:
                self.tokenizer = pickle.load(handle)
            return True
        except Exception as e:
            print(f"Error loading tokenizer: {e}")
            return False
    
    def is_ready(self) -> bool:
        """
        Mengecek apakah model dan tokenizer sudah dimuat
        
        Returns:
            True jika siap digunakan
        """
        return self.model is not None and self.tokenizer is not None
    
    def predict(self, text: str) -> Dict[str, Any]:
        """
        Melakukan prediksi sentimen untuk teks input
        
        Args:
            text: Teks input mentah
            
        Returns:
            Dictionary berisi:
                - label: Label sentimen (Positif/Netral/Negatif)
                - confidence: Confidence score (%)
                - probabilities: Dict probabilitas untuk setiap kelas
                - cleaned_text: Teks setelah preprocessing
                - preprocessing_steps: Detail setiap langkah preprocessing
        """
        if not self.is_ready():
            raise RuntimeError("Model dan tokenizer belum dimuat!")
        
        # Preprocessing
        cleaned_text = self.preprocessor.preprocess(text)
        preprocessing_steps = self.preprocessor.get_preprocessing_steps(text)
        
        # Tokenisasi dan padding
        padded_sequence = tokenize_and_pad(cleaned_text, self.tokenizer)
        
        # Prediksi
        prediction = self.model.predict(padded_sequence, verbose=0)
        
        # Ambil probabilitas dan label
        probabilities = prediction[0]
        predicted_class = np.argmax(probabilities)
        predicted_label = self.label_map[predicted_class]
        confidence = float(probabilities[predicted_class]) * 100
        
        return {
            'label': predicted_label,
            'confidence': confidence,
            'probabilities': {
                'Negatif': float(probabilities[0]) * 100,
                'Netral': float(probabilities[1]) * 100,
                'Positif': float(probabilities[2]) * 100
            },
            'cleaned_text': cleaned_text,
            'preprocessing_steps': preprocessing_steps
        }
    
    def predict_batch(self, texts: list) -> list:
        """
        Melakukan prediksi sentimen untuk batch teks
        
        Args:
            texts: List teks input mentah
            
        Returns:
            List hasil prediksi
        """
        return [self.predict(text) for text in texts]


def load_assets() -> Tuple[Optional[tf.keras.Model], Optional[Any], Optional[str]]:
    """
    Memuat model dan tokenizer dengan fallback paths
    
    Returns:
        Tuple (model, tokenizer, error_message)
        - Jika sukses: (model, tokenizer, None)
        - Jika gagal: (None, None, error_message)
    """
    model = None
    tokenizer = None
    
    try:
        # Coba muat dari folder models/ terlebih dahulu
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
            with open(TOKENIZER_PATH, 'rb') as handle:
                tokenizer = pickle.load(handle)
        except:
            # Fallback: coba dari direktori utama
            model = tf.keras.models.load_model(MODEL_PATH_FALLBACK)
            with open(TOKENIZER_PATH_FALLBACK, 'rb') as handle:
                tokenizer = pickle.load(handle)
        
        return model, tokenizer, None
    
    except Exception as e:
        return None, None, str(e)


def create_analyzer() -> Tuple[Optional[SentimentAnalyzer], Optional[str]]:
    """
    Factory function untuk membuat SentimentAnalyzer yang sudah siap digunakan
    
    Returns:
        Tuple (analyzer, error_message)
        - Jika sukses: (analyzer, None)
        - Jika gagal: (None, error_message)
    """
    model, tokenizer, error = load_assets()
    
    if error:
        return None, error
    
    analyzer = SentimentAnalyzer(model=model, tokenizer=tokenizer)
    return analyzer, None
