import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard Model Matematika Industri", layout="wide")
st.title("APLIKASI MODEL MATEMATIKA DALAM INDUSTRI")
st.markdown("Dashboard interaktif untuk memahami penerapan model matematika dalam berbagai skenario industri.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Panduan Aplikasi")
    st.markdown("""
    Aplikasi ini mendemonstrasikan empat model matematika kunci melalui studi kasus yang relevan dengan industri di Indonesia.

    **1. Optimasi Produksi:**
    Mencari kombinasi produk yang memaksimalkan keuntungan dengan sumber daya terbatas.
    *Studi Kasus: UKM Mebel Jati*

    **2. Model Persediaan (EOQ):**
    Menentukan kuantitas pesanan optimal untuk meminimalkan total biaya persediaan.
    *Studi Kasus: Kedai Kopi Spesialti*

    **3. Model Antrian:**
    Menganalisis kinerja sistem antrian untuk meningkatkan layanan pelanggan.
    *Studi Kasus: Layanan Drive-Thru Restoran Cepat Saji*

    **4. Keandalan Lini Produksi:**
    Menganalisis keandalan sistem seri dan mengidentifikasi komponen terlemah.
    *Studi Kasus: Lini Perakitan Otomotif*
    """)
    st.divider()
    st.caption("TIF208 - Matematika Terapan | Universitas Pelita Bangsa")
    st.caption("Versi Revisi untuk Presentasi")

