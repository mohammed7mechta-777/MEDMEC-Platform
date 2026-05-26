import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# تحميل المفتاح من ملف .env
load_dotenv()
client = Groq(api_key=os.getenv("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"))

# إعدادات الواجهة
st.set_page_config(page_title="MEDMEC Platform", page_icon="🤖", layout="wide")

# تعريف شخصية المساعد والخدمات
SYSTEM_PROMPT = """
أنت مساعد شركة MEDMEC الذكي. 
قائمة خدماتنا وأسعارنا:
1. خدمة تنظيف البيانات (Data Cleanse Pro): 8000 دج.
2. خدمة أتمتة علاقات العملاء (CRM Automation): 9000 دج.
يجب أن تكون إجاباتك مهنية، مختصرة، وودودة.
"""

def get_ai_response(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"عذراً، حدث خطأ في الاتصال: {str(e)}"

# منطق واجهة الترحيب
if "welcome" not in st.session_state: st.session_state.welcome = False
if "messages" not in st.session_state: st.session_state.messages = []

if not st.session_state.welcome:
    st.title("🤖 أهلاً بك في منصة MEDMEC")
    st.subheader("الحل الأمثل لأتمتة أعمالك بذكاء")
    if st.button("اضغط هنا للبدء"):
        st.session_state.welcome = True
        st.rerun()
else:
    # القائمة الجانبية
    with st.sidebar:
        st.header("🛠 القائمة")
        if st.button("الأسعار والخدمات"):
            st.session_state.messages.append({"role": "user", "content": "ما هي خدماتكم وأسعارها؟"})
        if st.button("مسح المحادثة"):
            st.session_state.messages = []
            st.rerun()

    # عرض سجل المحادثة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # مدخل المستخدم
    if prompt := st.chat_input("تفضل بطرح سؤالك..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("جاري المعالجة..."):
                answer = get_ai_response(prompt)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})