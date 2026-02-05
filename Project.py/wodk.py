import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Lab Usage Analytics", layout="wide", initial_sidebar_state="expanded")

# --- 🟢 ฟังก์ชันโหลดข้อมูล ---
@st.cache_data(ttl=10) 
def load_data(url, lab_name):
    df = pd.read_csv(url)
    df['ห้องปฏิบัติการ'] = lab_name 
    return df

# ใช้ CSS แต่งหน้าเว็บ
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eee; }
    /* เพิ่ม CSS เพื่อบังคับไม่ให้ตัวอักษรใน Metric ขึ้นบรรทัดใหม่แบบแปลกๆ */
    [data-testid="stMetricValue"] { font-size: 1.8rem !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 ระบบวิเคราะห์สถิติแยกรายห้องปฏิบัติการ")
st.markdown("---")

lab_configs = [
    {"name": "ห้องปฏิบัติการคอมพิวเตอร์ 1", "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-Kj4rvZmMJz3J17Slush5gfgy-qEE6qAZLdlb3WOUdyefiRdJ--MPa1Keg7IYQtuOAjbUizDQsYVB/pub?output=csv"},
    {"name": "ห้องปฏิบัติการคอมพิวเตอร์ 2", "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ24_wvhcv00Ul2BAYu-ReWYYiHEh2rieecrKc9G_WkHy5Hn2Wm_7kNYKZdwmDF-P6p59KGSeP6FCBm/pub?output=csv"},
    {"name": "ห้องปฏิบัติการคอมพิวเตอร์ 3", "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQwFgt7eU2NVyiy2Xm6gxcTqGIXu_Vtl7RZXMkPdtzVKeNLBmeh603DtL75aHUkDOOYxXadYHwArNwp/pub?output=csv"},
    {"name": "ห้องปฏิบัติการคอมพิวเตอร์ 4", "url": "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ6sYSZVKbaR9Qixq-lhw4HsMvzRZihL-3dd1XeCz5v5zhYvqfGzVX4vZTe7XWF2F8pXjeROFtjlfhH/pub?output=csv"}
]

    try:
    all_dfs = [load_data(config['url'], config['name']) for config in lab_configs]
    df_all = pd.concat(all_dfs, ignore_index=True)

    df = df_all[df_all['ห้องปฏิบัติการ'].isin(selected_lab)]

    if not df.empty:
        # --- ส่วนที่ 1: Metrics (จุดที่แก้ไขเรื่องชื่อยาว) ---
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("ผู้เข้าใช้ทั้งหมด", f"{len(df)} คน")
        with col_m2:
            st.metric("จำนวนห้องที่เลือก", f"{len(selected_lab)} ห้อง")
        with col_m3:
            # ตัดคำว่า 'ห้องปฏิบัติการคอมพิวเตอร์' ออกให้เหลือแค่ 'ห้อง X' เฉพาะในหน้านี้
            full_name = df['ห้องปฏิบัติการ'].mode()[0] if not df.empty else "N/A"
            short_name = full_name.replace("ห้องปฏิบัติการคอมพิวเตอร์ ", "ห้อง ")
            st.metric("ห้องที่มีผู้ใช้สูงสุด", short_name)
        with col_m4:
            st.metric("สถานะระบบ", "Online 🟢")

        st.markdown("##")

        # --- ส่วนที่ 2: กราฟ (ยังคงใช้ชื่อเต็มเพื่อให้ชัดเจน) ---
        st.subheader("🏢 เปรียบเทียบจำนวนผู้เข้าใช้งานรายห้อง")
        lab_summary = df.groupby('ห้องปฏิบัติการ').size().reset_index(name='จำนวนคน')
        fig_lab = px.bar(lab_summary, x='ห้องปฏิบัติการ', y='จำนวนคน', color='ห้องปฏิบัติการ',
                         text_auto=True, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_lab, use_container_width=True)

        col_chart1, col_chart2 = st.columns([2, 1])
        if 'ชั้นปี' in df.columns:
            with col_chart1:
                st.subheader("📊 จำนวนผู้เข้าใช้แยกตามระดับชั้นและห้อง")
                summary = df.groupby(['ชั้นปี', 'ห้องปฏิบัติการ']).size().reset_index(name='จำนวนคน')
                fig_bar = px.bar(summary, x='ชั้นปี', y='จำนวนคน', color='ห้องปฏิบัติการ', 
                                 barmode='group', text_auto=True)
                st.plotly_chart(fig_bar, use_container_width=True)

            with col_chart2:
                st.subheader("🎯 สัดส่วนระดับชั้นรวม")
                summary_grade = df['ชั้นปี'].value_counts().reset_index()
                summary_grade.columns = ['ชั้นปี', 'จำนวนคน']
                fig_pie = px.pie(summary_grade, values='จำนวนคน', names='ชั้นปี', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)

    with st.expander("🔍 ดูรายละเอียดข้อมูลทั้งหมด"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ เกิดข้อผิดพลาด: {e}")

st.sidebar.markdown("---")
if st.sidebar.button("🏠 กลับสู่หน้าหลัก"):
    st.markdown('<meta http-equiv="refresh" content="https://mnbvcrewa-star.github.io/Computer/">', unsafe_allow_html=True)



