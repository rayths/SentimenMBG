import streamlit as st
# Import modul lokal
from config import LABEL_MAP, LABEL_EMOJI
from model_utils import load_assets, SentimentAnalyzer
from preprocessing import TextPreprocessor
from data_storage import get_data_manager
from ui_components import (
    apply_custom_css,
    render_sidebar,
    render_header,
    render_error_message,
    render_input_section,
    render_analyze_button,
    render_results,
    render_feedback_section,
    render_footer
)


# ==================== LOAD MODEL & TOKENIZER (CACHED) ====================
@st.cache_resource
def get_analyzer():
    """
    Memuat dan menyimpan analyzer dalam cache untuk performa optimal
    
    Returns:
        Tuple (SentimentAnalyzer atau None, error_message atau None)
    """
    model, tokenizer, error = load_assets()
    
    if error:
        return None, error
    
    preprocessor = TextPreprocessor()
    analyzer = SentimentAnalyzer(model=model, tokenizer=tokenizer, preprocessor=preprocessor)
    
    return analyzer, None


# ==================== MAIN APPLICATION ====================
def main():
    """Entry point utama aplikasi"""
    
    # Konfigurasi halaman
    st.set_page_config(
        page_title="Analisis Sentimen MBG",
        page_icon="🍽️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    apply_custom_css()
    
    # Render sidebar
    render_sidebar()
    
    # Render header
    render_header()
    
    # Load analyzer
    analyzer, error = get_analyzer()
    
    if error:
        render_error_message(error)
        return
    
    # Get data manager
    data_manager = get_data_manager()
    
    # Render input section
    input_text = render_input_section()
    
    # Render analyze button
    analyze_clicked = render_analyze_button()
    
    # Process analysis
    if analyze_clicked:
        if not input_text.strip():
            st.warning("⚠️ Mohon masukkan komentar terlebih dahulu!")
        else:
            with st.spinner("🔄 Menganalisis sentimen..."):
                # Prediksi menggunakan analyzer
                result = analyzer.predict(input_text)
                
                # Simpan ke storage
                data_manager.save_prediction(
                    original_text=input_text,
                    cleaned_text=result.get('cleaned_text', ''),
                    result=result
                )
                
                # Simpan result ke session state untuk feedback
                st.session_state['last_result'] = result
                st.session_state['last_input'] = input_text
                
                # Render hasil
                render_results(input_text, result)
    
    # Render feedback section jika ada hasil prediksi
    if 'last_result' in st.session_state and 'last_input' in st.session_state:
        render_feedback_section(
            st.session_state['last_input'],
            st.session_state['last_result'],
            data_manager
        )
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