# --- TAB 1: OPTIMASI PRODUKSI ---
def optimasi_produksi():
    st.header("Optimasi Produksi Furnitur")
    st.subheader("Studi Kasus: UKM Mebel Jati 'Jati Indah'")
    
    col1, col2 = st.columns([1.5, 2])
    
    with col1:
        st.markdown("""
        **Skenario Bisnis:**
        'Jati Indah', sebuah UKM yang memproduksi mebel jati, ingin menentukan jumlah produksi meja dan kursi yang optimal untuk memaksimalkan keuntungan mingguan, dengan mempertimbangkan keterbatasan jam kerja pengrajin dan stok kayu jati.
        """)
        
        with st.expander("Parameter Model (Bisa Diubah)", expanded=True):
            profit_meja = st.number_input("Keuntungan per Meja (Rp)", min_value=0, value=750000, step=50000)
            profit_kursi = st.number_input("Keuntungan per Kursi (Rp)", min_value=0, value=300000, step=25000)
            jam_meja = st.number_input("Jam Kerja per Meja", min_value=1.0, value=6.0, step=0.5)
            jam_kursi = st.number_input("Jam Kerja per Kursi", min_value=1.0, value=2.0, step=0.5)
            kayu_meja = st.number_input("Kayu untuk Meja (unit)", min_value=1.0, value=4.0, step=0.5)
            kayu_kursi = st.number_input("Kayu untuk Kursi (unit)", min_value=1.0, value=1.5, step=0.5)
            total_jam = st.number_input("Total Jam Kerja Tersedia per Minggu", min_value=1, value=240, step=10)
            total_kayu = st.number_input("Total Kayu Jati Tersedia (unit)", min_value=1, value=120, step=10)

        # --- Perhitungan ---
        # Kendala:
        # jam_meja*x + jam_kursi*y <= total_jam
        # kayu_meja*x + kayu_kursi*y <= total_kayu
        A_matrix = np.array([[jam_meja, jam_kursi], [kayu_meja, kayu_kursi]])
        b_vector = np.array([total_jam, total_kayu])

        # Titik potong dengan sumbu
        x_intercept1 = total_jam / jam_meja if jam_meja > 0 else float('inf')
        y_intercept1 = total_jam / jam_kursi if jam_kursi > 0 else float('inf')
        x_intercept2 = total_kayu / kayu_meja if kayu_meja > 0 else float('inf')
        y_intercept2 = total_kayu / kayu_kursi if kayu_kursi > 0 else float('inf')


        # Titik potong antar kendala
        try:
            intersect_point = np.linalg.solve(A_matrix, b_vector)
            if intersect_point[0] < 0 or intersect_point[1] < 0:
                intersect_point = (0, 0)
        except np.linalg.LinAlgError:
            intersect_point = (0, 0)

        # Titik-titik pojok yang mungkin
        corner_points = [(0, 0)]
        if y_intercept1 > 0 and (kayu_meja*0 + kayu_kursi*y_intercept1 <= total_kayu):
            corner_points.append((0, y_intercept1))
        if y_intercept2 > 0 and (jam_meja*0 + jam_kursi*y_intercept2 <= total_jam):
            corner_points.append((0, y_intercept2))
        if x_intercept1 > 0 and (kayu_meja*x_intercept1 + kayu_kursi*0 <= total_kayu):
            corner_points.append((x_intercept1, 0))
        if x_intercept2 > 0 and (jam_meja*x_intercept2 + jam_kursi*0 <= total_jam):
            corner_points.append((x_intercept2, 0))
        if intersect_point[0] > 0 and intersect_point[1] > 0:
             corner_points.append(tuple(intersect_point))

        # Cari solusi optimal
        optimal_profit = 0
        optimal_point = (0, 0)
        for x, y in set(corner_points):
            profit = profit_meja * x + profit_kursi * y
            if profit > optimal_profit:
                optimal_profit = profit
                optimal_point = (math.floor(x), math.floor(y))

        st.divider()
        st.subheader("Hasil dan Rekomendasi")
        st.success(f"**Rekomendasi Produksi:** Untuk mencapai keuntungan maksimal, 'Jati Indah' harus memproduksi **{optimal_point[0]} Meja** dan **{optimal_point[1]} Kursi** per minggu.")
        
        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.metric(label="💰 Keuntungan Maksimal", value=f"Rp {optimal_profit:,.0f}")
        with col2_res:
            jam_terpakai = jam_meja * optimal_point[0] + jam_kursi * optimal_point[1]
            kayu_terpakai = kayu_meja * optimal_point[0] + kayu_kursi * optimal_point[1]
            st.metric(label="🛠️ Utilisasi Jam Kerja", value=f"{jam_terpakai:.1f} / {total_jam} Jam ({jam_terpakai/total_jam:.1%})")
            st.metric(label="🌲 Utilisasi Kayu Jati", value=f"{kayu_terpakai:.1f} / {total_kayu} Unit ({kayu_terpakai/total_kayu:.1%})")

    with col2:
        st.markdown("#### Visualisasi Daerah Produksi yang Layak (Feasible Region)")
        fig, ax = plt.subplots(figsize=(10, 7))
        
        max_x_intercept = 1
        if x_intercept1 != float('inf') and x_intercept2 != float('inf'):
             max_x_intercept = max(x_intercept1, x_intercept2)

        x = np.linspace(0, max_x_intercept * 1.1, 400)
        
        # Garis kendala jam kerja
        y1 = (total_jam - jam_meja * x) / jam_kursi if jam_kursi > 0 else np.full_like(x, float('inf'))
        ax.plot(x, y1, label=f'Kendala Jam Kerja ({jam_meja}x + {jam_kursi}y <= {total_jam})')
        
        # Garis kendala kayu
        y2 = (total_kayu - kayu_meja * x) / kayu_kursi if kayu_kursi > 0 else np.full_like(x, float('inf'))
        ax.plot(x, y2, label=f'Kendala Kayu ({kayu_meja}x + {kayu_kursi}y <= {total_kayu})')

        # Daerah feasible
        y_feasible = np.minimum(y1, y2)
        ax.fill_between(x, 0, y_feasible, where=(y_feasible>=0), color='green', alpha=0.2, label='Daerah Produksi Layak')
        
        # Titik optimal
        ax.plot(optimal_point[0], optimal_point[1], 'ro', markersize=10, label=f'Titik Optimal ({optimal_point[0]}, {optimal_point[1]})')

        ax.set_xlabel('Jumlah Meja (x)')
        ax.set_ylabel('Jumlah Kursi (y)')
        ax.set_title('Grafik Optimasi Produksi Mebel', fontsize=16)
        ax.legend()
        ax.grid(True)
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        st.pyplot(fig)

