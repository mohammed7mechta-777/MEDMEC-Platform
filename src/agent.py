import streamlit as st
import google.generativeai as genai

def run_assistant():
    st.subheader("🤖 مساعد MEDMEC الذكي")

    # 1. فحص وجود المفتاح في الـ Secrets
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("لم يتم العثور على GOOGLE_API_KEY في إعدادات الـ Secrets. يرجى إضافته في صفحة إعدادات Streamlit.")
        return

    # 2. إعداد الاتصال
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"خطأ في إعداد الاتصال بـ Gemini: {e}")
        return

    # 3. إدارة المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 4. المعالجة
    if prompt := st.chat_input("اسألني عن خدماتنا أو فوائد الأتمتة..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        system_context = """أنت مساعد ذكي لشركة MEDMEC Digital Solutions. 
        الخدمات: Data Cleanse Pro (8000 دج)، CRM Automation (9000 دج)، الاستشارات التقنية (2000 دج للساعة).
        أجب باحترافية واختصار."""
        
        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير..."):
                try:
                    response = model.generate_content(system_context + prompt)
                    answer = response.text
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error("تعذر الحصول على رد من الذكاء الاصطناعي.")
                    st.write(f"التفاصيل: {e}")