import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# 1. Konfigurasi Halaman & Tema Global
# ==============================================================================
st.set_page_config(
    page_title="Olist Analytics | BI Dashboard E-Commerce",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Styling BI Dashboard Padat, Bersih, dan Visual-First
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Font Konsisten (Inter) untuk seluruh elemen */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #EEF3EE !important;
        color: #0B2A1A !important;
    }
    
    /* Sembunyikan header/toolbar Streamlit & tombol Deploy bawaan */
    header[data-testid="stHeader"], [data-testid="stHeader"] {
        display: none !important;
        height: 0px !important;
    }
    [data-testid="stToolbar"] {
        display: none !important;
    }
    #MainMenu {
        visibility: hidden !important;
    }
    footer {
        visibility: hidden !important;
    }
    
    /* Layout Container & Spacing Bersih Padat */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 1.8rem !important;
        padding-right: 1.8rem !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
    }
    
    /* Sidebar Styling: Hijau Tua Gradasi (#0B2A1A ke #123D26) */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B2A1A 0%, #123D26 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    
    @media (min-width: 900px) {
        [data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
            transform: none !important;
            min-width: 280px !important;
            max-width: 280px !important;
            width: 280px !important;
        }
    }
    
    /* Tombol Toggle Sidebar saat Layar Kecil */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        position: fixed !important;
        top: 14px !important;
        left: 14px !important;
        z-index: 999999 !important;
        background: #0B2A1A !important;
        border: 1.5px solid #2ECC71 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        padding: 4px !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: #2ECC71 !important;
    }
    
    /* Sidebar Typography & Labels */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #DDEBDD !important;
    }
    
    /* Input Tanggal di Sidebar: 100% Lebar & Font 14px agar Tidak Terpotong */
    [data-testid="stSidebar"] div[data-testid="stDateInput"] {
        width: 100% !important;
    }
    [data-testid="stSidebar"] div[data-testid="stDateInput"] input {
        font-size: 14px !important;
        padding: 8px 12px !important;
        width: 100% !important;
        border-radius: 8px !important;
        color: #0B2A1A !important;
        background-color: #FFFFFF !important;
    }
    
    /* Radio Button Sidebar Bergaya Menu Tombol */
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 5px !important;
    }
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        margin-bottom: 3px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: rgba(46, 204, 113, 0.4) !important;
    }
    
    /* Sembunyikan lingkaran/indikator radio button asli */
    [data-testid="stSidebar"] div[data-testid="stRadio"] input[type="radio"] {
        display: none !important;
    }
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child:has(input[type="radio"]),
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label > div[data-testid="stRadioGroupSelectionVisual"],
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label > div > div:first-child {
        display: none !important;
    }
    
    /* Menu Aktif: Latar Hijau Terang rgba(46,204,113,0.18) & Teks Hijau #3DDC84 */
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked),
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"],
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[data-selected="true"] {
        background: rgba(46, 204, 113, 0.18) !important;
        border: 1.5px solid #2ECC71 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
    }
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label span {
        color: #FFFFFF !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) span,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[data-checked="true"] span,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[data-selected="true"] p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label[data-selected="true"] span {
        color: #3DDC84 !important;
        font-weight: 700 !important;
    }
    
    /* Tag Multiselect di Sidebar: Hijau Bersih */
    [data-testid="stSidebar"] div[data-baseweb="tag"] {
        background-color: #1A4D2E !important;
        border: 1px solid rgba(46, 204, 113, 0.4) !important;
        border-radius: 6px !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="tag"] * {
        color: #FFFFFF !important;
        font-size: 11.5px !important;
    }
    
    /* Card Container BI: Native Border Wrapper Styling */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1px solid rgba(11, 42, 26, 0.08) !important;
        border-radius: 18px !important;
        padding: 18px 20px !important;
        box-shadow: 0 4px 16px rgba(11, 42, 26, 0.06) !important;
        margin-bottom: 16px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        gap: 0.35rem !important;
    }
    
    /* Kartu KPI Mandiri */
    .kpi-card {
        border-radius: 18px;
        padding: 18px 20px;
        box-sizing: border-box;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-dark {
        background: #0B2A1A;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #FFFFFF;
        box-shadow: 0 4px 16px rgba(11, 42, 26, 0.15);
    }
    .kpi-light {
        background: #FFFFFF;
        border: 1px solid rgba(11, 42, 26, 0.08);
        box-shadow: 0 4px 16px rgba(11, 42, 26, 0.06);
    }
    .kpi-title {
        font-size: 12.5px;
        font-weight: 600;
        color: #718777;
        margin-bottom: 3px;
    }
    .kpi-title-dark {
        font-size: 12.5px;
        font-weight: 600;
        color: #A3C9A8;
        margin-bottom: 3px;
    }
    .kpi-num {
        font-size: 26px;
        font-weight: 800;
        color: #0B2A1A;
        letter-spacing: -0.02em;
        line-height: 1.15;
    }
    .kpi-num-dark {
        font-size: 26px;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.02em;
        line-height: 1.15;
    }
    .kpi-sub {
        font-size: 11.5px;
        color: #5E7566;
        font-weight: 500;
        margin-top: 3px;
    }
    .kpi-sub-dark {
        font-size: 11.5px;
        color: #3DDC84;
        font-weight: 600;
        margin-top: 3px;
    }
    
    /* Pill Badges untuk Tabel & Status */
    .badge-on-time {
        background: #D4EDDA;
        color: #155724;
        padding: 3px 8px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-warning {
        background: #FFF3CD;
        color: #856404;
        padding: 3px 8px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        display: inline-block;
    }
    .badge-danger {
        background: #F8D7DA;
        color: #721C24;
        padding: 3px 8px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        display: inline-block;
    }
    
    /* Tabel BI Elegan */
    .custom-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 13px;
    }
    .custom-table th {
        text-align: left;
        padding: 10px 12px;
        color: #5E7566;
        font-weight: 700;
        font-size: 11.5px;
        border-bottom: 1.5px solid #E6EEE6;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .custom-table td {
        padding: 10px 12px;
        border-bottom: 1px solid #F0F5F0;
        color: #0B2A1A;
        vertical-align: middle;
    }
    .custom-table tr:last-child td {
        border-bottom: none;
    }
    .custom-table tr:hover td {
        background-color: #F8FAF8;
    }
</style>""", unsafe_allow_html=True)


# ==============================================================================
# 2. Data Loading & Preprocessing
# ==============================================================================
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "main_data.csv")
    
    df = pd.read_csv(file_path, parse_dates=["order_purchase_timestamp"])
    df["is_late"] = df["delay_days"] > 0
    df["delay_group"] = pd.cut(
        df["delay_days"],
        bins=[-np.inf, 0, 3, 7, np.inf],
        labels=["Tepat waktu / Lebih cepat", "Telat 1–3 hari", "Telat 4–7 hari", "Telat >7 hari"]
    )
    return df


def format_currency(value):
    return f"R$ {value:,.0f}"


def format_number(value):
    return f"{value:,.0f}"


df_raw = load_data()

# Navigasi BI Menu
nav_options = [
    "Overview",
    "Kategori Produk",
    "Pengiriman & Review",
    "Wilayah & Geografis",
    "Segmentasi RFM",
    "Kesimpulan & Aksi"
]

if "active_nav" not in st.session_state:
    st.session_state["active_nav"] = nav_options[0]

if st.session_state["active_nav"] not in nav_options:
    st.session_state["active_nav"] = nav_options[0]


# ==============================================================================
# 3. Sidebar (Dark Green Gradient Navigation & Filter)
# ==============================================================================
with st.sidebar:
    st.markdown("""<div style="display:flex; align-items:center; gap:10px; padding:4px 0 14px 0; border-bottom:1px solid rgba(255,255,255,0.08); margin-bottom:14px;">
<div style="background:#2ECC71; width:34px; height:34px; border-radius:9px; display:flex; align-items:center; justify-content:center; font-weight:800; color:#0B2A1A; font-size:16px;">OA</div>
<div><div style="font-size:18px; font-weight:800; color:#FFFFFF; letter-spacing:-0.02em;">Olist Analytics</div></div>
</div>""", unsafe_allow_html=True)
    
    st.markdown('<div style="font-size:11px; font-weight:700; letter-spacing:0.08em; color:#5E8C6A; text-transform:uppercase; margin:8px 0 6px 2px;">MENU DASHBOARD</div>', unsafe_allow_html=True)
    
    current_index = nav_options.index(st.session_state["active_nav"])
    side_selection = st.radio(
        label="Menu Navigasi BI",
        options=nav_options,
        index=current_index,
        label_visibility="collapsed"
    )
    if side_selection != st.session_state["active_nav"]:
        st.session_state["active_nav"] = side_selection
        st.rerun()
    
    st.markdown('<div style="font-size:11px; font-weight:700; letter-spacing:0.08em; color:#5E8C6A; text-transform:uppercase; margin:20px 0 8px 2px;">FILTER DATA</div>', unsafe_allow_html=True)
    
    min_date = df_raw["order_purchase_timestamp"].min().date()
    max_date = df_raw["order_purchase_timestamp"].max().date()
    
    date_range = st.date_input(
        "Rentang Tanggal Pembelian",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date
        
    all_states = sorted(df_raw["customer_state"].dropna().unique().tolist())
    
    state_mode = st.radio(
        "Filter Wilayah",
        ["Semua State (27)", "Pilih State Tertentu"],
        index=0,
        horizontal=True
    )
    
    if state_mode == "Pilih State Tertentu":
        selected_states = st.multiselect(
            "State Pelanggan",
            options=all_states,
            default=["SP", "RJ", "MG", "RS", "PR"]
        )
        if not selected_states:
            selected_states = all_states
    else:
        selected_states = all_states
        st.markdown('<div style="background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.1); border-radius:8px; padding:6px 10px; font-size:12px; color:#A3C9A8; margin-bottom:12px;">✓ Semua 27 State Aktif</div>', unsafe_allow_html=True)
    
    top_n = st.slider("Jumlah Kategori Ditampilkan", min_value=5, max_value=15, value=10, step=1)
    
    st.markdown("""<div style="border-top:1px solid rgba(255,255,255,0.08); padding-top:14px; margin-top:24px; display:flex; align-items:center; gap:10px;">
<div style="width:32px; height:32px; border-radius:50%; background:#2ECC71; color:#0B2A1A; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:13px;">KS</div>
<div>
<div style="font-size:13px; font-weight:700; color:#FFFFFF;">Kartika Nur Savira</div>
<div style="font-size:11px; color:#A3C9A8;">Dicoding Analyst • Olist</div>
</div>
</div>""", unsafe_allow_html=True)


# ==============================================================================
# 4. Filter Application & Data Aggregation
# ==============================================================================
mask = (
    (df_raw["order_purchase_timestamp"].dt.date.between(start_date, end_date)) &
    (df_raw["customer_state"].isin(selected_states))
)
data = df_raw[mask]

if data.empty:
    st.warning("⚠️ Tidak ada data transaksi untuk kombinasi filter yang dipilih.")
    st.info("Silakan pilih rentang tanggal atau negara bagian yang lebih luas pada menu sidebar.")
    st.stop()

orders = data.drop_duplicates("order_id").copy()

total_orders_val = orders["order_id"].nunique()
total_customers_val = data["customer_unique_id"].nunique()
total_revenue_val = data["price"].sum()
avg_review_val = orders["review_score"].mean()

pct_late = orders["is_late"].mean() * 100
avg_delivery_days = orders["delivery_days"].mean()
late_review_val = orders.loc[orders["is_late"], "review_score"].mean()
ontime_review_val = orders.loc[~orders["is_late"], "review_score"].mean()

ontime_neg_pct = (orders.loc[~orders["is_late"], "review_score"] <= 2).mean() * 100 if (~orders["is_late"]).sum() > 0 else 0
late_neg_pct = (orders.loc[orders["is_late"], "review_score"] <= 2).mean() * 100 if orders["is_late"].sum() > 0 else 0

cat_summary = (
    data.groupby("category")
    .agg(
        revenue=("price", "sum"),
        unit_terjual=("order_item_id", "count")
    )
    .reset_index()
)
cat_summary["avg_price"] = cat_summary["revenue"] / cat_summary["unit_terjual"]
cat_sorted = cat_summary.sort_values("revenue", ascending=False)
top_cat_item = cat_sorted.iloc[0] if not cat_sorted.empty else None
top_cat_name = top_cat_item["category"].replace("_", " ").title() if top_cat_item is not None else "Health Beauty"
top_cat_rev = top_cat_item["revenue"] if top_cat_item is not None else 0
top_cat_rev_pct = (top_cat_rev / total_revenue_val * 100) if total_revenue_val > 0 else 0

top5_rev_val = cat_sorted.head(5)["revenue"].sum()
top5_rev_pct = (top5_rev_val / total_revenue_val * 100) if total_revenue_val > 0 else 0

bed_bath_row = cat_summary[cat_summary["category"] == "bed_bath_table"]
bed_bath_units = bed_bath_row["unit_terjual"].values[0] if not bed_bath_row.empty else 0

order_value = data.groupby("order_id")["price"].sum().rename("order_val")
orders_with_val = orders.merge(order_value, on="order_id", how="left")

state_summary = (
    orders_with_val.groupby("customer_state")
    .agg(
        pelanggan=("customer_unique_id", "nunique"),
        total_orders=("order_id", "count"),
        revenue=("order_val", "sum"),
        avg_delivery_days=("delivery_days", "mean"),
        pct_late=("is_late", lambda s: s.mean() * 100)
    )
    .reset_index()
)

sp_row = state_summary[state_summary["customer_state"] == "SP"]
if not sp_row.empty:
    sp_rev_share = (sp_row["revenue"].values[0] / total_revenue_val * 100) if total_revenue_val > 0 else 0
    sp_cust_share = (sp_row["pelanggan"].values[0] / total_customers_val * 100) if total_customers_val > 0 else 0
    sp_delivery_days = sp_row["avg_delivery_days"].values[0]
    sp_late_pct = sp_row["pct_late"].values[0]
else:
    sp_rev_share, sp_cust_share, sp_delivery_days, sp_late_pct = 0, 0, 0, 0

worst_late_row = state_summary.sort_values("pct_late", ascending=False).iloc[0] if not state_summary.empty else None
worst_state_name = worst_late_row["customer_state"] if worst_late_row is not None else "AL"
worst_state_late = worst_late_row["pct_late"] if worst_late_row is not None else 0
worst_state_days = worst_late_row["avg_delivery_days"] if worst_late_row is not None else 0

# RFM Calculation Sesuai Persis dengan Notebook
max_date_ts = data["order_purchase_timestamp"].max()
rfm = orders_with_val.groupby("customer_unique_id").agg(
    recency=("order_purchase_timestamp", lambda d: (max_date_ts - d.max()).days),
    frequency=("order_id", "count"),
    monetary=("order_val", "sum")
).reset_index()

try:
    rfm["r_score"] = pd.qcut(rfm["recency"], 4, labels=[4, 3, 2, 1]).astype(int)
except ValueError:
    rfm["r_score"] = 1

try:
    rfm["m_score"] = pd.qcut(rfm["monetary"], 4, labels=[1, 2, 3, 4]).astype(int)
except ValueError:
    rfm["m_score"] = 1

def segment_customer(row):
    if row["frequency"] > 1:
        return "Repeat Buyer"
    if row["r_score"] >= 3 and row["m_score"] >= 3:
        return "Baru - Nilai Tinggi"
    if row["r_score"] >= 3 and row["m_score"] < 3:
        return "Baru - Nilai Rendah"
    if row["r_score"] < 3 and row["m_score"] >= 3:
        return "Berisiko Hilang - Nilai Tinggi"
    return "Tidak Aktif - Nilai Rendah"

rfm["segment"] = rfm.apply(segment_customer, axis=1)
segment_counts = rfm["segment"].value_counts().to_dict()

repeat_buyers_count = segment_counts.get("Repeat Buyer", 0)
repeat_buyers_pct = (repeat_buyers_count / total_customers_val * 100) if total_customers_val > 0 else 0
inactive_count = segment_counts.get("Tidak Aktif - Nilai Rendah", 0)
new_low_count = segment_counts.get("Baru - Nilai Rendah", 0)
new_high_count = segment_counts.get("Baru - Nilai Tinggi", 0)
at_risk_count = segment_counts.get("Berisiko Hilang - Nilai Tinggi", 0)

active_page = st.session_state["active_nav"]


# ==============================================================================
# 5. Header Ringkas BI
# ==============================================================================
st.markdown(f"""<div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:12px;">
<div>
    <h1 style="font-size:24px; font-weight:800; color:#0B2A1A; margin:0; letter-spacing:-0.02em;">Olist Business Intelligence</h1>
    <div style="font-size:13px; color:#5E7566; margin-top:2px;">Analisis {format_number(total_orders_val)} pesanan terkirim (Januari 2017 – Agustus 2018)</div>
</div>
<div style="font-size:12px; font-weight:600; color:#2ECC71; background:#FFFFFF; border:1px solid rgba(11,42,26,0.08); padding:5px 12px; border-radius:10px;">
    Menu: {active_page}
</div>
</div>""", unsafe_allow_html=True)


# ==============================================================================
# 6. Baris 4 KPI (Padat & Rapi)
# ==============================================================================
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""<div class="kpi-card kpi-dark">
<div>
    <div class="kpi-title-dark">Total Pesanan</div>
    <div class="kpi-num-dark">{format_number(total_orders_val)}</div>
    <div class="kpi-sub-dark">↗ 100% pesanan terkirim</div>
</div>
</div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""<div class="kpi-card kpi-light">
<div>
    <div class="kpi-title">Total Pelanggan</div>
    <div class="kpi-num">{format_number(total_customers_val)}</div>
    <div class="kpi-sub">Konsumen unik terdaftar</div>
</div>
</div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""<div class="kpi-card kpi-light">
<div>
    <div class="kpi-title">Total Revenue</div>
    <div class="kpi-num">{format_currency(total_revenue_val)}</div>
    <div class="kpi-sub" style="color:#2ECC71;">Total perputaran transaksi</div>
</div>
</div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""<div class="kpi-card kpi-light">
<div>
    <div class="kpi-title">Rata-rata Review</div>
    <div class="kpi-num">{avg_review_val:.2f} <span style="font-size:14px;color:#829788;">/ 5.0</span></div>
    <div class="kpi-sub" style="color:#2ECC71;">Skor kepuasan pelanggan</div>
</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# Helper Functions: Plotly Charts Ringkas BI
# ==============================================================================
def plot_top_categories_bar(cat_df, metric_col="revenue", n=7):
    is_rev = metric_col == "revenue"
    df_plot = cat_df.sort_values(metric_col, ascending=False).head(n).copy()
    names = [c.replace("_", " ").title() for c in df_plot["category"]]
    colors = ["#2ECC71"] + ["#A8D5BA"] * (len(df_plot) - 1)
    
    fig = go.Figure(go.Bar(
        x=df_plot[metric_col],
        y=names,
        orientation="h",
        marker=dict(color=colors, cornerradius=5),
        text=[f"R$ {v:,.0f}" if is_rev else f"{v:,} unit" for v in df_plot[metric_col]],
        textposition="outside",
        textfont=dict(size=11, family="Inter", color="#0B2A1A"),
        hoverinfo="text",
        hovertext=[f"<b>{name}</b><br>Revenue: R$ {row['revenue']:,.0f}<br>Unit: {row['unit_terjual']:,}<br>Harga Rata-rata: R$ {row['avg_price']:,.2f}" for name, (_, row) in zip(names, df_plot.iterrows())]
    ))
    fig.update_layout(
        margin=dict(l=10, r=85, t=5, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=270,
        yaxis=dict(autorange="reversed", tickfont=dict(size=11.5, color="#0B2A1A", family="Inter")),
        xaxis=dict(showgrid=True, gridcolor="#EBF2EB", tickfont=dict(size=10.5, color="#718777"))
    )
    return fig


def plot_delay_review_bar(orders_df, avg_score):
    delay_sum = (
        orders_df.groupby("delay_group", observed=True)
        .agg(avg_score=("review_score", "mean"), count=("order_id", "count"))
        .reset_index()
    )
    colors = ["#2ECC71", "#F59E0B", "#F97316", "#EF4444"]
    
    fig = go.Figure(go.Bar(
        x=delay_sum["delay_group"],
        y=delay_sum["avg_score"],
        marker=dict(color=colors, cornerradius=5),
        text=[f"{v:.2f}" for v in delay_sum["avg_score"]],
        textposition="outside",
        textfont=dict(size=11.5, family="Inter", color="#0B2A1A", weight="bold"),
        hoverinfo="text",
        hovertext=[f"<b>{g}</b><br>Rata-rata Review: {s:.2f}<br>Jumlah Pesanan: {c:,}" for g, s, c in zip(delay_sum["delay_group"], delay_sum["avg_score"], delay_sum["count"])]
    ))
    fig.add_hline(
        y=avg_score,
        line_dash="dash",
        line_color="#0B2A1A",
        line_width=1.5,
        annotation_text=f"Rata-rata ({avg_score:.2f})",
        annotation_position="top right",
        annotation_font=dict(size=10.5, color="#0B2A1A")
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=20, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=270,
        yaxis=dict(range=[0, 5.2], showgrid=True, gridcolor="#EBF2EB", tickfont=dict(size=10.5, color="#718777")),
        xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#0B2A1A", family="Inter"))
    )
    return fig


def plot_state_revenue_bar(state_df, n=10):
    df_plot = state_df.sort_values("revenue", ascending=False).head(n).copy()
    colors = ["#2ECC71"] + ["#A8D5BA"] * (len(df_plot) - 1)
    
    fig = go.Figure(go.Bar(
        x=df_plot["revenue"],
        y=df_plot["customer_state"],
        orientation="h",
        marker=dict(color=colors, cornerradius=5),
        text=[f"R$ {v:,.0f}" for v in df_plot["revenue"]],
        textposition="outside",
        textfont=dict(size=11, family="Inter", color="#0B2A1A"),
        hoverinfo="text",
        hovertext=[f"<b>{st}</b><br>Revenue: R$ {row['revenue']:,.0f}<br>Pesanan: {row['total_orders']:,}<br>% Terlambat: {row['pct_late']:.1f}%" for st, (_, row) in zip(df_plot["customer_state"], df_plot.iterrows())]
    ))
    fig.update_layout(
        margin=dict(l=10, r=85, t=5, b=25),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=270,
        yaxis=dict(autorange="reversed", tickfont=dict(size=11.5, color="#0B2A1A", family="Inter")),
        xaxis=dict(showgrid=True, gridcolor="#EBF2EB", tickfont=dict(size=10.5, color="#718777"))
    )
    return fig


def plot_brazil_map(orders_df):
    geo = orders_df.dropna(subset=["lat", "lng"])[["lat", "lng"]]
    sample_size = min(len(geo), 3500)
    sample_geo = geo.sample(sample_size, random_state=42) if not geo.empty else geo
    
    fig = go.Figure(go.Scattergeo(
        lat=sample_geo["lat"],
        lon=sample_geo["lng"],
        mode="markers",
        marker=dict(size=3.5, color="#3DDC84", opacity=0.75),
        hoverinfo="none"
    ))
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        showland=True,
        landcolor="#123B25",
        showocean=True,
        oceancolor="#071F13",
        showcountries=True,
        countrycolor="#1A5333",
        bgcolor="#0B2A1A"
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="#0B2A1A",
        plot_bgcolor="#0B2A1A",
        height=270
    )
    return fig


# ==============================================================================
# 7. RENDER HALAMAN BI SESUAI MENU
# ==============================================================================

# ------------------------------------------------------------------------------
# HALAMAN 1: OVERVIEW (Semua dalam 1 layar laptop)
# ------------------------------------------------------------------------------
if active_page == "Overview":
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Card 1: Kategori Produk Teratas
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">{top_cat_name} Memimpin Revenue dengan {format_currency(top_cat_rev)}</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:8px;">5 kategori teratas menyumbang {top5_rev_pct:.1f}% dari total revenue platform.</div>
</div>""", unsafe_allow_html=True)
            fig1 = plot_top_categories_bar(cat_sorted, metric_col="revenue", n=7)
            st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

        # Card 3: Revenue per State
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">São Paulo (SP) Menguasai {sp_rev_share:.1f}% Revenue Nasional</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:8px;">Konsentrasi omzet terpusat di SP ({format_currency(sp_row['revenue'].values[0] if not sp_row.empty else 0)}), disusul RJ dan MG.</div>
</div>""", unsafe_allow_html=True)
            fig3 = plot_state_revenue_bar(state_summary, n=7)
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        # Card 2: Review vs Keterlambatan
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Review Turun dari {ontime_review_val:.2f} ke {late_review_val:.2f} Saat Pesanan Terlambat</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:8px;">Pesanan terlambat mencakup {pct_late:.1f}% total pesanan dan memicu {late_neg_pct:.1f}% ulasan negatif.</div>
</div>""", unsafe_allow_html=True)
            fig2 = plot_delay_review_bar(orders, avg_review_val)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

        # Card 4: Peta Sebaran Pesanan
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Sebaran Geografis Pelanggan di Brasil</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:8px;">{total_customers_val:,} pelanggan terdistribusi dengan kepadatan tertinggi di pesisir Tenggara dan Selatan.</div>
</div>""", unsafe_allow_html=True)
            fig4 = plot_brazil_map(data)
            st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})


# ------------------------------------------------------------------------------
# HALAMAN 2: KATEGORI PRODUK (Pertanyaan 1)
# ------------------------------------------------------------------------------
elif active_page == "Kategori Produk":
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Top Kategori Berdasarkan Revenue (Omzet)</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:8px;">{top_cat_name} mencatatkan pendapatan tertinggi sebesar {format_currency(top_cat_rev)}.</div>
</div>""", unsafe_allow_html=True)
            fig_rev = plot_top_categories_bar(cat_sorted, metric_col="revenue", n=top_n)
            st.plotly_chart(fig_rev, use_container_width=True, config={"displayModeBar": False})
            
    with col_c2:
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Top Kategori Berdasarkan Unit Terjual (Volume)</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:8px;">Bed Bath Table memimpin volume penjualan dengan {bed_bath_units:,} unit terjual.</div>
</div>""", unsafe_allow_html=True)
            cat_by_units = cat_summary.sort_values("unit_terjual", ascending=False).head(top_n).copy()
            unit_names = [c.replace("_", " ").title() for c in cat_by_units["category"]]
            unit_colors = ["#2ECC71"] + ["#A8D5BA"] * (len(cat_by_units) - 1)
            
            fig_unit = go.Figure(go.Bar(
                x=cat_by_units["unit_terjual"],
                y=unit_names,
                orientation="h",
                marker=dict(color=unit_colors, cornerradius=5),
                text=[f"{v:,} unit" for v in cat_by_units["unit_terjual"]],
                textposition="outside",
                textfont=dict(size=11, family="Inter", color="#0B2A1A"),
                hoverinfo="text",
                hovertext=[f"<b>{name}</b><br>Unit: {row['unit_terjual']:,}<br>Revenue: R$ {row['revenue']:,.0f}<br>Harga Rata-rata: R$ {row['avg_price']:,.2f}" for name, (_, row) in zip(unit_names, cat_by_units.iterrows())]
            ))
            fig_unit.update_layout(
                margin=dict(l=10, r=85, t=5, b=25),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=270,
                yaxis=dict(autorange="reversed", tickfont=dict(size=11.5, color="#0B2A1A", family="Inter")),
                xaxis=dict(showgrid=True, gridcolor="#EBF2EB", tickfont=dict(size=10.5, color="#718777"))
            )
            st.plotly_chart(fig_unit, use_container_width=True, config={"displayModeBar": False})

    # Tabel Ringkas Kategori
    with st.container(border=True):
        st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Tabel Ringkas Performa Kategori Produk (Top {top_n})</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:10px;">5 kategori teratas menguasai {top5_rev_pct:.1f}% ({format_currency(top5_rev_val)}) dari total omzet.</div>
</div>""", unsafe_allow_html=True)
        
        table_cat = cat_sorted.head(top_n).copy()
        table_cat["proporsi"] = table_cat["revenue"] / total_revenue_val * 100
        
        html_cat = """<table class="custom-table">
<thead>
<tr>
    <th>Peringkat</th>
    <th>Kategori</th>
    <th>Revenue</th>
    <th>Proporsi</th>
    <th>Unit Terjual</th>
    <th>Harga Rata-rata</th>
</tr>
</thead>
<tbody>"""
        for rank, (_, row) in enumerate(table_cat.iterrows(), start=1):
            c_name = row["category"].replace("_", " ").title()
            html_cat += f"""<tr>
    <td><strong>#{rank}</strong></td>
    <td><strong>{c_name}</strong></td>
    <td>{format_currency(row['revenue'])}</td>
    <td><strong>{row['proporsi']:.1f}%</strong></td>
    <td>{row['unit_terjual']:,}</td>
    <td>R$ {row['avg_price']:,.2f}</td>
</tr>"""
        html_cat += "</tbody></table>"
        st.markdown(html_cat, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# HALAMAN 3: PENGIRIMAN & REVIEW (Pertanyaan 2)
# ------------------------------------------------------------------------------
elif active_page == "Pengiriman & Review":
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Skor Review Berdasarkan Tingkat Keterlambatan</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:8px;">Keterlambatan >7 hari menghasilkan review terendah ({orders.loc[orders['delay_group']=='Telat >7 hari', 'review_score'].mean():.2f} / 5.0).</div>
</div>""", unsafe_allow_html=True)
            fig_del = plot_delay_review_bar(orders, avg_review_val)
            st.plotly_chart(fig_del, use_container_width=True, config={"displayModeBar": False})
            
    with col_p2:
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Proporsi Ulasan Negatif (★ 1–2): Tepat Waktu vs Terlambat</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:8px;">Ulasan negatif melonjak tajam dari {ontime_neg_pct:.1f}% menjadi {late_neg_pct:.1f}% saat pesanan terlambat.</div>
</div>""", unsafe_allow_html=True)
            
            fig_neg = go.Figure(go.Bar(
                x=["Tepat Waktu", "Terlambat"],
                y=[ontime_neg_pct, late_neg_pct],
                marker=dict(color=["#2ECC71", "#EF4444"], cornerradius=5),
                text=[f"{ontime_neg_pct:.1f}%", f"{late_neg_pct:.1f}%"],
                textposition="outside",
                textfont=dict(size=12, family="Inter", color="#0B2A1A", weight="bold"),
                hoverinfo="text",
                hovertext=[f"<b>Tepat Waktu</b><br>Ulasan Negatif: {ontime_neg_pct:.1f}%<br>Rata-rata Review: {ontime_review_val:.2f}",
                           f"<b>Terlambat</b><br>Ulasan Negatif: {late_neg_pct:.1f}%<br>Rata-rata Review: {late_review_val:.2f}"]
            ))
            fig_neg.update_layout(
                margin=dict(l=10, r=10, t=20, b=25),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=270,
                yaxis=dict(range=[0, 65], showgrid=True, gridcolor="#EBF2EB", tickfont=dict(size=10.5, color="#718777")),
                xaxis=dict(showgrid=False, tickfont=dict(size=11.5, color="#0B2A1A", family="Inter"))
            )
            st.plotly_chart(fig_neg, use_container_width=True, config={"displayModeBar": False})

    # Tabel Komparasi Logistik
    with st.container(border=True):
        st.markdown("""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Tabel Komparasi Performa Logistik & Ulasan Pelanggan</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:10px;">Perbandingan menyeluruh antara pesanan tepat waktu dan pesanan terlambat.</div>
</div>""", unsafe_allow_html=True)
        
        ontime_orders_count = (~orders["is_late"]).sum()
        late_orders_count = orders["is_late"].sum()
        
        html_del = f"""<table class="custom-table">
<thead>
<tr>
    <th>Status Pengiriman</th>
    <th>Jumlah Pesanan</th>
    <th>Proporsi</th>
    <th>Rata-rata Review</th>
    <th>Proporsi Ulasan Negatif (★ 1–2)</th>
    <th>Rata-rata Hari Pengiriman</th>
</tr>
</thead>
<tbody>
<tr>
    <td><span class="badge-on-time">Tepat Waktu</span></td>
    <td>{ontime_orders_count:,}</td>
    <td><strong>{100 - pct_late:.1f}%</strong></td>
    <td><strong>{ontime_review_val:.2f} / 5.0</strong></td>
    <td>{ontime_neg_pct:.1f}%</td>
    <td>{orders.loc[~orders['is_late'], 'delivery_days'].mean():.1f} hari</td>
</tr>
<tr>
    <td><span class="badge-danger">Terlambat</span></td>
    <td>{late_orders_count:,}</td>
    <td><strong>{pct_late:.1f}%</strong></td>
    <td><strong>{late_review_val:.2f} / 5.0</strong></td>
    <td>{late_neg_pct:.1f}%</td>
    <td>{orders.loc[orders['is_late'], 'delivery_days'].mean():.1f} hari</td>
</tr>
</tbody>
</table>"""
        st.markdown(html_del, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# HALAMAN 4: WILAYAH & GEOGRAFIS (Pertanyaan 3)
# ------------------------------------------------------------------------------
elif active_page == "Wilayah & Geografis":
    col_w1, col_w2 = st.columns(2)
    
    with col_w1:
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Top 10 State dengan Tingkat Keterlambatan Tertinggi</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:8px;">{worst_state_name} mencatatkan keterlambatan tertinggi ({worst_state_late:.1f}%) dengan waktu kirim {worst_state_days:.1f} hari.</div>
</div>""", unsafe_allow_html=True)
            
            top_late_states = state_summary.sort_values("pct_late", ascending=False).head(10).copy()
            late_colors = ["#EF4444" if v > 15 else "#F59E0B" if v > 8 else "#2ECC71" for v in top_late_states["pct_late"]]
            
            fig_state_late = go.Figure(go.Bar(
                x=top_late_states["pct_late"],
                y=top_late_states["customer_state"],
                orientation="h",
                marker=dict(color=late_colors, cornerradius=5),
                text=[f"{v:.1f}%" for v in top_late_states["pct_late"]],
                textposition="outside",
                textfont=dict(size=11, family="Inter", color="#0B2A1A"),
                hoverinfo="text",
                hovertext=[f"<b>{st}</b><br>% Terlambat: {row['pct_late']:.1f}%<br>Waktu Kirim: {row['avg_delivery_days']:.1f} hari<br>Pesanan: {row['total_orders']:,}" for st, (_, row) in zip(top_late_states["customer_state"], top_late_states.iterrows())]
            ))
            fig_state_late.update_layout(
                margin=dict(l=10, r=70, t=5, b=25),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=270,
                yaxis=dict(autorange="reversed", tickfont=dict(size=11.5, color="#0B2A1A", family="Inter")),
                xaxis=dict(showgrid=True, gridcolor="#EBF2EB", tickfont=dict(size=10.5, color="#718777"))
            )
            st.plotly_chart(fig_state_late, use_container_width=True, config={"displayModeBar": False})
            
    with col_w2:
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Sebaran Geografis Pelanggan di Brasil</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:8px;">Titik hijau terang menunjukkan konsentrasi pemesanan pelanggan di 27 state.</div>
</div>""", unsafe_allow_html=True)
            fig_map_geo = plot_brazil_map(data)
            st.plotly_chart(fig_map_geo, use_container_width=True, config={"displayModeBar": False})

    # Tabel Performa State
    with st.container(border=True):
        st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Tabel Performa 10 State Terbesar Berdasarkan Nilai Transaksi</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:10px;">São Paulo (SP) menguasai {sp_rev_share:.1f}% omzet dan {sp_cust_share:.1f}% pelanggan dengan keterlambatan rendah ({sp_late_pct:.1f}%).</div>
