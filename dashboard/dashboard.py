import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency


# Load data
url = "https://raw.githubusercontent.com/Najiann/dataset/refs/heads/main/all_data.csv"
all_data = pd.read_csv(url)

print(all_data.info())
print(all_data.head())

# HEADER
st.title("Dashboard Penyewaan Sepeda 🚲")

st.markdown("""
    Halloo! Selamat Datang Di Dashboard Analisis Penyewaan Sepeda. Dashboard ini di buat untuk
    memaparkan hasil analisis mengenai penggunaan sepeda b eradarkan dataset "Bike Sharing".
    Dan disini juga akan memaparkan jawaban atas 2 pertanyaan saya yaitu:
    - **Kapan waktu paling banyak penyewaan sepeda berdasarkan musim?**
    - **Bagaimana hubungan suhu dengan penyewaan sepeda?**
    
    Nah, selain kedua itu saya juga akan memaparkan analisis lainnya, yukk langsung saja scroll! ^^
    """)

def sewa_hariandf(df):
    sewa_harian_df = df.groupby('dteday').agg({
        "cnt": "sum", 
        "temp" : "mean"
    }).reset_index()

    sewa_harian_df.rename(columns={
        "cnt": "total_sewa",
        "temp": "average_suhu"
    }, inplace= True) 

    return sewa_harian_df

datetime_columns = ["dteday"]
all_data['dteday'] = pd.to_datetime(all_data['dteday'])

# Side bar 
st.sidebar.header("Pengaturan Dashboard")
st.sidebar.markdown("Silahkan Gunakan Pengaturan Di Bawah Ini Sebagai Filter ^_^")

min_date = all_data['dteday'].min()
max_date = all_data['dteday'].max()

with st.sidebar:
    min_date = all_data['dteday'].min().date()
    max_date = all_data['dteday'].max().date()

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date,max_date]
    )

start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

main_df = all_data[(all_data['dteday'] >= start_date) & (all_data['dteday'] <= end_date)]
# end side bar

# Line Chart untukk penyewaan daily
st.subheader("Sewa Harian")
fig, ax = plt.subplots(figsize=(16,8))
ax.plot(all_data['dteday'], all_data['cnt'], marker='o', color="#90CAF9", linewidth=2)
ax.set_xlabel("Tanggal", fontsize=15)
ax.set_ylabel("Sewa Harian", fontsize=20)
st.pyplot(fig)    

# pertanyaan nomor 1 
musim = {1: "Musim Dingin", 2: "Musim Semi", 3: "Musim Panas", 4: "Musim Gugur"}
all_data['season'] = all_data['season'].map(musim)

st.subheader("Kapan waktu paling banyak penyewaan sepeda berdasarkan musim?")
fig, ax = plt.subplots(figsize=(10,6))

sns.barplot(x="season", y="cnt", data=all_data, color="skyblue", ax=ax)
ax.set_title("Penyewaan Berdasarkan Musim")
ax.set_xlabel("Musim", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=13)
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """ musim yang memiliki jumlah penyewaan sepeda tertinggi adalah musim panas, sementara di urutan kedua ada musim gugur. 
            mungkin ini di sebabkan karena cuacanya yang nyaman dan hangat untuk melakukan aktivitas di luar ruangan seperti bersepeda
        """
    )

# Pertanyaan nomor 2
st.subheader("Bagaimana hubungan suhu dengan penyewaan sepeda?")
fig, ax = plt.subplots(figsize=(12,6))
sns.scatterplot(x=all_data['temp'], y=all_data['cnt'], color="#90CAF9", ax=ax)
ax.set_title("Relasi Antara Suhu Dan Penyewaan", fontsize=18)
ax.set_xlabel("Suhu", fontsize=14)
ax.set_ylabel("Total Sewa", fontsize=14)
st.pyplot(fig)  

with st.expander("See explanation"):
    st.write(
        """ regresi antara suhu dan penyewaan sepeda menunjukkan hasil yang positif jelas. semakin tinggi suhu, semakin banyak sepeda yang disewa. 
        itu di karenakan cuaca yang nyaman untuk melakukan aktifitas luar ruangan.
        """
    )

# ANALISIS LANJUTAN
# 1:  pola berdasarkan jam
st.subheader("Pola penyewaan bersadarkan jam")
hourly_usage = all_data.groupby("hr")["cnt"].mean()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=hourly_usage.index, y=hourly_usage.values, marker="o", color="coral", ax=ax)
ax.set_title("Rata rata penyewaan sepeda berdasarkan hari libu vs. hari kerja", fontsize=14)
ax.set_xlabel("Jam", fontsize=12)
ax.set_ylabel("Jumlah rata rata penyewaan", fontsize=12)
plt.xticks(range(0,24))
plt.grid(axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
        """ Penyewaan sepeda paling banyak terjadi pada jam 8 pagi dan 6 sore, 
        yang dimana di jam jam tersebut adalah jam berangkat dan pulang kerja.
        """
    )

# 2: pola hari kerja vs. hari libur
st.subheader("Pola hari kerja vs. hari libur")
harikerja_usage = all_data.groupby("workingday")["cnt"].mean()
harikerja_labels = ["Libur", "Hari Kerja"]

fig, ax = plt.subplots(figsize=(8,6))
sns.barplot(x=harikerja_labels, y=harikerja_usage.values, palette="pastel")
ax.set_title("Rata-rata Penyewaan: Hari Kerja vs Hari Libur", fontsize=16)
ax.set_xlabel("Kategori", fontsize=14)
ax.set_ylabel("Jumlah Penyewaan Rata-rata", fontsize=14)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

with st.expander("See explanation"):
    st.text("""
    Penyewaan sepeda lebih banyak terjadi pada hari kerja dibandingkan hari libur, 
    hal ini menunjukkan bahwa sepeda banyak digunakan untuk keperluan aktivitas harian seperti berangkat kerja.
    """)

# 3: pola berdasarkan bulan
st.subheader("Pola penyewaan berdasarkan bulan")
monthly_usage = all_data.groupby("mnth")["cnt"].mean()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=monthly_usage.index, y=monthly_usage.values, palette="coolwarm", ax=ax)
ax.set_title("Rata rata penyewaan sepeda berdasarkan bulan", fontsize=14)
ax.set_xlabel("bulan", fontsize=12)
ax.set_ylabel("Jumlah rata rata penyewaan", fontsize=12)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

with st.expander("See explanation"):
    st.text("""
    Penyewaan sepeda tertinggi terjadi pada bulan juni yang pertepatan dengan musim panas 
    dan september yang bertepatan dengan musim gugur. Hal ini bisa terjadi karena
    cuaca atau suhu yang nyaman untuk aktifitas di luar ruangan.
    """)

# Footer

st.caption('Jiannala 2025')

