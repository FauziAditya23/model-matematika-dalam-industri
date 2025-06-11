import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
import plotly.express as px
import pandas as pd

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
    st.info("**Tips:** Arahkan kursor pada grafik untuk melihat detail, atau gunakan ikon di pojok kanan atas grafik untuk memperbesar.")
    
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
            if intersect_point[0] < 0 or intersect_point[1] < 0: intersect_point = (0, 0)
        except np.linalg.LinAlgError:
            intersect_point = (0, 0)
        corner_points = [(0, 0)]
        if y_intercept1 != float('inf') and (kayu_meja*0 + kayu_kursi*y_intercept1 <= total_kayu): corner_points.append((0, y_intercept1))
        if y_intercept2 != float('inf') and (jam_meja*0 + jam_kursi*y_intercept2 <= total_jam): corner_points.append((0, y_intercept2))
        if x_intercept1 != float('inf') and (kayu_meja*x_intercept1 + kayu_kursi*0 <= total_kayu): corner_points.append((x_intercept1, 0))
        if x_intercept2 != float('inf') and (jam_meja*x_intercept2 + jam_kursi*0 <= total_jam): corner_points.append((x_intercept2, 0))
        if intersect_point[0] > 0 and intersect_point[1] > 0: corner_points.append(tuple(intersect_point))
        
        optimal_profit, optimal_point = 0, (0, 0)
        for x, y in set(corner_points):
            profit = profit_meja * x + profit_kursi * y
            if profit > optimal_profit:
                optimal_profit, optimal_point = profit, (math.floor(x), math.floor(y))
        
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
            if (total_jam - jam_terpakai) < 1 and (total_kayu - kayu_terpakai) < 1:
                 st.error("**Kritis!** Kedua sumber daya (jam dan kayu) habis. Peningkatan kapasitas mutlak diperlukan.")
            elif (total_jam - jam_terpakai) < 1:
                st.warning("**Jam Kerja adalah Kendala Utama (Bottleneck)!** Pertimbangkan untuk menambah jam lembur atau pengrajin baru.")
            elif (total_kayu - kayu_terpakai) < 1:
                st.warning("**Stok Kayu adalah Kendala Utama (Bottleneck)!** Pertimbangkan mencari pemasok kayu tambahan.")
            else:
                st.info("Kedua sumber daya masih tersisa. Ada ruang untuk meningkatkan produksi jika permintaan meningkat.")

        st.markdown("#### Visualisasi Interaktif Daerah Produksi")
        
        max_x = max(x_intercept1, x_intercept2) if max(x_intercept1, x_intercept2) > 0 else 50
        x_vals = np.linspace(0, max_x * 1.1, 100)
        
        df_lines = pd.DataFrame({
            'Meja (x)': np.concatenate([x_vals, x_vals]),
            'Kursi (y)': np.concatenate([
                (total_jam - jam_meja * x_vals) / jam_kursi if jam_kursi > 0 else np.inf,
                (total_kayu - kayu_meja * x_vals) / kayu_kursi if kayu_kursi > 0 else np.inf
            ]),
            'Kendala': ['Batas Jam Kerja'] * 100 + ['Batas Stok Kayu'] * 100
        })
        df_lines = df_lines[df_lines['Kursi (y)'] >= 0]

        fig = px.line(df_lines, x='Meja (x)', y='Kursi (y)', color='Kendala', 
                      title='Grafik Optimasi Produksi Mebel',
                      labels={'Meja (x)': 'Jumlah Meja', 'Kursi (y)': 'Jumlah Kursi'})

        df_feasible = df_lines.groupby('Meja (x)')['Kursi (y)'].min().reset_index()
        fig.add_scatter(x=df_feasible['Meja (x)'], y=df_feasible['Kursi (y)'], fill='tozeroy', 
                        mode='none', name='Daerah Layak', fillcolor='rgba(0,128,0,0.2)')
        
        fig.add_scatter(x=[optimal_point[0]], y=[optimal_point[1]], mode='markers', 
                        marker=dict(color='red', size=15, symbol='star'), name='Titik Optimal',
                        hoverinfo='text', text=f"Optimal: {optimal_point[0]} Meja, {optimal_point[1]} Kursi<br>Profit: Rp {optimal_profit:,.0f}")
        
        fig.update_layout(legend_title_text='Legenda')
        fig.update_xaxes(range=[0, None])
        fig.update_yaxes(range=[0, None])
        st.plotly_chart(fig, use_container_width=True)

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
        st.markdown("#### Visualisasi Interaktif Analisis Biaya")
        q = np.linspace(max(1, eoq * 0.1), eoq * 2 if eoq > 0 else 200, 100)
        df_cost = pd.DataFrame({
            'Kuantitas Pesanan': q,
            'Biaya Penyimpanan': (q / 2) * H,
            'Biaya Pemesanan': (D / q) * S,
        })
        df_cost['Total Biaya'] = df_cost['Biaya Penyimpanan'] + df_cost['Biaya Pemesanan']
        
        fig = px.line(df_cost, x='Kuantitas Pesanan', y=['Biaya Penyimpanan', 'Biaya Pemesanan', 'Total Biaya'],
                      title='Analisis Biaya Persediaan (EOQ)', labels={'value': 'Biaya Tahunan (Rp)', 'variable': 'Jenis Biaya'})
        
        fig.update_traces(selector=dict(name='Total Biaya'), line=dict(width=4))
        
        if eoq > 0:
            fig.add_vline(x=eoq, line_width=3, line_dash="dash", line_color="purple", annotation_text="EOQ")
        
        st.plotly_chart(fig, use_container_width=True)

        with st.container(border=True):
             st.markdown("**Wawasan Tambahan:** Titik EOQ adalah titik di mana **Biaya Penyimpanan** dan **Biaya Pemesanan** berpotongan, menghasilkan biaya total terendah. Stok pengaman tidak mempengaruhi EOQ, tetapi meningkatkan ROP untuk melindungi dari kehabisan stok.")


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

        rho = lmbda / mu; L = rho / (1 - rho); Lq = (rho**2) / (1 - rho); W = L / lmbda; Wq = Lq / lmbda

        st.divider()
        st.subheader("💡 Hasil dan Wawasan Bisnis")

        if rho > 0.85: st.warning(f"**Risiko Tinggi:** Utilisasi **({rho:.1%})** sangat tinggi. Antrian panjang dan waktu tunggu lama berisiko membuat pelanggan kecewa.")
        elif rho > 0.7: st.info(f"**Cukup Sibuk:** Utilisasi **({rho:.1%})** pada tingkat yang sibuk. Kinerja baik, namun perlu diawasi saat jam puncak.")
        else: st.success(f"**Efisien:** Utilisasi **({rho:.1%})** pada tingkat yang sehat. Sistem mampu menangani pelanggan dengan cepat.")

        col1_res, col2_res = st.columns(2)
        with col1_res:
            st.metric(label="🚗 Rata-rata Mobil di Sistem (L)", value=f"{L:.2f} mobil")
            st.metric(label="⏳ Rata-rata Total Waktu (W)", value=f"{W*60:.2f} menit")
        with col2_res:
            st.metric(label="🚗 Rata-rata Panjang Antrian (Lq)", value=f"{Lq:.2f} mobil")
            st.metric(label="⏳ Rata-rata Waktu Tunggu (Wq)", value=f"{Wq*60:.2f} menit")
            
    with col2:
        st.markdown("#### Visualisasi Kinerja Antrian")
        
        waktu_pelayanan_menit = (1/mu) * 60; waktu_tunggu_menit = Wq * 60
        df_pie = pd.DataFrame({
            'Aktivitas': ['Waktu Menunggu', 'Waktu Dilayani'],
            'Durasi (menit)': [waktu_tunggu_menit, waktu_pelayanan_menit]
        })
        fig_pie = px.pie(df_pie, values='Durasi (menit)', names='Aktivitas', title="Bagaimana Pelanggan Menghabiskan Waktunya?",
                         color_discrete_sequence=['#ff6347','#90ee90'])
        st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("#### Probabilitas Panjang Antrian")
        n_values = np.arange(0, 15)
        p_n_values = [(1 - rho) * (rho ** n) for n in n_values]
        df_bar = pd.DataFrame({'Jumlah Mobil': n_values, 'Probabilitas': p_n_values})
        fig_bar = px.bar(df_bar, x='Jumlah Mobil', y='Probabilitas', title='Seberapa Mungkin Antrian Menjadi Panjang?',
                         text_auto='.2%')
        fig_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

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
        st.markdown("#### Visualisasi Interaktif Dampak Keandalan")
        
        labels = list(reliabilities.keys())
        values = list(reliabilities.values())
        labels.append("SISTEM TOTAL")
        values.append(keandalan_sistem)
        
        df_bar = pd.DataFrame({'Komponen': labels, 'Keandalan': values})
        df_bar['Warna'] = ['Komponen'] * len(reliabilities) + ['Sistem Total']
        df_bar.loc[df_bar['Komponen'] == weakest_link_name, 'Warna'] = 'Mata Rantai Terlemah'
        
        fig = px.bar(df_bar, x='Komponen', y='Keandalan', color='Warna', text_auto='.2%',
                     title='Perbandingan Keandalan Komponen dan Sistem',
                     color_discrete_map={
                         'Komponen': '#87CEEB',
                         'Mata Rantai Terlemah': '#FF6347',
                         'Sistem Total': '#9370DB'
                     })
        fig.update_layout(yaxis_range=[min(0.7, min(values)*0.9), 1.01])
        st.plotly_chart(fig, use_container_width=True)
        
        with st.container(border=True):
            st.markdown("**🔍 Cara Membaca Grafik:**")
            st.markdown("""
            Arahkan kursor pada bar untuk melihat nilai presisi.
            - **Bar Merah:** Menunjukkan mesin dengan keandalan terendah, yang menjadi **mata rantai terlemah**.
            - **Bar Ungu:** Menunjukkan keandalan total sistem. Perhatikan bagaimana nilainya selalu **lebih rendah** dari komponen terlemah sekalipun.
            
            **Kesimpulan:** Dalam sistem seri, keandalan keseluruhan sangat dipengaruhi oleh komponen yang paling tidak andal.
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
st.caption("© 2025 TIF208 - Matematika Terapan | Dikembangkan untuk Tugas Kelompok")
