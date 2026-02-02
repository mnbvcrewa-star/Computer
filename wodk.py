import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ตั้งค่าหน้าเว็บให้ดูทันสมัย
st.set_page_config(page_title="Lab Usage Analytics", layout="wide", initial_sidebar_state="expanded")

# ใช้ CSS เพื่อปรับแต่งตัวอักษรและสีพื้นหลังเล็กน้อย
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 ระบบวิเคราะห์สถิติห้องปฏิบัติการคอมพิวเตอร์")
st.markdown("---")

# ลิงก์ข้อมูล (ใช้ตัวเดิมของคุณ)
urls = [
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vT-Kj4rvZmMJz3J17Slush5gfgy-qEE6qAZLdlb3WOUdyefiRdJ--MPa1Keg7IYQtuOAjbUizDQsYVB/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ24_wvhcv00Ul2BAYu-ReWYYiHEh2rieecrKc9G_WkHy5Hn2Wm_7kNYKZdwmDF-P6p59KGSeP6FCBm/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQwFgt7eU2NVyiy2Xm6gxcTqGIXu_Vtl7RZXMkPdtzVKeNLBmeh603DtL75aHUkDOOYxXadYHwArNwp/pub?output=csv",
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ6sYSZVKbaR9Qixq-lhw4HsMvzRZihL-3dd1XeCz5v5zhYvqfGzVX4vZTe7XWF2F8pXjeROFtjlfhH/pub?output=csv"
]

try:
    # โหลดและรวมข้อมูล
    all_dfs = [pd.read_csv(url) for url in urls]
    df = pd.concat(all_dfs, ignore_index=True)

    # --- ส่วนที่ 1: สรุปตัวเลขสำคัญ (Metrics Cards) ---
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.metric("ผู้เข้าใช้ทั้งหมด", f"{len(df)} คน", "📈")
    with col_m2:
        top_grade = df['ชั้นปี'].mode()[0]
        st.metric("กลุ่มที่เข้าใช้หลัก", top_grade)
    with col_m3:
        # สมมติว่ามีคอลัมน์ 'สาขา' หรือใช้ 'ชั้นปี' นับความหลากหลาย
        grade_count = df['ชั้นปี'].nunique()
        st.metric("ความหลากหลายระดับชั้น", f"{grade_count} กลุ่ม")
    with col_m4:
        st.metric("สถานะระบบ", "Online", delta_color="normal")

    st.markdown("##") # เพิ่มช่องว่าง

    # --- ส่วนที่ 2: กราฟสถิติแบบสองคอลัมน์ ---
    col_chart1, col_chart2 = st.columns([2, 1])

    with col_chart1:
        st.subheader("📊 จำนวนผู้เข้าใช้งานแยกตามระดับชั้น")
        summary = df['ชั้นปี'].value_counts().reset_index()
        summary.columns = ['ชั้นปี', 'จำนวนคน']
        
        # แก้ไขบรรทัดด้านล่างนี้ ตรง y='จำนวนคน' (เดิมอาจจะเป็น 'จำนวน人')
        fig_bar = px.bar(summary, 
                 x='ชั้นปี', 
                 y='จำนวนคน',  # ตรวจสอบให้แน่ใจว่าพิมพ์ 'จำนวนคน' เป๊ะๆ
                 color='จำนวนคน', 
                 color_continuous_scale='Blues',
                 text_auto=True)
        fig_bar.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

    # ... (โค้ดส่วนบนถึงจบกราฟวงกลม col_chart2) ...

    with col_chart2:
        st.subheader("🎯 สัดส่วนการเข้าใช้")
        fig_pie = px.pie(summary, values='จำนวนคน', names='ชั้นปี', 
                         hole=0.4, 
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- วางตรงนี้ครับ (ส่วนที่ 2.5) ---
    st.markdown("---")
    st.subheader("📅 สถิติการเข้าใช้งานแยกตามวัน")
    
    # 1. จัดกลุ่มข้อมูลตามคอลัมน์ 'วัน' และนับจำนวน
    # หมายเหตุ: ใน Google Sheets ของคุณต้องมีหัวตารางที่ชื่อว่า 'วัน' เป๊ะๆ นะครับ
    daily_summary = df['วัน'].value_counts().reset_index()
    daily_summary.columns = ['วันที่', 'จำนวนคน']
    
    # 2. เรียงลำดับวันที่
    daily_summary = daily_summary.sort_values('วันที่')

    # 3. สร้างกราฟเส้น
    fig_daily = px.line(daily_summary, x='วันที่', y='จำนวนคน', 
                        title='แนวโน้มการเข้าใช้งานรายวัน',
                        markers=True,
                        line_shape='spline',
                        color_discrete_sequence=['#ff7f0e'])
    
    st.plotly_chart(fig_daily, use_container_width=True)


    # --- ส่วนที่ 3: ตารางข้อมูลดิบ (ของเดิมจะอยู่ต่อท้ายตรงนี้) ---
    with st.expander("🔍 ดูรายละเอียดข้อมูลดิบทั้งหมด"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")

    # เพิ่มปุ่มย้อนกลับที่ Sidebar หรือส่วนบนของหน้า
if st.sidebar.button("🏠 กลับสู่หน้าหลัก"):
    # ใช้ JavaScript เล็กน้อยเพื่อสั่งให้ Browser เปลี่ยน URL กลับไปหน้า HTML
    # เปลี่ยน 'index.html' เป็นชื่อไฟล์หน้าหลักของคุณ
    st.markdown('<meta http-equiv="refresh" content="0;URL=\'index.html\'">', unsafe_allow_html=True)

# หรือจะใช้เป็นลิงก์สวยๆ ใน Sidebar ก็ได้
st.sidebar.markdown("---")
