import streamlit as st

def run_assistant():
    st.title("🤖 مساعد MEDMEC")
    if "messages" not in st.session_state: st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("اسألني عن الخدمات..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        p = prompt.lower()
        if any(w in p for w in ["سعر", "أسعار", "خدمات", "بكم"]):
            response = "خدماتنا:\n- Data Cleanse Pro: 8000 دج\n- CRM Automation: 9000 دج"
        else:
            response = "أنا مساعد MEDMEC، اسألني عن أسعار خدماتنا."
        
        with st.chat_message("assistant"): st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
