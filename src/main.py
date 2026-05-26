import streamlit as st
from groq import Groq
import requests
from reportlab.pdfgen import canvas
import io
import datetime

# الإعدادات الأساسية
client = Groq(api_key="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")
TELEGRAM_TOKEN = "8017768054:AAFCuZzTMQ0yZR_w_V3chiYAUN1v3MUtZnI"
CHAT_ID = "8015319712"

st.set_page_config(page_title="MEDMEC Business OS", layout="wide")

# --- 1. اللوحة الإدارية السرية (Dashboard) ---
def show_admin_dashboard():
    st.sidebar.title("🔒 لوحة الإدارة")
    password = st.sidebar.text_input("كلمة مرور الإدارة", type="password")
    if password == "MEDMEC2026":
        st.sidebar.success("أهلاً بك يا محمد")
        st.sidebar.metric("زيارات اليوم", "42")
        st.sidebar.metric("طلبات مؤكدة", "8")
    elif password:
        st.sidebar.error("كلمة سر خاطئة")

show_admin_dashboard()

# --- 2. الأنظمة المساعدة ---
if "persona" not in st.session_state: st.session_state.persona = None

def get_system_prompt(persona):
    return f"أنت مستشار أعمال خبير في MEDMEC AI، وتخاطب حالياً: {persona}. ركز على احتياجات هذا النوع من العملاء."

def generate_invoice(name, email, plan):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, 800, "MEDMEC OFFICIAL INVOICE")
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, f"Customer: {name}")
    c.drawString(50, 730, f"Plan: {plan}")
    c.save()
    buffer.seek(0)
    return buffer

# --- 3. الواجهة الترحيبية ---
st.markdown("<div style='text-align:center; padding:30px; background:#1e3c72; color:white; border-radius:20px;'><h1>مرحباً بك في MEDMEC Business OS</h1></div>", unsafe_allow_html=True)

if not st.session_state.persona:
    persona = st.radio("حدد صفتك للبدء:", ["صاحب شركة", "فريلانسر", "آخر"])
    if st.button("بدء الاستشارة"):
        st.session_state.persona = persona
        st.rerun()
else:
    st.info(f"أسلوب المساعدة الحالي: {st.session_state.persona}")

# --- 4. الدردشة ---
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("كيف يمكنني أتمتة عملك اليوم؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": get_system_prompt(st.session_state.persona)}, 
                      {"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})

# --- 5. الفوترة ---
st.markdown("---")
st.subheader("📦 طلب خدماتنا")
col1, col2 = st.columns(2)
with col1:
    plan = st.selectbox("الباقة:", ["مجاني", "محترف", "شركة"])
    name = st.text_input("الاسم:")
    email = st.text_input("الإيميل:")
with col2:
    if st.button("تأكيد الطلب والحصول على الفاتورة"):
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": f"طلب جديد: {plan}"})
        invoice = generate_invoice(name, email, plan)
        st.download_button("📥 تحميل الفاتورة PDF", invoice, "Invoice.pdf")