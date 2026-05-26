import streamlit as st
import google.generativeai as genai

def run_assistant():
    st.subheader("🤖 مساعد MEDMEC الذكي")

    # تشخيص حالة الـ Secrets
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("خطأ: لم يتم العثور على GOOGLE_API_KEY في الـ Secrets!")
        return
    
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("اسألني عن خدماتنا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                # محاولة الاتصال
                response = model.generate_content(f"أنت مساعد شركة MEDMEC. أجب على: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
    except Exception as e:
        st.error(f"خطأ تقني في API: {str(e)}")