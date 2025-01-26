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
    memaparkan hasil analisis mengenai penggunaan sepeda beradarkan dataset "Bike Sharing".
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

st.sidebar.subheader("Filter Berdasarkan Bulan atau Tahun")
# end side bar

# Line Chart untukk penyewaan daily
st.subheader("Sewa Harian")
fig, ax = plt.subplots(figsize=(16,8))
ax.plot(main_df['dteday'], main_df['cnt'], marker='o', color="#90CAF9", linewidth=2)
ax.set_xlabel("Tanggal", fontsize=15)
ax.set_ylabel("Sewa Harian", fontsize=20)
st.pyplot(fig)    

# pertanyaan nomor 1 
musim = {1: "Musim Dingin", 2: "Musim Semi", 3: "Musim Panas", 4: "Musim Gugur"}
all_data['season'] = all_data['season'].map(musim)

st.subheader("Kapan waktu paling banyak penyewaan sepeda berdasarkan musim?")
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(x="season", y="cnt", hue="season", data=all_data, palette="coolwarm", ax=ax)
ax.set_title("Penyewaan Berdasarkan Musim")
ax.set_xlabel("season", fontsize=14)
ax.set_ylabel("Total Sewa", fontsize=14)
st.pyplot(fig)

st.text("""musim yang memiliki jumlah penyewaan sepeda tertinggi adalah musim panas, sementara di urutan kedua ada musim gugur. 
             mungkin ini di sebabkan karena cuacanya yang nyaman dan hangat untuk melakukan aktivitas di luar ruangan seperti bersepeda
             """)

# Pertanyaan nomor 2
st.subheader("Bagaimana hubungan suhu dengan penyewaan sepeda?")
fig, ax = plt.subplots(figsize=(12,6))
sns.scatterplot(x=main_df['temp'], y=main_df['cnt'], color="#90CAF9", ax=ax)
ax.set_title("Relasi Antara Suhu Dan Penyewaan", fontsize=18)
ax.set_xlabel("Suhu", fontsize=14)
ax.set_ylabel("Total Sewa", fontsize=14)
st.pyplot(fig)  

st.text("""regresi antara suhu dan penyewaan sepeda menunjukkan hasil yang positif jelas. semakin tinggi suhu, semakin banyak sepeda yang disewa. 
        itu di karenakan cuaca yang nyaman untuk melakukan aktifitas luar ruangan.
    """)

# catatan bawah
st.subheader("Insight: ")
st.markdown("""
    - **Recency** menggambarkan waktu terakhir pelanggan menyewa sepeda. Semakin rendah nilai recency, semakin baru aktivitas pelanggan.
    - **Frequency** menggambarkan jumlah total sewa sepeda dalam waktu yang sudah ditentukan. Semakin tinggi nilai frequency, semakin sering pelanggan menyewa.
    - **Monetary** mengukur jumlah total penyewaan dalam suatu waktu, yang menghitung seberapa banyak uang yang dihasilkan dari setiap bulannya.
""")

# RFM Analisinya
st.subheader("Analisis Recency, Frequency, dan Monetary (RFM)")

all_data['dteday'] = pd.to_datetime(all_data['dteday'])
last_date = all_data['dteday'].max()
all_data['recency'] = (last_date - all_data['dteday']).dt.days

# Frequency
all_data['month'] = all_data['dteday'].dt.to_period('M')  
frequency = all_data.groupby('month')['cnt'].sum()

# Monetary
monetary = all_data.groupby('month')['cnt'].sum()

# Recency
recency = all_data.groupby('month')['recency'].min()

# Gabungkan ketiganya
rfm = pd.DataFrame({
    'recency': recency,
    'frequency': frequency,
    'monetary': monetary
}).reset_index()

pilih_bulan = st.sidebar.selectbox("Pilih Bulan", pd.to_datetime(all_data['dteday']).dt.month.unique())
filter_data = all_data[all_data['dteday'].dt.month == pilih_bulan]

st.subheader(f"Data Penyewaan Sepeda untuk Bulan {pilih_bulan}")
st.write(filter_data)

# Footer
st.caption('Jiannala 2025')
