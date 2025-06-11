import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Dashboard Model Matematika Industri", layout="wide", initial_sidebar_state="expanded")
st.title("📈 Dashboard Model Matematika untuk Industri")
st.markdown("Sebuah aplikasi interaktif untuk memahami penerapan model matematika kunci dalam skenario bisnis di dunia nyata.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Panduan Aplikasi")
    st.markdown("""
    Aplikasi ini mendemonstrasikan empat model matematika melalui studi kasus yang relevan dengan industri di Indonesia. Setiap tab menyediakan **analisis, visualisasi, dan wawasan bisnis** yang dapat ditindaklanjuti.
    """)
    st.info("**Tips:** Ubah parameter di setiap model untuk melihat bagaimana hasilnya berubah secara real-time!")
    
    st.markdown("""
    ---
    **1. 📊 Optimasi Produksi:**
    Mencari kombinasi produk yang memaksimalkan keuntungan dengan sumber daya terbatas.
    
    **2. 📦 Model Persediaan (EOQ):**
    Menentukan kuantitas pesanan optimal untuk meminimalkan total biaya persediaan.
    
    **3. ⏳ Model Antrian:**
    Menganalisis kinerja sistem antrian untuk meningkatkan layanan dan efisiensi.
    
    **4. 🔗 Keandalan Lini Produksi:**
    Mengevaluasi keandalan sistem dan mengidentifikasi titik rawan kegagalan.
    """)
    st.divider()
    st.caption("Teknik Informatika - Matematika Terapan | Universitas Pelita Bangsa")

