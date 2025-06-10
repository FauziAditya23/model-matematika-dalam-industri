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
    Studi kasus: Perusahaan furnitur  
    Visualisasi: Grafik daerah solusi optimal  
    
    **Tab 2: Model Persediaan**  
    Studi kasus: Toko elektronik  
    Visualisasi: Grafik hubungan biaya  
    
    **Tab 3: Model Antrian**  
    Studi kasus: Drive-thru restoran  
    Visualisasi: Diagram metrik kinerja  
    
    **Tab 4: Model Keandalan Sistem**  
    Studi kasus: Sistem komputer redundan  
    Visualisasi: Grafik fungsi keandalan
    """)
    st.divider()
    st.caption("TIF208 - Matematika Terapan | Universitas Pelita Bangsa")

# Tab 1: Optimasi Produksi (Studi Kasus Baru: Perusahaan Furnitur)
def optimasi_produksi():
    st.header("Optimasi Produksi Furnitur")
    st.subheader("Perusahaan Meubel Jaya")
    st.markdown("""
    **Studi Kasus Baru:**  
    Perusahaan furnitur memproduksi meja dan kursi.  
    - Keuntungan per meja = Rp250.000  
    - Keuntungan per kursi = Rp120.000  
    - Waktu produksi meja = 3 jam  
    - Waktu produksi kursi = 1 jam  
    - Total waktu produksi tersedia = 120 jam  
    - Kayu tersedia = 200 m² (meja: 5m², kursi: 2m²)
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Parameter Produksi")
        profit_meja = st.number_input("Keuntungan Meja (Rp)", min_value=0, value=250000, step=10000)
        profit_kursi = st.number_input("Keuntungan Kursi (Rp)", min_value=0, value=120000, step=10000)
        waktu_meja = st.number_input("Waktu Produksi Meja (jam)", min_value=0.0, value=3.0, step=0.5)
        waktu_kursi = st.number_input("Waktu Produksi Kursi (jam)", min_value=0.0, value=1.0, step=0.1)
        kayu_meja = st.number_input("Kayu per Meja (m²)", min_value=0.0, value=5.0, step=0.5)
        kayu_kursi = st.number_input("Kayu per Kursi (m²)", min_value=0.0, value=2.0, step=0.5)
        total_waktu = st.number_input("Total Waktu Tersedia (jam)", min_value=0, value=120, step=10)
        total_kayu = st.number_input("Total Kayu Tersedia (m²)", min_value=0, value=200, step=10)
        
        # Hitung titik pojok
        # Kendala waktu: 3x + y ≤ 120
        # Kendala kayu: 5x + 2y ≤ 200
        
        # Titik A (0,0)
        # Titik B (0, min(120, 100)) -> (0,100)
        # Titik C: perpotongan 3x+y=120 dan 5x+2y=200
        #   => 6x+2y=240 dan 5x+2y=200 -> x=40, y=120-120=0? -> hitung:
        #   3x + y = 120
        #   5x + 2y = 200
        #   Kalikan pers1 dengan 2: 6x + 2y = 240
        #   Kurangi dengan pers2: (6x+2y) - (5x+2y) = 240-200 => x=40
        #   Substitusi: 3(40) + y = 120 => y=0? -> tidak, cari y: 120 - 120 = 0? 
        #   Sebenarnya: dari pers1: y = 120 - 3x = 120 - 120 = 0
        #   Tapi cek ke pers2: 5(40)+2(0)=200 -> tepat
        # Titik D (40,0) -> dari kayu: 5x=200 => x=40, y=0
        # Titik E (0,100) dari kayu: 2y=200 => y=100
        
        # Titik potong:
        # A: (0,0)
        # B: (0, min(total_waktu/waktu_kursi, total_kayu/kayu_kursi)) = (0, min(120, 100)) = (0,100)
        # C: perpotongan dua kendala
        #   x = (2*total_waktu - total_kayu) / (2*waktu_meja - waktu_kursi*kayu_meja/kayu_kursi) -> lebih baik hitung numerik
        
        # Hitung titik potong kendala
        A = np.array([
            [waktu_meja, waktu_kursi],
            [kayu_meja, kayu_kursi]
        ])
        b = np.array([total_waktu, total_kayu])
        try:
            titik_potong = np.linalg.solve(A, b)
            x_potong = titik_potong[0]
            y_potong = titik_potong[1]
        except:
            x_potong = 0
            y_potong = 0
        
        # Titik pojok
        titik_A = (0, 0)
        titik_B = (0, min(total_waktu/waktu_kursi, total_kayu/kayu_kursi))
        titik_C = (x_potong, y_potong)
        titik_D = (min(total_waktu/waktu_meja, total_kayu/kayu_meja), 0)
        
        # Hitung keuntungan di setiap titik
        Z_A = profit_meja * titik_A[0] + profit_kursi * titik_A[1]
        Z_B = profit_meja * titik_B[0] + profit_kursi * titik_B[1]
        Z_C = profit_meja * titik_C[0] + profit_kursi * titik_C[1]
        Z_D = profit_meja * titik_D[0] + profit_kursi * titik_D[1]
        
        # Cari solusi optimal
        solusi = max(Z_A, Z_B, Z_C, Z_D)
        if solusi == Z_A:
            titik_opt = titik_A
            produk_opt = "Tidak memproduksi"
        elif solusi == Z_B:
            titik_opt = titik_B
            produk_opt = f"0 meja, {titik_B[1]:.0f} kursi"
        elif solusi == Z_C:
            titik_opt = titik_C
            produk_opt = f"{titik_C[0]:.0f} meja, {titik_C[1]:.0f} kursi"
        else:
            titik_opt = titik_D
            produk_opt = f"{titik_D[0]:.0f} meja, 0 kursi"
        
        # Tampilkan hasil
        st.divider()
        st.metric("Solusi Optimal", produk_opt)
        st.metric("Keuntungan Maksimal", f"Rp{solusi:,.0f}")
    
    with col2:
        # Visualisasi grafik
        st.markdown("### Grafik Daerah Solusi")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot garis kendala waktu
        x_waktu = np.linspace(0, total_waktu/waktu_meja + 10, 100)
        y_waktu = (total_waktu - waktu_meja * x_waktu) / waktu_kursi
        ax.plot(x_waktu, y_waktu, 'r-', label=f'Waktu: {waktu_meja}x + {waktu_kursi}y ≤ {total_waktu}')
        
        # Plot garis kendala kayu
        x_kayu = np.linspace(0, total_kayu/kayu_meja + 10, 100)
        y_kayu = (total_kayu - kayu_meja * x_kayu) / kayu_kursi
        ax.plot(x_kayu, y_kayu, 'b-', label=f'Kayu: {kayu_meja}x + {kayu_kursi}y ≤ {total_kayu}')
        
        # Plot titik pojok
        ax.plot(titik_A[0], titik_A[1], 'ko')
        ax.plot(titik_B[0], titik_B[1], 'ko')
        ax.plot(titik_C[0], titik_C[1], 'ro', markersize=8, label='Solusi Optimal')
        ax.plot(titik_D[0], titik_D[1], 'ko')
        
        # Area feasible
        x_feasible = np.linspace(0, min(total_waktu/waktu_meja, total_kayu/kayu_meja) + 10, 100)
        y_feasible = np.minimum(
            (total_waktu - waktu_meja * x_feasible) / waktu_kursi,
            (total_kayu - kayu_meja * x_feasible) / kayu_kursi
        )
        ax.fill_between(x_feasible, 0, y_feasible, where=(y_feasible >= 0), alpha=0.2, color='green')
        
        ax.set_xlim(0, max(total_waktu/waktu_meja, total_kayu/kayu_meja) + 10)
        ax.set_ylim(0, max(total_waktu/waktu_kursi, total_kayu/kayu_kursi) + 10)
        ax.set_xlabel('Jumlah Meja')
        ax.set_ylabel('Jumlah Kursi')
        ax.legend()
        ax.grid(True)
        ax.set_title('Daerah Solusi Optimal Produksi Furnitur')
        st.pyplot(fig)

