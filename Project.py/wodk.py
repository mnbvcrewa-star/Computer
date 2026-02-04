import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Lab Usage Analytics", layout="wide", initial_sidebar_state="expanded")

# --- 🟢 ส่วนฟังก์ชันต่างๆ (วางไว้ด้านบนเพื่อให้เรียกใช้ง่าย) ---
@st.cache_data(ttl=10) 
def load_data(url):
    return pd.read_csv(url)

# ฟังก์ชันสำหรับสร้างกราฟในแต่ละ Tab
def display_lab_stats(df_lab, lab_name):
    if not df_lab.empty:
        col1, col2 = st.columns([2, 1])
        summary = df_lab['ชั้นปี'].value_counts().reset_index()
        summary.columns = ['ชั้นปี', 'จำนวนคน']
        
        with col1:
            st.write(f"**จำนวนผู้ใช้ {lab_name}:** {len(df_lab)} คน")
            fig = px.bar(summary, x='ชั้นปี', y='จำนวนคน', color='ชั้นปี', 
                         title=f"สถิติ {lab_name}", text_auto=True)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.write("**สัดส่วนชั้นปี**")
            fig_pie = px.pie(summary, values='จำนวนคน', names='ชั้นปี', hole=0.3)
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning(f"ยังไม่มีข้อมูลการเข้าใช้ใน {lab_name}")

# ใช้ CSS แต่งหน้าเว็บ
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 ระบบวิเคราะห์สถิติห้องปฏิบัติการคอมพิวเตอร์")
st.markdown("---")

# ลิงก์ข้อมูลจริงของคุณ
urls = [
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-Kj4rvZmMJz3J17Slush5gfgy-qEE6qAZLdlb3WOUdyefiRdJ--MPa1Keg7IYQtuOAjbUizDQsYVB/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ24_wvhcv00Ul2BAYu-ReWYYiHEh2rieecrKc9G_WkHy5Hn2Wm_7kNYKZdwmDF-P6p59KGSeP6FCBm/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQwFgt7eU2NVyiy2Xm6gxcTqGIXu_Vtl7RZXMkPdtzVKeNLBmeh603DtL75aHUkDOOYxXadYHwArNwp/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ6sYSZVKbaR9Qixq-lhw4HsMvzRZihL-3dd1XeCz5v5zhYvqfGzVX4vZTe7XWF2F8pXjeROFtjlfhH/pub?output=csv"
]

try:
    # โหลดและรวมข้อมูล
    all_dfs = [load_data(url) for url in urls]
    df = pd.concat(all_dfs, ignore_index=True)

    if not df.empty:
        # --- ส่วนที่ 1: Metrics ---
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("ผู้เข้าใช้ทั้งหมด", f"{len(df)} คน", "📈")
        with col_m2:
            top_grade = df['ชั้นปี'].mode()[0] if 'ชั้นปี' in df.columns else "N/A"
            st.metric("กลุ่มที่เข้าใช้หลัก", top_grade)
        with col_m3:
            grade_count = df['ชั้นปี'].nunique() if 'ชั้นปี' in df.columns else 0
            st.metric("ความหลากหลายระดับชั้น", f"{grade_count} กลุ่ม")
        with col_m4:
            st.metric("สถานะระบบ", "Online")

        st.markdown("##")

        # --- ส่วนที่ 2: แยกวิเคราะห์รายห้อง (วางตรงนี้เพื่อให้เด่น) ---
        st.markdown("---")
        st.subheader("🖥️ แยกวิเคราะห์รายห้องปฏิบัติการ")

        tab1, tab2, tab3, tab4, tab_all = st.tabs(["คอม 1", "คอม 2", "คอม 3", "คอม 4", "📊 ภาพรวมทุกห้อง"])

        with tab1:
            display_lab_stats(all_dfs[0], "คอมพิวเตอร์ 1")
        with tab2:
            display_lab_stats(all_dfs[1], "คอมพิวเตอร์ 2")
        with tab3:
            display_lab_stats(all_dfs[2], "คอมพิวเตอร์ 3")
        with tab4:
            display_lab_stats(all_dfs[3], "คอมพิวเตอร์ 4")
        with tab_all:
            # ดึงกราฟรวมเดิมมาใส่ใน Tab นี้
            col_total1, col_total2 = st.columns([2, 1])
            summary_total = df['ชั้นปี'].value_counts().reset_index()
            summary_total.columns = ['ชั้นปี', 'จำนวนคน']
            
            with col_total1:
                st.write(f"**จำนวนผู้ใช้รวมทั้งหมด:** {len(df)} คน")
                fig_total_bar = px.bar(summary_total, x='ชั้นปี', y='จำนวนคน', color='จำนวนคน', 
                                      color_continuous_scale='Blues', text_auto=True)
                st.plotly_chart(fig_total_bar, use_container_width=True)
            with col_total2:
                st.write("**สัดส่วนรวม**")
                fig_total_pie = px.pie(summary_total, values='จำนวนคน', names='ชั้นปี', hole=0.4)
                st.plotly_chart(fig_total_pie, use_container_width=True)

        # --- กราฟเส้นรายวัน (วางใต้ Tabs) ---
        if 'วัน' in df.columns:
            st.markdown("---")
            st.subheader("📅 แนวโน้มการเข้าใช้งานรายวัน (รวมทุกห้อง)")
            daily = df['วัน'].value_counts().reset_index()
            daily.columns = ['วันที่', 'จำนวนคน']
            daily = daily.sort_values('วันที่')
            fig_line = px.line(daily, x='วันที่', y='จำนวนคน', markers=True)
            st.plotly_chart(fig_line, use_container_width=True)

    # --- ส่วนที่ 3: ตารางข้อมูลดิบ ---
    st.markdown("---")
    with st.expander("🔍 ดูรายละเอียดข้อมูลดิบทั้งหมด"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ เกิดข้อผิดพลาด: {e}")

# Sidebar
if st.sidebar.button("🏠 กลับสู่หน้าหลัก"):
    st.markdown('<meta http-equiv="refresh" content="0;URL=\'index.html\'">', unsafe_allow_html=True)