# --- TAB 1: OPTIMASI PRODUKSI ---
def optimasi_produksi():
    st.header("📊 Optimasi Produksi Furnitur")
    st.subheader("Studi Kasus: UKM Mebel Jati 'Jati Indah'")
    
    col1, col2 = st.columns([1.5, 2])
    
    with col1:
        st.markdown("""
        **Skenario Bisnis:**
        'Jati Indah' ingin menentukan jumlah produksi meja dan kursi yang optimal untuk memaksimalkan keuntungan mingguan, dengan keterbatasan jam kerja pengrajin dan stok kayu jati.
        """)
        
        with st.container(border=True):
            st.subheader("🛠️ Parameter Model")
            profit_meja = st.number_input("Keuntungan per Meja (Rp)", min_value=0, value=750000, step=50000)
            profit_kursi = st.number_input("Keuntungan per Kursi (Rp)", min_value=0, value=300000, step=25000)
            jam_meja = st.number_input("Jam Kerja per Meja", min_value=1.0, value=6.0, step=0.5)
            jam_kursi = st.number_input("Jam Kerja per Kursi", min_value=1.0, value=2.0, step=0.5)
            kayu_meja = st.number_input("Kayu untuk Meja (unit)", min_value=1.0, value=4.0, step=0.5)
            kayu_kursi = st.number_input("Kayu untuk Kursi (unit)", min_value=1.0, value=1.5, step=0.5)
            total_jam = st.number_input("Total Jam Kerja Tersedia per Minggu", min_value=1, value=240, step=10)
            total_kayu = st.number_input("Total Kayu Jati Tersedia (unit)", min_value=1, value=120, step=10)
            
        with st.expander("Penjelasan Rumus Model: Linear Programming"):
            st.markdown("""
            Linear Programming adalah metode untuk mencapai hasil terbaik (seperti keuntungan maksimal atau biaya minimal) dalam suatu model matematika yang persyaratannya diwakili oleh hubungan linear.
            - **Fungsi Tujuan:** Ini adalah formula yang ingin kita maksimalkan (keuntungan) atau minimalkan (biaya). Dalam kasus ini, kita ingin memaksimalkan total keuntungan dari penjualan semua meja dan kursi.
            - **Fungsi Kendala:** Ini adalah batasan atau aturan yang harus dipatuhi, seperti sumber daya yang terbatas (jam kerja, bahan baku). Solusi yang kita cari tidak boleh melanggar salah satu dari kendala ini.
            """)
            st.markdown("""
            **Variabel Keputusan:**
            - $x$ = Jumlah Meja
            - $y$ = Jumlah Kursi
            """)
            st.markdown("**Fungsi Tujuan (Maksimalkan Keuntungan):**")
            st.latex(r'''Z = (\text{Profit Meja} \cdot x) + (\text{Profit Kursi} \cdot y)''')
            
            st.markdown("**Fungsi Kendala (Batasan Sumber Daya):**")
            st.latex(r'''1. \quad (\text{Jam Meja} \cdot x) + (\text{Jam Kursi} \cdot y) \le \text{Total Jam}''')
            st.latex(r'''2. \quad (\text{Kayu Meja} \cdot x) + (\text{Kayu Kursi} \cdot y) \le \text{Total Kayu}''')
            st.latex(r'''3. \quad x \ge 0, y \ge 0''')

        # --- Perhitungan ---
        A_matrix = np.array([[jam_meja, jam_kursi], [kayu_meja, kayu_kursi]])
        b_vector = np.array([total_jam, total_kayu])
        x_intercept1 = total_jam / jam_meja if jam_meja > 0 else float('inf')
        y_intercept1 = total_jam / jam_kursi if jam_kursi > 0 else float('inf')
        x_intercept2 = total_kayu / kayu_meja if kayu_meja > 0 else float('inf')
        y_intercept2 = total_kayu / kayu_kursi if kayu_kursi > 0 else float('inf')
        try:
            intersect_point = np.linalg.solve(A_matrix, b_vector)
            if intersect_point[0] < 0 or intersect_point[1] < 0: intersect_point = (0, 0)
        except np.linalg.LinAlgError:
            intersect_point = (0, 0)
        
        corner_points = [(0, 0)]
        if y_intercept1 != float('inf') and (kayu_meja*0 + kayu_kursi*y_intercept1 <= total_kayu): corner_points.append((0, y_intercept1))
        if y_intercept2 != float('inf') and (jam_meja*0 + jam_kursi*y_intercept2 <= total_jam): corner_points.append((0, y_intercept2))
        if x_intercept1 != float('inf') and (kayu_meja*x_intercept1 + kayu_kursi*0 <= total_kayu): corner_points.append((x_intercept1, 0))
        if x_intercept2 != float('inf') and (jam_meja*x_intercept2 + jam_kursi*0 <= total_jam): corner_points.append((x_intercept2, 0))
        if intersect_point[0] > 0 and intersect_point[1] > 0: corner_points.append(tuple(intersect_point))
        
        corner_points_unique = sorted(list(set(corner_points)), key=lambda k: (k[0], k[1]))

        optimal_profit, optimal_point = 0, (0, 0)
        profits_at_corners = []
        for x, y in corner_points_unique:
            profit = profit_meja * x + profit_kursi * y
            profits_at_corners.append({'x': round(x, 2), 'y': round(y, 2), 'profit': round(profit, 2)})
            if profit > optimal_profit:
                optimal_profit, optimal_point = profit, (math.floor(x), math.floor(y))
        
        with st.expander("Lihat Proses Perhitungan"):
            st.markdown("**Fungsi Tujuan dengan Angka:**")
            st.latex(f"Z = {profit_meja:,.0f}x + {profit_kursi:,.0f}y")
            st.markdown("**Fungsi Kendala dengan Angka:**")
            st.latex(f"1. \quad {jam_meja}x + {jam_kursi}y \le {total_jam}")
            st.latex(f"2. \quad {kayu_meja}x + {kayu_kursi}y \le {total_kayu}")
            st.markdown("**Perhitungan di Titik-Titik Sudut:**")
            for p in profits_at_corners:
                is_optimal = (math.floor(p['x']) == optimal_point[0] and math.floor(p['y']) == optimal_point[1])
                st.write(f"- Titik ({p['x']}, {p['y']}): Keuntungan = Rp {p['profit']:,.0f} {'**(Optimal)**' if is_optimal else ''}")

    with col2:
        st.subheader("💡 Hasil dan Wawasan Bisnis")
        st.success(f"**Rekomendasi Produksi:** Untuk keuntungan maksimal, 'Jati Indah' harus memproduksi **{optimal_point[0]} Meja** dan **{optimal_point[1]} Kursi** per minggu.")
        
        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.metric(label="💰 Keuntungan Maksimal", value=f"Rp {optimal_profit:,.0f}")
        with col2_res:
            jam_terpakai = jam_meja * optimal_point[0] + jam_kursi * optimal_point[1]
            kayu_terpakai = kayu_meja * optimal_point[0] + kayu_kursi * optimal_point[1]
            st.metric(label="🛠️ Utilisasi Jam Kerja", value=f"{jam_terpakai:.1f} / {total_jam} Jam", help=f"{(jam_terpakai/total_jam):.1%} terpakai")
            st.metric(label="🌲 Utilisasi Kayu Jati", value=f"{kayu_terpakai:.1f} / {total_kayu} Unit", help=f"{(kayu_terpakai/total_kayu):.1%} terpakai")
        
        with st.container(border=True):
            st.markdown("**Analisis Sumber Daya (Bottleneck):**")
            # --- PERUBAHAN: Teks Analisis Diringkas ---
            if (total_jam - jam_terpakai) < 1 and (total_kayu - kayu_terpakai) < 1:
                 st.error("- **Kritis:** Kedua sumber daya (jam dan kayu) habis. Peningkatan kapasitas mutlak diperlukan.")
            elif (total_jam - jam_terpakai) < 1:
                st.warning("- **Kendala Utama:** Jam kerja habis. Fokus pada penambahan jam kerja atau efisiensi pengrajin.")
            elif (total_kayu - kayu_terpakai) < 1:
                st.warning("- **Kendala Utama:** Stok kayu habis. Prioritaskan mencari pemasok tambahan.")
            else:
                st.info("- **Kapasitas Tersedia:** Sumber daya masih ada. Ada ruang untuk meningkatkan produksi jika permintaan meningkat.")

        st.markdown("#### Visualisasi Daerah Produksi yang Layak")
        fig, ax = plt.subplots(figsize=(10, 5))
        
        max_x = max(x_intercept1, x_intercept2) if max(x_intercept1, x_intercept2) > 0 else 50
        x_vals = np.linspace(0, max_x * 1.1, 400)
        
        y1 = (total_jam - jam_meja * x_vals) / jam_kursi if jam_kursi > 0 else np.full_like(x_vals, float('inf'))
        ax.plot(x_vals, y1, label=f'Batas Jam Kerja')
        
        y2 = (total_kayu - kayu_meja * x_vals) / kayu_kursi if kayu_kursi > 0 else np.full_like(x_vals, float('inf'))
        ax.plot(x_vals, y2, label=f'Batas Stok Kayu')
        
        y_feasible = np.minimum(y1, y2)
        ax.fill_between(x_vals, 0, y_feasible, where=(y_feasible>=0), color='green', alpha=0.2, label='Daerah Produksi Layak')
        
        ax.plot(optimal_point[0], optimal_point[1], 'ro', markersize=12, label=f'Titik Optimal ({optimal_point[0]}, {optimal_point[1]})')
        
        ax.set_xlabel('Jumlah Meja (x)')
        ax.set_ylabel('Jumlah Kursi (y)')
        ax.set_title('Grafik Optimasi Produksi Mebel', fontsize=16)
        ax.legend()
        ax.grid(True)
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        st.pyplot(fig)

        with st.container(border=True):
            st.markdown("**🔍 Penjelasan Grafik:**")
            st.markdown("""
            Grafik ini memvisualisasikan semua kemungkinan kombinasi produksi.
            - **Garis Batas:** Setiap garis mewakili batas maksimum dari satu sumber daya (jam kerja atau kayu).
            - **Daerah Hijau (Feasible Region):** Ini adalah area di mana semua kombinasi produksi (jumlah meja dan kursi) **memenuhi semua kendala** yang ada. Solusi yang valid harus berada di dalam atau di batas area ini.
            - **Titik Merah (Solusi Optimal):** Dari semua titik di sudut daerah hijau, titik ini adalah yang memberikan **keuntungan tertinggi**. Ini adalah jawaban yang kita cari.
            """)

