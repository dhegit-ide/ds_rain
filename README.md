# 📊 Dashboard Analitik Time Series

Dashboard interaktif berbasis **Streamlit** untuk eksplorasi data (EDA), forecasting, dan evaluasi model time series.  
Dikembangkan dengan struktur modular agar mudah diperluas dan di-debug.

---

## 🚀 Ringkasan
- Mendukung analisis data time series (misalnya curah hujan).
- Menggunakan model **NHITS** untuk forecasting.
- Menyediakan komponen EDA, visualisasi, dan evaluasi hasil cross-validation.
- Input dataset fleksibel: raw data maupun cross-validation dataset.

---

## 📂 Format Dataset
- **Raw data**: wajib menyertakan kolom
  - `ds` → datetime
  - `y` → target variabel
- **Cross-validation data**: wajib menyertakan kolom
  - `ds`, `y`
  - ≥1 kolom tambahan selain `ds` dan `y`

---

## ✨ Fitur Utama
- **EDA (Exploratory Data Analysis)**
  - Preview dataset
  - Informasi meta dataset
  - Statistik deskriptif
  - Seleksi fitur interaktif
- **Forecasting & Evaluasi**
  - Preview dataset cross-validation
  - Deskripsi dataset CV
  - Evaluasi model dengan metrik
- **Modular & Terstruktur**
  - Komponen per baris (row) untuk EDA dan Forecast
  - Folder `data` untuk raw dataset dan cross-validation dataset
- **Dashboard Interaktif**
  - Navigasi tab (EDA vs Forecast)
  - Visualisasi hasil prediksi dan evaluasi model

---

## 🛠️ Cara Penggunaan
1. Clone repository:
   ```
   bash
   git clone https://github.com/username/repo-name.git
   cd repo-name
   ```
2. Install dependency:
   ```
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```
   streamlit run app.py
   ```


