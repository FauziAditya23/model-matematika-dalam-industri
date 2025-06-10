import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import linprog

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Aplikasi Model Matematika Industri",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Aplikasi Model Matematika dalam Industri")

# --- Sidebar ---
with st.sidebar:
    st.header("Panduan Aplikasi")
    st.markdown("""
- **Tab 1: Optimasi Produksi**: Linear Programming (Pabrik meja & kursi)
- **Tab 2: Model Persediaan (EOQ)**: Minimasi biaya total
- **Tab 3: Model Antrian (M/M/1)**: Kinerja bank drive-thru
- **Tab 4: Regresi Linear**: Prediksi permintaan vs suhu udara

Adjust parameter pada setiap tab, lalu lihat hasil perhitungan dan grafik interaktif.
    """)
    st.markdown("---")
    st.caption("© 2025 Matematika Terapan | Universitas Pelita Bangsa")

# --- Tab 1: Optimasi Produksi ---
def optimasi_produksi():
    st.header("1. Optimasi Produksi (Linear Programming)")
    st.markdown("Tentukan kombinasi produksi meja & kursi untuk memaksimalkan keuntungan.")

    # Input parameter
    profit = {
        'table': st.number_input("Keuntungan per meja (Rp)", 0, value=500_000, step=10_000),
        'chair': st.number_input("Keuntungan per kursi (Rp)", 0, value=300_000, step=10_000)
    }
    time = {
        'table': st.number_input("Jam kayu per meja", value=3.0, step=0.5),
        'chair': st.number_input("Jam kayu per kursi", value=2.0, step=0.5)
    }
    assemble = {
        'table': st.number_input("Jam perakitan per meja", value=2.0, step=0.5),
        'chair': st.number_input("Jam perakitan per kursi", value=1.0, step=0.5)
    }
    capacity = {
        'wood': st.number_input("Total jam kayu tersedia", value=120.0, step=10.0),
        'assemble': st.number_input("Total jam perakitan tersedia", value=80.0, step=10.0)
    }

    # Bangun LP (maximize -> minimize -profit)
    c = [-profit['table'], -profit['chair']]
    A = [[time['table'], time['chair']], [assemble['table'], assemble['chair']]]
    b = [capacity['wood'], capacity['assemble']]
    bounds = [(0, None), (0, None)]
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if res.success:
        x_opt, y_opt = res.x
        profit_opt = profit['table']*x_opt + profit['chair']*y_opt
        st.subheader(f"Solusi Optimal: {x_opt:.0f} meja & {y_opt:.0f} kursi")
        st.metric("Keuntungan Maksimum", f"Rp{profit_opt:,.0f}")
    else:
        st.error("Optimasi gagal. Periksa parameter.")
        return

    # Visualisasi Feasible Region
    x_vals = np.linspace(0, x_opt*1.5, 200)
    y_wood = (capacity['wood'] - time['table']*x_vals)/time['chair']
    y_ass = (capacity['assemble'] - assemble['table']*x_vals)/assemble['chair']
    y_bound = np.minimum(y_wood, y_ass)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_wood, label='Kendala Kayu')
    ax.plot(x_vals, y_ass, label='Kendala Perakitan')
    ax.fill_between(x_vals, 0, y_bound, where=y_bound>=0, alpha=0.3)
    ax.scatter(x_opt, y_opt, color='red', zorder=5, label='Optimal')
    ax.set_xlim(0, max(x_vals))
    ax.set_ylim(0, max(y_bound)*1.1)
    ax.set_xlabel('Jumlah Meja')
    ax.set_ylabel('Jumlah Kursi')
    ax.legend()
    ax.set_title('Daerah Feasible & Titik Optimal')
    st.pyplot(fig)

