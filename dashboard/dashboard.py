import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Dashboard E-Commerce Olist", layout="wide")


@st.cache_data
def load_data():
    return pd.read_csv(Path(__file__).parent / "main_data.csv", parse_dates=["order_purchase_timestamp"])


def rupiah_style(angka):
    return f"{angka:,.0f}".replace(",", ".")


all_df = load_data()

st.sidebar.header("Filter")
tgl_min = all_df["order_purchase_timestamp"].min().date()
tgl_max = all_df["order_purchase_timestamp"].max().date()
rentang = st.sidebar.date_input(
    "Rentang tanggal pembelian", value=(tgl_min, tgl_max), min_value=tgl_min, max_value=tgl_max
)

awal, akhir = rentang if len(rentang) == 2 else (tgl_min, tgl_max)

main_df = all_df[
    (all_df["order_purchase_timestamp"].dt.date >= awal) & (all_df["order_purchase_timestamp"].dt.date <= akhir)
]
pesanan_df = main_df.drop_duplicates("order_id")

st.title("Dashboard Analisis E-Commerce Olist")
st.caption("Pesanan delivered Januari 2017 - Agustus 2018. Nilai uang dalam Real Brasil (R$).")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pendapatan", f"R$ {rupiah_style(main_df['price'].sum())}")
col2.metric("Jumlah Pesanan", rupiah_style(pesanan_df["order_id"].nunique()))
col3.metric("Pesanan Terlambat", f"{pesanan_df['terlambat'].mean() * 100:.1f}%")
col4.metric("Rata-rata Review", f"{pesanan_df['review_score'].mean():.2f}")

st.subheader("Pertanyaan 1: Kategori dengan Pertumbuhan Pendapatan Tertinggi")
st.caption("Perbandingan Januari-Agustus 2018 dengan Januari-Agustus 2017. Bagian ini tidak mengikuti filter tanggal karena periodenya sudah ditetapkan.")

@st.cache_data
def hitung_pertumbuhan(df):
    df = df.copy()
    df["tahun"] = df["order_purchase_timestamp"].dt.year
    df["bulan"] = df["order_purchase_timestamp"].dt.month
    df = df[(df["bulan"] <= 8) & (df["tahun"].isin([2017, 2018]))]

    total = df.groupby("tahun")["price"].sum()
    pertumbuhan_total = (total[2018] / total[2017] - 1) * 100

    df = df[df["kategori"] != "unknown"]
    tabel = df.pivot_table(index="kategori", columns="tahun", values="price", aggfunc="sum").fillna(0)
    total_2018 = tabel[2018].sum()

    tabel = tabel[tabel[2017] >= 50000].copy()
    tabel["pertumbuhan_%"] = (tabel[2018] / tabel[2017] - 1) * 100
    tabel["kontribusi_2018_%"] = tabel[2018] / total_2018 * 100
    return tabel, pertumbuhan_total


pertumbuhan_df, pertumbuhan_total = hitung_pertumbuhan(all_df)

jumlah = st.slider("Jumlah kategori yang ditampilkan", 5, 15, 10)
top_df = (pertumbuhan_df.sort_values("pertumbuhan_%", ascending=False)
          .head(jumlah).sort_values("pertumbuhan_%"))

warna = ["#1f77b4" if x > pertumbuhan_total else "#b0b0b0" for x in top_df["pertumbuhan_%"]]

fig, ax = plt.subplots(figsize=(10, 0.55 * jumlah + 1.5))
ax.barh(top_df.index, top_df["pertumbuhan_%"], color=warna)
ax.axvline(pertumbuhan_total, color="black", linestyle="--", linewidth=1,
           label=f"Pertumbuhan total: {pertumbuhan_total:.1f}%")

batas_x = top_df["pertumbuhan_%"].max()
for i, (nilai, kontribusi) in enumerate(zip(top_df["pertumbuhan_%"], top_df["kontribusi_2018_%"])):
    ax.text(max(nilai, pertumbuhan_total) + batas_x * 0.015, i,
            f"{nilai:.0f}% (kontribusi {kontribusi:.1f}%)", va="center", fontsize=9)

ax.set_title("Pertumbuhan Pendapatan per Kategori\nJan-Agu 2018 dibandingkan Jan-Agu 2017", fontsize=12)
ax.set_xlabel("Pertumbuhan pendapatan (%)")
ax.set_xlim(0, batas_x * 1.6)
ax.legend(loc="lower right")
plt.tight_layout()
st.pyplot(fig)

st.subheader("Pertanyaan 2: Keterlambatan Pengiriman dan Review Score")
st.caption("Bagian ini mengikuti filter tanggal di sidebar.")

review_df = pesanan_df.dropna(subset=["review_score"]).copy()
skor_tepat = review_df[~review_df["terlambat"]]["review_score"]
telat_df = review_df[review_df["terlambat"]].copy()

if telat_df.empty:
    st.info("Tidak ada pesanan terlambat pada rentang tanggal ini.")
