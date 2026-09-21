import streamlit as st
import pandas as pd
import plotly.express as px

# ตั้งค่าหน้าเว็บให้เป็นแบบกว้าง (Wide layout)
st.set_page_config(page_title="แดชบอร์ดนำเสนอข้อมูลเกรดนักศึกษา", layout="wide")

# 1. ฟังก์ชันโหลด/จัดการข้อมูล
def load_and_process_data():
    try:
        df = pd.read_csv("student.csv")
    except FileNotFoundError:
        # สร้างข้อมูลตัวอย่างหากไม่พบไฟล์ student.csv
        data = {
            "StudentID": [65001, 65002, 65003, 65004, 65005],
            "Name": ["สมชาย ใจดี", "สมหญิง รักเรียน", "มานะ ขยัน", "มานี มีใจ", "วิชัย เรียนดี"],
            "Score": [85, 82, 68, 59, 45]
        }
        df = pd.DataFrame(data)

    # ฟังก์ชันคำนวณเกรดตามเงื่อนไข
    def calculate_grade(score):
        if score >= 80:
            return 'A'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'C+'
        elif score >= 60:
            return 'C'
        elif score >= 55:
            return 'D+'
        elif score >= 50:
            return 'D'
        else:
            return 'F'

    # ค้นหาคอลัมน์คะแนน (รองรับทั้ง Score และ Grade)
    score_col = 'Score' if 'Score' in df.columns else ('Grade' if 'Grade' in df.columns else df.columns[2])
    
    # เพิ่มคอลัมน์ Student_Grade และบันทึกไฟล์
    df['Student_Grade'] = df[score_col].apply(calculate_grade)
    df.to_csv("student.csv", index=False)
    
    return df, score_col

df, score_col = load_and_process_data()

# --- ส่วนหัวแดชบอร์ด ---
st.title("🎓 แดชบอร์ดนำเสนอข้อมูลเกรดนักศึกษา")
st.caption("ประมวลผลจาก student.csv คำนวณเกรด และแสดงผลข้อมูลรวมของชั้นเรียนโดยอัตโนมัติ")

st.markdown("---")

# --- 2. การ์ดตัวเลขสรุป (Metrics) ---
col1, col2, col3, col4, col5 = st.columns(5)

total_students = len(df)
avg_score = df[score_col].mean()
max_score = df[score_col].max()
min_score = df[score_col].min()
passed_students = len(df[df['Student_Grade'] != 'F'])
pass_rate = (passed_students / total_students) * 100 if total_students > 0 else 0

col1.metric("จำนวนนักเรียน", f"{total_students} คน")
col2.metric("คะแนนเฉลี่ย", f"{avg_score:.2f}")
col3.metric("คะแนนสูงสุด", f"{max_score}")
col4.metric("คะแนนต่ำสุด", f"{min_score}")
col5.metric("อัตราการสอบผ่าน", f"{pass_rate:.2f}%")

st.markdown("---")

# --- 3. รายงานผลการเรียน (ตารางข้อมูล) ---
st.subheader("📋 รายงานผลการเรียน")
st.dataframe(df, use_container_width=True)

st.markdown("---")

# --- 4. กราฟแสดงผล (Bar Chart & Pie/Donut Chart) ---
col_chart1, col_chart2 = st.columns(2)

# สรุปจำนวนผู้เรียนแยกตามเกรด
grade_counts = df['Student_Grade'].value_counts().reset_index()
grade_counts.columns = ['Student_Grade', 'Count']

# ลำดับเกรดมาตรฐาน
grade_order = ['A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F']
grade_counts['Student_Grade'] = pd.Categorical(grade_counts['Student_Grade'], categories=grade_order, ordered=True)
grade_counts = grade_counts.sort_values('Student_Grade')

with col_chart1:
    st.subheader("📊 จำนวนผู้เรียนตามเกรด")
    fig_bar = px.bar(
        grade_counts, 
        x='Student_Grade', 
        y='Count',
        labels={'Student_Grade': 'เกรด', 'Count': 'จำนวน (คน)'},
        color_discrete_sequence=['#2b5c8f']
    )
    fig_bar.update_layout(showlegend=False, yaxis=dict(dtick=1))
    st.plotly_chart(fig_bar, use_container_width=True)

with col_chart2:
    st.subheader("🍩 สัดส่วนผู้เรียนตามเกรด")
    fig_pie = px.pie(
        grade_counts, 
        names='Student_Grade', 
        values='Count',
        hole=0.5,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)