# --- TAB 2: MODEL PERSEDIAAN ---
def model_persediaan():
    st.header("📦 Manajemen Persediaan (EOQ)")
    st.subheader("Studi Kasus: Kedai Kopi 'Kopi Kita'")

    col1, col2 = st.columns([1.5, 2])

    with col1:
        st.markdown("""
        **Skenario Bisnis:**
        'Kopi Kita' perlu menentukan jumlah pesanan biji kopi impor yang optimal untuk meminimalkan total biaya persediaan (biaya pesan dan biaya simpan).
        """)
        
        with st.container(border=True):
            st.subheader("⚙️ Parameter Model")
            D = st.number_input("Permintaan Tahunan (kg)", min_value=1, value=1200)
            S = st.number_input("Biaya Pemesanan per Pesanan (Rp)", min_value=0, value=500000)
            H = st.number_input("Biaya Penyimpanan per kg per Tahun (Rp)", min_value=0, value=25000)
            lead_time = st.number_input("Lead Time Pengiriman (hari)", min_value=1, value=14)
            safety_stock = st.number_input("Stok Pengaman (Safety Stock) (kg)", min_value=0, value=10, help="Stok tambahan untuk mengantisipasi ketidakpastian permintaan atau keterlambatan.")
        
        with st.expander("Penjelasan Rumus Model: Economic Order Quantity (EOQ)"):
            st.markdown("""
            EOQ adalah model yang digunakan untuk menemukan kuantitas pesanan yang dapat meminimalkan total biaya persediaan. Model ini menyeimbangkan dua jenis biaya yang berlawanan:
            - **Biaya Pemesanan (S):** Biaya yang dikeluarkan setiap kali memesan barang (misalnya, biaya pengiriman, administrasi). Semakin sering memesan, semakin tinggi biaya ini.
            - **Biaya Penyimpanan (H):** Biaya untuk menyimpan barang di gudang (misalnya, sewa, asuransi, pendingin). Semakin banyak barang yang disimpan, semakin tinggi biaya ini.
            - **Reorder Point (ROP):** Menentukan kapan harus memesan kembali untuk menghindari kehabisan stok, dengan mempertimbangkan waktu tunggu (lead time) dan stok pengaman.
            """)
            st.markdown("**Variabel:** $Q^*$ (EOQ), $D$ (Permintaan Tahunan), $S$ (Biaya Pesan), $H$ (Biaya Simpan)")
            st.latex(r''' Q^* = \sqrt{\frac{2DS}{H}} \quad | \quad ROP = (D/360) \times \text{Lead Time} + \text{Safety Stock}''')
        
        if H > 0 and D > 0:
            eoq = math.sqrt((2 * D * S) / H)
            frekuensi_pesanan = D / eoq if eoq > 0 else 0
            biaya_pemesanan = (D/eoq) * S if eoq > 0 else 0
            biaya_penyimpanan = (eoq/2) * H
            total_biaya = biaya_pemesanan + biaya_penyimpanan
            permintaan_harian = D / 360
            rop = (permintaan_harian * lead_time) + safety_stock
            siklus_pemesanan = 360 / frekuensi_pesanan if frekuensi_pesanan > 0 else 0
        else:
            eoq = 0; total_biaya = 0; rop = 0; siklus_pemesanan = 0
            
        with st.expander("Lihat Proses Perhitungan"):
            st.markdown(f"**1. Perhitungan EOQ ($Q^*$):**")
            st.latex(fr"Q^* = \sqrt{{\frac{{2 \times {D} \times {S}}}{{{H}}}}} = {eoq:.2f} \text{{ unit}}")
            st.markdown(f"**2. Perhitungan Titik Pemesanan Ulang (ROP):**")
            st.latex(fr"ROP = ({D}/360 \times {lead_time}) + {safety_stock} = {rop:.2f} \text{{ unit}}")
            st.markdown(f"**3. Perhitungan Biaya Total Tahunan:**")
            st.latex(fr"TC = \left(\frac{{{D}}}{{{eoq:.2f}}}\right){S} + \left(\frac{{{eoq:.2f}}}{{2}}\right){H} = \text{{Rp }}{total_biaya:,.2f}")

    with col2:
        st.subheader("💡 Hasil dan Wawasan Bisnis")
        st.success(f"**Kebijakan Optimal:** Pesan **{eoq:.0f} kg** biji kopi setiap kali stok mencapai **{rop:.1f} kg**.")
        
        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.metric(label="📦 Kuantitas Pesanan Optimal (EOQ)", value=f"{eoq:.0f} kg")
            st.metric(label="🎯 Titik Pemesanan Ulang (ROP)", value=f"{rop:.1f} kg")
        with col2_res:
            st.metric(label="💰 Total Biaya Persediaan Tahunan", value=f"Rp {total_biaya:,.0f}")
            st.metric(label="🔄 Siklus Pemesanan", value=f"~{siklus_pemesanan:.1f} hari")

        with st.container(border=True):
            st.markdown("**Analisis Kebijakan Persediaan:**")
            # --- PERUBAHAN: Teks Analisis Diringkas ---
            if eoq > (D/4):
                st.warning("- **Frekuensi Rendah:** Pesanan dalam jumlah besar tapi jarang. Ini hemat biaya pesan, tapi boros biaya simpan.")
            elif eoq < (D/12):
                st.info("- **Frekuensi Tinggi:** Pesanan dalam jumlah kecil tapi sering. Ini hemat biaya simpan, tapi boros biaya administrasi pemesanan.")
            else:
                st.success("- **Kebijakan Seimbang:** Kuantitas pesanan Anda menyeimbangkan biaya pesan dan biaya simpan dengan baik.")
        
        st.markdown("#### Visualisasi Analisis Biaya")
        q = np.linspace(max(1, eoq * 0.1), eoq * 2 if eoq > 0 else 200, 100)
        holding_costs = (q / 2) * H
        ordering_costs = (D / q) * S
        total_costs = holding_costs + ordering_costs
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(q, holding_costs, 'b-', label='Biaya Penyimpanan')
        ax.plot(q, ordering_costs, 'g-', label='Biaya Pemesanan')
        ax.plot(q, total_costs, 'r-', linewidth=3, label='Total Biaya')
        if eoq > 0:
            ax.axvline(x=eoq, color='purple', linestyle='--', label=f'EOQ')
            ax.annotate(f'Biaya Terendah\nRp {total_biaya:,.0f}', xy=(eoq, total_biaya), xytext=(eoq*1.3, total_biaya*0.6),
                        arrowprops=dict(facecolor='black', shrink=0.05), fontsize=12)

        ax.set_xlabel('Kuantitas Pemesanan (kg)')
        ax.set_ylabel('Biaya Tahunan (Rp)')
        ax.set_title('Analisis Biaya Persediaan (EOQ)', fontsize=16)
        ax.legend()
        ax.grid(True)
        ax.ticklabel_format(style='plain', axis='y')
        st.pyplot(fig)

        # --- PENAMBAHAN: Penjelasan Grafik Analisis Biaya ---
        with st.container(border=True):
             st.markdown("**🔍 Penjelasan Grafik Analisis Biaya:**")
             st.markdown("""
             Grafik ini menunjukkan trade-off antara biaya pemesanan dan biaya penyimpanan.
            - **Garis Biru (Biaya Penyimpanan):** Semakin banyak barang yang dipesan, semakin tinggi biaya untuk menyimpannya.
            - **Garis Hijau (Biaya Pemesanan):** Semakin banyak barang yang dipesan dalam satu waktu, semakin jarang kita memesan, sehingga total biaya pemesanan tahunan menurun.
            - **Garis Merah (Total Biaya):** Adalah penjumlahan dari kedua biaya di atas.
            - **Garis Ungu (EOQ):** Menandai titik di mana kurva total biaya mencapai titik terendahnya. Ini adalah kuantitas pesanan yang paling efisien.
            """)

        st.markdown("#### Visualisasi Siklus Persediaan")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        if siklus_pemesanan > 0 and eoq > 0:
            t_total = siklus_pemesanan * 2
            t = np.linspace(0, t_total, 200)
            stok_level = []
            for time_point in t:
                sisa_waktu_siklus = time_point % siklus_pemesanan
                stok = (eoq + safety_stock) - permintaan_harian * sisa_waktu_siklus
                stok_level.append(max(stok, safety_stock))
            
            ax2.plot(t, stok_level, label='Tingkat Persediaan')
            ax2.axhline(y=rop, color='orange', linestyle='--', label=f'ROP ({rop:.1f} kg)')
            ax2.axhline(y=safety_stock, color='red', linestyle=':', label=f'Stok Pengaman ({safety_stock} kg)')
            
            t_pesan = siklus_pemesanan - lead_time
            if t_pesan > 0:
                ax2.scatter(t_pesan, rop, color='red', s=100, zorder=5)
                ax2.annotate('Pesan Ulang!', xy=(t_pesan, rop), xytext=(t_pesan, rop + eoq*0.3),
                             arrowprops=dict(facecolor='red', shrink=0.05))

        ax2.set_xlabel('Waktu (Hari)')
        ax2.set_ylabel('Jumlah Stok (kg)')
        ax2.set_title('Simulasi Siklus Persediaan', fontsize=16)
        ax2.legend()
        ax2.grid(True)
        ax2.set_ylim(bottom=0)
        st.pyplot(fig2)

        with st.container(border=True):
             st.markdown("**🔍 Penjelasan Grafik Siklus:**")
             st.markdown("""
             Grafik ini menyimulasikan pergerakan stok dari waktu ke waktu.
             - **Garis Biru:** Menunjukkan tingkat persediaan yang terus menurun seiring penjualan harian.
             - **Garis Oranye (ROP):** Ketika stok menyentuh garis ini, inilah saatnya untuk memesan barang baru.
             - **Garis Merah (Stok Pengaman):** Stok minimum yang harus dijaga untuk menghindari kehabisan barang jika terjadi keterlambatan pengiriman.
             - **Siklus:** Stok akan kembali penuh (ke level EOQ + Stok Pengaman) setelah pesanan baru tiba.
             """)

