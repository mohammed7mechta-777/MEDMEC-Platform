from groq import Groq

client = Groq(api_key="ضع_مفتاحك_هنا")

try:
    client.chat.completions.create(messages=[{"role": "user", "content": "hi"}], model="llama-3.3-70b-versatile")
    print("✅ الاتصال ناجح! المفتاح يعمل.")
except Exception as e:
    print(f"❌ خطأ: {e}")