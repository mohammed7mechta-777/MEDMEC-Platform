import streamlit as st
import requests
import subprocess

# إعداد الصفحة
st.set_page_config(page_title="MEDMEC Platform", page_icon="🤖", layout="wide")

# دالة الاتصال بـ Ollama
def get_ai_response(prompt):
    payload = {
        "model": "qwen2.5:1.5b",
        "prompt": f"أنت مساعد MEDMEC. الأسعار: Data Cleanse Pro بـ 8000 دج، CRM Automation بـ 9000 دج. المستخدم يسأل: {prompt}",
        "stream": False
    }
    try:
        # الاتصال بالسيرفر المحلي
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=10)
        return response.json().get("response", "لم أتلقَ رداً.")
    except Exception as e:
        return f"خطأ: تأكد أن Ollama يعمل. التفاصيل: {str(e)}"

# واجهة الترحيب
if "welcome_complete" not in st.session_state:
    st.session_state.welcome_complete = False
if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.welcome_complete:
    st.title("🚀 أهلاً بك في منصة MEDMEC")
    st.markdown("منصة ذكية تعمل محلياً لأتمتة أعمالك بخصوصية تامة.")
    if st.button("اضغط هنا للبدء"):
        st.session_state.welcome_complete = True
        st.rerun()
else:
    # القائمة الجانبية
    with st.sidebar:
        st.header("🛠 خدماتنا")
        if st.button("الأسعار والخدمات"):
            st.session_state.messages.append({"role": "user", "content": "ما هي خدماتكم وأسعارها؟"})
    
    # عرض المحادثة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # مدخل المستخدم
    if prompt := st.chat_input("اكتب سؤالك هنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("جاري المعالجة..."):
                answer = get_ai_response(prompt)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})