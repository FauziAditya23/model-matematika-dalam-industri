import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.optimize import linprog

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Model Matematika Industri",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("APLIKASI MODEL MATEMATIKA DALAM INDUSTRI")

# --- Sidebar ---
with st.sidebar:
    st.header("Panduan Aplikasi")
    st.markdown("""
- **Tab 1: Optimasi Produksi**: Linear Programming (Pabrik meja & kursi)
- **Tab 2: Model Persediaan**: EOQ (Toko lampu LED)
- **Tab 3: Model Antrian**: M/M/1 (Bank drive-thru)
- **Tab 4: Regresi Linear**: Prediksi permintaan vs suhu udara

Sesuaikan parameter di setiap tab, lalu lihat hasil perhitungan dan grafik interaktif.
    """)
    st.markdown("---")
    st.caption("TIF208 - Matematika Terapan | Universitas Pelita Bangsa")

# --- Tab 1: Optimasi Produksi ---
def optimasi_produksi():
    st.header("1. Optimasi Produksi (Linear Programming)")
    st.markdown("Pabrik memproduksi meja & kursi: maksimalkan keuntungan dengan kendala kayu & perakitan.")

    # Input
    p_table = st.number_input("Keuntungan meja (Rp)", 0, value=250_000, step=10_000)
    p_chair = st.number_input("Keuntungan kursi (Rp)", 0, value=120_000, step=10_000)
    t_table = st.number_input("Jam kayu per meja", value=3.0)
    t_chair = st.number_input("Jam kayu per kursi", value=1.0)
    a_table = st.number_input("Jam rakit per meja", value=2.0)
    a_chair = st.number_input("Jam rakit per kursi", value=1.0)
    cap_wood = st.number_input("Total jam kayu tersedia", value=120.0)
    cap_assemble = st.number_input("Total jam rakit tersedia", value=200.0)

    # LP
    c = [-p_table, -p_chair]
    A = [[t_table, t_chair], [a_table, a_chair]]
    b = [cap_wood, cap_assemble]
    res = linprog(c, A_ub=A, b_ub=b, bounds=[(0, None),(0, None)], method='highs')

    if res.success:
        x_opt, y_opt = res.x
        profit_opt = p_table*x_opt + p_chair*y_opt
        st.subheader(f"Solusi Optimal: {x_opt:.0f} meja & {y_opt:.0f} kursi")
        st.metric("Keuntungan Maksimum", f"Rp{profit_opt:,.0f}")
    else:
        st.error("Optimasi gagal. Cek kembali parameter.")
        return

    # Plot
    x = np.linspace(0, x_opt*1.5, 200)
    y1 = (cap_wood - t_table*x)/t_chair
    y2 = (cap_assemble - a_table*x)/a_chair
    y_bound = np.minimum(y1, y2)

    fig, ax = plt.subplots()
    ax.plot(x, y1, label='Kendala Kayu')
    ax.plot(x, y2, label='Kendala Perakitan')
    ax.fill_between(x, 0, y_bound, where=y_bound>=0, alpha=0.3)
    ax.scatter(x_opt, y_opt, color='red', label='Optimal')
    ax.set_xlabel('Jumlah Meja')
    ax.set_ylabel('Jumlah Kursi')
    ax.legend()
    ax.set_title('Daerah Feasible & Titik Optimal')
    st.pyplot(fig)

# --- Tab 2: Model Persediaan (EOQ) ---
def model_persediaan():
    st.header("2. Model Persediaan (EOQ)")
    st.markdown("Toko lampu LED: tentukan EOQ untuk minimal biaya.")

    D = st.number_input("Permintaan tahunan (unit)", 1, value=2400)
    S = st.number_input("Biaya pemesanan (Rp)", 0, value=150_000)
    H = st.number_input("Biaya simpan per unit (Rp/tahun)", 0, value=15_000)
    lead = st.number_input("Lead time (hari)", 0, value=5)

    eoq = math.sqrt(2*D*S/H)
    rop = (D/365)*lead
    total = (D/eoq)*S + (eoq/2)*H

    st.subheader(f"EOQ: {eoq:.0f} unit")
    st.metric("Reorder Point (ROP)", f"{rop:.0f} unit")
    st.metric("Biaya Total Minimum", f"Rp{total:,.0f}")

    q = np.linspace(eoq*0.2, eoq*3, 200)
    c_order = (D/q)*S
    c_hold = (q/2)*H
    fig, ax = plt.subplots()
    ax.plot(q, c_order, label='Order Cost')
    ax.plot(q, c_hold, label='Holding Cost')
    ax.plot(q, c_order+c_hold, label='Total Cost')
    ax.axvline(eoq, linestyle='--', label='EOQ')
    ax.set_xlabel('Q')
    ax.set_ylabel('Cost (Rp)')
    ax.legend()
    ax.set_title('Biaya EOQ')
    st.pyplot(fig)

# --- Tab 3: Model Antrian (M/M/1) ---
def model_antrian():
    st.header("3. Model Antrian (M/M/1)")
    st.markdown("Bank drive-thru: analisis metrik antrian.")

    lam = st.number_input("λ (arrivals/jam)", 0.1, value=40.0)
    mu = st.number_input("μ (services/jam)", 0.1, value=45.0)
    if mu <= lam:
        st.error("μ harus > λ!")
        return

    rho = lam/mu
    L = rho/(1-rho)
    Lq = rho**2/(1-rho)
    W = 1/(mu-lam)
    Wq = rho/(mu-lam)
    P0 = 1-rho

    st.metric("Utilisasi ρ", f"{rho:.2%}")
    st.metric("Avg Sys L", f"{L:.2f}")
    st.metric("Avg Queue Lq", f"{Lq:.2f}")
    st.metric("Waktu Sistem W", f"{W*60:.1f} mnt")
    st.metric("Waktu Antri Wq", f"{Wq*60:.1f} mnt")
    st.metric("Prob Kosong P0", f"{P0:.2%}")

    n = np.arange(0, 15)
    p_n = (1-rho)*(rho**n)
    fig, ax = plt.subplots()
    ax.bar(n, p_n)
    ax.set_xlabel('n pelanggan')
    ax.set_ylabel('P(n)')
    ax.set_title('Distribusi Jumlah Pelanggan')
    st.pyplot(fig)

# --- Tab 4: Regresi Linear Sederhana ---
def model_regresi():
    st.header("4. Regresi Linear Sederhana")
    st.markdown("Prediksi penjualan berdasarkan suhu udara.")

    xs = st.text_input("Suhu (°C), pisahkan koma", "20,22,24,26,28,30,32")
    ys = st.text_input("Penjualan (unit), pisahkan koma", "200,220,260,300,340,360,380")
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

# --- Main App ---

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

st.caption("© 2025 TIF208 - Matematika Terapan | Dikembangkan untuk Tugas Kelompok")
