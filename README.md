# Proyek Analisis Data: E-Commerce Public Dataset (Olist)

https://olist-business-intelligence.streamlit.app/

Submission Proyek Akhir untuk Kelas **"Belajar Analisis Data dengan Python"** - Dicoding Indonesia.

- **Nama:** Kartika Nur Savira
- **Dataset:** Brazilian E-Commerce Public Dataset by Olist
- **Domain:** E-Commerce, Supply Chain & Logistics, Customer Segmentation (RFM)

---

## Ringkasan Proyek

Proyek ini bertujuan untuk menganalisis performa bisnis dan operasional platform e-commerce Olist di Brasil pada periode **Januari 2017 – Agustus 2018** (pesanan berstatus *delivered*). Analisis ini mencakup:
1. **Performa Kategori Produk:** Identifikasi kategori penyumbang revenue tertinggi dan kuantitas unit terjual terbanyak serta kategori underperformer.
2. **Logistik & Kepuasan Pelanggan:** Mengukur dampak keterlambatan pengiriman terhadap penurunan skor review dan lonjakan ulasan negatif.
3. **Sebaran Geografis Konsumen:** Pemetaan konsentrasi pasar dan disparitas waktu tempuh serta rasio keterlambatan antardaerah di Brasil.
4. **Segmentasi Pelanggan (RFM):** Pengelompokan perilaku belanja konsumen (*Recency, Frequency, Monetary*) untuk merancang strategi retensi dan reaktivasi yang tepat sasaran.

---

## Struktur Berkas

```
submission
├── dashboard
│   ├── dashboard.py         # Skrip aplikasi dashboard Streamlit modern & interaktif
│   └── main_data.csv        # Data hasil pembersihan & agregasi untuk dashboard
├── data
│   ├── customers_dataset.csv
│   ├── geolocation_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   ├── products_dataset.csv
│   └── sellers_dataset.csv
├── Proyek_Analisis_Data.ipynb # Jupyter Notebook analisis lengkap dari Data Wrangling hingga Kesimpulan
├── README.md                 # Dokumentasi proyek
├── requirements.txt          # Daftar pustaka Python yang dibutuhkan
└── url.txt                   # Tautan aplikasi dashboard yang telah di-deploy (opsional)
```

---

## Panduan Menjalankan Proyek di Lokal

### 1. Prasyarat
Pastikan Python 3.9+ telah terpasang di komputer Anda.

### 2. Membuat dan Mengaktifkan Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Menginstal Dependensi
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Dashboard Streamlit
```bash
streamlit run dashboard/dashboard.py
```
Aplikasi akan secara otomatis terbuka pada peramban web di alamat `http://localhost:8501`.

---

## Pertanyaan Bisnis (Metode SMART)

1. **Pertanyaan 1 (Performa Kategori):** Kategori produk apa saja yang menghasilkan total revenue tertinggi dan kuantitas unit terjual terbanyak, serta kategori mana yang paling rendah selama periode Januari 2017 – Agustus 2018?
2. **Pertanyaan 2 (Logistik & Review):** Seberapa besar penurunan rata-rata review score dan kenaikan persentase review negatif (skor 1–2) pada pesanan yang terlambat dibandingkan pesanan yang tiba tepat waktu selama periode Januari 2017 – Agustus 2018?
3. **Pertanyaan 3 (Sebaran Geografis):** Negara bagian (state) mana yang menyumbang jumlah pelanggan dan revenue terbesar, serta di state mana performa pengiriman paling lambat dan persentase keterlambatan paling tinggi selama periode Januari 2017 – Agustus 2018?

---

## Temuan Utama (Key Insights)

- **Revenue vs Volume:** Kategori `bed_bath_table` memimpin volume penjualan (10.945 unit), namun kategori `health_beauty` (R$ 1,23 juta) dan `watches_gifts` (R$ 1,16 juta) menghasilkan pendapatan tertinggi karena harga rata-rata yang lebih tinggi.
- **Titik Kritis Logistik:** Pesanan terlambat hanya mencakup 8,1% dari total pesanan, namun kepuasan pelanggan anjlok tajam: rata-rata rating turun dari **4.30 ke 2.57**, dan review negatif melonjak dari **9.1% ke 52.9%** (bahkan mencapai **76.1%** untuk keterlambatan >7 hari).
- **Dominasi Wilayah:** Negara bagian São Paulo (SP) menyumbang **38.4% total revenue** dan **41.9% pelanggan**, sedangkan tantangan logistik terberat berada di wilayah Utara (waktu kirim 24–30 hari) dan Timur Laut (rasio keterlambatan hingga 24% di Alagoas).
- **Potensi Retensi:** Hanya **3.0%** pelanggan yang merupakan pembeli berulang (*repeat buyer*), sementara **23.6%** merupakan pelanggan bernilai tinggi yang berisiko hilang (*at-risk high value*).