# Tab 2: Model Persediaan (Studi Kasus Baru: Toko Elektronik)
def model_persediaan():
    st.header("Manajemen Persediaan Toko Elektronik")
    st.subheader("Toko Elektronik Maju Jaya")
    st.markdown("""
    **Studi Kasus Baru:**  
    Toko elektronik menjual baterai laptop populer.  
    - Permintaan tahunan: 2.400 unit  
    - Biaya pemesanan: Rp150.000 per pesanan  
    - Biaya penyimpanan: Rp15.000 per unit per tahun  
    - Hitung EOQ untuk minimalisasi biaya  
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Parameter Persediaan")
        D = st.number_input("Permintaan Tahunan (unit)", min_value=1, value=2400)
        S = st.number_input("Biaya Pemesanan per Pesanan (Rp)", min_value=0, value=150000)
        H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", min_value=0, value=15000)
        
        # Hitung EOQ
        eoq = math.sqrt((2 * D * S) / H)
        total_pesanan = D / eoq
        biaya_pemesanan = total_pesanan * S
        biaya_penyimpanan = (eoq / 2) * H
        total_biaya = biaya_pemesanan + biaya_penyimpanan
        
        # Hitung ROP (asumsi lead time 5 hari, 1 tahun = 365 hari)
        lead_time = st.number_input("Lead Time (hari)", min_value=0, value=5)
        ROP = (D / 365) * lead_time
        
        # Tampilkan hasil
        st.divider()
        st.metric("EOQ Optimal", f"{eoq:.0f} unit")
        st.metric("Total Biaya Minimum", f"Rp{total_biaya:,.0f}")
        st.metric("Reorder Point (ROP)", f"{ROP:.1f} unit")
        st.markdown(f"**Strategi**: Pesan **{eoq:.0f} unit** ketika persediaan mencapai **{ROP:.1f} unit**")
    
    with col2:
        # Visualisasi grafik
        st.markdown("### Grafik Biaya Total")
        quantities = np.linspace(50, 500, 100)
        holding_costs = (quantities / 2) * H
        ordering_costs = (D / quantities) * S
        total_costs = holding_costs + ordering_costs
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(quantities, holding_costs, 'b-', label='Biaya Penyimpanan')
        ax.plot(quantities, ordering_costs, 'g-', label='Biaya Pemesanan')
        ax.plot(quantities, total_costs, 'r-', label='Total Biaya')
        ax.plot(eoq, total_biaya, 'ro', markersize=8, label='EOQ Optimal')
        
        ax.set_xlabel('Kuantitas Pemesanan (unit)')
        ax.set_ylabel('Biaya (Rp)')
        ax.legend()
        ax.grid(True)
        ax.set_title('Minimalisasi Biaya Persediaan')
        st.pyplot(fig)
        
        # Grafik siklus persediaan
        st.markdown("### Grafik Siklus Persediaan")
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        
        waktu_siklus = eoq / (D/365)  # dalam hari
        waktu = np.linspace(0, waktu_siklus * 3, 100)
        persediaan = np.maximum(eoq - (D/365)*waktu, 0)
        
        for i in range(3):
            ax2.plot(waktu + i*waktu_siklus, persediaan, 'b-')
            ax2.axvline(x=(i+1)*waktu_siklus - lead_time, color='r', linestyle='--')
        
        ax2.axhline(y=ROP, color='g', linestyle='--', label='ROP')
        ax2.set_xlabel('Waktu (hari)')
        ax2.set_ylabel('Tingkat Persediaan (unit)')
        ax2.set_title('Siklus Persediaan dan Reorder Point')
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)

# Tab 3: Model Antrian (Studi Kasus Baru: Drive-thru Restoran)
def model_antrian():
    st.header("Analisis Antrian Drive-thru Restoran")
    st.subheader("Restoran Cepat Saji Segar")
    st.markdown("""
    **Studi Kasus Baru:**  
    Analisis antrian drive-thru restoran cepat saji.  
    - Rata-rata kedatangan pelanggan: 40 per jam  
    - Rata-rata pelayanan: 45 pelanggan per jam  
    - Model antrian M/M/1  
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Parameter Antrian")
        lmbda = st.number_input("Tingkat Kedatangan (λ - pelanggan/jam)", min_value=0.1, value=40.0, step=1.0)
        mu = st.number_input("Tingkat Pelayanan (μ - pelanggan/jam)", min_value=0.1, value=45.0, step=1.0)
        
        if mu <= lmbda:
            st.error("Tingkat pelayanan harus lebih besar dari tingkat kedatangan!")
            return
        
        # Hitung metrik antrian
        rho = lmbda / mu
        L = lmbda / (mu - lmbda)  # Rata-rata pelanggan dalam sistem
        Lq = rho * L  # Rata-rata pelanggan dalam antrian
        W = 1 / (mu - lmbda)  # Rata-rata waktu dalam sistem (jam)
        Wq = Lq / lmbda  # Rata-rata waktu antrian (jam)
        
        # Konversi waktu ke menit
        W_min = W * 60
        Wq_min = Wq * 60
        
        # Probabilitas antrian
        p0 = 1 - rho  # Probabilitas sistem kosong
        p_wait = 1 - p0  # Probabilitas harus menunggu
        
        # Tampilkan hasil
        st.divider()
        st.metric("Utilisasi Sistem (ρ)", f"{rho:.2%}")
        st.metric("Rata-rata Pelanggan dalam Sistem", f"{L:.2f}")
        st.metric("Rata-rata Waktu di Drive-thru", f"{W_min:.1f} menit")
        st.metric("Rata-rata Waktu Antrian", f"{Wq_min:.1f} menit")
        st.metric("Probabilitas Antrian", f"{p_wait:.2%}")
    
    with col2:
        # Visualisasi grafik
        st.markdown("### Distribusi Jumlah Pelanggan")
        n_values = np.arange(0, 15)
        p_n = [(1 - rho) * (rho ** n) for n in n_values]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(n_values, p_n, color='skyblue')
        ax.set_xlabel('Jumlah Pelanggan dalam Sistem')
        ax.set_ylabel('Probabilitas')
        ax.set_title('Distribusi Jumlah Pelanggan')
        ax.grid(True, axis='y')
        st.pyplot(fig)
        
        # Diagram metrik
        st.markdown("### Diagram Metrik Antrian")
        labels = ['Waktu Pelayanan', 'Waktu Antrian']
        times = [W - Wq, Wq]
        
        fig2, ax2 = plt.subplots()
        wedges, texts, autotexts = ax2.pie(
            times, 
            labels=labels, 
            autopct='%1.1f%%',
            startangle=90,
            colors=['lightgreen', 'lightcoral']
        )
        ax2.axis('equal')
        ax2.set_title('Komposisi Waktu di Drive-thru')
        st.pyplot(fig2)
        
        # Interpretasi
        st.markdown("**Rekomendasi:**")
        if rho < 0.7:
            st.success("Sistem berjalan efisien")
        elif rho < 0.85:
            st.info("Sistem baik, monitor secara berkala")
        elif rho < 0.95:
            st.warning("Pertimbangkan penambahan jalur atau optimasi proses")
        else:
            st.error("Perlu penambahan jalur segera!")

# Tab 4: Model Keandalan Sistem (Studi Kasus Baru: Sistem Komputer Redundan)
def model_keandalan():
    st.header("Analisis Keandalan Sistem Komputer")
    st.subheader("Sistem Server Redundan")
    st.markdown("""
    **Studi Kasus Baru:**  
    Sistem komputer dengan komponen redundan untuk meningkatkan keandalan.  
    - Setiap server memiliki keandalan 0.95  
    - Sistem menggunakan konfigurasi paralel  
    - Hitung keandalan sistem dengan berbagai jumlah server  
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Parameter Sistem")
        keandalan = st.number_input("Keandalan Tiap Komponen", min_value=0.1, max_value=1.0, value=0.95, step=0.01)
        n_komponen = st.slider("Jumlah Komponen Paralel", min_value=1, max_value=5, value=2)
        
        # Hitung keandalan sistem
        # Untuk sistem paralel: R_system = 1 - (1 - R)^n
        R_system = 1 - (1 - keandalan) ** n_komponen
        
        # Hitung MTTF (asumsi failure rate konstan)
        failure_rate = -math.log(keandalan)  # untuk periode tertentu
        MTTF = 1 / failure_rate
        
        # Tampilkan hasil
        st.divider()
        st.metric("Keandalan Sistem", f"{R_system:.4f} ({R_system:.2%})")
        st.metric("Peningkatan Keandalan", f"{(R_system - keandalan)/keandalan:.2%}")
        st.metric("MTTF Sistem", f"{MTTF:.2f} periode")
        
        # Rekomendasi
        st.markdown("**Rekomendasi Konfigurasi:**")
        if R_system < 0.99:
            st.warning(f"Tambahkan 1 server lagi untuk meningkatkan keandalan menjadi {1 - (1-keandalan)**(n_komponen+1):.2%}")
        else:
            st.success("Konfigurasi memadai untuk sistem kritis")
    
    with col2:
        # Visualisasi grafik
        st.markdown("### Grafik Keandalan Sistem")
        n_values = np.arange(1, 6)
        R_values = [1 - (1 - keandalan) ** n for n in n_values]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(n_values, R_values, 'bo-', markersize=8)
        ax.axhline(y=0.99, color='r', linestyle='--', label='Standar Tinggi (99%)')
        ax.axhline(y=0.95, color='g', linestyle='--', label='Standar Minimum (95%)')
        
        ax.set_xlabel('Jumlah Komponen Paralel')
        ax.set_ylabel('Keandalan Sistem')
        ax.set_title('Peningkatan Keandalan dengan Redundansi')
        ax.set_xticks(n_values)
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
        
        # Diagram blok sistem
        st.markdown("### Diagram Konfigurasi Sistem")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        
        # Gambar sederhana sistem paralel
        for i in range(n_komponen):
            ax2.plot([0, 1], [i, i], 'b-', linewidth=2)
            ax2.text(0.5, i, f"Server {i+1}", ha='center', va='center', 
                    bbox=dict(facecolor='white', alpha=0.8))
        
        ax2.plot([0, 0], [0, n_komponen-1], 'k-', linewidth=3)
        ax2.plot([1, 1], [0, n_komponen-1], 'k-', linewidth=3)
        ax2.text(-0.1, (n_komponen-1)/2, 'Input', ha='right', va='center')
        ax2.text(1.1, (n_komponen-1)/2, 'Output', ha='left', va='center')
        
        ax2.set_xlim(-0.5, 1.5)
        ax2.set_ylim(-1, n_komponen)
        ax2.axis('off')
        ax2.set_title(f'Konfigurasi {n_komponen} Server Paralel')
        st.pyplot(fig2)

# Main App
tab1, tab2, tab3, tab4 = st.tabs([
    "Optimasi Produksi", 
    "Model Persediaan", 
    "Model Antrian", 
    "Keandalan Sistem"
])

with tab1:
    optimasi_produksi()

with tab2:
    model_persediaan()

with tab3:
    model_antrian()

with tab4:
    model_keandalan()

# Footer
st.divider()
st.caption("© 2025 TIF208 - Matematika Terapan | Dikembangkan untuk Tugas Kelompok")