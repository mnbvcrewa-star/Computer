import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Lab Usage Analytics", layout="wide", initial_sidebar_state="expanded")

# --- 🟢 วางฟังก์ชันโหลดข้อมูลไว้ตรงนี้ (ก่อน try:) ---
@st.cache_data(ttl=10) # ตั้งค่าให้โหลดใหม่ทุก 10 วินาที
def load_data(url):
    return pd.read_csv(url)

# ใช้ CSS แต่งหน้าเว็บ
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 ระบบวิเคราะห์สถิติห้องปฏิบัติการคอมพิวเตอร์")
st.markdown("---")

# ลิงก์ข้อมูล
urls = [
    "https://docs.google.com/spreadsheets/d/e/...URL1.../pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/...URL2.../pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/...URL3.../pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/...URL4.../pub?output=csv"
]

try:
    # --- 🟡 เปลี่ยนการโหลดข้อมูลมาใช้ฟังก์ชัน load_data ---
    # เดิม: all_dfs = [pd.read_csv(url) for url in urls]
    all_dfs = [load_data(url) for url in urls] # เรียกใช้ผ่านฟังก์ชันที่ตั้ง ttl ไว้
    df = pd.concat(all_dfs, ignore_index=True)

    # ... (โค้ดส่วน Metrics และ กราฟ ของคุณเหมือนเดิมทั้งหมด) ...

    # --- ส่วนที่ 3: ตารางข้อมูลดิบ ---
    with st.expander("🔍 ดูรายละเอียดข้อมูลดิบทั้งหมด"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")

# --- ส่วนของ Sidebar (อยู่นอก try) ---
if st.sidebar.button("🏠 กลับสู่หน้าหลัก"):
    st.markdown('<meta http-equiv="refresh" content="0;URL=\'index.html\'">', unsafe_allow_html=True)

st.sidebar.markdown("---")