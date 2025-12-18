import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, Any

from config import LABEL_EMOJI, LABEL_COLORS, EXAMPLE_COMMENTS


def apply_custom_css():
    """Menerapkan custom CSS untuk styling aplikasi"""
    st.markdown("""
    <style>
    /* ==================== CSS VARIABLES FOR THEME SUPPORT ==================== */
    :root {
        --text-color: #1E1E1E;
        --text-secondary: #555555;
        --bg-secondary: rgba(0, 0, 0, 0.05);
        --border-color: rgba(0, 0, 0, 0.1);
        --code-bg: rgba(0, 0, 0, 0.08);
        --code-text: #0066cc;
    }
    
    /* Dark theme overrides - Streamlit adds data-theme attribute */
    [data-theme="dark"], 
    .stApp[data-theme="dark"],
    [data-testid="stAppViewContainer"][data-theme="dark"] {
        --text-color: #E8E8E8;
        --text-secondary: #B0B0B0;
        --bg-secondary: rgba(255, 255, 255, 0.05);
        --border-color: rgba(255, 255, 255, 0.1);
        --code-bg: rgba(0, 0, 0, 0.3);
        --code-text: #A8D5A2;
    }
    
    /* Detect dark theme via background color */
    @media (prefers-color-scheme: dark) {
        :root {
            --text-color: #E8E8E8;
            --text-secondary: #B0B0B0;
            --bg-secondary: rgba(255, 255, 255, 0.05);
            --border-color: rgba(255, 255, 255, 0.1);
            --code-bg: rgba(0, 0, 0, 0.3);
            --code-text: #A8D5A2;
        }
    }
    
    /* ==================== MAIN TITLE & SUBTITLE ==================== */
    .main-title {
        font-size: clamp(1.5rem, 5vw, 2.5rem);
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
        word-wrap: break-word;
    }
    .subtitle {
        font-size: clamp(0.9rem, 3vw, 1.2rem);
        text-align: center;
        opacity: 0.8;
        margin-bottom: 2rem;
        word-wrap: break-word;
    }
    
    /* ==================== RESULT CARDS ==================== */
    .result-card {
        padding: clamp(1rem, 3vw, 1.5rem);
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .result-positive {
        background: linear-gradient(135deg, #00CC66 0%, #00AA55 100%);
        color: white !important;
    }
    .result-negative {
        background: linear-gradient(135deg, #FF4B4B 0%, #CC3333 100%);
        color: white !important;
    }
    .result-neutral {
        background: linear-gradient(135deg, #808080 0%, #666666 100%);
        color: white !important;
    }
    .result-card * {
        color: white !important;
    }
    .sentiment-label {
        font-size: clamp(1.5rem, 4vw, 2rem);
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .confidence-score {
        font-size: clamp(1rem, 2.5vw, 1.2rem);
    }
    
    /* ==================== INFO & STEP BOXES ==================== */
    .info-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .step-box {
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.4rem 0;
        border-left: 4px solid #6C9BF5;
        word-break: break-word;
        overflow-wrap: break-word;
        background-color: rgba(108, 155, 245, 0.1);
    }
    .step-box code {
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-size: 0.9em;
        word-break: break-all;
        display: inline-block;
        max-width: 100%;
        background-color: rgba(108, 155, 245, 0.15);
        color: #2563eb;
    }
    
    /* Dark theme step-box code */
    [data-theme="dark"] .step-box code,
    @media (prefers-color-scheme: dark) {
        .step-box code {
            background-color: rgba(0, 0, 0, 0.3);
            color: #A8D5A2;
        }
    }
    
    /* ==================== TEXT AREA ==================== */
    .stTextArea textarea {
        font-size: clamp(0.95rem, 2vw, 1.1rem) !important;
        border-radius: 8px !important;
    }
    
    /* ==================== BUTTONS - RESPONSIVE ==================== */
    .stButton > button {
        font-size: clamp(0.75rem, 2vw, 0.9rem) !important;
        padding: 0.5rem 0.75rem !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        height: auto !important;
        min-height: 40px !important;
        line-height: 1.3 !important;
    }
    
    /* ==================== EXPANDER ==================== */
    .streamlit-expanderHeader {
        font-size: clamp(0.9rem, 2.5vw, 1rem) !important;
        border-radius: 8px !important;
    }
    .streamlit-expanderContent {
        border-radius: 0 0 8px 8px !important;
    }
    
    /* ==================== METRICS ==================== */
    [data-testid="stMetricValue"] {
        font-size: clamp(1.2rem, 3vw, 1.5rem) !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: clamp(0.8rem, 2vw, 1rem) !important;
    }
    
    /* ==================== RESPONSIVE COLUMNS ==================== */
    @media (max-width: 768px) {
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
        .main-title {
            font-size: 1.5rem;
        }
        .subtitle {
            font-size: 0.95rem;
        }
        .result-card {
            padding: 1rem;
        }
        .sentiment-label {
            font-size: 1.5rem;
        }
        /* Stack example buttons vertically on mobile */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
    }
    
    /* ==================== FOOTER ==================== */
    .footer-text {
        text-align: center;
        opacity: 0.7;
        font-size: clamp(0.75rem, 2vw, 0.9rem);
        padding: 1rem 0;
    }
    
    /* ==================== GENERAL FIXES ==================== */
    .stAlert {
        border-radius: 8px !important;
    }
    
    /* ==================== PLOTLY CHART ==================== */
    .js-plotly-plot .plotly .modebar {
        background-color: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Menampilkan sidebar dengan informasi aplikasi"""
    with st.sidebar:
        # Centering image menggunakan columns
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("https://img.icons8.com/color/96/000000/restaurant.png", width=80)
        
        st.markdown("## 📊 Tentang Aplikasi")
        st.markdown("""
        Aplikasi ini menganalisis sentimen opini publik terhadap program 
        **Makan Bergizi Gratis (MBG)** menggunakan teknologi Deep Learning.
        """)
        
        st.markdown("---")
        
        st.markdown("### 🤖 Model yang Digunakan")
        st.markdown("""
        - **Arsitektur**: Bidirectional GRU (Bi-GRU)
        - **Training**: Dataset Twitter/X & YouTube tentang MBG
        - **Teknik**: Oversampling untuk data imbalance
        - **Vocab Size**: 15,000
        - **Max Length**: 60
        """)
        
        st.markdown("---")
        
        st.markdown("### 📝 Cara Penggunaan")
        st.markdown("""
        1. Masukkan komentar/opini di kolom input
        2. Klik tombol **"🔍 Analisis Sentimen"**
        3. Lihat hasil prediksi dan visualisasi
        """)
        
        st.markdown("---")
        
        st.markdown("### 🔧 Pipeline Preprocessing")
        st.markdown("""
        1. Case Folding (lowercase)
        2. Hapus URL, @username, #hashtag
        3. Hapus angka & tanda baca
        4. Normalisasi singkatan
        5. Hapus stopwords
        6. Hapus kata pendek (≤1 huruf)
        """)
        
        st.markdown("---")
        
        st.markdown("### 👥 Tim Pengembang")
        st.markdown("""
        **Tugas Besar Deep Learning Kelompok 9:**
        - 👤 [Raid Muhammad Naufal](https://github.com/rayths)
        - 👤 [Najla Juwairia](https://github.com/najlajuwa)
        - 👤 [Tessa Kania Sagala](https://github.com/tessakanias)
        """)
        
        st.markdown("---")
        
        st.markdown("### 📚 Label Sentimen")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("🟢 **Positif**")
        with col2:
            st.markdown("⚪ **Netral**")
        with col3:
            st.markdown("🔴 **Negatif**")


def render_header():
    """Menampilkan header aplikasi"""
    st.markdown('<h1 class="main-title">🍽️ Analisis Sentimen Program MBG</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Makan Bergizi Gratis - Menggunakan Model Bi-GRU Deep Learning</p>', unsafe_allow_html=True)


def render_error_message(error: str):
    """Menampilkan pesan error"""
    st.error(f"""
    ⚠️ **Gagal memuat model atau tokenizer!**
    
    Pastikan file berikut tersedia:
    - `models/Best_Oversampled_Model.keras`
    - `models/tokenizer.pickle`
    
    Error: {error}
    """)


def render_input_section() -> str:
    """
    Menampilkan section input teks
    
    Returns:
        Teks input dari user
    """
    st.markdown("### 💬 Masukkan Komentar/Opini")
    
    # Inisialisasi session state untuk input text
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ''
    
    # Fungsi callback untuk set contoh komentar
    def set_example(comment):
        st.session_state.input_text = comment
    
    with st.expander("📋 Lihat Contoh Komentar", expanded=False):
        # Menggunakan 2 baris untuk tampilan lebih baik di mobile
        # Baris pertama: 3 contoh
        row1_cols = st.columns(3)
        for i, col in enumerate(row1_cols):
            if i < len(EXAMPLE_COMMENTS):
                with col:
                    st.button(
                        f"📝 Contoh {i+1}", 
                        key=f"example_{i+1}", 
                        on_click=set_example, 
                        args=(EXAMPLE_COMMENTS[i],),
                        use_container_width=True,
                        help=EXAMPLE_COMMENTS[i][:50] + "..."
                    )
        
        # Baris kedua: 2 contoh sisanya
        if len(EXAMPLE_COMMENTS) > 3:
            row2_cols = st.columns(3)
            for i, col in enumerate(row2_cols):
                idx = i + 3
                if idx < len(EXAMPLE_COMMENTS):
                    with col:
                        st.button(
                            f"📝 Contoh {idx+1}", 
                            key=f"example_{idx+1}", 
                            on_click=set_example, 
                            args=(EXAMPLE_COMMENTS[idx],),
                            use_container_width=True,
                            help=EXAMPLE_COMMENTS[idx][:50] + "..."
                        )
    
    # Text input
    input_text = st.text_area(
        "Tulis komentar atau pendapat Anda tentang program MBG:",
        value=st.session_state.input_text,
        height=150,
        placeholder="Contoh: Program makan bergizi gratis sangat membantu keluarga kurang mampu...",
    )
    
    return input_text


def render_analyze_button() -> bool:
    """
    Menampilkan tombol analisis
    
    Returns:
        True jika tombol diklik
    """
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        return st.button("🔍 Analisis Sentimen", type="primary", use_container_width=True)


def render_result_card(result: Dict[str, Any]):
    """Menampilkan card hasil prediksi"""
    label = result['label']
    confidence = result['confidence']
    emoji = LABEL_EMOJI[label]
    color_class = f"result-{label.lower()}"
    
    st.markdown(f"""
    <div class="result-card {color_class}">
        <div style="font-size: 3rem;">{emoji}</div>
        <div class="sentiment-label">{label}</div>
        <div class="confidence-score">Confidence: {confidence:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)


def render_preprocessing_details(original_text: str, result: Dict[str, Any]):
    """Menampilkan detail preprocessing"""
    with st.expander("🔧 Detail Preprocessing"):
        st.markdown("**Teks Original:**")
        st.info(original_text)
        
        st.markdown("**Teks Setelah Preprocessing:**")
        st.success(result['cleaned_text'] if result['cleaned_text'] else "(kosong setelah preprocessing)")
        
        # Tampilkan langkah-langkah preprocessing jika ada
        if 'preprocessing_steps' in result:
            st.markdown("---")
            st.markdown("**Langkah-langkah Preprocessing:**")
            
            step_names = {
                '0_original': '📝 Original',
                '1_case_folding': '🔡 Case Folding',
                '2_remove_url_mention_hashtag': '🔗 Hapus URL/Mention/Hashtag',
                '3_remove_non_alpha': '🔢 Hapus Non-Alfabet',
                '4_remove_extra_whitespace': '⬜ Hapus Spasi Berlebih',
                '5_normalize_slang': '📖 Normalisasi Singkatan',
                '6_remove_stopwords': '🚫 Hapus Stopwords',
                '7_remove_short_words': '✂️ Hapus Kata Pendek'
            }
            
            for key, value in result['preprocessing_steps'].items():
                if key != 'final':
                    step_label = step_names.get(key, key)
                    st.markdown(f"""
                    <div class="step-box">
                        <strong>{step_label}:</strong><br>
                        <code>{value if value else '(kosong)'}</code>
                    </div>
                    """, unsafe_allow_html=True)


def render_probability_chart(result: Dict[str, Any]):
    """Menampilkan bar chart probabilitas"""
    st.markdown("#### 📊 Distribusi Probabilitas")
    
    prob_data = pd.DataFrame({
        'Sentimen': ['Negatif', 'Netral', 'Positif'],
        'Probabilitas (%)': [
            result['probabilities']['Negatif'],
            result['probabilities']['Netral'],
            result['probabilities']['Positif']
        ]
    })
    
    fig = px.bar(
        prob_data, 
        x='Sentimen', 
        y='Probabilitas (%)',
        color='Sentimen',
        color_discrete_map={
            'Negatif': '#FF4B4B',
            'Netral': '#808080',
            'Positif': '#00CC66'
        },
        text='Probabilitas (%)'
    )
    
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(
        showlegend=False,
        yaxis_range=[0, 100],
        xaxis_title="",
        yaxis_title="Probabilitas (%)",
        height=350,
        # Transparent background to adapt to Streamlit theme
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
        ),
        yaxis=dict(
            gridcolor='rgba(128,128,128,0.2)',
        ),
        margin=dict(l=20, r=20, t=30, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_probability_metrics(result: Dict[str, Any]):
    """Menampilkan metric probabilitas"""
    st.markdown("#### 📈 Detail Probabilitas")
    prob_cols = st.columns(3)
    
    with prob_cols[0]:
        st.metric(
            label="🔴 Negatif",
            value=f"{result['probabilities']['Negatif']:.2f}%"
        )
    
    with prob_cols[1]:
        st.metric(
            label="⚪ Netral",
            value=f"{result['probabilities']['Netral']:.2f}%"
        )
    
    with prob_cols[2]:
        st.metric(
            label="🟢 Positif",
            value=f"{result['probabilities']['Positif']:.2f}%"
        )


def render_wordcloud(cleaned_text: str):
    """Menampilkan word cloud"""
    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt
        
        if cleaned_text:
            st.markdown("---")
            st.markdown("#### ☁️ Word Cloud")
            
            # Menggunakan warna yang netral agar terlihat di kedua tema
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color=None,  # Transparent
                mode='RGBA',
                colormap='plasma',
                max_words=50,
                min_font_size=10
            ).generate(cleaned_text)
            
            fig_wc, ax = plt.subplots(figsize=(10, 5))
            fig_wc.patch.set_alpha(0)  # Transparent figure background
            ax.set_facecolor('none')   # Transparent axes background
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig_wc, transparent=True)
            plt.close()
    except ImportError:
        pass  # Word cloud library tidak tersedia


def render_footer():
    """Menampilkan footer"""
    st.markdown("---")
    st.markdown("""
    <div class="footer-text">
        <p>© 2025 - Tugas Besar Deep Learning Kelompok 9 | Analisis Sentimen MBG</p>
    </div>
    """, unsafe_allow_html=True)


def render_feedback_section(input_text: str, result: Dict[str, Any], data_manager):
    """
    Menampilkan section feedback dari user
    
    Args:
        input_text: Teks input original
        result: Hasil prediksi dari model
        data_manager: Instance DataManager untuk menyimpan feedback
    """
    st.markdown("---")
    st.markdown("### 💬 Berikan Feedback")
    st.markdown("Bantu kami meningkatkan akurasi model dengan memberikan feedback!")
    
    # Initialize feedback state
    if 'feedback_submitted' not in st.session_state:
        st.session_state.feedback_submitted = False
    
    if st.session_state.feedback_submitted:
        st.success("✅ Terima kasih atas feedback Anda!")
        if st.button("🔄 Berikan Feedback Lagi", key="reset_feedback"):
            st.session_state.feedback_submitted = False
            st.rerun()
        return
    
    with st.container():
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"**Hasil Prediksi:** {LABEL_EMOJI[result['label']]} **{result['label']}**")
            st.markdown(f"**Confidence:** {result['confidence']:.2f}%")
        
        with col2:
            is_correct = st.radio(
                "Apakah prediksi ini benar?",
                options=["Ya, benar", "Tidak, salah"],
                key="feedback_correct",
                horizontal=True
            )
        
        # Jika prediksi salah, tanyakan label yang benar
        correct_label = None
        if is_correct == "Tidak, salah":
            correct_label = st.selectbox(
                "Label yang seharusnya:",
                options=["Positif", "Netral", "Negatif"],
                key="feedback_correct_label"
            )
        
        # Komentar tambahan
        feedback_comment = st.text_area(
            "Komentar tambahan (opsional):",
            placeholder="Berikan komentar atau saran untuk meningkatkan model...",
            key="feedback_comment",
            height=80
        )
        
        # Tombol submit
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("📤 Kirim Feedback", type="primary", use_container_width=True, key="submit_feedback"):
                # Simpan feedback
                success = data_manager.save_feedback(
                    original_text=input_text,
                    predicted_label=result['label'],
                    is_correct=(is_correct == "Ya, benar"),
                    correct_label=correct_label,
                    feedback_comment=feedback_comment
                )
                
                if success:
                    st.session_state.feedback_submitted = True
                    st.rerun()
                else:
                    st.error("❌ Gagal menyimpan feedback. Silakan coba lagi.")


def render_results(input_text: str, result: Dict[str, Any]):
    """
    Menampilkan seluruh hasil analisis
    
    Args:
        input_text: Teks input original
        result: Hasil prediksi dari model
    """
    st.markdown("---")
    st.markdown("### 📊 Hasil Analisis")
    
    # Layout hasil
    col_result, col_chart = st.columns([1, 1])
    
    with col_result:
        render_result_card(result)
        render_preprocessing_details(input_text, result)
    
    with col_chart:
        render_probability_chart(result)
    
    render_probability_metrics(result)
    render_wordcloud(result['cleaned_text'])
