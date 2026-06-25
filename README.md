# EM_Rules

Chatbot AI untuk tim compliance yang membantu menjawab pertanyaan terkait kebijakan, regulasi, dan prosedur internal yayasan/sekolah. Dibangun menggunakan teknologi RAG (Retrieval-Augmented Generation) dengan LangChain.

## Arsitektur Sistem

```
Katalog Produk (TXT)
       |
  Document Loader        <- Membaca file katalog
       |
  Text Splitter          <- Memotong dokumen jadi chunk kecil
       |
HuggingFace Embeddings   <- Mengubah teks jadi vektor angka
       |
  FAISS Vector Store     <- Menyimpan vektor untuk pencarian cepat
       |
    Retriever            <- Mencari chunk paling relevan saat ada query
       |
 Groq LLM (Llama 3.3)   <- Merangkai jawaban dari chunk yang diambil
       |
  Jawaban Final
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

Salin file `.env.example` dan rename menjadi `.env`:

```bash
cp .env.example .env
```

Lalu isi API key Groq di file `.env`:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

Cara mendapatkan API key:
1. Buka https://console.groq.com
2. Daftar atau login
3. Klik "Create API Key"
4. Salin dan tempelkan ke file .env

### 3. Jalankan aplikasi

```bash
streamlit run app.py
```

Buka browser dan akses http://localhost:8501

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
    └── 07_complaint_and_grievance_handling_policy.txt <- Penanganan 
    complain

```

## Ruang Lingkup Kebijakan

1. Kebijakan Privasi dan Keamanan Data
2. Kebijakan Akademik/SKL
3. Kebijakan Anti Korupsi dan Gratifikasi
4. Kebijakan Partnership 
5. Kesehatan dan Keselamatan Kerja (K3)
6. Kebijakan Keamanan Siber
7. Kebijakan Penanganan Komplain

## Contoh Pertanyaan

- "Apa yang akan dimiliki peserta didik setelah lulus?"
- "Bagaimana penanganan keselamatan, jika terjadi insident di Sekolah?"
- "SOP apa yang dilakukan oleh perusahaan untuk menangani komplain dari orang tua?"
- "Apa sanksi bagi karyawan yang melakukan gratifikasi?"
- "Bagaimana prosedur pengajuan cuti bagi karyawan?"

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
