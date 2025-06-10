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
        st.markdown("""
        **Apa yang Dihitung?**  
        Aplikasi ini mencari kombinasi produksi meja dan kursi yang memberikan keuntungan tertinggi  
        dengan kendala waktu produksi dan bahan baku kayu.

        **Variabel:**  
        - `x` = Jumlah meja  
        - `y` = Jumlah kursi  

        **Fungsi Tujuan:**  
        Maksimalkan `Z = 250.000x + 120.000y`  

        **Kendala:**  
        1. Waktu produksi: `3x + y ≤ 120`  
        2. Bahan baku kayu: `5x + 2y ≤ 200`  
        """)
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
        titik_A = (0, 0)
        
        # Titik B (0, min(total_waktu/waktu_kursi, total_kayu/kayu_kursi))
        titik_B = (0, min(total_waktu/waktu_kursi, total_kayu/kayu_kursi))
        
        # Titik D (min(total_waktu/waktu_meja, total_kayu/kayu_meja), 0)
        titik_D = (min(total_waktu/waktu_meja, total_kayu/kayu_meja), 0)
        
        # Titik C: perpotongan dua kendala
        try:
            A = np.array([[waktu_meja, waktu_kursi], [kayu_meja, kayu_kursi]])
            b = np.array([total_waktu, total_kayu])
            titik_C = np.linalg.solve(A, b)
            # Pastikan titik berada dalam kuadran positif
            if titik_C[0] < 0 or titik_C[1] < 0:
                raise np.linalg.LinAlgError
        except np.linalg.LinAlgError:
            # Jika tidak ada perpotongan di kuadran positif
            titik_C = (0, 0)
        
        # Titik pojok yang feasible
        titik_pokok = [
            (titik_A[0], titik_A[1]),
            (titik_B[0], min(titik_B[1], (total_kayu - kayu_meja*0)/kayu_kursi)),
            (titik_C[0], titik_C[1]),
            (min(titik_D[0], (total_waktu - waktu_kursi*0)/waktu_meja), titik_D[1])
        ]
        
        # Hitung keuntungan di setiap titik
        Z_values = [
            profit_meja * x + profit_kursi * y
            for (x, y) in titik_pokok
        ]
        
        # Cari solusi optimal
        solusi_idx = np.argmax(Z_values)
        solusi = Z_values[solusi_idx]
        titik_opt = titik_pokok[solusi_idx]
        
        # Tampilkan hasil
        st.divider()
        st.metric("Solusi Optimal", f"{titik_opt[0]:.0f} meja, {titik_opt[1]:.0f} kursi")
        st.metric("Keuntungan Maksimal", f"Rp{solusi:,.0f}")
        st.markdown(f"**Detail Perhitungan:**")
        st.markdown(f"- Total waktu digunakan: {waktu_meja*titik_opt[0] + waktu_kursi*titik_opt[1]:.1f} jam dari {total_waktu} jam")
        st.markdown(f"- Total kayu digunakan: {kayu_meja*titik_opt[0] + kayu_kursi*titik_opt[1]:.1f} m² dari {total_kayu} m²")
    
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
        ax.plot(titik_A[0], titik_A[1], 'ko', label='Titik A (0,0)')
        ax.plot(titik_B[0], titik_B[1], 'ko', label='Titik B (0,{:.0f})'.format(titik_B[1]))
        if titik_C[0] > 0 and titik_C[1] > 0:
            ax.plot(titik_C[0], titik_C[1], 'ko', label='Titik C ({:.0f},{:.0f})'.format(titik_C[0], titik_C[1]))
        ax.plot(titik_D[0], titik_D[1], 'ko', label='Titik D ({:.0f},0)'.format(titik_D[0]))
        
        # Tandai solusi optimal
        ax.plot(titik_opt[0], titik_opt[1], 'ro', markersize=8, label='Solusi Optimal')
        
        # Area feasible
        x_feasible = np.linspace(0, min(total_waktu/waktu_meja, total_kayu/kayu_meja) + 10, 100)
        y_feasible_waktu = (total_waktu - waktu_meja * x_feasible) / waktu_kursi
        y_feasible_kayu = (total_kayu - kayu_meja * x_feasible) / kayu_kursi
        y_feasible = np.minimum(y_feasible_waktu, y_feasible_kayu)
        ax.fill_between(x_feasible, 0, y_feasible, where=(y_feasible >= 0), alpha=0.2, color='green', label='Daerah Feasible')
        
        ax.set_xlim(0, max(total_waktu/waktu_meja, total_kayu/kayu_meja) + 10)
        ax.set_ylim(0, max(total_waktu/waktu_kursi, total_kayu/kayu_kursi) + 10)
        ax.set_xlabel('Jumlah Meja')
        ax.set_ylabel('Jumlah Kursi')
        ax.legend(loc='upper right')
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
        lead_time = st.number_input("Lead Time (hari)", min_value=0, value=5)
        hari_kerja = st.number_input("Hari Kerja per Tahun", min_value=1, value=365)
        
        # Hitung EOQ
        eoq = math.sqrt((2 * D * S) / H)
        total_pesanan = D / eoq
        biaya_pemesanan = total_pesanan * S
        biaya_penyimpanan = (eoq / 2) * H
        total_biaya = biaya_pemesanan + biaya_penyimpanan
        
        # Hitung ROP
        permintaan_harian = D / hari_kerja
        ROP = permintaan_harian * lead_time
        
        # Hitung waktu antar pesanan
        waktu_antar_pesanan = (eoq / D) * hari_kerja
        
        # Tampilkan hasil
        st.divider()
        st.metric("EOQ Optimal", f"{eoq:.0f} unit")
        st.metric("Total Biaya Minimum", f"Rp{total_biaya:,.0f}")
        st.metric("Reorder Point (ROP)", f"{ROP:.1f} unit")
        st.metric("Waktu Antar Pesanan", f"{waktu_antar_pesanan:.1f} hari")
        st.markdown(f"**Strategi**: Pesan **{eoq:.0f} unit** setiap **{waktu_antar_pesanan:.1f} hari**")
    
    with col2:
        # Visualisasi grafik biaya
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
        
        siklus = eoq / permintaan_harian
        waktu = np.linspace(0, siklus * 3, 100)
        
        # Buat 3 siklus
        for i in range(3):
            t_start = i * siklus
            t_order = t_start + siklus - lead_time
            t_end = (i+1) * siklus
            
            # Garis persediaan
            t_cycle = np.linspace(t_start, t_end, 100)
            persediaan = np.maximum(eoq - permintaan_harian*(t_cycle - t_start), 0)
            ax2.plot(t_cycle, persediaan, 'b-')
            
            # Garis pemesanan (ROP)
            ax2.axvline(x=t_order, color='r', linestyle='--')
            
            # Tanda terima pesanan
            ax2.axvline(x=t_start + siklus, color='g', linestyle='-')
        
        ax2.axhline(y=ROP, color='orange', linestyle='--', label='ROP')
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
        n_pelanggan = st.slider("Jumlah Pelanggan untuk Probabilitas", min_value=0, max_value=20, value=5)
        
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
        
        # Probabilitas n pelanggan dalam sistem
        p_n = (1 - rho) * (rho ** n_pelanggan)
        
        # Tampilkan hasil
        st.divider()
        st.metric("Utilisasi Sistem (ρ)", f"{rho:.2%}")
        st.metric("Rata-rata Pelanggan dalam Sistem", f"{L:.2f}")
        st.metric("Rata-rata Pelanggan dalam Antrian", f"{Lq:.2f}")
        st.metric("Rata-rata Waktu di Sistem", f"{W_min:.1f} menit")
        st.metric("Rata-rata Waktu Antrian", f"{Wq_min:.1f} menit")
        st.metric(f"Probabilitas {n_pelanggan} Pelanggan dalam Sistem", f"{p_n:.2%}")
    
    with col2:
        # Visualisasi grafik
        st.markdown("### Distribusi Jumlah Pelanggan")
        n_values = np.arange(0, 15)
        p_n_values = [(1 - rho) * (rho ** n) for n in n_values]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(n_values, p_n_values, color='skyblue')
        ax.bar(n_pelanggan, p_n, color='red')
        
        # Anotasi probabilitas
        for i, prob in enumerate(p_n_values):
            ax.text(i, prob + 0.01, f'{prob:.2%}', ha='center', fontsize=9)
        
        ax.set_xlabel('Jumlah Pelanggan dalam Sistem')
        ax.set_ylabel('Probabilitas')
        ax.set_title('Distribusi Jumlah Pelanggan')
        ax.grid(True, axis='y')
        st.pyplot(fig)
        
        # Diagram metrik
        st.markdown("### Diagram Metrik Antrian")
        fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Pie chart waktu
        waktu_labels = ['Waktu Pelayanan', 'Waktu Antrian']
        waktu_values = [W - Wq, Wq]
        warna = ['#66c2a5', '#fc8d62']
        ax1.pie(waktu_values, labels=waktu_labels, autopct='%1.1f%%', 
               startangle=90, colors=warna)
        ax1.set_title('Komposisi Waktu di Sistem')
        
        # Pie chart pelanggan
        pelanggan_labels = ['Dalam Pelayanan', 'Dalam Antrian']
        pelanggan_values = [L - Lq, Lq]
        ax2.pie(pelanggan_values, labels=pelanggan_labels, autopct='%1.1f%%', 
               startangle=90, colors=warna)
        ax2.set_title('Komposisi Pelanggan dalam Sistem')
        
        st.pyplot(fig2)
        
        # Rekomendasi
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
        waktu_operasi = st.number_input("Waktu Operasi (jam)", min_value=1, value=1000)
        
        # Hitung keandalan sistem
        # Untuk sistem paralel: R_system = 1 - (1 - R)^n
        R_system = 1 - (1 - keandalan) ** n_komponen
        
        # Hitung MTTF (asumsi failure rate konstan)
        failure_rate = -math.log(keandalan) / waktu_operasi
        MTTF = 1 / failure_rate
        
        # Hitung availability
        MTTR = st.number_input("MTTR (jam)", min_value=0.1, value=24.0)
        availability = MTTF / (MTTF + MTTR)
        
        # Tampilkan hasil
        st.divider()
        st.metric("Keandalan Sistem", f"{R_system:.4f} ({R_system:.2%})")
        st.metric("MTTF Sistem", f"{MTTF:.2f} jam")
        st.metric("Availability Sistem", f"{availability:.2%}")
        
        # Rekomendasi
        st.markdown("**Rekomendasi Konfigurasi:**")
        if R_system < 0.99:
            rekom_n = math.ceil(math.log(1-0.99)/math.log(1-keandalan))
            st.warning(f"Tambahkan server untuk mencapai keandalan 99%: minimal {rekom_n} server")
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
        ax.plot(n_komponen, R_system, 'ro', markersize=10)
        
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
        height = 0.8
        for i in range(n_komponen):
            y_pos = i - (n_komponen-1)/2
            # Garis input-output
            ax2.plot([0, 3], [y_pos, y_pos], 'b-', linewidth=2)
            # Kotak server
            ax2.add_patch(plt.Rectangle((1, y_pos-height/2), 1, height, fill=True, 
                                      facecolor='lightblue', edgecolor='blue'))
            ax2.text(1.5, y_pos, f"Server {i+1}", ha='center', va='center')
        
        # Garis input
        ax2.plot([0, 0], [-2, 2], 'k-', linewidth=3)
        ax2.text(-0.2, 0, 'Input', ha='right', va='center', fontsize=12)
        
        # Garis output
        ax2.plot([3, 3], [-2, 2], 'k-', linewidth=3)
        ax2.text(3.2, 0, 'Output', ha='left', va='center', fontsize=12)
        
        ax2.set_xlim(-0.5, 3.5)
        ax2.set_ylim(-2, 2)
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