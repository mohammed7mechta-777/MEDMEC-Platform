import streamlit as st
import pandas as pd
from src.cleaner import clean_data
from src.agent import run_assistant

st.set_page_config(page_title="MEDMEC Platform", page_icon="💼", layout="wide")

# الشريط الجانبي للمساعد الذكي
with st.sidebar:
    run_assistant() 

# المحتوى الرئيسي
st.title("🧹 Data Cleanse Pro")
st.write("أداة تنظيف البيانات الاحترافية لشركة MEDMEC")

uploaded_file = st.file_uploader("ارفع ملف CSV هنا", type=['csv'])

if uploaded_file:
    if st.button("ابدأ التنظيف الآن"):
        with st.spinner("جاري معالجة البيانات..."):
            cleaned_df = clean_data(uploaded_file)
            
            # حماية من الخطأ في حال كانت البيانات فارغة
            if cleaned_df is not None and not cleaned_df.empty:
                st.success("تم التنظيف بنجاح!")
                st.dataframe(cleaned_df.head())
                
                # زر التحميل
                csv = cleaned_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 تحميل الملف النظيف",
                    csv,
                    "cleaned_data.csv",
                    "text/csv"
                )
            else:
                st.error("لم يتم العثور على بيانات صالحة للتنظيف.")