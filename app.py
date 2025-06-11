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
    st.image("https://www.gstatic.com/mobilesdk/160503_mobilesdk/logo/2x/firebase_28.png", width=60)
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
    st.caption("TIF208 - Matematika Terapan | Universitas Pelita Bangsa")
    st.caption("Versi Revisi untuk Presentasi")

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
        
        with st.expander("Rumus Model: Linear Programming"):
            st.markdown("""
            **Variabel Keputusan:**
            - $x$ = Jumlah Meja
            - $y$ = Jumlah Kursi
            """)
            st.markdown("**Fungsi Tujuan (Maksimalkan Keuntungan):**")
            st.latex(r'''Z = (\text{Keuntungan per Meja} \cdot x) + (\text{Keuntungan per Kursi} \cdot y)''')
            
            st.markdown("**Fungsi Kendala (Batasan Sumber Daya):**")
            st.latex(r'''1. \quad (\text{Jam per Meja} \cdot x) + (\text{Jam per Kursi} \cdot y) \le \text{Total Jam Tersedia}''')
            st.latex(r'''2. \quad (\text{Kayu per Meja} \cdot x) + (\text{Kayu per Kursi} \cdot y) \le \text{Total Kayu Tersedia}''')
            st.latex(r'''3. \quad x \ge 0, y \ge 0''')

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

        # --- Perhitungan ---
        A_matrix = np.array([[jam_meja, jam_kursi], [kayu_meja, kayu_kursi]])
        b_vector = np.array([total_jam, total_kayu])
        x_intercept1 = total_jam / jam_meja if jam_meja > 0 else float('inf')
        y_intercept1 = total_jam / jam_kursi if jam_kursi > 0 else float('inf')
        x_intercept2 = total_kayu / kayu_meja if kayu_meja > 0 else float('inf')
        y_intercept2 = total_kayu / kayu_kursi if kayu_kursi > 0 else float('inf')
        try:
            intersect_point = np.linalg.solve(A_matrix, b_vector)
            if intersect_point[0] < 0 or intersect_point[1] < 0:
                intersect_point = (0, 0)
        except np.linalg.LinAlgError:
            intersect_point = (0, 0)
        corner_points = [(0, 0)]
        if y_intercept1 != float('inf') and (kayu_meja*0 + kayu_kursi*y_intercept1 <= total_kayu):
            corner_points.append((0, y_intercept1))
        if y_intercept2 != float('inf') and (jam_meja*0 + jam_kursi*y_intercept2 <= total_jam):
            corner_points.append((0, y_intercept2))
        if x_intercept1 != float('inf') and (kayu_meja*x_intercept1 + kayu_kursi*0 <= total_kayu):
            corner_points.append((x_intercept1, 0))
        if x_intercept2 != float('inf') and (jam_meja*x_intercept2 + jam_kursi*0 <= total_jam):
            corner_points.append((x_intercept2, 0))
        if intersect_point[0] > 0 and intersect_point[1] > 0:
             corner_points.append(tuple(intersect_point))
        optimal_profit = 0
        optimal_point = (0, 0)
        for x, y in set(corner_points):
            profit = profit_meja * x + profit_kursi * y
            if profit > optimal_profit:
                optimal_profit = profit
                optimal_point = (math.floor(x), math.floor(y))
        
    with col2:
        st.subheader("💡 Hasil dan Wawasan Bisnis")
        st.success(f"**Rekomendasi Produksi:** Untuk keuntungan maksimal, 'Jati Indah' harus memproduksi **{optimal_point[0]} Meja** dan **{optimal_point[1]} Kursi** per minggu.")
        
        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.metric(label="💰 Keuntungan Maksimal", value=f"Rp {optimal_profit:,.0f}")
        with col2_res:
            jam_terpakai = jam_meja * optimal_point[0] + jam_kursi * optimal_point[1]
            kayu_terpakai = kayu_meja * optimal_point[0] + kayu_kursi * optimal_point[1]
            st.metric(label="🛠️ Utilisasi Jam Kerja", value=f"{jam_terpakai:.1f} / {total_jam} Jam", help=f"{jam_terpakai/total_jam:.1%} terpakai")
            st.metric(label="🌲 Utilisasi Kayu Jati", value=f"{kayu_terpakai:.1f} / {total_kayu} Unit", help=f"{kayu_terpakai/total_kayu:.1%} terpakai")
        
        with st.container(border=True):
            st.markdown("**Analisis Sumber Daya:**")
            if (total_jam - jam_terpakai) < 1:
                st.warning("**Jam Kerja adalah Kendala Utama (Bottleneck)!** Sumber daya waktu habis terpakai. Pertimbangkan untuk menambah jam lembur atau pengrajin baru untuk meningkatkan produksi.")
            elif (total_kayu - kayu_terpakai) < 1:
                st.warning("**Stok Kayu adalah Kendala Utama (Bottleneck)!** Stok kayu habis terpakai. Pertimbangkan mencari pemasok kayu tambahan untuk meningkatkan kapasitas.")
            else:
                st.info("Kedua sumber daya (jam kerja dan kayu) masih tersisa. Ada ruang untuk meningkatkan produksi jika permintaan meningkat.")

        st.markdown("#### Visualisasi Daerah Produksi yang Layak")
        fig, ax = plt.subplots(figsize=(10, 6))
        max_x_intercept = 1
        if x_intercept1 != float('inf') and x_intercept2 != float('inf'):
             max_x_intercept = max(x_intercept1, x_intercept2) if max(x_intercept1, x_intercept2) > 0 else 50
        x = np.linspace(0, max_x_intercept * 1.1, 400)
        y1 = (total_jam - jam_meja * x) / jam_kursi if jam_kursi > 0 else np.full_like(x, float('inf'))
        ax.plot(x, y1, label=f'Batas Jam Kerja')
        y2 = (total_kayu - kayu_meja * x) / kayu_kursi if kayu_kursi > 0 else np.full_like(x, float('inf'))
        ax.plot(x, y2, label=f'Batas Stok Kayu')
        y_feasible = np.minimum(y1, y2)
        ax.fill_between(x, 0, y_feasible, where=(y_feasible>=0), color='green', alpha=0.2, label='Daerah Produksi Layak')
        ax.plot(optimal_point[0], optimal_point[1], 'ro', markersize=12, label=f'Titik Optimal ({optimal_point[0]}, {optimal_point[1]})')
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
    st.header("📦 Manajemen Persediaan (EOQ)")
    st.subheader("Studi Kasus: Kedai Kopi 'Kopi Kita'")

    col1, col2 = st.columns([1.5, 2])

    with col1:
        st.markdown("""
        **Skenario Bisnis:**
        'Kopi Kita' perlu menentukan jumlah pesanan biji kopi impor yang optimal untuk meminimalkan total biaya persediaan (biaya pesan dan biaya simpan).
        """)
        
        with st.expander("Rumus Model: Economic Order Quantity (EOQ)"):
            st.markdown("**Variabel:** $Q^*$ (EOQ), $D$ (Permintaan Tahunan), $S$ (Biaya Pesan), $H$ (Biaya Simpan)")
            st.latex(r''' Q^* = \sqrt{\frac{2DS}{H}} \quad | \quad ROP = (D/360) \times \text{Lead Time} + \text{Safety Stock}''')

        with st.container(border=True):
            st.subheader("⚙️ Parameter Model")
            D = st.number_input("Permintaan Tahunan (kg)", min_value=1, value=1200)
            S = st.number_input("Biaya Pemesanan per Pesanan (Rp)", min_value=0, value=500000)
            H = st.number_input("Biaya Penyimpanan per kg per Tahun (Rp)", min_value=0, value=25000)
            lead_time = st.number_input("Lead Time Pengiriman (hari)", min_value=1, value=14)
            safety_stock = st.number_input("Stok Pengaman (Safety Stock) (kg)", min_value=0, value=10, help="Stok tambahan untuk mengantisipasi ketidakpastian permintaan atau keterlambatan.")
        
        # --- Perhitungan ---
        if H > 0 and D > 0:
            eoq = math.sqrt((2 * D * S) / H)
            frekuensi_pesanan = D / eoq if eoq > 0 else 0
            biaya_pemesanan_tahunan = frekuensi_pesanan * S
            biaya_penyimpanan_tahunan = (eoq / 2) * H
            total_biaya = biaya_pemesanan_tahunan + biaya_penyimpanan_tahunan
            permintaan_harian = D / 360
            rop = (permintaan_harian * lead_time) + safety_stock
            siklus_pemesanan = 360 / frekuensi_pesanan if frekuensi_pesanan > 0 else 0
        else:
            eoq = 0; total_biaya = 0; rop = 0; siklus_pemesanan = 0

        st.divider()
        st.subheader("💡 Hasil dan Wawasan Bisnis")
        st.success(f"**Kebijakan Optimal:** Pesan **{eoq:.0f} kg** biji kopi setiap kali stok mencapai **{rop:.1f} kg**.")
        
        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.metric(label="📦 Kuantitas Pesanan Optimal (EOQ)", value=f"{eoq:.0f} kg")
            st.metric(label="🎯 Titik Pemesanan Ulang (ROP)", value=f"{rop:.1f} kg")
        with col2_res:
            st.metric(label="💰 Total Biaya Persediaan Tahunan", value=f"Rp {total_biaya:,.0f}")
            st.metric(label="🔄 Siklus Pemesanan", value=f"~{siklus_pemesanan:.1f} hari")
            
    with col2:
        st.markdown("#### Visualisasi Analisis Biaya")
        q = np.linspace(max(1, eoq * 0.1), eoq * 2 if eoq > 0 else 200, 100)
        holding_costs = (q / 2) * H
        ordering_costs = (D / q) * S
        total_costs = holding_costs + ordering_costs
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(q, holding_costs, 'b-', label='Biaya Penyimpanan (Naik seiring kuantitas)')
        ax.plot(q, ordering_costs, 'g-', label='Biaya Pemesanan (Turun seiring kuantitas)')
        ax.plot(q, total_costs, 'r-', linewidth=3, label='Total Biaya')
        if eoq > 0:
            ax.axvline(x=eoq, color='purple', linestyle='--', label=f'EOQ - Titik Biaya Terendah')
            ax.annotate(f'Biaya Terendah\nRp {total_biaya:,.0f}', xy=(eoq, total_biaya), xytext=(eoq*1.3, total_biaya*0.6),
                        arrowprops=dict(facecolor='black', shrink=0.05), fontsize=12)

        ax.set_xlabel('Kuantitas Pemesanan (kg)')
        ax.set_ylabel('Biaya Tahunan (Rp)')
        ax.set_title('Analisis Biaya Persediaan (EOQ)', fontsize=16)
        ax.legend()
        ax.grid(True)
        ax.ticklabel_format(style='plain', axis='y')
        st.pyplot(fig)

        with st.container(border=True):
             st.markdown("**Wawasan Tambahan:** Titik EOQ adalah titik di mana **Biaya Penyimpanan** dan **Biaya Pemesanan** hampir sama, menghasilkan biaya total terendah. Stok pengaman tidak mempengaruhi EOQ, tetapi meningkatkan ROP untuk melindungi dari kehabisan stok.")