# --- Tab 2: Model Persediaan (EOQ) ---
def model_persediaan():
    st.header("2. Model Persediaan (EOQ)")
    st.markdown("Hitung EOQ dan total biaya persediaan.")

    D = st.number_input("Permintaan tahunan (unit)", 1, value=10_000)
    S = st.number_input("Biaya pemesanan (Rp/pesanan)", 0, value=100_000)
    H = st.number_input("Biaya penyimpanan (Rp/unit/tahun)", 0, value=5_000)
    lead = st.number_input("Lead time (hari)", 0, value=5)

    # EOQ & ROP
    eoq = math.sqrt(2*D*S/H)
    rop = (D/365)*lead
    total_cost = (D/eoq)*S + (eoq/2)*H

    st.subheader(f"EOQ Optimal: {eoq:.0f} unit")
    st.metric("Reorder Point (ROP)", f"{rop:.0f} unit")
    st.metric("Total Biaya Minimum", f"Rp{total_cost:,.0f}")

    # Grafik biaya
    qs = np.linspace(eoq*0.2, eoq*3, 200)
    cost_order = (D/qs)*S
    cost_hold = (qs/2)*H
    fig, ax = plt.subplots()
    ax.plot(qs, cost_order, label='Biaya Pemesanan')
    ax.plot(qs, cost_hold, label='Biaya Penyimpanan')
    ax.plot(qs, cost_order+cost_hold, label='Total Biaya')
    ax.axvline(eoq, linestyle='--', color='grey', label='EOQ')
    ax.set_xlabel('Kuantitas Pesanan')
    ax.set_ylabel('Biaya (Rp)')
    ax.legend()
    ax.set_title('Kurva Biaya Persediaan')
    st.pyplot(fig)

# --- Tab 3: Model Antrian (M/M/1) ---
def model_antrian():
    st.header("3. Model Antrian (M/M/1)")
    st.markdown("Analisis antrian bank drive-thru.")

    lam = st.number_input("Tingkat kedatangan λ (per jam)", 0.1, value=10.0)
    mu = st.number_input("Tingkat layanan μ (per jam)", 0.1, value=15.0)
    if mu <= lam:
        st.error("μ harus > λ untuk kestabilan sistem.")
        return

    rho = lam/mu
    L = rho/(1-rho)
    Lq = rho**2/(1-rho)
    W = 1/(mu-lam)
    Wq = rho/(mu-lam)
    P0 = 1-rho

    st.metric("Utilisasi (ρ)", f"{rho:.2%}")
    st.metric("Avg Pelanggan di Sistem (L)", f"{L:.2f}")
    st.metric("Avg Pelanggan di Antrian (Lq)", f"{Lq:.2f}")
    st.metric("Waktu di Sistem (W)", f"{W*60:.1f} menit")
    st.metric("Waktu Antri (Wq)", f"{Wq*60:.1f} menit")
    st.metric("Prob Sistem Kosong (P0)", f"{P0:.2%}")

    # Distribusi Pn
    n = np.arange(0, 15)
    p_n = (1-rho)*(rho**n)
    fig, ax = plt.subplots()
    ax.bar(n, p_n)
    ax.set_xlabel('Jumlah Pelanggan')
    ax.set_ylabel('P(n)')
    ax.set_title('Distribusi Jumlah Pelanggan')
    st.pyplot(fig)

# --- Tab 4: Regresi Linear Sederhana ---
def model_regresi():
    st.header("4. Regresi Linear Sederhana")
    st.markdown("Prediksi penjualan berdasarkan suhu udara.")

    xs = st.text_input("Suhu (°C), koma-separator", "20,22,24,26,28,30,32")
    ys = st.text_input("Penjualan (unit), koma-separator", "200,220,260,300,340,360,380")
    if st.button("Hitung Regresi"):
        try:
            X = np.array(list(map(float, xs.split(','))))
            Y = np.array(list(map(float, ys.split(','))))
            b1, b0 = np.polyfit(X, Y, 1)
            Ypred = b0 + b1*X
            r2 = 1 - np.sum((Y-Ypred)**2)/np.sum((Y-np.mean(Y))**2)

            st.subheader(f"Model: Y = {b0:.2f} + {b1:.2f}X (R²={r2:.3f})")
            fig, ax = plt.subplots()
            ax.scatter(X, Y, label='Data')
            line = np.linspace(min(X), max(X), 100)
            ax.plot(line, b0 + b1*line, 'r-', label='Garis Regresi')
            ax.set_xlabel('Suhu (°C)')
            ax.set_ylabel('Penjualan')
            ax.set_title('Regresi Linear Sederhana')
            ax.legend()
            st.pyplot(fig)

            temp = st.number_input("Prediksi suhu (°C)", value=25.0)
            pred = b0 + b1*temp
            st.metric("Prediksi Penjualan", f"{pred:.0f} unit")
        except Exception:
            st.error("Data tidak valid. Periksa format input.")

# --- Main ---
t1, t2, t3, t4 = st.tabs([
    "Optimasi Produksi",
    "Model Persediaan",
    "Model Antrian",
    "Regresi Linear"
])
with t1:
    optimasi_produksi()
with t2:
    model_persediaan()
with t3:
    model_antrian()
with t4:
    model_regresi()

st.divider()
st.caption("Aplikasi ini dikembangkan untuk tugas Matematika Terapan 2025.")
