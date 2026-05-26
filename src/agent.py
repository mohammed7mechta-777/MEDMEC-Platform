import streamlit as st
import requests
import subprocess

def run_local_command(command):
    """تنفيذ أوامر محلية عبر النظام (لأغراض الأتمتة)"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"حدث خطأ أثناء تنفيذ الأمر: {str(e)}"

def run_assistant():
    st.title("🤖 منصة MEDMEC - الذكاء الاصطناعي المحلي")
    
    # تهيئة حالة المحادثة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # عرض الرسائل المخزنة
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # مدخلات المستخدم
    if prompt := st.chat_input("اطلب مني مهمة أو اسأل عن خدماتنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 1. تنفيذ الأوامر المحلية (أتمتة) إذا بدأ الأمر بـ 'run:'
        if prompt.startswith("run:"):
            cmd = prompt.replace("run:", "").strip()
            with st.chat_message("assistant"):
                st.write(f"⚙️ جاري تنفيذ: `{cmd}`")
                output = run_local_command(cmd)
                st.code(output, language='bash')
                st.session_state.messages.append({"role": "assistant", "content": f"النتيجة:\n{output}"})

        # 2. الاستعلام من نموذج الذكاء الاصطناعي المحلي (Ollama)
        else:
            with st.chat_message("assistant"):
                with st.spinner("جاري التفكير محلياً..."):
                    try:
                        # الربط مع Ollama
                        payload = {
                            "model": "qwen2.5:1.5b", 
                            "prompt": f"أنت مساعد MEDMEC. خدماتنا: Data Cleanse Pro (8000 دج)، CRM (9000 دج). سياق: {prompt}",
                            "stream": False
                        }
                        response = requests.post("http://localhost:11434/api/generate", json=payload)
                        response_data = response.json()
                        answer = response_data.get("response", "لم أتمكن من الحصول على رد.")
                        
                        st.markdown(answer)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error("خطأ: تأكد أن سيرفر Ollama يعمل على المنفذ 11434!")