import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats

# Konfigurasi halaman
st.set_page_config(page_title="Model Matematika Industri", layout="wide")
st.title("APLIKASI MODEL MATEMATIKA DALAM INDUSTRI")

# Sidebar
with st.sidebar:
    st.header("Panduan Aplikasi")
    st.markdown("""
    **Tab 1: Optimasi Produksi**  
    Masukkan parameter produksi untuk optimasi keuntungan  
    Visualisasi: Grafik daerah solusi optimal  
    
    **Tab 2: Model Persediaan**  
    Hitung EOQ untuk minimalisasi biaya persediaan  
    Visualisasi: Grafik hubungan biaya dan kuantitas pesanan  
    
    **Tab 3: Model Antrian**  
    Analisis sistem antrian M/M/1  
    Visualisasi: Diagram metrik kinerja antrian  
    
    **Tab 4: Model Pertumbuhan**  
    Prediksi pertumbuhan eksponensial dalam industri  
    Visualisasi: Grafik proyeksi pertumbuhan
    """)
    st.divider()
    st.caption("TIF208 - Matematika Terapan | Universitas Pelita Bangsa")

# Tab 1: Optimasi Produksi (Linear Programming)
def optimasi_produksi():
    st.header("Model Optimasi Produksi")
    st.subheader("Linear Programming")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Parameter Produksi")
        profit_a = st.number_input("Keuntungan Produk A (Rp)", min_value=0, value=40000, step=1000)
        profit_b = st.number_input("Keuntungan Produk B (Rp)", min_value=0, value=60000, step=1000)
        waktu_a = st.number_input("Waktu Mesin Produk A (jam)", min_value=0.0, value=2.0, step=0.5)
        waktu_b = st.number_input("Waktu Mesin Produk B (jam)", min_value=0.0, value=3.0, step=0.5)
        total_waktu = st.number_input("Total Waktu Mesin Tersedia (jam)", min_value=0, value=100, step=10)
        
        # Hitung solusi
        x1 = total_waktu / waktu_a
        y1 = 0
        x2 = 0
        y2 = total_waktu / waktu_b
        
        # Fungsi objektif
        Z1 = profit_a * x1 + profit_b * y1
        Z2 = profit_a * x2 + profit_b * y2
        
        solusi = "50 unit A" if Z1 >= Z2 else f"{y2:.0f} unit B"
        profit_max = max(Z1, Z2)
        
        # Tampilkan hasil
        st.divider()
        st.metric("Solusi Optimal", solusi)
        st.metric("Keuntungan Maksimal", f"Rp{profit_max:,.0f}")
        st.markdown(f"**Interpretasi**: Produksi **{solusi}** untuk memaksimalkan keuntungan")
    
    with col2:
        # Visualisasi grafik
        st.markdown("### Grafik Daerah Solusi")
        fig, ax = plt.subplots()
        
        # Plot garis kendala
        x = np.linspace(0, x1 + 10, 100)
        y = (total_waktu - waktu_a * x) / waktu_b
        ax.plot(x, y, 'r-', label=f'2x + 3y ≤ {total_waktu}')
        
        # Plot titik solusi
        ax.plot(x1, y1, 'bo', label=f'Produk A ({x1:.0f},0)')
        ax.plot(x2, y2, 'go', label=f'Produk B (0,{y2:.0f})')
        
        # Area feasible
        ax.fill_between(x, 0, y, where=(y >= 0), alpha=0.1, color='blue')
        
        ax.set_xlim(0, max(x1, x2) + 10)
        ax.set_ylim(0, max(y1, y2) + 10)
        ax.set_xlabel('Jumlah Produk A')
        ax.set_ylabel('Jumlah Produk B')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# Tab 2: Model Persediaan (EOQ)
def model_persediaan():
    st.header("Model Persediaan (EOQ)")
    st.subheader("Economic Order Quantity")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Parameter Permintaan")
        D = st.number_input("Permintaan Tahunan (unit)", min_value=1, value=10000)
        S = st.number_input("Biaya Pemesanan per Pesanan (Rp)", min_value=0, value=50000)
        H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", min_value=0, value=2000)
        
        # Hitung EOQ
        eoq = math.sqrt((2 * D * S) / H)
        total_pesanan = D / eoq
        biaya_pemesanan = total_pesanan * S
        biaya_penyimpanan = (eoq / 2) * H
        total_biaya = biaya_pemesanan + biaya_penyimpanan
        
        # Tampilkan hasil
        st.divider()
        st.metric("EOQ Optimal", f"{eoq:.0f} unit")
        st.metric("Total Biaya Minimum", f"Rp{total_biaya:,.0f}")
        st.markdown(f"**Interpretasi**: Pesan **{eoq:.0f} unit** setiap kali pemesanan")
    
    with col2:
        # Visualisasi grafik
        st.markdown("### Grafik Biaya Total")
        quantities = np.linspace(100, 2000, 50)
        holding_costs = (quantities / 2) * H
        ordering_costs = (D / quantities) * S
        total_costs = holding_costs + ordering_costs
        
        fig, ax = plt.subplots()
        ax.plot(quantities, holding_costs, 'b-', label='Biaya Penyimpanan')
        ax.plot(quantities, ordering_costs, 'g-', label='Biaya Pemesanan')
        ax.plot(quantities, total_costs, 'r-', label='Total Biaya')
        ax.plot(eoq, total_biaya, 'ro', label='EOQ Optimal')
        
        ax.set_xlabel('Kuantitas Pemesanan (unit)')
        ax.set_ylabel('Biaya (Rp)')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

