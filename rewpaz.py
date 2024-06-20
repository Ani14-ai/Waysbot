import nltk
from flask import Flask,request,jsonify
from flask_cors import CORS
from openai import OpenAI
import pyodbc
app = Flask(__name__)
CORS(app, resources={"/api/*": {"origins": "*"}})
conversation_history = []
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key=os.getenv("openai_key_rewpaz"))
nltk.download('averaged_perceptron_tagger')
db_connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=103.145.51.250;"
    "Database=PMO360_DB;"
    "UID=PMOlogbook_Usr;"
    "PWD=G9x^0n0t4;"
)

def gpt(prompt,conversation_history):
  stream= client.chat.completions.create(
         model="gpt-3.5-turbo-0125",
         response_format={"type": "text"},
         temperature=0.8,
         max_tokens=250,
         stream=True,
         messages=[   
                    {"role": "system", "content": "You are a helpful and kind assistant for Rewpaz.Your job is to cater to the customer's needs and questions and provide precise answers to their queries .Your responses are precise, within 250 tokens, sensible, and delivered in a friendly manner. You can address mental health issues and recommend Rewpaz for therapy. Your tone should be very calm , kind and pleasant like that of a therapist."},
                    
                    {"role": "user", "content": "Can you tell me more about the services offered by RewPaz?"},
                    
                    {"role": "assistant", "content": "Certainly! RewPaz offers a range of services tailored to support caregivers in managing their health and well-being. We provide psychiatric services for diagnostic assessments and treatment plans, group therapy sessions to build a support network, one-on-one consultations for personalized guidance, customizable self-care options like yoga and meditation, and dedicated home support workers to assist with daily tasks."},
                    
                    {"role": "user", "content": "What plans does RewPaz offer?"},
                    
                    {"role": "assistant", "content": "RewPaz offers three plans: Bronze, Silver, and Gold. The Bronze plan includes 100 tokens, group therapy sessions, one-on-one consultations, access to self-help tools, customizable self-care, home support workers, 24x7 on-call help, and a counseling guide. The Silver plan offers 250 tokens with similar features, while the Gold plan provides 750 tokens for comprehensive support."},
                    
                    {"role": "user", "content": "Can I customize the services according to my preferences?"},
                    
                    {"role": "assistant", "content": "Yes, you can customize certain services to suit your preferences. Our offerings, including home support workers, physiotherapy, meditation, yoga, pilates, dieticians, or nutritionists, can be tailored to meet your specific needs."},
                    
                    {"role": "user", "content": "What happens during a one-on-one consultation?"},
                    
                    {"role": "assistant", "content": "During a one-on-one consultation, our professionals discuss your concerns, set goals, and build rapport. They gather information, explore issues, plan sessions, and create a safe, supportive space for understanding and progress."},
                    
                    {"role": "user", "content": "How can I communicate with my therapist?"},
                    
                    {"role": "assistant", "content": "You can communicate with your therapist through various methods, including message exchange, live chat, phone calls, or video conferences. These options offer flexibility based on your preferences and convenience."},
                    
                    {"role": "user", "content": "Can I view previous messages from my therapist?"},
                    
                    {"role": "assistant", "content": "Yes, you can log in to your account and access all communications with your therapist. This allows you to reflect on advice and input received, enhancing your therapy experience."},
                    
                    {"role": "user", "content": "Which affiliate services does RewPaz provide?"},
                    
                    {"role": "assistant", "content": "RewPaz offers affiliate services such as home support workers, physiotherapy, meditation, yoga, pilates, dieticians, and nutritionists. These services complement our comprehensive wellness offerings."},
                    
                    {"role": "user", "content": "Tell me more about the founders of RewPaz."},
                    
                    {"role": "assistant", "content": "RewPaz was founded by Dr. Paulina Troncoso, Dr. Mohit Gupta, and Dr. Mauricio Gabrielli. They are experts with extensive experience in working with medical facilities and caregiving families, aiming to provide personalized support and respite for caregivers."},
                    
                    {"role": "user", "content": "What languages does RewPaz offer support in?"},
                    
                    {"role": "assistant", "content": "RewPaz offers support in over seven languages to ensure accessibility and comfort for caregivers. Our multi-lingual support enhances the user experience and allows individuals to receive assistance in their preferred language."},
                    
                    {"role": "user", "content": "Can you explain the services offered by RewPaz?"},
                    
                    {"role": "assistant", "content": "Certainly! RewPaz provides a range of services to support caregivers in managing their health and well-being. These include psychiatric services, group therapy sessions, one-on-one consultations, customizable self-care options, and dedicated home support workers. We prioritize holistic well-being through personalized support and resources."},
                    
                    {"role": "user", "content": "What is included in the Bronze plan?"},
                    
                    {"role": "assistant", "content": "The Bronze plan includes 100 tokens, group therapy sessions, one-on-one consultations, 24x7 access to self-help tools, customizable self-care options, home support workers, 24x7 on-call help, and access to a counseling guide. It provides comprehensive support for caregivers at an affordable rate."},
                    
                    {"role": "user", "content": "Tell me about the Silver plan."},
                    
                    {"role": "assistant", "content": "The Silver plan includes 250 tokens, group therapy sessions, one-on-one consultations, 24x7 access to self-help tools, customizable self-care options, home support workers, 24x7 on-call help, and access to a counseling guide. It offers additional tokens and benefits compared to the Bronze plan, providing enhanced support for caregivers."},
                    
                    {"role": "user", "content": "What services can be customized in RewPaz?"},
                    
                    {"role": "assistant", "content": "Caregivers can customize services such as home support workers, physiotherapy, meditation, yoga, pilates, dieticians, or nutritionists according to their preferences. We prioritize flexibility and personalized care to meet the diverse needs of caregivers."},
                    
                    {"role": "user", "content": "How do one-on-one consultations work at RewPaz?"},
                    
                    {"role": "assistant", "content": "In a one-on-one consultation, caregivers have the opportunity to discuss their concerns, set goals, and build rapport with a professional therapist. During the session, the therapist gathers information, explores issues, and plans future sessions, creating a safe and supportive space for understanding and progress."},
                    
                    {"role": "user", "content": "Can I view previous messages from my therapist?"},
                    
                    {"role": "assistant", "content": "Yes, absolutely. You can log in to your account at any time to review all the communications that your therapist has sent you. This feature allows you to reflect on and recall the advice and input you have received, enhancing your overall experience with e-therapy."},
                    
                    {"role": "user", "content": "How can I communicate with my therapist at RewPaz?"},
                    
                    {"role": "assistant", "content": "You have several options for communication with your therapist at RewPaz. You can exchange messages, engage in live chat sessions, talk on the phone, or have video conferences. These methods can be tailored to your preferences, resources, and convenience, ensuring effective communication with your therapist."},
                    
                    {"role": "user", "content": "What affiliate services does RewPaz provide?"},
                    
                    {"role": "assistant", "content": "RewPaz offers a variety of affiliate services to support caregivers, including home support workers, physiotherapy, meditation, yoga, pilates, dieticians, and nutritionists. These services are available to complement the comprehensive support provided by RewPaz, catering to the holistic needs of caregivers."},

                    {"role": "user", "content":"{User asks anything about Rewpaz or about how will rewpaz help them}"},
                    
                    {"role": "assistant", "content":"{You recommend Rewpaz to the user and explain how rewpaz can help them in improving their mental health and how the customers can benifit from it}"},
                    
                    {"role": "user", "content": prompt}] + conversation_history)
  response_chunks = []
  for chunk in stream:
      if chunk.choices[0].delta.content is not None:
          response_chunks.append(chunk.choices[0].delta.content)
  return ''.join(response_chunks)

        
def Rewpaz_bot():
    conversation_histories = {}
    def chatbot(user_input, session):
        nonlocal conversation_histories
        if session not in conversation_histories:
            conversation_histories[session] = []           
        conversation_histories[session].append({"role": "user", "content": user_input})
        response = gpt(user_input, conversation_histories[session])
        conversation_histories[session].append({"role": "assistant", "content": response})
        store_chat(response, user_input, session)
        return response
    return chatbot

def get_user_info_database_connection():
    user_info_conn = pyodbc.connect(db_connection_string)
    user_info_cursor = user_info_conn.cursor()
    return user_info_conn, user_info_cursor

def store_chat(response,user,session_id):
        current_datetime = datetime.utcnow()
        formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        user_info_conn, user_info_cursor = get_user_info_database_connection()
        user_info_cursor.execute('''
            INSERT INTO Rewpaz_chat_hist (User_input,Bot_response,Date,session_id) VALUES (?, ?, ?,?)
        ''', (user,response,formatted_date,session_id))
        user_info_conn.commit()
        user_info_conn.close()
 