# --- TAB 2: MODEL PERSEDIAAN ---
def model_persediaan():
    st.header("Manajemen Persediaan (EOQ)")
    st.subheader("Studi Kasus: Kedai Kopi 'Kopi Kita'")

    col1, col2 = st.columns([1.5, 2])

    with col1:
        st.markdown("""
        **Skenario Bisnis:**
        'Kopi Kita', sebuah kedai kopi spesialti, perlu menentukan jumlah pesanan biji kopi impor yang optimal. Tujuannya adalah untuk meminimalkan total biaya yang mencakup biaya pemesanan (pengiriman, bea cukai) dan biaya penyimpanan (sewa gudang, pendingin).
        """)
        
        with st.expander("Parameter Model (Bisa Diubah)", expanded=True):
            D = st.number_input("Permintaan Tahunan (kg)", min_value=1, value=1200)
            S = st.number_input("Biaya Pemesanan per Pesanan (Rp)", min_value=0, value=500000)
            H = st.number_input("Biaya Penyimpanan per kg per Tahun (Rp)", min_value=0, value=25000)
            lead_time = st.number_input("Lead Time Pengiriman (hari)", min_value=1, value=14)
            hari_kerja = st.number_input("Hari Operasional per Tahun", min_value=1, value=360)

        # --- Perhitungan ---
        if H > 0 and D > 0:
            eoq = math.sqrt((2 * D * S) / H)
            frekuensi_pesanan = D / eoq
            biaya_pemesanan_tahunan = frekuensi_pesanan * S
            biaya_penyimpanan_tahunan = (eoq / 2) * H
            total_biaya = biaya_pemesanan_tahunan + biaya_penyimpanan_tahunan
            permintaan_harian = D / hari_kerja
            rop = permintaan_harian * lead_time
            siklus_pemesanan = hari_kerja / frekuensi_pesanan
        else:
            eoq = 0; total_biaya = 0; rop = 0; siklus_pemesanan = 0

        st.divider()
        st.subheader("Hasil dan Rekomendasi")
        st.success(f"**Kebijakan Persediaan Optimal:** Pesan **{eoq:.0f} kg** biji kopi setiap kali persediaan mencapai **{rop:.1f} kg**. Ini setara dengan memesan kira-kira setiap **{siklus_pemesanan:.1f} hari**.")

        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.metric(label="📦 Kuantitas Pesanan Optimal (EOQ)", value=f"{eoq:.0f} kg")
            st.metric(label="ROP (Titik Pemesanan Ulang)", value=f"{rop:.1f} kg")
        with col2_res:
            st.metric(label="💰 Total Biaya Persediaan Minimum", value=f"Rp {total_biaya:,.0f}")
            st.metric(label="🔄 Siklus Pemesanan", value=f"{siklus_pemesanan:.1f} hari")
            
    with col2:
        st.markdown("#### Visualisasi Biaya Persediaan")
        q_start = 1 if eoq == 0 else eoq * 0.1
        q = np.linspace(q_start, eoq * 2, 100)
        holding_costs = (q / 2) * H
        ordering_costs = (D / q) * S
        total_costs = holding_costs + ordering_costs
        
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.plot(q, holding_costs, 'b-', label='Biaya Penyimpanan (Holding Cost)')
        ax.plot(q, ordering_costs, 'g-', label='Biaya Pemesanan (Ordering Cost)')
        ax.plot(q, total_costs, 'r-', linewidth=3, label='Total Biaya Persediaan')
        if eoq > 0:
            ax.axvline(x=eoq, color='purple', linestyle='--', label=f'EOQ = {eoq:.0f} kg')
        
        ax.set_xlabel('Kuantitas Pemesanan (kg)')
        ax.set_ylabel('Biaya Tahunan (Rp)')
        ax.set_title('Grafik Analisis Biaya Persediaan (EOQ)', fontsize=16)
        ax.legend()
        ax.grid(True)
        ax.ticklabel_format(style='plain', axis='y')
        st.pyplot(fig)