</div>""", unsafe_allow_html=True)
        
        top_10_states = state_summary.sort_values("revenue", ascending=False).head(10).copy()
        top_10_states["proporsi"] = top_10_states["revenue"] / total_revenue_val * 100
        
        html_states = """<table class="custom-table">
<thead>
<tr>
    <th>State</th>
    <th>Pelanggan</th>
    <th>Total Pesanan</th>
    <th>Revenue</th>
    <th>Proporsi</th>
    <th>Rata-rata Waktu Kirim</th>
    <th>% Terlambat</th>
</tr>
</thead>
<tbody>"""
        for _, row in top_10_states.iterrows():
            late_val = row["pct_late"]
            badge_class = "badge-on-time" if late_val <= 8.0 else "badge-warning" if late_val <= 14.0 else "badge-danger"
            html_states += f"""<tr>
    <td><strong>{row['customer_state']}</strong></td>
    <td>{row['pelanggan']:,}</td>
    <td>{row['total_orders']:,}</td>
    <td>{format_currency(row['revenue'])}</td>
    <td><strong>{row['proporsi']:.1f}%</strong></td>
    <td>{row['avg_delivery_days']:.1f} hari</td>
    <td><span class="{badge_class}">{late_val:.1f}%</span></td>
</tr>"""
        html_states += "</tbody></table>"
        st.markdown(html_states, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# HALAMAN 5: SEGMENTASI RFM (Analisis Lanjutan)
# ------------------------------------------------------------------------------
elif active_page == "Segmentasi RFM":
    col_rfm1, col_rfm2 = st.columns(2)
    
    with col_rfm1:
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Jumlah Pelanggan per Segmen RFM</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:8px;">Repeat buyer hanya {repeat_buyers_pct:.1f}% ({repeat_buyers_count:,} konsumen), didominasi segmen Tidak Aktif ({inactive_count:,}).</div>
</div>""", unsafe_allow_html=True)
            
            seg_names = [
                "Tidak Aktif - Nilai Rendah",
                "Baru - Nilai Rendah",
                "Baru - Nilai Tinggi",
                "Berisiko Hilang - Nilai Tinggi",
                "Repeat Buyer"
            ]
            seg_vals = [inactive_count, new_low_count, new_high_count, at_risk_count, repeat_buyers_count]
            seg_colors = ["#D1DDD1", "#A8D5BA", "#3DDC84", "#F59E0B", "#2ECC71"]
            
            fig_rfm_cust = go.Figure(go.Bar(
                x=seg_vals,
                y=seg_names,
                orientation="h",
                marker=dict(color=seg_colors, cornerradius=5),
                text=[f"{v:,} ({v/total_customers_val*100:.1f}%)" if total_customers_val > 0 else f"{v:,}" for v in seg_vals],
                textposition="outside",
                textfont=dict(size=11, family="Inter", color="#0B2A1A", weight="bold"),
                hoverinfo="text",
                hovertext=[f"<b>{name}</b><br>Jumlah Pelanggan: {val:,}<br>Proporsi: {val/total_customers_val*100:.2f}%" for name, val in zip(seg_names, seg_vals)]
            ))
            fig_rfm_cust.update_layout(
                margin=dict(l=10, r=100, t=5, b=25),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=270,
                yaxis=dict(tickfont=dict(size=11.5, color="#0B2A1A", family="Inter")),
                xaxis=dict(showgrid=True, gridcolor="#EBF2EB", tickfont=dict(size=10.5, color="#718777"))
            )
            st.plotly_chart(fig_rfm_cust, use_container_width=True, config={"displayModeBar": False})
            
    with col_rfm2:
        with st.container(border=True):
            st.markdown("""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Total Nilai Moneter (Revenue) per Segmen RFM</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:8px;">Segmen Baru Nilai Tinggi dan Berisiko Hilang menyumbang mayoritas revenue.</div>
</div>""", unsafe_allow_html=True)
            
            rfm_rev_series = rfm.groupby("segment")["monetary"].sum().reindex(seg_names).fillna(0)
            fig_rfm_rev = go.Figure(go.Bar(
                x=rfm_rev_series.values,
                y=seg_names,
                orientation="h",
                marker=dict(color=seg_colors, cornerradius=5),
                text=[f"R$ {v:,.0f}" for v in rfm_rev_series.values],
                textposition="outside",
                textfont=dict(size=11, family="Inter", color="#0B2A1A"),
                hoverinfo="text",
                hovertext=[f"<b>{name}</b><br>Total Revenue: R$ {val:,.0f}" for name, val in zip(seg_names, rfm_rev_series.values)]
            ))
            fig_rfm_rev.update_layout(
                margin=dict(l=10, r=90, t=5, b=25),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=270,
                yaxis=dict(tickfont=dict(size=11.5, color="#0B2A1A", family="Inter")),
                xaxis=dict(showgrid=True, gridcolor="#EBF2EB", tickfont=dict(size=10.5, color="#718777"))
            )
            st.plotly_chart(fig_rfm_rev, use_container_width=True, config={"displayModeBar": False})

    # Tabel Ringkas RFM
    with st.container(border=True):
        st.markdown(f"""<div>
<div style="font-size:15px; font-weight:700; color:#0B2A1A;">Tabel Ringkasan Metrik Segmen Pelanggan RFM</div>
<div style="font-size:13px; color:#5E7566; margin-top:3px; margin-bottom:10px;">Perhitungan kuartil recency dan monetary persis sesuai analisis notebook.</div>
</div>""", unsafe_allow_html=True)
        
        rfm_table_df = rfm.groupby("segment").agg(
            pelanggan=("customer_unique_id", "count"),
            revenue=("monetary", "sum"),
            avg_recency=("recency", "mean"),
            avg_monetary=("monetary", "mean")
        ).reindex(seg_names).reset_index()
        
        html_rfm = """<table class="custom-table">
<thead>
<tr>
    <th>Segmen Pelanggan</th>
    <th>Jumlah Pelanggan</th>
    <th>Proporsi</th>
    <th>Total Revenue</th>
    <th>Rata-rata Recency</th>
    <th>Rata-rata Belanja</th>
</tr>
</thead>
<tbody>"""
        for _, row in rfm_table_df.iterrows():
            prop = row["pelanggan"] / total_customers_val * 100 if total_customers_val > 0 else 0
            html_rfm += f"""<tr>
    <td><strong>{row['segment']}</strong></td>
    <td>{row['pelanggan']:,}</td>
    <td><strong>{prop:.1f}%</strong></td>
    <td>{format_currency(row['revenue'])}</td>
    <td>{row['avg_recency']:.0f} hari</td>
    <td>R$ {row['avg_monetary']:,.2f}</td>
</tr>"""
        html_rfm += "</tbody></table>"
        st.markdown(html_rfm, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# HALAMAN 6: KESIMPULAN & AKSI
# ------------------------------------------------------------------------------
elif active_page == "Kesimpulan & Aksi":
    st.markdown('<div style="font-size:16px; font-weight:800; color:#0B2A1A; margin-bottom:8px;">Ringkasan Jawaban 3 Pertanyaan Bisnis</div>', unsafe_allow_html=True)
    
    cq1, cq2, cq3 = st.columns(3)
    
    with cq1:
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:11.5px; font-weight:700; color:#2ECC71; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:4px;">PERTANYAAN 1 • PRODUK</div>
<div style="font-size:15px; font-weight:800; color:#0B2A1A; margin-bottom:6px;">{top_cat_name} Memimpin Pendapatan</div>
<div style="font-size:13px; color:#34503C; line-height:1.5;">
{top_cat_name} menghasilkan pendapatan terbesar ({format_currency(top_cat_rev)}), sementara 5 kategori teratas menyumbang {top5_rev_pct:.1f}% total revenue platform. Bed Bath Table merupakan kategori dengan volume penjualan terbanyak ({bed_bath_units:,} unit).
</div>
</div>""", unsafe_allow_html=True)

    with cq2:
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:11.5px; font-weight:700; color:#2ECC71; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:4px;">PERTANYAAN 2 • LOGISTIK</div>
<div style="font-size:15px; font-weight:800; color:#0B2A1A; margin-bottom:6px;">Review Anjlok Saat Terlambat</div>
<div style="font-size:13px; color:#34503C; line-height:1.5;">
Keterlambatan pengiriman ({pct_late:.1f}% pesanan) menurunkan rata-rata review secara drastis dari {ontime_review_val:.2f} menjadi {late_review_val:.2f}. Keterlambatan juga melipatgandakan ulasan negatif bintang 1–2 dari {ontime_neg_pct:.1f}% menjadi {late_neg_pct:.1f}%.
</div>
</div>""", unsafe_allow_html=True)

    with cq3:
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="font-size:11.5px; font-weight:700; color:#2ECC71; letter-spacing:0.05em; text-transform:uppercase; margin-bottom:4px;">PERTANYAAN 3 • WILAYAH</div>
<div style="font-size:15px; font-weight:800; color:#0B2A1A; margin-bottom:6px;">São Paulo Menguasai Pasar</div>
<div style="font-size:13px; color:#34503C; line-height:1.5;">
São Paulo mendominasi {sp_rev_share:.1f}% revenue dan {sp_cust_share:.1f}% pelanggan dengan waktu kirim {sp_delivery_days:.1f} hari ({sp_late_pct:.1f}% telat). Sebaliknya, state luar Tenggara seperti {worst_state_name} menghadapi waktu kirim {worst_state_days:.1f} hari dan keterlambatan {worst_state_late:.1f}%.
</div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div style="font-size:16px; font-weight:800; color:#0B2A1A; margin:16px 0 8px 0;">4 Rekomendasi Action Items Terukur</div>', unsafe_allow_html=True)

    ca1, ca2 = st.columns(2)
    
    with ca1:
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
    <div style="background:#2ECC71; color:#0B2A1A; font-weight:800; font-size:12px; width:24px; height:24px; border-radius:50%; display:flex; align-items:center; justify-content:center;">1</div>
    <div style="font-size:14.5px; font-weight:800; color:#0B2A1A;">Optimasi Rantai Pasok Wilayah Jauh (Luar Tenggara)</div>
