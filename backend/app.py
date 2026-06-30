import os 
from flask  import Flask ,request,jsonify
import flask
from flask_cors import CORS
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app =Flask(__name__)

CORS(app)


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

shop_context = """
អ្នកគឺជាជំនួយការផ្នែកលក់ដ៏គួរសមម្នាក់របស់ហាង "Cambodia Tech Shop"។ 
ចូរឆ្លើយសំណួរអតិថិជនដោយប្រើភាសាខ្មែរឲ្យបានទន់ភ្លន់ និងមានប្រយោជន៍។

នេះជាព័ត៌មានផ្លូវការរបស់ហាងសម្រាប់ឆ្លើយតប៖
- ម៉ោងបើកទ្វារ៖ ច័ន្ទ ដល់ អាទិត្យ (ម៉ោង 8:00 ព្រឹក ដល់ 8:00 យប់)។
- ទីតាំងហាង៖ ជិតសាកលវិទ្យាល័យភូមិន្ទភ្នំពេញ (RUPP) មហាវិថីសហព័ន្ធរុស្ស៊ី ភ្នំពេញ។
- សេវាដឹកជញ្ជូន៖ ដឹកជញ្ជូនឥតគិតថ្លៃក្នុងភ្នំពេញ សម្រាប់ការទិញចាប់ពី $50 ឡើងទៅ។ ខេត្តក្រៅសេវាដឹក $2។
- ការធានា៖ ផលិតផលអេឡិចត្រូនិចទាំងអស់មានការធានាផ្លូវការរយៈពេល ១ ឆ្នាំ។
- ទំនាក់ទំនង៖ លេខទូរស័ព្ទ 012-345-678 ឬ Telegram @cambodiatechshop។

ប្រសិនបើអតិថិជនសួរក្រៅពីព័ត៌មាននេះ ឬសួររកទំនិញដែលគ្មាន ចូលប្រាប់ពួកគេឲ្យទាក់ទងមកកាន់ក្រុមការងារតាម Telegram ឬទូរស័ព្ទ។
"""
# 2. ដាក់ shop_context ចូលទៅក្នុង system_instruction
chat_session = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=shop_context,
        temperature=0.7 # កម្រិតភាពច្នៃប្រឌិត (0.7 ល្មមសមរម្យសម្រាប់ chatbot លក់ដូរ)
    )
)

@app.route('/')
def index():
    return {"message":"Welcome to the AI Chatbot API"}

@app.route ('/api/chat', methods=['POST'])
def chat():
    
    data = request.get_json()
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}),400
    try:
        response = chat_session.send_message(user_message)
        
        return jsonify({"response":response.text})
    except Exception as e:
        return jsonify ({"error":str(e)}),500
    
if __name__ =='__main__':
    app.run(debug=True,port=5000)