# Tab 3: Model Antrian (M/M/1)
def model_antrian():
    st.header("Model Antrian (M/M/1)")
    st.subheader("Analisis Sistem Pelayanan")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Parameter Antrian")
        lmbda = st.number_input("Tingkat Kedatangan (λ - pelanggan/jam)", min_value=0.1, value=10.0, step=0.5)
        mu = st.number_input("Tingkat Pelayanan (μ - pelanggan/jam)", min_value=0.1, value=12.0, step=0.5)
        
        if mu <= lmbda:
            st.error("Tingkat pelayanan harus lebih besar dari tingkat kedatangan!")
            return
        
        # Hitung metrik antrian
        rho = lmbda / mu
        L = lmbda / (mu - lmbda)
        W = 1 / (mu - lmbda)
        Wq = lmbda / (mu * (mu - lmbda))
        
        # Konversi waktu ke menit
        W_min = W * 60
        Wq_min = Wq * 60
        
        # Tampilkan hasil
        st.divider()
        st.metric("Utilisasi Sistem (ρ)", f"{rho:.2%}")
        st.metric("Rata-rata Pelanggan dalam Sistem (L)", f"{L:.2f}")
        st.metric("Rata-rata Waktu dalam Sistem (W)", f"{W_min:.1f} menit")
        st.metric("Rata-rata Waktu Antrian (Wq)", f"{Wq_min:.1f} menit")
    
    with col2:
        # Visualisasi grafik
        st.markdown("### Diagram Metrik Antrian")
        labels = ['Utilisasi', 'Pelanggan dalam Sistem', 'Waktu Antrian']
        values = [rho, L, Wq]
        
        fig, ax = plt.subplots()
        bars = ax.bar(labels, values, color=['blue', 'green', 'red'])
        
        # Tambahkan nilai di atas bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}', ha='center', va='bottom')
        
        ax.set_ylabel('Nilai')
        ax.set_title('Kinerja Sistem Antrian')
        plt.xticks(rotation=15)
        st.pyplot(fig)
        
        # Interpretasi
        st.markdown("**Interpretasi:**")
        if rho < 0.7:
            st.info("Sistem relatif stabil dengan antrian pendek")
        elif rho < 0.9:
            st.warning("Sistem cukup sibuk, mungkin perlu penambahan kapasitas")
        else:
            st.error("Sistem overload! Perlu penambahan server atau optimasi")

# Tab 4: Model Matematika Lainnya (Pertumbuhan Eksponensial)
def model_pertumbuhan():
    st.header("Model Pertumbuhan Eksponensial")
    st.subheader("Prediksi Pertumbuhan dalam Industri")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Parameter Pertumbuhan")
        st.info("Contoh kasus nyata: Prediksi pertumbuhan pengguna aplikasi")
        
        P0 = st.number_input("Nilai Awal (P0)", min_value=1, value=1000)
        r = st.number_input("Laju Pertumbuhan Harian (r)", value=0.05, step=0.01, format="%.2f")
        t = st.slider("Jangka Waktu Prediksi (hari)", 1, 365, 180)
        
        # Hitung pertumbuhan
        t_values = np.arange(0, t+1)
        P = P0 * np.exp(r * t_values)
        
        # Tampilkan hasil
        st.divider()
        st.metric("Nilai Awal", f"{P0:,}")
        st.metric(f"Prediksi Hari ke-{t}", f"{P[-1]:,.0f}")
        st.metric("Pertumbuhan Total", f"{P[-1]/P0:.1f}x")
    
    with col2:
        # Visualisasi grafik
        st.markdown("### Grafik Proyeksi Pertumbuhan")
        fig, ax = plt.subplots()
        ax.plot(t_values, P, 'b-')
        ax.set_xlabel('Hari')
        ax.set_ylabel('Jumlah Pengguna')
        ax.set_title('Pertumbuhan Eksponensial Pengguna Aplikasi')
        ax.grid(True)
        st.pyplot(fig)
        
        # Analisis
        st.markdown("**Aplikasi Industri:**")
        st.markdown("""
        - Prediksi pertumbuhan pengguna aplikasi
        - Proyeksi penjualan produk baru
        - Perencanaan kapasitas server
        - Estimasi kebutuhan stok selama periode pertumbuhan
        """)

# Main App
tab1, tab2, tab3, tab4 = st.tabs([
    "Optimasi Produksi", 
    "Model Persediaan", 
    "Model Antrian", 
    "Model Pertumbuhan"
])

with tab1:
    optimasi_produksi()

with tab2:
    model_persediaan()

with tab3:
    model_antrian()

with tab4:
    model_pertumbuhan()

# Footer
st.divider()
st.caption("© 2025 TIF208 - Matematika Terapan | Dikembangkan untuk Tugas Kelompok")