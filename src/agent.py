import streamlit as st
import google.generativeai as genai

def run_assistant():
    st.subheader("🤖 مساعد MEDMEC الذكي")

    # 1. التأكد من إعداد المفتاح في الـ Secrets
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("ملاحظة للمطور: يرجى إضافة GOOGLE_API_KEY في إعدادات الـ Secrets.")
        return

    # 2. إعداد الاتصال بالنموذج المحدث
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        # استخدام النسخة الأحدث والأسرع من Gemini
        model = genai.GenerativeModel('gemini-1.5-flash') 
    except Exception as e:
        st.error(f"خطأ في إعداد الاتصال: {e}")
        return

    # 3. إدارة حالة المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 4. معالجة طلب المستخدم
    if prompt := st.chat_input("اسألني عن خدماتنا أو فوائد الأتمتة..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # سياق الشركة (System Prompt)
        system_context = """
        أنت المساعد الذكي لشركة MEDMEC Digital Solutions.
        - خدماتنا: 
            - Data Cleanse Pro: 8000 دج.
            - CRM Automation: 9000 دج.
            - الاستشارات التقنية: 2000 دج للساعة.
        - القواعد: أجب باحترافية، وبشكل مختصر، وباللغة التي يسأل بها المستخدم.
        """
        
        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير..."):
                try:
                    # الدمج بين السياق وسؤال المستخدم
                    full_prompt = f"{system_context}\nسؤال المستخدم: {prompt}"
                    response = model.generate_content(full_prompt)
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error("تعذر الحصول على رد. يرجى التحقق من اتصال الـ API.")