# --- TAB 3: MODEL ANTRIAN ---
def model_antrian():
    st.header("⏳ Analisis Sistem Antrian")
    st.subheader("Studi Kasus: Drive-Thru 'Ayam Goreng Juara' saat Jam Sibuk")
    
    col1, col2 = st.columns([1.5, 2])
    
    with col1:
        st.markdown("""
        **Skenario Bisnis:**
        Manajemen 'Ayam Goreng Juara' ingin menganalisis efisiensi layanan drive-thru mereka. Analisis ini bertujuan untuk menyeimbangkan antara biaya operasional dan kepuasan pelanggan (waktu tunggu).
        """)
        
        with st.expander("Rumus Model: Antrian M/M/1"):
            st.markdown("**Variabel:** $\lambda$ (Tingkat Kedatangan), $\mu$ (Tingkat Pelayanan)")
            st.latex(r''' \rho = \frac{\lambda}{\mu} \quad | \quad L = \frac{\rho}{1 - \rho} \quad | \quad W = \frac{L}{\lambda} ''')

        with st.container(border=True):
            st.subheader("📈 Parameter Sistem")
            lmbda = st.slider("Tingkat Kedatangan (λ - mobil/jam)", 1, 100, 30)
            mu = st.slider("Tingkat Pelayanan (μ - mobil/jam)", 1, 100, 35)
            
        if mu <= lmbda:
            st.error("Tingkat pelayanan (μ) harus lebih besar dari tingkat kedatangan (λ) agar antrian stabil.")
            return

        # --- Perhitungan ---
        rho = lmbda / mu; L = rho / (1 - rho); Lq = (rho**2) / (1 - rho)
        W = L / lmbda; Wq = Lq / lmbda

        st.divider()
        st.subheader("💡 Hasil dan Wawasan Bisnis")

        if rho > 0.85:
             st.warning(f"**Risiko Tinggi:** Utilisasi **({rho:.1%})** sangat tinggi. Antrian panjang dan waktu tunggu lama berisiko membuat pelanggan kecewa dan pergi.")
        elif rho > 0.7:
            st.info(f"**Cukup Sibuk:** Utilisasi **({rho:.1%})** berada pada tingkat yang sibuk. Kinerja baik, namun perlu diawasi saat jam puncak.")
        else:
             st.success(f"**Efisien:** Utilisasi **({rho:.1%})** berada pada tingkat yang sehat. Sistem mampu menangani pelanggan dengan cepat.")

        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.metric(label="🚗 Rata-rata Mobil di Sistem (L)", value=f"{L:.2f} mobil")
            st.metric(label="⏳ Rata-rata Total Waktu (W)", value=f"{W*60:.2f} menit")
        with col2_res:
            st.metric(label="🚗 Rata-rata Panjang Antrian (Lq)", value=f"{Lq:.2f} mobil")
            st.metric(label="⏳ Rata-rata Waktu Tunggu (Wq)", value=f"{Wq*60:.2f} menit")
            
    with col2:
        st.markdown("#### Visualisasi Kinerja Antrian")
        
        # Pie chart komposisi waktu
        fig, ax1 = plt.subplots(figsize=(8, 4))
        waktu_pelayanan_menit = (1/mu) * 60
        waktu_tunggu_menit = Wq * 60
        labels = ['Waktu Menunggu di Antrian', 'Waktu Dilayani']
        sizes = [waktu_tunggu_menit, waktu_pelayanan_menit]
        colors = ['#ff6347','#90ee90']
        explode = (0.1, 0)
        
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax1.axis('equal')
        ax1.set_title("Bagaimana Pelanggan Menghabiskan Waktunya?")
        st.pyplot(fig)

        st.markdown("#### Probabilitas Panjang Antrian")
        n_values = np.arange(0, 15)
        p_n_values = [(1 - rho) * (rho ** n) for n in n_values]
        
        fig2, ax2 = plt.subplots(figsize=(10, 4))
        bars = ax2.bar(n_values, p_n_values, color='skyblue')
        ax2.set_xlabel('Jumlah Mobil dalam Sistem (n)')
        ax2.set_ylabel('Probabilitas P(n)')
        ax2.set_title('Seberapa Mungkin Antrian Menjadi Panjang?')
        ax2.set_xticks(n_values)
        ax2.grid(True, axis='y', linestyle='--')
        st.pyplot(fig2)


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
        
        with st.expander("Rumus Model: Keandalan Sistem Seri"):
            st.latex(r''' R_s = R_1 \times R_2 \times \dots \times R_n = \prod_{i=1}^{n} R_i ''')

        with st.container(border=True):
            st.subheader("🔧 Keandalan per Mesin")
            r1 = st.slider("Stamping (R1)", 0.80, 1.00, 0.98, 0.01)
            r2 = st.slider("Welding (R2)", 0.80, 1.00, 0.99, 0.01)
            r3 = st.slider("Painting (R3)", 0.80, 1.00, 0.96, 0.01)
            r4 = st.slider("Assembly (R4)", 0.80, 1.00, 0.97, 0.01)

        # --- Perhitungan ---
        reliabilities = {'Stamping': r1, 'Welding': r2, 'Painting': r3, 'Assembly': r4}
        keandalan_sistem = np.prod(list(reliabilities.values()))
        weakest_link_name = min(reliabilities, key=reliabilities.get)
        weakest_link_value = reliabilities[weakest_link_name]

        st.divider()
        st.subheader("💡 Hasil dan Wawasan Bisnis")
        st.warning(f"**Mata Rantai Terlemah:** Mesin **{weakest_link_name}** ({weakest_link_value:.1%}) adalah komponen paling berisiko. Prioritaskan perawatan dan perbaikan pada mesin ini untuk dampak terbesar.")

        col1_res, col2_res = st.columns(2)
        with col1_res:
             st.metric(label="📉 Keandalan Keseluruhan Lini", value=f"{keandalan_sistem:.2%}")
        with col2_res:
             st.metric(label="📈 Probabilitas Kegagalan Lini", value=f"{1 - keandalan_sistem:.2%}", delta_color="inverse")

    with col2:
        st.markdown("#### Visualisasi Dampak Keandalan Komponen")
        
        # Data untuk bar chart
        labels = list(reliabilities.keys())
        values = list(reliabilities.values())
        labels.append("SISTEM TOTAL")
        values.append(keandalan_sistem)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        
        # Warna bar
        bar_colors = ['#87CEEB'] * len(reliabilities) # Skyblue untuk semua komponen
        weakest_idx = list(reliabilities.keys()).index(weakest_link_name)
        bar_colors[weakest_idx] = '#FF6347' # Tomato/Red untuk terlemah
        bar_colors.append('#9370DB') # MediumPurple untuk total

        bars = ax.bar(labels, values, color=bar_colors)
        
        ax.set_ylabel('Tingkat Keandalan (Reliability)')
        ax.set_title('Perbandingan Keandalan Komponen dan Sistem', fontsize=16)
        ax.set_ylim(min(0.75, min(values) * 0.95 if values else 0.75), 1.01)

        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.005, f'{yval:.2%}', ha='center', va='bottom')
            
        st.pyplot(fig)
        
        # --- Penjelasan Grafik ---
        with st.container(border=True):
            st.markdown("**🔍 Cara Membaca Grafik:**")
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
