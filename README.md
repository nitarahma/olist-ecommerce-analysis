# Analisis Data E-Commerce Olist (2017-2018)

Proyek analisis data pada dataset e-commerce Brasil (Olist) untuk menjawab dua pertanyaan bisnis: kategori produk mana yang paling cepat tumbuh, dan bagaimana keterlambatan pengiriman berkaitan dengan kepuasan pelanggan. Hasilnya disajikan dalam notebook dan dashboard interaktif Streamlit.

**Dashboard:** [isi tautan Streamlit Cloud setelah deploy]

## Pertanyaan Bisnis

1. Kategori produk apa yang memiliki pertumbuhan pendapatan (dalam Real Brasil) tertinggi dari pesanan berstatus delivered pada periode Januari-Agustus 2018 dibandingkan Januari-Agustus 2017, dan berapa persen kontribusi masing-masing kategori terhadap total pendapatan 2018?
2. Berapa selisih rata-rata review score antara pesanan yang tiba tepat waktu dan yang terlambat dari estimasi pada pesanan delivered selama Januari 2017 sampai Agustus 2018?

## Temuan Utama

- Pendapatan Januari-Agustus tumbuh **141,1%**, dari sekitar R$ 2,99 juta (2017) menjadi R$ 7,22 juta (2018).
- Kategori `health_beauty` (tumbuh 210,3%, kontribusi 10,6%) dan `watches_gifts` (tumbuh 241,8%, kontribusi 9,6%) tumbuh cepat sekaligus berkontribusi besar. Kategori `baby` tumbuh paling tinggi (268,6%), tetapi kontribusinya baru 3,5%.
- Sebanyak **8,1%** pesanan terlambat. Rata-rata review score pesanan tepat waktu **4,30**, sedangkan pesanan terlambat **2,57** (selisih **1,73 poin**). Skor turun tajam setelah keterlambatan melewati 3 hari.
- Analisis RFM: **97%** pelanggan hanya membeli sekali. Segmen Bernilai Tinggi hanya 23,2% dari pelanggan tetapi menyumbang 57,9% pendapatan.

## Rekomendasi

- Prioritaskan stok dan promosi pada kategori yang tumbuh cepat dan berkontribusi besar.
- Tekan keterlambatan pengiriman agar tidak melewati 3 hari dari estimasi.
- Jalankan kampanye pengaktifan kembali untuk pelanggan lama bernilai tinggi dan bangun program loyalitas untuk mendorong pembelian ulang.

## Teknik dan Alat

Python, Pandas, NumPy, Matplotlib, Seaborn, Streamlit. Tahapan: data wrangling (gathering, assessing, cleaning), exploratory data analysis, visualisasi, dan analisis lanjutan RFM dengan segmentasi manual.

## Struktur Folder

```
submission
├───dashboard
│   ├───dashboard.py
│   └───main_data.csv
├───data
│   └───... (9 file CSV dataset Olist)
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Cara Menjalankan Dashboard

1. Buka terminal pada folder proyek (`submission`).
2. Buat dan aktifkan virtual environment (opsional, tetapi disarankan):
```
   python -m venv venv
   venv\Scripts\activate
```
3. Pasang library yang dibutuhkan:
```
   pip install -r requirements.txt
```
4. Jalankan dashboard:
```
   streamlit run dashboard/dashboard.py
```
5. Dashboard terbuka di browser, biasanya pada `http://localhost:8501`.

## Catatan Data

- Sumber data: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) di Kaggle (lisensi CC BY-NC-SA 4.0).
- Seluruh nilai uang menggunakan Real Brasil (R$) sesuai dokumentasi dataset. Pendapatan dihitung dari harga barang (`price`) tanpa ongkos kirim.
- Analisis dibatasi pada pesanan berstatus delivered periode Januari 2017 sampai Agustus 2018, karena volume pesanan di luar periode itu sangat kecil.

## Pembuat

[Isi nama] - [isi ID Dicoding atau tautan profil]