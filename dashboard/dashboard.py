import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

current_dir = os.path.dirname(__file__)

st. set_page_config(layout="wide")
font_size = "100px"
st.markdown(f'<h1 style="font-size: {font_size}; text-align: center;">Analisis Data Bike Sharing</h1>', unsafe_allow_html=True)


day = pd.read_csv(os.path.join(current_dir,"day_clean.csv"))
hour = pd.read_csv(os.path.join(current_dir,"hour_clean.csv"))

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

# Fungsi untuk menghitung total pemesanan masing-masing user
def cnt_user(df):
    casual = df['casual'].sum()
    registered = df['registered'].sum()
    count = df['count'].sum()
    return casual,registered,count

# Fungsi membuat line plot
def make_Line_Plot(df_x,df_y,labelx=None,labely=None,labelrotation=0):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(df_x,df_y)
    ax.set_ylabel(labely)
    ax.set_xlabel(labelx)
    ax.tick_params(axis='y', labelsize=2)
    ax.tick_params(axis='x', labelsize=2,rotation=labelrotation)
    st.pyplot(fig)

# Fungsi untuk menghitung total pemesanan masing-masing time category
def cnt_timecat(df):
    data = df[['time_category','count']].groupby(by='time_category').sum().reset_index()
    if data.empty:
        Morning=0
        Afternoon=0
        Evening=0
        Night=0
    else:
        Morning = data.loc[data['time_category']=='Morning','count'].values[0]        
        Afternoon = data.loc[data['time_category']=='Afternoon','count'].values[0]
        Evening = data.loc[data['time_category']=='Evening','count'].values[0]
        Night = data.loc[data['time_category']=='Night','count'].values[0]
    return Morning, Afternoon, Evening, Night

# Fungsi membuat bar plot
def make_bar_Plot(df_x,df_y,labelx=None,labely=None,labelrotation=0):
    figx, ax = plt.subplots(figsize=(10, 4))
    ax.bar(df_x, df_y, color='#00827F')
    ax.tick_params(axis='x', labelsize=7,rotation=labelrotation)
    ax.set_ylabel(labely)
    ax.set_xlabel(labelx)
    addlabels(df_x,df_y)
    st.pyplot(figx)

# Baca File csv
day_df = pd.read_csv("dashboard/day_clean.csv")
hour_df = pd.read_csv("dashboard/hour_clean.csv")

# mengolah data
day_df.sort_values(by="rental_date", inplace=True)
hour_df.sort_values(by="rental_date", inplace=True)
day_df['rental_date'] = pd.to_datetime(day_df['rental_date'])
hour_df['rental_date'] = pd.to_datetime(hour_df['rental_date'])

# Membuat Sidebar 
min_date = hour_df["rental_date"].min()
max_date = hour_df["rental_date"].max()


# Membuat Grafik pemesanan berdasarkan kategori musim
st.markdown("""---""")
st.header('1. Rental Berdasarkan Musim')
fig, ax = plt.subplots()
season_rental = day_df[['count','season']].groupby(by='season').sum().reset_index()
season_map = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Salju'}
season_rental['season'] = season_rental['season'].map(season_map)
season_rental.sort_values(by='count', ascending=False,inplace=True)
season_rental = season_rental.reset_index()
col1, col2, col3 = st.columns([1,4,1])
with col2:
    make_bar_Plot(season_rental["season"],season_rental["count"],None,'count',0)
# Membuat analisa kesimpulan
st.markdown('''
    <p style="font-size: 30px;">Analisis Rental Berdasarkan Musim : Performa penyewaan sepeda pada setiap musim terlihat baik dan tidak ada anjlokan yang terlalu jauh. Musim gugur menjadi musim paling ramai untuk menyewa sepeda karena musim gugur adalah musim terbaik untuk bersepeda.</p>
''', unsafe_allow_html=True)

# Membuat Grafik perbandingan pemesanan pada hari kerja dan libur
st.markdown("""---""")
st.header('2. Rental pada Hari Kerja VS Hari Libur')
tab1, tab2 = st.tabs(["by user","by time"])

with tab1:
    col1, col2,col3 = st.columns([1,5,1])
    with col2:
        workingday_rental = day_df[['workingday','casual','registered','count']].groupby(by='workingday').sum().reset_index()
        fig, ax = plt.subplots(figsize=(16, 7))
        ax = workingday_rental.plot(kind='bar', x='workingday', y=['casual', 'registered', 'count'], ax=ax)
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 4., p.get_height()), ha='center', va='center', xytext=(0, 7), textcoords='offset points')
        plt.ylabel('Total')
        plt.xlabel(None)
        plt.xticks([1, 0], ['Workingday', 'Holiday'], rotation=0)
        plt.legend(['Casual', 'Registered', 'count'])
        st.pyplot(fig)

with tab2:
    col1, col2,col3 = st.columns([1,5,1])
    with col2:
        time_rental = hour_df[['time_category','count','workingday']].groupby(['workingday','time_category']).sum().reset_index()
        time_order = ['Morning', 'Afternoon', 'Evening', 'Night']
        time_rental['time_category'] = pd.Categorical(time_rental['time_category'], categories=time_order, ordered=True)
        fig, ax = plt.subplots(figsize=(16, 9))
        ax = sns.barplot(x='workingday', y='count', hue='time_category', data=time_rental, )
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 4., p.get_height()), ha='center', va='center', xytext=(0, 7), textcoords='offset points')
        plt.xlabel(None)
        plt.ylabel('Total')
        plt.xticks([1, 0], ['Workingday', 'Holiday'], rotation=0)
        plt.legend(loc='upper left')
        st.pyplot(fig)


# Membuat analisa kesimpulan
st.markdown('''
    <p style="font-size: 30px;">Analisis Rental pada Hari Kerja VS Hari Libur : Analisis berdasarkan user dan berdasarkan time, jumlah rental pada hari kerja lebih banyak 2 kali lipat dari hari libur. Hal ini bisa terjadi karena sepeda digunakan untuk bekerja atau sekolah.</p>
''', unsafe_allow_html=True)