# --- TAB 3: MODEL ANTRIAN ---
def model_antrian():
    st.header("⏳ Analisis Sistem Antrian")
    st.subheader("Studi Kasus: Drive-Thru 'Ayam Goreng Juara' saat Jam Sibuk")
    
    col1, col2 = st.columns([1.5, 2])
    
    with col1:
        st.markdown("""
        **Skenario Bisnis:**
        Manajemen 'Ayam Goreng Juara' ingin menganalisis efisiensi layanan drive-thru untuk menyeimbangkan biaya operasional dan kepuasan pelanggan (waktu tunggu).
        """)
        
        with st.container(border=True):
            st.subheader("📈 Parameter Sistem")
            lmbda = st.slider("Tingkat Kedatangan (λ - mobil/jam)", 1, 100, 30)
            mu = st.slider("Tingkat Pelayanan (μ - mobil/jam)", 1, 100, 35)
            
        with st.expander("Penjelasan Rumus Model: Antrian M/M/1"):
            st.markdown("""
            Model antrian M/M/1 digunakan untuk menganalisis sistem dengan satu server (pelayan). Model ini membantu kita memahami metrik kinerja utama:
            - **Utilisasi (ρ):** Seberapa sibuk server? Nilai mendekati 100% berarti sangat sibuk dan berisiko antrian panjang.
            - **Panjang Antrian (L, Lq):** Berapa rata-rata jumlah pelanggan yang menunggu di sistem atau di antrian?
            - **Waktu Tunggu (W, Wq):** Berapa lama rata-rata pelanggan menghabiskan waktu di sistem atau di antrian?
            Model ini mengasumsikan kedatangan pelanggan dan waktu pelayanan mengikuti distribusi Poisson (acak).
            """)
            st.markdown("**Variabel:** $\lambda$ (Tingkat Kedatangan), $\mu$ (Tingkat Pelayanan)")
            st.latex(r''' \rho = \frac{\lambda}{\mu} \quad | \quad L = \frac{\rho}{1 - \rho} \quad | \quad W = \frac{L}{\lambda} ''')
            
        if mu <= lmbda:
            st.error("Tingkat pelayanan (μ) harus lebih besar dari tingkat kedatangan (λ) agar antrian stabil.")
            return

        rho = lmbda / mu; L = rho / (1 - rho); Lq = (rho**2) / (1 - rho); W = L / lmbda; Wq = Lq / lmbda
        
        with st.expander("Lihat Proses Perhitungan"):
            st.latex(fr"\rho = \frac{{{lmbda}}}{{{mu}}} = {rho:.2f} \quad (Utilisasi)")
            st.latex(fr"L = \frac{{{rho:.2f}}}{{1 - {rho:.2f}}} = {L:.2f} \text{{ mobil di sistem}}")
            st.latex(fr"L_q = \frac{{{rho:.2f}^2}}{{1 - {rho:.2f}}} = {Lq:.2f} \text{{ mobil di antrian}}")
            st.latex(fr"W = \frac{{{L:.2f}}}{{{lmbda}}} = {W:.3f} \text{{ jam, atau }} {W*60:.2f} \text{{ menit}}")
            st.latex(fr"W_q = \frac{{{Lq:.2f}}}{{{lmbda}}} = {Wq:.3f} \text{{ jam, atau }} {Wq*60:.2f} \text{{ menit}}")

    with col2:
        st.subheader("💡 Hasil dan Wawasan Bisnis")

        st.success(f"**Rekomendasi:** Dengan tingkat pelayanan saat ini, rata-rata pelanggan akan menunggu **{Wq*60:.1f} menit** dalam antrian.")
        
        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.metric(label="🚗 Rata-rata Mobil di Sistem (L)", value=f"{L:.2f} mobil")
            st.metric(label="⏳ Rata-rata Total Waktu (W)", value=f"{W*60:.2f} menit")
        with col2_res:
            st.metric(label="🚗 Rata-rata Panjang Antrian (Lq)", value=f"{Lq:.2f} mobil")
            st.metric(label="⏳ Rata-rata Waktu Tunggu (Wq)", value=f"{Wq*60:.2f} menit")
        
        with st.container(border=True):
            st.markdown("**Analisis Kinerja Sistem:**")
            # --- PERUBAHAN: Teks Analisis Diringkas ---
            if rho > 0.85:
                st.error(f"- **Kondisi Kritis ({rho:.1%}):** Tingkat kesibukan sangat tinggi. Waktu tunggu yang lama berisiko merusak reputasi.")
            elif rho > 0.7:
                st.warning(f"- **Perlu Diwaspadai ({rho:.1%}):** Sistem cukup sibuk dan berisiko kewalahan jika ada lonjakan pelanggan.")
            else:
                st.info(f"- **Kinerja Sehat ({rho:.1%}):** Sistem terkendali, namun mungkin ada kapasitas layanan yang belum termanfaatkan.")
            
        st.markdown("#### Visualisasi Kinerja Antrian")
        
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        waktu_pelayanan_menit = (1/mu) * 60
        waktu_tunggu_menit = Wq * 60
        labels = ['Waktu Menunggu di Antrian', 'Waktu Dilayani']
        sizes = [waktu_tunggu_menit, waktu_pelayanan_menit]
        colors = ['#ff6347','#90ee90']
        explode = (0.1, 0)
        
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax1.axis('equal')
        ax1.set_title("Bagaimana Pelanggan Menghabiskan Waktunya?")
        st.pyplot(fig1)

        st.markdown("#### Probabilitas Panjang Antrian")
        n_values = np.arange(0, 15)
        p_n_values = [(1 - rho) * (rho ** n) for n in n_values]
        
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.bar(n_values, p_n_values, color='skyblue')
        for i, v in enumerate(p_n_values):
            ax2.text(i, v, f"{v:.1%}", ha='center', va='bottom', fontsize=9)

        ax2.set_xlabel('Jumlah Mobil dalam Sistem (n)')
        ax2.set_ylabel('Probabilitas P(n)')
        ax2.set_title('Seberapa Mungkin Antrian Menjadi Panjang?')
        ax2.set_xticks(n_values)
        ax2.grid(True, axis='y', linestyle='--')
        ax2.set_yticklabels([])
        st.pyplot(fig2)

        with st.container(border=True):
            st.markdown("**🔍 Penjelasan Grafik:**")
            st.markdown("""
            - **Grafik Pie:** Membagi total waktu pelanggan menjadi dua bagian: waktu yang dihabiskan untuk benar-benar dilayani (hijau) dan waktu yang terbuang untuk menunggu dalam antrian (merah). Persentase waktu tunggu yang besar menandakan pengalaman pelanggan yang buruk.
            - **Grafik Batang:** Menunjukkan probabilitas (kemungkinan) ada sejumlah mobil di dalam sistem. Jika bar di sebelah kanan (misalnya, 5 mobil atau lebih) memiliki nilai yang signifikan, itu berarti antrian panjang sering terjadi.
            """)
            