# --- TAB 3: MODEL ANTRIAN ---
def model_antrian():
    st.header("Analisis Sistem Antrian")
    st.subheader("Studi Kasus: Drive-Thru 'Ayam Goreng Juara' saat Jam Sibuk")
    
    col1, col2 = st.columns([1.5, 2])
    
    with col1:
        st.markdown("""
        **Skenario Bisnis:**
        Manajemen 'Ayam Goreng Juara' ingin menganalisis efisiensi layanan drive-thru mereka selama jam makan siang (12:00-13:00). Data menunjukkan tingkat kedatangan dan pelayanan tertentu. Analisis ini bertujuan untuk memahami pengalaman pelanggan dan efisiensi operasional.
        """)

        with st.expander("Parameter Model (Bisa Diubah)", expanded=True):
            lmbda = st.slider("Tingkat Kedatangan (λ - mobil/jam)", 1, 100, 30)
            mu = st.slider("Tingkat Pelayanan (μ - mobil/jam)", 1, 100, 35)
            
        if mu <= lmbda:
            st.error("Tingkat pelayanan (μ) harus lebih besar dari tingkat kedatangan (λ) agar antrian stabil.")
            return

        # --- Perhitungan ---
        rho = lmbda / mu  # Utilisasi
        L = rho / (1 - rho) # Rata-rata mobil dalam sistem
        Lq = (rho**2) / (1 - rho) # Rata-rata mobil dalam antrian
        W = (1 / mu) / (1 - rho) # Rata-rata waktu di sistem (jam)
        Wq = W - (1 / mu) # Rata-rata waktu di antrian (jam)
        p0 = 1 - rho # Probabilitas tidak ada mobil

        st.divider()
        st.subheader("Hasil Analisis Kinerja")
        
        if rho > 0.85:
             st.warning(f"**Peringatan:** Utilisasi sistem **({rho:.1%})** sangat tinggi. Antrian panjang dan waktu tunggu lama kemungkinan besar terjadi, berisiko membuat pelanggan tidak puas.")
        else:
             st.success(f"**Informasi:** Utilisasi sistem **({rho:.1%})** berada pada tingkat yang sehat. Sistem mampu menangani arus pelanggan dengan baik.")

        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.metric(label="🚗 Rata-rata Mobil di Sistem (L)", value=f"{L:.2f} mobil")
            st.metric(label="⏳ Rata-rata Waktu di Sistem (W)", value=f"{W*60:.2f} menit")
        with col2_res:
            st.metric(label="� Rata-rata Mobil dalam Antrian (Lq)", value=f"{Lq:.2f} mobil")
            st.metric(label="⏳ Rata-rata Waktu Menunggu (Wq)", value=f"{Wq*60:.2f} menit")
            
    with col2:
        st.markdown("#### Visualisasi Kinerja Antrian")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))
        
        # Pie chart komposisi waktu
        waktu_pelayanan_menit = (1/mu) * 60
        waktu_tunggu_menit = Wq * 60
        labels = ['Waktu Menunggu', 'Waktu Dilayani']
        sizes = [waktu_tunggu_menit, waktu_pelayanan_menit]
        colors = ['#ff9999','#66b3ff']
        explode = (0.1, 0)
        
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax1.axis('equal')
        ax1.set_title("Komposisi Total Waktu Pelanggan")
        
        # Bar chart utilitas
        labels_util = ['Sibuk (Utilisasi)', 'Idle']
        sizes_util = [rho, 1 - rho]
        colors_util = ['#ff6347', '#90ee90']
        
        ax2.bar(labels_util, sizes_util, color=colors_util)
        ax2.set_ylabel('Proporsi Waktu')
        ax2.set_title('Utilisasi Waktu Server')
        ax2.set_ylim(0, 1)
        for i, v in enumerate(sizes_util):
            ax2.text(i, v + 0.02, f"{v:.1%}", ha='center', fontweight='bold')
            
        st.pyplot(fig)

