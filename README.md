# EM_Rules_Assistant

An AI chatbot for compliance teams that helps answer questions about foundation/school policies, regulations, and internal procedures. Built using RAG (Retrieval-Augmented Generation) technology with LangChain.

## System Architecture

```
   Rules (TXT)
       |
  Document Loader        <- Read file
       |
  Text Splitter          <- Cut the document to a little part
       |
HuggingFace Embeddings   <- Change vektor teks to numeric
       |
  FAISS Vector Store     <- Save vector to quick search
       |
    Retriever            <- Search a good chunk with query
       |
 Groq LLM (Llama 3.3)   <- Constructing answers from the captured chunks
       |
  Final Answered
```

## Tech Stack

- LLM: Groq API + Llama 3.3 70B Versatile
- RAG Framework: LangChain
- Embeddings: HuggingFace (paraphrase-multilingual-MiniLM-L12-v2)
- Vector Store: FAISS (lokal, tidak perlu server)
- UI: Streamlit

## Cara Setup dan Menjalankan

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Buat file .env

Copy file `.env.example` and rename to `.env`:

```bash
cp .env.example .env
```

Next fill API key Groq in file `.env`:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

How to get an API key:
1. Go to https://console.groq.com
2. Register or log in
3. Click "Create API Key"
4. Copy and paste it into the .env file

### 3. Jalankan aplikasi

```bash
streamlit run app.py
```

Open browser and access http://localhost:8501

## Struktur Project

```
em_ai/
├── app.py                  <- Antarmuka Streamlit (entry point)
├── rag_pipeline.py         <- Logika RAG LangChain
├── requirements.txt        <- Daftar library yang dibutuhkan
├── .env.example            <- Template konfigurasi API key
├── .env                    <- API key (JANGAN di-commit ke GitHub)
├── .gitignore
├── README.md
└── data/
    └── 01_privacy_and_data_protection_policy.txt  <- Kebijakan       
          privasi
    └── 02_academic_policy_and_graduate_standards.txt <- Kebijakan 
          akademik/SKL
    └── 03_anti_bribery_and_gratuity_policy.txt <- Kebijakan anti 
          korupsi
    └── 04_procurement_and_vendor_partnership_procedure.txt 
          <- Kebijakan kerja sama
    └── 05_occupational_health_and_safety_policy.txt <- Kebijakan K3
    └── 06_technology_usage_and_cybersecurity_policy.txt 
    <- Keamanan siber
    └── 07_complaint_and_grievance_handling_policy.txt <- Penanganan complain
    └── rules.txt <- Gabungan dataset yang digunakan

```

## Policy Scope

1. Privacy and Data Security Policy
2. Academic Policy/SKL
3. Anti-Corruption and Gratification Policy
4. Partnership Policy
5. Occupational Health and Safety (K3)
6. Cybersecurity Policy
7. Complaint Handling Policy

## Contoh Pertanyaan

"**Example questions you can ask:**"
- "What will students have after graduating?"
- "How is safety handled if an incident occurs at school?"
- "What are the procedures for handling complaints from parents?"

"**Contoh pertanyaan dalam Bahasa Indonesia:**"
- "Apa yang akan didapatkan siswa setelah lulus?"
- "Bagaimana penanganan keamanan jika terjadi insiden di sekolah?"
- "Apa prosedur penanganan pengaduan dari orang tua?"

## Deployment ke Streamlit Community Cloud

1. Upload project ke GitHub (pastikan .env tidak ikut ter-commit)
2. Buka https://share.streamlit.io
3. Hubungkan dengan repository GitHub
4. Tambahkan GROQ_API_KEY di bagian Secrets:
   ```
   GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxxxxxx"
   ```
5. Deploy

Catatan: File .env tidak digunakan di Streamlit Cloud.
API key dibaca dari Secrets yang dikonfigurasi di dashboard.
