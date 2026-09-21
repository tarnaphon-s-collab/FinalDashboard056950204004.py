import streamlit as st
import pandas as pd

st.title("ระบบคำนวณและเพิ่มเกรดนักเรียน")

try:
    df = pd.read_csv("student.csv")
    
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

    score_col = 'Score' if 'Score' in df.columns else 'Grade'
    df['Student_Grade'] = df[score_col].apply(calculate_grade)

    st.success("คำนวณเกรดเรียบร้อยแล้ว!")
    st.dataframe(df)

except FileNotFoundError:
    st.error("ไม่พบไฟล์ student.csv กรุณาเพิ่มไฟล์ student.csv เข้ามาใน Repository นี้ก่อน")
  