# --- TAB 4: KEANDALAN LINI PRODUKSI ---
def model_keandalan_produksi():
    st.header("🔗 Analisis Keandalan Lini Produksi")
    st.subheader("Studi Kasus: Lini Perakitan Otomotif 'Nusantara Motor'")
    
    col1, col2 = st.columns([1.5, 2])
    
    with col1:
        st.markdown("""
        **Skenario Bisnis:**
        Sebuah lini perakitan terdiri dari beberapa mesin yang beroperasi secara seri. Jika satu mesin berhenti, seluruh lini terhenti. Analisis ini menghitung keandalan total dan mengidentifikasi 'mata rantai terlemah'.
        """)
        
        with st.container(border=True):
            st.subheader("🔧 Keandalan per Mesin")
            r1 = st.slider("Stamping (R1)", 0.80, 1.00, 0.98, 0.01)
            r2 = st.slider("Welding (R2)", 0.80, 1.00, 0.99, 0.01)
            r3 = st.slider("Painting (R3)", 0.80, 1.00, 0.96, 0.01)
            r4 = st.slider("Assembly (R4)", 0.80, 1.00, 0.97, 0.01)
        
        with st.expander("Penjelasan Rumus Model: Keandalan Sistem Seri"):
            st.markdown("""
            Keandalan sistem seri dihitung dengan mengalikan keandalan dari setiap komponennya.
            - **Keandalan (R):** Adalah probabilitas sebuah komponen atau sistem akan berfungsi dengan baik selama periode waktu tertentu.
            - **Sistem Seri:** Komponen-komponen yang tersusun berurutan. Jika salah satu saja gagal, maka seluruh sistem akan gagal. Akibatnya, keandalan sistem seri **selalu lebih rendah** daripada keandalan komponen terlemahnya.
            """)
            st.latex(r''' R_s = R_1 \times R_2 \times \dots \times R_n = \prod_{i=1}^{n} R_i ''')

        reliabilities = {'Stamping': r1, 'Welding': r2, 'Painting': r3, 'Assembly': r4}
        keandalan_sistem = np.prod(list(reliabilities.values()))
        weakest_link_name = min(reliabilities, key=reliabilities.get)
        weakest_link_value = reliabilities[weakest_link_name]
        
        with st.expander("Lihat Proses Perhitungan"):
            st.latex(fr"R_s = R_{{Stamping}} \times R_{{Welding}} \times R_{{Painting}} \times R_{{Assembly}}")
            st.latex(fr"R_s = {r1} \times {r2} \times {r3} \times {r4} = {keandalan_sistem:.4f}")
            st.markdown(f"**Keandalan Sistem ($R_s$)** adalah **{keandalan_sistem:.2%}**.")

    with col2:
        st.subheader("💡 Hasil dan Wawasan Bisnis")
        st.warning(f"**Mata Rantai Terlemah:** Mesin **{weakest_link_name}** ({weakest_link_value:.1%}) adalah komponen paling berisiko. Prioritaskan perawatan dan perbaikan pada mesin ini untuk dampak terbesar.")

        col1_res, col2_res = st.columns(2)
        with col1_res:
             st.metric(label="📉 Keandalan Keseluruhan Lini", value=f"{keandalan_sistem:.2%}")
        with col2_res:
             st.metric(label="📈 Probabilitas Kegagalan Lini", value=f"{1 - keandalan_sistem:.2%}", delta_color="inverse")

        with st.container(border=True):
            st.markdown("**Analisis Dampak Kegagalan:**")
            dampak = (1 - keandalan_sistem) * 100
            # --- PERUBAHAN: Teks Analisis Diringkas ---
            if dampak > 10:
                st.error(f"- **Sangat Berisiko ({dampak:.1f}%):** Lini produksi kemungkinan besar akan sering berhenti, menyebabkan kerugian signifikan.")
            elif dampak > 5:
                st.warning(f"- **Risiko Menengah ({dampak:.1f}%):** Probabilitas kegagalan cukup tinggi. Perbaikan pada mesin terlemah sangat disarankan.")
            else:
                st.info(f"- **Risiko Rendah ({dampak:.1f}%):** Probabilitas kegagalan terkendali. Fokus pada perawatan rutin untuk mempertahankan kinerja.")

        st.markdown("#### Visualisasi Dampak Keandalan Komponen")
        
        labels = list(reliabilities.keys())
        values = list(reliabilities.values())
        labels.append("SISTEM TOTAL")
        values.append(keandalan_sistem)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        bar_colors = ['#87CEEB'] * len(reliabilities)
        weakest_idx = list(reliabilities.keys()).index(weakest_link_name)
        bar_colors[weakest_idx] = '#FF6347'
        bar_colors.append('#9370DB')

        bars = ax.bar(labels, values, color=bar_colors)
        
        ax.set_ylabel('Tingkat Keandalan (Reliability)')
        ax.set_title('Perbandingan Keandalan Komponen dan Sistem', fontsize=16)
        ax.set_ylim(min(0.75, min(values) * 0.95 if values else 0.75), 1.01)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:.2%}', ha='center', va='bottom', fontsize=10, color='black')
            
        st.pyplot(fig)
        
        with st.container(border=True):
            st.markdown("**🔍 Penjelasan Grafik:**")
            st.markdown("""
            Grafik ini menunjukkan bagaimana keandalan setiap mesin mempengaruhi keandalan seluruh lini produksi.
            - **Bar Biru & Merah:** Menunjukkan keandalan setiap mesin. Bar **merah** adalah mesin dengan keandalan terendah, yang menjadi **mata rantai terlemah**.
            - **Bar Ungu:** Menunjukkan keandalan total sistem. Perhatikan bagaimana nilainya selalu **lebih rendah** dari komponen terlemah sekalipun.
            
            **Kesimpulan:** Dalam sistem seri, keandalan keseluruhan sangat dipengaruhi oleh komponen yang paling tidak andal. Meningkatkan keandalan 'mata rantai terlemah' akan memberikan dampak terbesar pada peningkatan keandalan seluruh lini produksi.
            """)

# --- KONTROL TAB UTAMA ---
st.header("Pilih Model Matematika", divider='rainbow')
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Optimasi Produksi", 
    "📦 Model Persediaan", 
    "⏳ Model Antrian", 
    "🔗 Keandalan Lini Produksi"
])

with tab1: optimasi_produksi()
with tab2: model_persediaan()
with tab3: model_antrian()
with tab4: model_keandalan_produksi()

# --- FOOTER ---
st.divider()
st.caption("Fauzi Aditya | Marita Andika Putri | Naufal Khoirul Ibrahim | Poppi Marsanti Ramadani")
st.caption("© 2025 Kelompok 9 - Matematika Terapan | Dikembangkan untuk Tugas Kelompok")
