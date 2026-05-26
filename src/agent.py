import streamlit as st
import google.generativeai as genai

# إعداد الربط مع Gemini
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error("خطأ في إعدادات API. تأكد من ضبط الـ Secrets.")

def run_assistant():
    st.subheader("🤖 مساعد MEDMEC الذكي")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # سياق الشركة (هذا يوجه Gemini للرد بناءً على معلوماتك)
    system_context = """
    أنت المساعد الذكي لشركة MEDMEC Digital Solutions.
    - مهمتك: مساعدة العملاء والإجابة على استفساراتهم باحترافية.
    - معلومات الشركة:
        1. الاسم: MEDMEC Digital Solutions.
        2. الخدمات والأسعار: 
           - Data Cleanse Pro: 8000 دج.
           - CRM Automation: 9000 دج.
           - الاستشارات التقنية: 2000 دج للساعة.
    - القواعد: أجب باحترافية، وإذا سُئلت عن شيء غير متعلق بخدماتنا، اعتذر بلطف.
    """

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("اسألني عن فوائد أتمتة البيانات أو خدماتنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # دمج السياق مع سؤال المستخدم
        full_query = f"{system_context} \n سؤال المستخدم: {prompt}"
        
        try:
            response = model.generate_content(full_query)
            answer = response.text
        except Exception:
            answer = "عذراً، أواجه مشكلة في الاتصال بالذكاء الاصطناعي حالياً."
        
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})