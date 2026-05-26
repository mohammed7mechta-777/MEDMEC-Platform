import streamlit as st
import pandas as pd
import sys
import os

# هذا السطر يخبر بايثون أن يبحث عن الملفات في المجلد الحالي
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cleaner import clean_data
from agent import run_assistant

st.set_page_config(page_title="MEDMEC Platform", page_icon="💼", layout="wide")

with st.sidebar:
    run_assistant()

st.title("🧹 Data Cleanse Pro")
st.write("أداة تنظيف البيانات الاحترافية لشركة MEDMEC")

uploaded_file = st.file_uploader("ارفع ملف CSV هنا", type=['csv'])

if uploaded_file:
    if st.button("ابدأ التنظيف الآن"):
        with st.spinner("جاري معالجة البيانات..."):
            cleaned_df = clean_data(uploaded_file)
            if cleaned_df is not None:
                st.success("تم التنظيف بنجاح!")
                st.dataframe(cleaned_df.head())
                csv = cleaned_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 تحميل الملف النظيف", csv, "cleaned_data.csv", "text/csv")
            else:
                st.error("حدث خطأ في معالجة الملف.")