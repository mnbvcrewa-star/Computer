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

# --- 🎨 ปรับแต่ง CSS ให้ดู Premium และอ่านง่ายขึ้น ---
st.markdown("""
    <style>
    /* พื้นหลังหน้าเว็บ */
    .main { background-color: #f0f2f6; }
    
    /* ปรับแต่ง Metric Cards ให้เด่นชัด */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        border-left: 5px solid #007bff; /* เพิ่มแถบสีด้านข้าง */
    }
    
    /* ขยายขนาดตัวเลขใน Metric */
    div[data-testid="stMetricValue"] > div {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #1f77b4 !important;
    }
    
    /* ปรับแต่งหัวข้อ */
    h1, h2, h3 { color: #1e3d59; font-weight: 800; }
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

    st.sidebar.title("🔍 ตัวกรองข้อมูล")
    selected_lab = st.sidebar.multiselect(
        "เลือกห้องปฏิบัติการ:",
        options=df_all['ห้องปฏิบัติการ'].unique(),
        default=df_all['ห้องปฏิบัติการ'].unique()
    )

    df = df_all[df_all['ห้องปฏิบัติการ'].isin(selected_lab)]

    if not df.empty:
        # --- ส่วนที่ 1: Metrics ---
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.metric("👥 ผู้เข้าใช้ทั้งหมด", f"{len(df)} คน")
        with col_m2:
            st.metric("🏫 ห้องที่เลือก", f"{len(selected_lab)} ห้อง")
        with col_m3:
            full_name = df['ห้องปฏิบัติการ'].mode()[0] if not df.empty else "N/A"
            short_name = full_name.replace("ห้องปฏิบัติการคอมพิวเตอร์ ", "ห้อง ")
            st.metric("🏆 ห้องยอดนิยม", short_name)
        with col_m4:
            st.metric("📡 สถานะระบบ", "Online 🟢")

        st.markdown("##")

        # --- ส่วนที่ 2: กราฟขนาดใหญ่ขึ้น ---
        st.subheader("🏢 เปรียบเทียบการใช้งานรายห้อง")
        lab_summary = df.groupby('ห้องปฏิบัติการ').size().reset_index(name='จำนวนคน')
        # ใช้สีแบบ Vivid เพื่อความชัดเจน
        fig_lab = px.bar(lab_summary, x='ห้องปฏิบัติการ', y='จำนวนคน', color='ห้องปฏิบัติการ',
                         text_auto='.0f', color_discrete_sequence=px.colors.qualitative.Vivid)
        
        fig_lab.update_traces(textfont_size=20, textposition="outside", cliponaxis=False) # ขยายตัวเลขบนแท่งกราฟ
        fig_lab.update_layout(height=500, font=dict(size=14)) # เพิ่มความสูงกราฟ
        st.plotly_chart(fig_lab, use_container_width=True)

        col_chart1, col_chart2 = st.columns([2, 1])
        if 'ชั้นปี' in df.columns:
            with col_chart1:
                st.subheader("📊 แยกตามระดับชั้น")
                summary = df.groupby(['ชั้นปี', 'ห้องปฏิบัติการ']).size().reset_index(name='จำนวนคน')
                fig_bar = px.bar(summary, x='ชั้นปี', y='จำนวนคน', color='ห้องปฏิบัติการ', 
                                 barmode='group', text_auto=True,
                                 color_discrete_sequence=px.colors.qualitative.Bold)
                fig_bar.update_layout(height=450)
                st.plotly_chart(fig_bar, use_container_width=True)

            with col_chart2:
                st.subheader("🎯 สัดส่วนรวม")
                summary_grade = df['ชั้นปี'].value_counts().reset_index()
                summary_grade.columns = ['ชั้นปี', 'จำนวนคน']
                fig_pie = px.pie(summary_grade, values='จำนวนคน', names='ชั้นปี', hole=0.5,
                                 color_discrete_sequence=px.colors.qualitative.Safe)
                fig_pie.update_traces(textinfo='percent+label', textfont_size=16)
                st.plotly_chart(fig_pie, use_container_width=True)

    # --- ส่วนที่ 3: ตารางแบบ Highlight ข้อมูล ---
    st.markdown("---")
    with st.expander("🔍 ดูรายละเอียดข้อมูลดิบ (Highlight ค่าสูงสุด)", expanded=True):
        # ทำ Highlight สีเหลืองในคอลัมน์ที่เป็นตัวเลขเพื่อความเด่นชัด
        st.dataframe(df.style.highlight_max(axis=0, subset=['เลขเครื่องที่นั่ง'], color='#ffffb3'), use_container_width=True)

except Exception as e:
    st.error(f"⚠️ เกิดข้อผิดพลาด: {e}")

# Sidebar Bottom
st.sidebar.markdown("---")
if st.sidebar.button("🏠 กลับสู่หน้าหลัก"):
    nav_link = "https://mnbvcrewa-star.github.io/Computer/"
    st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{nav_link}\'">', unsafe_allow_html=True)
