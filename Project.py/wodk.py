import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Lab Usage Analytics", layout="wide", initial_sidebar_state="expanded")

# --- 🟢 ฟังก์ชันโหลดข้อมูลอัปเดตอัตโนมัติทุก 10 วินาที ---
@st.cache_data(ttl=10) 
def load_data(url):
    return pd.read_csv(url)

# ใช้ CSS แต่งหน้าเว็บ
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 ระบบวิเคราะห์สถิติห้องปฏิบัติการคอมพิวเตอร์")
st.markdown("---")

# ลิงก์ข้อมูล
urls = [
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-Kj4rvZmMJz3J17Slush5gfgy-qEE6qAZLdlb3WOUdyefiRdJ--MPa1Keg7IYQtuOAjbUizDQsYVB/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ24_wvhcv00Ul2BAYu-ReWYYiHEh2rieecrKc9G_WkHy5Hn2Wm_7kNYKZdwmDF-P6p59KGSeP6FCBm/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQwFgt7eU2NVyiy2Xm6gxcTqGIXu_Vtl7RZXMkPdtzVKeNLBmeh603DtL75aHUkDOOYxXadYHwArNwp/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ6sYSZVKbaR9Qixq-lhw4HsMvzRZihL-3dd1XeCz5v5zhYvqfGzVX4vZTe7XWF2F8pXjeROFtjlfhH/pub?output=csv"
]

try:
    all_dfs = [load_data(url) for url in urls]
    df = pd.concat(all_dfs, ignore_index=True)

    if not df.empty:
        # --- ส่วนที่ 1: สรุปตัวเลขสำคัญ ---
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("ผู้เข้าใช้ทั้งหมด", f"{len(df)} คน")
        with col_m2:
            top_grade = df['ชั้นปี'].mode()[0] if 'ชั้นปี' in df.columns else "N/A"
            st.metric("กลุ่มที่เข้าใช้หลัก", top_grade)
        with col_m3:
            grade_count = df['ชั้นปี'].nunique() if 'ชั้นปี' in df.columns else 0
            st.metric("ความหลากหลายระดับชั้น", f"{grade_count} กลุ่ม")
        with col_m4:
            st.metric("สถานะระบบ", "Online 🟢")

        st.markdown("##")

        # --- ส่วนที่ 2: กราฟสถิติ (จุดที่ปรับปรุงเรื่องสี) ---
        col_chart1, col_chart2 = st.columns([2, 1])

        if 'ชั้นปี' in df.columns:
            summary = df['ชั้นปี'].value_counts().reset_index()
            summary.columns = ['ชั้นปี', 'จำนวนคน']
            
            with col_chart1:
                st.subheader("📊 จำนวนผู้เข้าใช้งานแยกตามระดับชั้น")
                # ใช้สีแบบ color_discrete_sequence (ชุดสีแบบกระจาย) เพื่อให้แต่ละแท่งสีต่างกันชัดเจน
                fig_bar = px.bar(summary, 
                                 x='ชั้นปี', 
                                 y='จำนวนคน', 
                                 color='ชั้นปี', 
                                 text_auto='.0f',
                                 color_discrete_sequence=px.colors.qualitative.Safe) # ใช้โทนสีที่อ่านง่าย
                
                fig_bar.update_layout(showlegend=False, xaxis_title="ระดับชั้น", yaxis_title="จำนวนคน")
                st.plotly_chart(fig_bar, use_container_width=True)

            with col_chart2:
                st.subheader("🎯 สัดส่วนการเข้าใช้")
                fig_pie = px.pie(summary, values='จำนวนคน', names='ชั้นปี', 
                                 hole=0.4, 
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_pie.update_traces(textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)

        # --- กราฟเส้นรายวัน ---
        if 'วัน' in df.columns:
            st.markdown("---")
            st.subheader("📅 แนวโน้มการเข้าใช้งานรายวัน")
            daily = df['วัน'].value_counts().reset_index()
            daily.columns = ['วันที่', 'จำนวนคน']
            daily = daily.sort_values('วันที่')
            
            fig_line = px.line(daily, x='วันที่', y='จำนวนคน', markers=True, 
                               line_shape="spline", # ปรับเส้นให้โค้งมนดูนุ่มนวล
                               color_discrete_sequence=['#FF4B4B']) 
            st.plotly_chart(fig_line, use_container_width=True)

    with st.expander("🔍 ดูรายละเอียดข้อมูลดิบทั้งหมด"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ เกิดข้อผิดพลาด: {e}")

# Sidebar
st.sidebar.title("เมนูควบคุม")
if st.sidebar.button("🏠 กลับสู่หน้าหลัก"):
    st.markdown('<meta http-equiv="refresh" content="0;URL=\'index.html\'">', unsafe_allow_html=True)
