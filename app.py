# ============================================================
# SMARTPHONE ADVISOR
# Chatbot Perbandingan Produk untuk Tim Sales & Marketing
# Powered by LangChain + Groq + FAISS
# ============================================================
#
# CARA MENJALANKAN:
#   streamlit run app.py
#
# ============================================================

import streamlit as st
import re
from langdetect import detect, DetectorFactory
from rag_pipeline import build_rag_pipeline


# ── Konfigurasi Halaman ────────────────────────────────────────────────
st.set_page_config(
    page_title="Edukasi Merakyat (EM_Rules) AI",
    page_icon="📝",
    layout="centered"
)

# ── Header ─────────────────────────────────────────────────────────────
st.title("📝 EM_Rules AI")
st.caption(
    "AI assistant for compliance team at Edukasi Merakyat Foundation,\n\n"    
    "Answering questions about internal policies and procedures."
)

# ── Load RAG Pipeline ──────────────────────────────────────────────────
# Menggunakan st.cache_resource agar pipeline hanya dibangun sekali.
# Tanpa ini, pipeline akan dibangun ulang setiap ada interaksi pengguna.
@st.cache_resource(show_spinner=False)
def load_pipeline():
    return build_rag_pipeline()

# Tampilkan proses loading kepada pengguna
if "pipeline_loaded" not in st.session_state:
    with st.status("Loading AI system, please wait ...", expanded=True) as status:
        chain, num_chunks = load_pipeline()
        st.session_state.chain = chain
        st.session_state.num_chunks = num_chunks
        st.session_state.pipeline_loaded = True
        status.update(
            label=f"AI system ready!",
            state="complete"
        )

chain = st.session_state.chain

# ── Inisialisasi Riwayat Chat ──────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Tampilkan Contoh Pertanyaan (hanya saat belum ada chat) ───────────
if not st.session_state.messages:
    st.info(
        "**Example questions you can ask:**\n\n"
    "- What will students have after graduating?\n"
    "- How is safety handled if an incident occurs at school?\n"
    "- What are the procedures for handling complaints from parents?\n"
    "- What are the consequences for employees who engage in gratification?\n"
    "- What is the procedure for requesting leave as an employee?\n\n"
    "**Contoh pertanyaan dalam Bahasa Indonesia:**\n"
    "- Apa yang akan didapatkan siswa setelah lulus?\n"
    "- Bagaimana penanganan keamanan jika terjadi insiden di sekolah?\n"
    "- Apa prosedur penanganan pengaduan dari orang tua?\n"
    "- Apa konsekuensi bagi karyawan yang terlibat gratifikasi?\n"
    "- Bagaimana prosedur pengajuan cuti sebagai karyawan?"
    )

# ── Tampilkan Riwayat Chat ─────────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    
# ── Input Pengguna ─────────────────────────────────────────────────────
DetectorFactory.seed = 0  # agar hasil konsisten

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        # Kembalikan 'id' untuk indonesia, 'en' untuk english, fallback 'id'
        return 'id' if lang == 'id' else 'en'
    except:
        return 'id'  # fallback ke Indonesia jika gagal



if user_input := st.chat_input("Ask about internal policies and procedures..."):
    # Deteksi bahasa
    user_lang = detect_language(user_input)

    # Buat query yang diperkuat dengan instruksi bahasa
    if user_lang == 'id':
        enhanced_query = f"[WAJIB jawab dalam BAHASA INDONESIA] {user_input}"
    else:
        enhanced_query = f"[MUST answer in ENGLISH] {user_input}"
        
    # Simpan pesan user (tampilkan tanpa prefiks)
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate jawaban
    with st.chat_message("assistant"):
        with st.spinner("Mencari informasi di dokumen ..."):
            result = chain.invoke({"query": enhanced_query})
            answer = result["result"]
            source_docs = result["source_documents"]
        st.markdown(answer)
    
        # # Tampilkan sumber (opsional)
        # with st.expander("📚 Lihat referensi dokumen"):
        #     for i, doc in enumerate(source_docs, 1):
        #         st.text(f"Referensi {i}:")
        #         st.caption(doc.page_content[:300] + "...")
        #         st.divider()
    
     

        # Tampilkan referensi dokumen sumber (bisa di-collapse)
        # with st.expander("Lihat referensi dari katalog"):
        #     for i, doc in enumerate(source_docs, 1):
        #         st.markdown(f"**Referensi {i}:**")
        #         st.text(doc.page_content[:300] + "...")
        #         st.divider()

    # Simpan jawaban ke riwayat
    st.session_state.messages.append({"role": "assistant", "content": answer})


# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📋 About This AI")
    st.markdown(
        "This application is built with **RAG** technology "
        "_(Retrieval-Augmented Generation)_ for answeres" 
        " to user questions based on the foundation's policy documents.\n\n"
        "Answers are drawn **purely** from the foundation's policy documents, with no external sources, "
        "Not sourced from general AI knowledge."
    )

    # st.divider()

    # st.subheader("📱 Produk Tersedia")
    # st.markdown(
    #     "1. Xiaomi Redmi Note 13 Pro+ 5G\n"
    #     "2. Samsung Galaxy A55 5G\n"
    #     "3. OPPO Reno 12 Pro\n"
    #     "4. Samsung Galaxy S24\n"
    #     "5. Apple iPhone 15\n"
    #     "6. Apple iPhone 15 Pro Max"
    # )

    st.divider()

    st.subheader("⚙️ System Architecture")
    st.markdown(
        "```\n"
        "    Rules (TXT)\n"
        "       ↓\n"
        "  Document Loader\n"
        "       ↓\n"
        "  Text Splitter\n"
        "       ↓\n"
        "HuggingFace Embeddings\n"
        "       ↓\n"
        "  FAISS Vector Store\n"
        "       ↓\n"
        "    Retriever\n"
        "       ↓\n"
        " Groq LLM (Llama 3.3)\n"
        "       ↓\n"
        "  Final Answer\n"
        "```"
    )

    st.divider()
            
    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
