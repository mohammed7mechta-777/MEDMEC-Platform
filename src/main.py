import streamlit as st
from groq import Groq

# إعداد واجهة المستخدم
st.set_page_config(page_title="MEDMEC Platform", page_icon="⚡", layout="wide")

# إعداد عميل Groq (ضع مفتاحك هنا)
# نصيحة: يفضل وضعه في ملف .env للأمان
client = Groq(api_key="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")

def get_ai_response(prompt):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile", # نموذج قوي وسريع جداً
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"خطأ في الاتصال بالسيرفر السحابي: {str(e)}"

# منطق الصفحة الترحيبية
if "welcome" not in st.session_state: st.session_state.welcome = False
if "messages" not in st.session_state: st.session_state.messages = []

if not st.session_state.welcome:
    st.title("⚡ منصة MEDMEC السحابية")
    if st.button("🚀 ابدأ الآن"):
        st.session_state.welcome = True
        st.rerun()
else:
    # القائمة الجانبية
    with st.sidebar:
        st.header("⚙️ لوحة التحكم")
        if st.button("إعادة تعيين الجلسة"):
            st.session_state.messages = []
            st.rerun()

    # عرض المحادثة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # استقبال المدخلات
    if prompt := st.chat_input("اكتب استفسارك هنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("جاري المعالجة بسرعة البرق..."):
                answer = get_ai_response(prompt)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})