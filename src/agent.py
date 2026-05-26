import streamlit as st

COMPANY_INFO = {
    "name": "م م للحلول الرقمية (MEDMEC)",
    "services": {
        "Data Cleanse Pro": "8000 دج",
        "CRM Automation": "9000 دج",
        "الاستشارة التقنية": "2000 دج للساعة"
    }
}

def run_assistant():
    st.title("🤖 مساعد MEDMEC")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("اسألني عن خدماتنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        p = prompt.lower()
        if any(w in p for w in ["سعر", "أسعار", "خدمات", "بكم"]):
            response = "إليك قائمة خدماتنا:\n" + "\n".join([f"- **{k}**: {v}" for k, v in COMPANY_INFO["services"].items()])
        else:
            response = "أنا هنا للمساعدة! يمكنك سؤالي عن أسعار خدماتنا."
        
        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})