# --- TAB 4: KEANDALAN LINI PRODUKSI ---
def model_keandalan_produksi():
    st.header("Analisis Keandalan Lini Produksi")
    st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")
    
    col1, col2 = st.columns([1.5, 2])
    
    with col1:
        st.markdown("""
        **Skenario Bisnis:**
        'Nusantara Motor' memiliki lini perakitan yang terdiri dari beberapa stasiun kerja (mesin) yang beroperasi secara seri. Jika salah satu mesin berhenti, seluruh lini produksi akan terhenti. Analisis ini bertujuan untuk menghitung keandalan total lini produksi dan mengidentifikasi mesin mana yang menjadi 'mata rantai terlemah'.
        """)
        
        with st.expander("Parameter Model (Bisa Diubah)", expanded=True):
            r1 = st.slider("Keandalan Mesin Stamping (R1)", 0.80, 1.00, 0.98, 0.01)
            r2 = st.slider("Keandalan Mesin Welding (R2)", 0.80, 1.00, 0.99, 0.01)
            r3 = st.slider("Keandalan Mesin Painting (R3)", 0.80, 1.00, 0.96, 0.01)
            r4 = st.slider("Keandalan Mesin Assembly (R4)", 0.80, 1.00, 0.97, 0.01)

        # --- Perhitungan ---
        # Sistem seri: Rs = R1 * R2 * R3 * ... * Rn
        reliabilities = {'Stamping': r1, 'Welding': r2, 'Painting': r3, 'Assembly': r4}
        keandalan_sistem = np.prod(list(reliabilities.values()))
        
        # Cari komponen terlemah
        weakest_link_name = min(reliabilities, key=reliabilities.get)
        weakest_link_value = reliabilities[weakest_link_name]

        st.divider()
        st.subheader("Hasil Analisis Keandalan")

        st.warning(f"**Mata Rantai Terlemah:** Mesin **{weakest_link_name}** dengan keandalan **{weakest_link_value:.2%}** adalah komponen paling berisiko. Prioritaskan perawatan dan potensi peningkatan pada mesin ini.")

        col1_res, col2_res = st.columns(2)
        with col1_res:
             st.metric(label="📉 Keandalan Keseluruhan Lini", value=f"{keandalan_sistem:.2%}")
        with col2_res:
             st.metric(label="📈 Probabilitas Kegagalan Lini", value=f"{1 - keandalan_sistem:.2%}")

    with col2:
        st.markdown("#### Visualisasi Keandalan Sistem Seri")
        
        # Data untuk bar chart
        labels = list(reliabilities.keys())
        values = list(reliabilities.values())
        
        labels.append("SISTEM TOTAL")
        values.append(keandalan_sistem)
        
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # Warna bar
        bar_colors = ['blue'] * len(reliabilities)
        weakest_idx = list(reliabilities.keys()).index(weakest_link_name)
        bar_colors[weakest_idx] = 'red'
        bar_colors.append('purple')

        bars = ax.bar(labels, values, color=bar_colors)
        
        ax.set_ylabel('Tingkat Keandalan (Reliability)')
        ax.set_title('Perbandingan Keandalan Komponen dan Sistem', fontsize=16)
        ax.set_ylim(min(0.75, min(values) * 0.95), 1.01)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.005, f'{yval:.2%}', ha='center', va='bottom')
            
        st.pyplot(fig)


# --- KONTROL TAB UTAMA ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Optimasi Produksi", 
    "Model Persediaan", 
    "Model Antrian", 
    "Keandalan Lini Produksi"
])

with tab1:
    optimasi_produksi()

with tab2:
    model_persediaan()

with tab3:
    model_antrian()

with tab4:
    model_keandalan_produksi()

# --- FOOTER ---
st.divider()
st.caption("© 2025 TIF208 - Matematika Terapan | Dikembangkan untuk Tugas Kelompok")
