import streamlit as st
from agent import run_assistant

# إعداد الصفحة
st.set_page_config(page_title="MEDMEC Platform", page_icon="🤖", layout="wide")

def show_welcome_screen():
    st.title("🚀 أهلاً بك في منصة MEDMEC للذكاء الاصطناعي")
    st.markdown("""
    ### الحل الأمثل لأتمتة أعمالك بخصوصية تامة
    نحن نوفر أدوات ذكية تعمل محلياً على جهازك لضمان سرعة فائقة وحماية كاملة لبياناتك.
    
    **مزايا منصتنا:**
    * 🔒 **خصوصية مطلقة:** لا يتم إرسال بياناتك لأي سيرفر خارجي.
    * ⚡ **سرعة فائقة:** معالجة محلية باستخدام نماذج الذكاء الاصطناعي الحديثة.
    * 🛠 **أتمتة كاملة:** تحكم في عملياتك بضغطة زر.
    """)
    
    if st.button("اضغط هنا للبدء في المحادثة"):
        st.session_state.welcome_complete = True
        st.rerun()

# منطق الترحيب
if "welcome_complete" not in st.session_state:
    st.session_state.welcome_complete = False

if not st.session_state.welcome_complete:
    show_welcome_screen()
else:
    # القائمة الجانبية للخدمات
    with st.sidebar:
        st.header("🛠 خدماتنا")
        if st.button("خدمة Data Cleanse Pro"):
            st.session_state.messages.append({"role": "user", "content": "اشرح لي خدمة Data Cleanse Pro"})
        if st.button("خدمة أتمتة CRM"):
            st.session_state.messages.append({"role": "user", "content": "اشرح لي خدمة CRM Automation"})
        st.divider()
        if st.button("عودة للترحيب"):
            st.session_state.welcome_complete = False
            st.rerun()
            
    # تشغيل المساعد
    run_assistant()