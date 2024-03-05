import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Membaca file CSV 
main_df = pd.read_csv("main_data.csv")

# Memastikan data
main_df.sort_values(by='dteday', inplace=True)
main_df.reset_index(inplace=True)

main_df['dteday'] = pd.to_datetime(main_df['dteday'])
 
# Menambahkan Judul
st.title('Dashboard Bike Sharing :bike:')

# Menambahkan caption sebagai deskripsi data
st.caption('Dashboard ini menggunakan Bike Sharing Dataset yang berasal dari sumber: https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset ')

# Membuat tab
tab1, tab2, tab3, tab4= st.tabs(["Statistik Deskriptif", "Bar Chart Berdasar Musim", "Scatterplot Suhu vs Cnt", "Pola Data Berdasar Tanggal"])

# Bar chart untuk visualisasi 1
day_season = main_df.groupby(by='season').cnt.sum().reset_index()
season_names = {1: 'springer', 2: 'summer', 3: 'fall', 4: 'winter'}
day_season['season'] = day_season['season'].map(season_names)

with tab1:
    st.caption('Berikut Statistik Deskriptif dari Data')
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        banyak = main_df['dteday'].count()
        st.metric(label="Banyak Data", value="{:,.0f}".format(banyak))

    with col2:
        jumlah = main_df['cnt'].sum()
        st.metric(label="jumlah Peminjaman", value="{:,.0f}".format(jumlah))

    with col3:
        mean = main_df['cnt'].mean()
        st.metric(label="Rata-Rata Peminjaman", value="{:,.0f}".format(mean))

    with col4:
        stdev = main_df['cnt'].std()
        st.metric(label="Standar Deviasi", value="{:,.0f}".format(stdev))

    st.write(pd.DataFrame(main_df))

with tab2:
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = sns.color_palette("hls", 4)
    ax.bar(day_season['season'], day_season['cnt'], color=colors)
    ax.set_title("Jumlah Peminjaman Berdasar Musim", loc="center", fontsize=20)
    ax.set_ylabel("Total Peminjaman")
    ax.set_xlabel("Season")
    ax.set_xticks(day_season['season'], ['Spring', 'Summer', 'Fall', 'Winter'])
    formatter = ticker.StrMethodFormatter('{x:,.0f}')
    ax.yaxis.set_major_formatter(formatter)
    st.pyplot(fig)

with tab3:
    fig3, ax = plt.subplots(figsize=(10, 5))
    sns.regplot(x=main_df['cnt'], y=main_df['temp'])
    st.pyplot(fig3)

with tab4:
    # Membuat Filter
    min_date = main_df['dteday'].min()
    max_date = main_df['dteday'].max()

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date.date(),  # Mengonversi ke tipe data date
        max_value=max_date.date(),  # Mengonversi ke tipe data date
        value=[min_date.date(), max_date.date()] 
    )
    main_df['dteday'] = main_df['dteday'].dt.date

    # Data terfilter
    filtered_df = main_df[(main_df['dteday'] >= start_date) & (main_df['dteday'] <= end_date)]
    
    #plot
    fig2, ax = plt.subplots(figsize=(10, 5))
    ax.plot(filtered_df['dteday'], filtered_df['cnt'], color='#3cb371', marker='o')
    ax.set_xlabel('Tanggal',size=15)
    ax.set_ylabel('Jumlah Peminjam',size=15)
    plt.xticks(rotation=90)
    st.pyplot(fig2)