else:
    telat_df["kelompok"] = pd.cut(
        telat_df["hari_telat"],
        bins=[-1, 3, 7, 14, float("inf")],
        labels=["0-3 hari", "4-7 hari", "8-14 hari", "lebih dari 14 hari"],
    )
    skor_telat = telat_df.groupby("kelompok", observed=True)["review_score"].agg(["mean", "count"])

    labels = ["Tepat waktu"] + [f"Terlambat\n{k}" for k in skor_telat.index]
    nilai = [skor_tepat.mean()] + list(skor_telat["mean"])
    jumlah_pesanan = [skor_tepat.count()] + list(skor_telat["count"])
    warna = ["#1f77b4"] + ["#b0b0b0"] * len(skor_telat)

    selisih = skor_tepat.mean() - telat_df["review_score"].mean()

    fig2, ax2 = plt.subplots(figsize=(10, 5.5))
    ax2.bar(labels, nilai, color=warna)
    for i, (n, j) in enumerate(zip(nilai, jumlah_pesanan)):
        ax2.text(i, n + 0.08, f"{n:.2f}\n({rupiah_style(j)} pesanan)", ha="center", fontsize=9)

    ax2.set_title("Rata-rata Review Score Berdasarkan Ketepatan Pengiriman\n"
                  f"Selisih tepat waktu vs terlambat: {selisih:.2f} poin", fontsize=12)
    ax2.set_ylabel("Rata-rata review score (skala 1-5)")
    ax2.set_ylim(0, 5.3)
    plt.tight_layout()
    st.pyplot(fig2)

    st.subheader("Analisis Lanjutan: Segmentasi Pelanggan (RFM)")
st.caption("Segmentasi memakai seluruh data (Januari 2017 - Agustus 2018), jadi tidak mengikuti filter tanggal. "
           "97% pelanggan hanya membeli sekali, sehingga segmen dibuat manual.")


@st.cache_data
def hitung_rfm(df):
    tanggal_acuan = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("customer_unique_id").agg(
        recency=("order_purchase_timestamp", lambda x: (tanggal_acuan - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("price", "sum"),
    ).reset_index()

    batas_recency = rfm["recency"].median()
    batas_monetary = rfm["monetary"].quantile(0.75)

    kondisi = [
        rfm["frequency"] >= 2,
        (rfm["recency"] <= batas_recency) & (rfm["monetary"] >= batas_monetary),
        (rfm["recency"] > batas_recency) & (rfm["monetary"] >= batas_monetary),
        rfm["recency"] <= batas_recency,
    ]
    nama_segmen = ["Pelanggan Berulang", "Baru - Bernilai Tinggi", "Lama - Bernilai Tinggi", "Baru - Nilai Biasa"]
    rfm["segmen"] = np.select(kondisi, nama_segmen, default="Lama - Nilai Biasa")

    ringkasan = rfm.groupby("segmen").agg(
        jumlah=("customer_unique_id", "count"),
        rata_monetary=("monetary", "mean"),
        total_monetary=("monetary", "sum"),
    )
    ringkasan["persen_pelanggan"] = ringkasan["jumlah"] / ringkasan["jumlah"].sum() * 100
    ringkasan["persen_pendapatan"] = ringkasan["total_monetary"] / ringkasan["total_monetary"].sum() * 100
    return ringkasan, batas_recency, batas_monetary


ringkasan_rfm, batas_recency, batas_monetary = hitung_rfm(all_df)

st.write(f"Pelanggan **Baru** terakhir membeli dalam {batas_recency:.0f} hari terakhir (median recency), "
         f"sedangkan **Bernilai Tinggi** berarti pengeluaran minimal R$ {batas_monetary:.1f} (kuartil teratas).")

plot_df = ringkasan_rfm.sort_values("persen_pendapatan")[["persen_pelanggan", "persen_pendapatan"]]

fig3, ax3 = plt.subplots(figsize=(10, 5.5))
plot_df.plot(kind="barh", ax=ax3, color=["#b0b0b0", "#1f77b4"], width=0.75)
for container in ax3.containers:
    ax3.bar_label(container, fmt="%.1f%%", padding=3, fontsize=9)

ax3.set_title("Proporsi Pelanggan vs Kontribusi Pendapatan per Segmen RFM", fontsize=12)
ax3.set_xlabel("Persentase (%)")
ax3.set_ylabel("")
ax3.set_xlim(0, 45)
ax3.legend(["% pelanggan", "% pendapatan"], loc="lower right")
plt.tight_layout()
st.pyplot(fig3)

with st.expander("Lihat tabel ringkasan segmen"):
    tabel_tampil = ringkasan_rfm.sort_values("jumlah", ascending=False).round(1)
    tabel_tampil.columns = ["Jumlah Pelanggan", "Rata-rata Pengeluaran (R$)", "Total Pengeluaran (R$)",
                            "% Pelanggan", "% Pendapatan"]
    st.dataframe(tabel_tampil)