</div>
<div style="font-size:13px; color:#34503C; line-height:1.5;">
Bermitra dengan kurir regional dan mikro-hub di Timur Laut guna memangkas waktu kirim {worst_state_name} ({worst_state_days:.1f} hari) dan menekan tingkat keterlambatan dari {worst_state_late:.1f}%.
</div>
</div>""", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(f"""<div>
<div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
    <div style="background:#2ECC71; color:#0B2A1A; font-weight:800; font-size:12px; width:24px; height:24px; border-radius:50%; display:flex; align-items:center; justify-content:center;">3</div>
    <div style="font-size:14.5px; font-weight:800; color:#0B2A1A;">Promosi & Bundling Fokus pada 5 Kategori Dominan</div>
</div>
<div style="font-size:13px; color:#34503C; line-height:1.5;">
Alokasikan anggaran kampanye pada 5 kategori penyumbang {top5_rev_pct:.1f}% revenue (Health & Beauty, Watches Gifts, Bed Bath Table, Sports Leisure, Computers Accessories) untuk meningkatkan Average Order Value.
</div>
</div>""", unsafe_allow_html=True)

    with ca2:
        with st.container(border=True):
            st.markdown(f"""<div>
<div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
    <div style="background:#2ECC71; color:#0B2A1A; font-weight:800; font-size:12px; width:24px; height:24px; border-radius:50%; display:flex; align-items:center; justify-content:center;">2</div>
    <div style="font-size:14.5px; font-weight:800; color:#0B2A1A;">Sistem Peringatan Dini & Voucher Proaktif Keterlambatan</div>
</div>
<div style="font-size:13px; color:#34503C; line-height:1.5;">
Kirimkan kompensasi otomatis pada H+1 keterlambatan estimasi guna mencegah review score anjlok ke {late_review_val:.2f} dan ulasan negatif melonjak hingga {late_neg_pct:.1f}%.
</div>
</div>""", unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown(f"""<div>
<div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
    <div style="background:#2ECC71; color:#0B2A1A; font-weight:800; font-size:12px; width:24px; height:24px; border-radius:50%; display:flex; align-items:center; justify-content:center;">4</div>
    <div style="font-size:14.5px; font-weight:800; color:#0B2A1A;">Program Reaktivasi Segmen Berisiko Hilang (RFM)</div>
</div>
<div style="font-size:13px; color:#34503C; line-height:1.5;">
Luncurkan email marketing personal dan insentif pembelian kedua bagi {at_risk_count:,} pelanggan Berisiko Hilang - Nilai Tinggi guna menaikkan rasio repeat buyer dari {repeat_buyers_pct:.1f}%.
</div>
</div>""", unsafe_allow_html=True)

# Spasi Penutup di Akhir Halaman
st.markdown("<div style='height: 30px; margin-bottom: 30px;'></div>", unsafe_allow_html=True)
