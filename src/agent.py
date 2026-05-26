import streamlit as st

COMPANY_DATA = {
    "name": "MEDMEC Digital Solutions",
    "services": {
        "Data Cleanse Pro": "8000 دج",
        "CRM Automation": "9000 دج",
        "الاستشارات التقنية": "2000 دج للساعة"
    },
    "about": "نحن شركة رائدة في الحلول الرقمية، نساعد الشركات على أتمتة عملياتها."
}

def run_assistant():
    st.subheader("🤖 مساعد MEDMEC")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("اسألني أي شيء..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        p = prompt.lower()
        if any(w in p for w in ["اسم", "شركتكم", "من أنتم"]):
            response = f"نحن شركة **{COMPANY_DATA['name']}**.\n{COMPANY_DATA['about']}"
        elif any(w in p for w in ["سعر", "أسعار", "خدمات", "بكم"]):
            list_s = "\n".join([f"- **{k}**: {v}" for k, v in COMPANY_DATA["services"].items()])
            response = f"قائمة خدماتنا:\n{list_s}"
        else:
            response = "أنا هنا للمساعدة! اسألني عن 'اسم الشركة' أو 'أسعار الخدمات'."
        
        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})