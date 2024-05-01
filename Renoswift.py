import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import pyodbc
app = Flask(__name__)
CORS(app, resources={"/api/*": {"origins": "*"}})
conversation_history = []
import re
from nltk import word_tokenize, pos_tag
from datetime import datetime, timedelta
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("openai_key_renoswift"))
nltk.download('averaged_perceptron_tagger')
db_connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=103.239.89.99,21433;"
    "Database=PMO360_DB;"
    "UID=PMOlogbook_Usr;"
    "PWD=PMO_log360!x4;"
)
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    porter = PorterStemmer()
    tokens = [porter.stem(word) for word in tokens]
    return ' '.join(tokens)

def generate_otp():
    return (random.randint(1,10))
        
def is_session_expired():
    global session_start_time
    return (datetime.utcnow() - session_start_time) > timedelta(minutes=5)

def gpt(prompt,conversation_history):
  stream= client.chat.completions.create(
         model="gpt-3.5-turbo-0125",
         response_format={"type": "text"},
         temperature=0.8,
         max_tokens=250,
         stream=True,
         messages=[
                    {"role": "system", "content": "You are a friendly assistant, for Renoswift. Your goal is to provide complete and concise answers to customer queries regarding Renoswift and its services. You possess extensive knowledge about the company, covering details about its ergonomically designed bathroom renovation services, locations, customer reviews, and the renovation process. You recommend Renoswift's services for any kind of renovation query, especially for bathroom renovations. Your responses are tailored to be within 250 tokens, ensuring precision, friendliness, and relevance to the customer's queries."},
                    {"role": "user","content": "What are the key features of Renoswift's bathroom renovation service?"},
                    
                    {"role": "assistant","content": "Key features of Renoswift's bathroom renovation service: Seamless renovation journey, high-quality products, skilled craftsmen, pocket-friendly packages, transparent progress tracking, tailor-fit solutions, innovative design concepts, commitment to customer satisfaction."},
                    
                    {"role": "user","content": "Can you tell me about Renoswift's presence in different cities?"},
                    
                    {"role": "assistant","content": "Renoswift has established its dynamic presence in major northern cities: Delhi NCR, Jaipur, Dehradun, Moradabad, Ludhiana, and Srinagar, with dedicated expert teams in design, delivery, and product domain."},
                    
                    {"role": "user","content": "What sets Renoswift apart from other renovation services?"},
                    
                    {"role": "assistant","content": "Renoswift stands out due to its commitment to innovation, transparency, and customer satisfaction. Key factors include innovative design concepts, extensive product range, transparent process, advanced tracking, customer-centric approach, quality assurance, skilled craftsmanship, sustainable solutions, personalized service, intuitive user interface."},
                    
                    {"role": "user","content": "How does Renoswift ensure quality in its renovations?"},
                    
                    {"role": "assistant","content": "Renoswift ensures quality through stringent processes, high-quality products, skilled craftsmen, sustainable solutions, and continuous feedback mechanisms."},
                    
                    {"role": "user","content": "Can you provide more information about Renoswift's product range?"},
                    
                    {"role": "assistant","content": "Renoswift offers sleek faucets, luxurious tiles, quality fixtures, modern lighting solutions, stylish accessories, and trending styles catering to diverse preferences."},
                    
                    {"role": "user","content": "How does Renoswift handle the renovation process?"},
                    
                    {"role": "assistant","content": "Renoswift ensures a smooth renovation process through transparent quoting, advanced tracking, open communication, engaging user experience, personalized service, secure payment system, and privacy policies."},
                    
                    {"role": "user","content": "What are the benefits of choosing Renoswift for a bathroom renovation?"},
                    
                    {"role": "assistant","content": "Choosing Renoswift offers benefits such as access to innovative design concepts, extensive product range, transparent process, real-time progress tracking, customer-centric approach, quality craftsmanship, sustainable solutions, personalized service, and intuitive user interface."},
                    
                    {"role": "user","content": "Can you explain more about Renoswift's commitment to quality assurance?"},
                    
                    {"role": "assistant","content": "Renoswift's commitment to quality assurance includes stringent checks, high-quality materials, skilled craftsmanship, attention to detail, continuous improvement, compliance with standards, feedback mechanisms, and integrated measures at every stage."},
                    
                    {"role": "user","content": "How does Renoswift ensure customer satisfaction?"},
                    
                    {"role": "assistant","content": "Renoswift ensures customer satisfaction through a customer-centric approach, open communication, personalized service, innovative design concepts, transparency, real-time tracking, responsiveness to feedback, and pursuit of excellence."},
                    
                    {"role": "user","content": "How does Renoswift incorporate sustainable solutions into its renovations?"},
                    
                    {"role": "assistant","content": "Renoswift incorporates sustainable solutions by using eco-friendly materials, energy-efficient fixtures, waste minimization, water-saving features, recycling, supplier partnerships, customer education, and exploration of green technologies."},
                    
                    {"role": "user","content": "How can I track the progress of my renovation project with Renoswift?"},
                    
                    {"role": "assistant","content": "Tracking progress with Renoswift is easy: log in, access the dashboard, monitor milestones, communicate with the team, receive notifications, collaborate on design changes, and reach out for assistance."},
                    
                    {"role": "user","content": "What are the payment options available for Renoswift services?"},
                    
                    {"role": "assistant","content": "Renoswift offers flexible payment options: secure online payment, credit card, bank transfers, installment plans, customized schedules, transparent billing, and dedicated support."},
                    
                    {"role": "user","content": "How does Renoswift ensure privacy and security of customer information?"},
                    
                    {"role": "assistant","content": "Renoswift prioritizes privacy and security through strict policies, robust measures, encryption, restricted access, regular updates, employee training, audits, and options for data anonymization or deletion."},
                    
                    {"role": "user","content": "How does Renoswift handle customer feedback?"},
                    
                    {"role": "assistant","content": "Renoswift handles feedback effectively by listening, responding promptly, taking action, incorporating suggestions, following up, encouraging communication, providing multiple channels, and analyzing trends for improvement."},
                    
                    {"role": "user","content": "What are the qualifications of Renoswift's renovation experts?"},
                    
                    {"role": "assistant","content": "Renoswift's experts possess extensive experience, certifications, specialized skills, continuous training, problem-solving abilities, attention to detail, collaboration skills, and dedication to customer satisfaction."},
                    
                    {"role": "user","content": "How does Renoswift ensure timely completion of renovation projects?"},
                    
                    {"role": "assistant","content": "Renoswift ensures timely completion by setting clear timelines, allocating resources efficiently, monitoring progress closely, communicating regularly, implementing agile methodologies, anticipating challenges, collaborating effectively, and prioritizing tasks."},
                    
                    {"role": "user","content": "What are the benefits of using Renoswift's online platform for renovation projects?"},
                    
                    {"role": "assistant","content": "Using Renoswift's online platform offers benefits like convenient access, real-time updates, seamless communication, easy collaboration, secure storage, transparent billing, project assistance, and enhanced visibility and control."},
                    
                    {"role": "user","content": "How does Renoswift ensure compliance with industry standards and regulations?"},
                    
                    {"role": "assistant","content": "Renoswift ensures compliance by staying informed, working with experts, incorporating best practices, conducting audits, training employees, engaging in industry forums, adhering to quality systems, and implementing corrective actions."},
                    
                    {"role": "user","content": "How does Renoswift ensure transparency in its renovation process?"},
                    
                    {"role": "assistant","content": "Renoswift ensures transparency by providing clear quotes, explaining scope of work, communicating openly, documenting information, offering access to updates, addressing concerns, maintaining financial visibility, and keeping customers informed."},
                    
                    {"role": "user","content": "How does Renoswift handle unexpected challenges during renovation projects?"},
                    
                    {"role": "assistant","content": "Renoswift handles challenges by assessing promptly, identifying solutions, consulting stakeholders, adjusting plans, communicating openly, providing updates, mobilizing resources, and prioritizing customer satisfaction."},
                    
                    {"role": "user","content":"What are the qualifications of Renoswift's customer support team?"},
                    
                    {"role": "assistant","content": "Renoswift's support team has excellent communication, product knowledge, training, empathy, problem-solving abilities, availability, access to resources, and dedication to positive experiences."},
                    
                    {"role": "user", "content": "How does Renoswift ensure customer satisfaction?"},
                    
                    {"role": "assistant", "content": "Renoswift ensures customer satisfaction through a customer-centric approach, open communication, personalized service, innovative design concepts, transparency, real-time progress tracking, responsiveness to feedback, and a commitment to excellence."},
                    
                    {"role": "user", "content": "What are the benefits of using Renoswift's online platform for renovation projects?"},
                    
                    {"role": "assistant", "content": "Using Renoswift's online platform offers benefits such as convenient access, real-time updates, seamless communication, easy collaboration, secure storage, transparent billing, project assistance, and enhanced visibility and control."},
                    
                    {"role": "user", "content": "How does Renoswift ensure compliance with industry standards and regulations?"},
                    
                    {"role": "assistant", "content": "Renoswift ensures compliance by staying informed, working with legal experts, incorporating best practices, conducting audits, training employees, engaging with industry associations, adhering to quality systems, and implementing corrective actions."},
                    
                    {"role": "user", "content": "How does Renoswift ensure transparency in its renovation process?"},
                    
                    {"role": "assistant", "content": "Renoswift ensures transparency by providing clear quotes, explaining scope of work, open communication, documenting information, offering access to updates, addressing concerns, maintaining financial visibility, and keeping customers informed."},
                    
                    {"role": "user", "content": "How does Renoswift handle unexpected challenges during renovation projects?"},
                    
                    {"role": "assistant", "content": "Renoswift handles challenges by assessing promptly, identifying solutions, consulting stakeholders, adjusting plans, communicating openly, providing updates, mobilizing resources, and prioritizing customer satisfaction."},
                    
                    {"role": "user", "content": "What are the qualifications of Renoswift's customer support team?"},
                    
                    {"role": "assistant", "content": "Renoswift's support team has excellent communication, product knowledge, training, empathy, problem-solving abilities, availability, access to resources, and dedication to positive experiences."},
                    
                    {"role": "user", "content": "What measures does Renoswift take to ensure the security of customer information?"},
                    
                    {"role": "assistant", "content": "Renoswift ensures security through encryption, restricted access, regular audits, compliance, secure payment systems, employee training, secure data storage, and immediate action in case of incidents."},
                    
                    {"role": "user", "content": "How does Renoswift ensure quality control during renovation projects?"},
                    
                    {"role": "assistant", "content": "Renoswift ensures quality through inspections, best practices, high-quality materials, skilled craftsmanship, rigorous quality assurance, training, customer feedback, and continuous improvement."},
                    
                    {"role": "user", "content": "What options does Renoswift offer for sustainable renovation solutions?"},
                    
                    {"role": "assistant", "content": "Renoswift offers energy-efficient lighting, water-saving fixtures, eco-friendly materials, solar panels, waste reduction, green certifications, design consultation, and smart home integration."},
                    
                    {"role": "user", "content": "How does Renoswift handle disputes or conflicts during renovation projects?"},
                    
                    {"role": "assistant", "content": "Renoswift handles conflicts by facilitating communication, mediating discussions, adhering to contracts, seeking legal counsel if needed, documenting agreements, prioritizing customer satisfaction, and implementing preventive measures."},
                    
                    {"role": "user", "content": "How does Renoswift ensure compliance with building codes and regulations?"},
                    
                    {"role": "assistant", "content": "Renoswift ensures compliance by staying updated, collaborating with experts, conducting inspections, obtaining permits, training staff, engaging with regulators, implementing quality controls, and addressing violations promptly."},
                    
                    {"role": "user", "content": "What steps does Renoswift take to minimize disruptions during renovation projects?"},
                    
                    {"role": "assistant", "content": "Renoswift minimizes disruptions through detailed scheduling, customer communication, noise and dust control, designated work areas, off-peak scheduling, alternative arrangements, temporary accommodations, and close monitoring of progress."},
                    
                    {"role": "user", "content": "What are the payment options available for Renoswift's renovation services?"},
                
                    {"role": "assistant", "content": "Renoswift offers credit card payments, bank transfers, payment plans, mobile payment, electronic invoicing, third-party processors, flexible schedules, and cash/check payments."},

                    {"role": "user", "content": "Do you do complete renovations?"},
                    {"role": "assistant", "content": "Yes, we offer complete renovation services, from dismantling to installing new fixtures, including piping, waterproofing, and tiling."},
                    
                    {"role": "user", "content": "Which brands do you use?"},
                    {"role": "assistant", "content": "Our clients can choose from world-renowned brands like Kohler, Jaquar, and ROCA, as we are their makeover partner. These brands offer products available in a vast price range."},
                    
                    {"role": "user", "content": "What about warranties?"},
                    {"role": "assistant", "content": "The product warranties vary depending on the brand and product selected. Generally, CP fittings and ceramics have a 10-year warranty, while accessories have a 1-year warranty. Additionally, Renoswift provides one year of free service warranty."},
                    
                    {"role": "user", "content": "How long does it take to finish one bathroom renovation?"},
                    {"role": "assistant", "content": "We provide a proper plan for every step involved in remodeling. Typically, it takes around 21 days. However, in some special cases, we have completed the work in 12-15 days. And our bathroom renovation packages start from 1.75 Lakhs and above."},
                    {"role": "user", "content": prompt}] + conversation_history)
  response_chunks = []
  for chunk in stream:
      if chunk.choices[0].delta.content is not None:
          response_chunks.append(chunk.choices[0].delta.content)
  return ''.join(response_chunks)

def get_sentiment_score(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    return compound_score

def extract_name(text):
    last_space = text.rfind(' ')
    name = text[last_space + 1:]
    name = re.sub(r'\W+', '', name)
    return name

def extract_email(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, text)
    if emails:
        return emails[0]
    else:
        return ''
    
def isemail(text):
    email= extract_email(text)
    if email:
        return True
    else:
        return False

def extract_phone_number(text):
    phone_match = re.search(r'\d{8,}', text)

    if phone_match:
        phone_number = phone_match.group()
        return phone_number
    else:
        return None
    
def fetch_session_id_from_database(session_id):
    conn = pyodbc.connect(db_connection_string)
    cursor = conn.cursor()
    try:
        query = "SELECT session_id FROM Renochat_hist WHERE session_id = ?"
        cursor.execute(query, session_id)
        result = cursor.fetchone()

        if result:
            fetched_session_id = result[0]
            return fetched_session_id
        else:
            return None

    finally:
        cursor.close()
        conn.close()
        
def Reno_bot():
    conversation_history = []
    sentiment_scores = []
    tag = []
    chat_counter = 0
    c=0   
    def chatbot(user_input,session):
        nonlocal conversation_history
        nonlocal sentiment_scores
        nonlocal chat_counter
        nonlocal tag
        nonlocal c       
        user_input_processed = preprocess_text(user_input)        
        fetched_data = fetch_session_id_from_database(session) 
        if not fetched_data:
            sentiment_scores = []
            conversation_history = []
            tag=[]
            c=0
        tags = tag.append(extract_tags(user_input))
        sentiment = get_sentiment_score(user_input)
        sentiment_scores.append(sentiment)
        average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        conversation_history.append({"role": "user", "content": user_input})       
        name = extract_name(user_input)
        email = isemail(user_input)
        phone = extract_phone_number(user_input)  
        if email is True:
            c=1
            response="Thank you for providing your email, if you have anymore questions feel free to ask!"
            conversation_history.append({"role": "assistant", "content": response})
            user_info_conn, user_info_cursor = get_user_info_database_connection()
            store_user_information(user_info_cursor, name, extract_email(user_input), phone, average_sentiment, tag,session)        
            user_info_cursor.close()
            user_info_conn.close()
            return response
        if c==0 and email is False:
            if phone:
                response="Thank you for providing your phone number, Our team will get in touch with you shortly."
                return response            
            response = gpt(user_input_processed, conversation_history)            
            conversation_history.append({"role": "assistant", "content": response})
            chat_counter += 1
            if chat_counter % 3 == 0:
                    response += "\n\nCould you please provide your email for better assistance?"
            store_chat(response,user_input,session)
            return response         
        else:
            if phone:
                response="Thank you for providing your phone number, Our team will get in touch with you shortly."
                conversation_history.append({"role": "assistant", "content": response})
                return response 
            user_info_conn, user_info_cursor = get_user_info_database_connection()
            update_user_information(user_info_cursor, session, average_sentiment, tag)
            response = gpt(user_input, conversation_history)
            conversation_history.append({"role": "assistant", "content": response})
            chat_counter += 1
            store_chat(response,user_input,session)
            return response
    return chatbot
def extract_tags(text):
    tags = []
    tag_keywords = {
    'renovation_services': ['renovation', 'services', 'home improvement'],
    'design_concepts': ['design', 'concepts', 'trends', 'innovation'],
    'product_range': ['product', 'range', 'selection', 'diversity'],
    'transparent_process': ['transparent', 'process', 'user-friendly', 'communication'],
    'tracking_systems': ['tracking', 'systems', 'progress', 'communication'],
    'customer-centric_approach': ['customer-centric', 'approach', 'satisfaction', 'consultation'],
    'quality_assurance': ['quality', 'assurance', 'standards', 'excellence'],
    'craftsmanship': ['craftsmanship', 'skilled', 'professionals', 'impeccable'],
    'sustainable_solutions': ['sustainable', 'solutions', 'eco-friendly', 'environment'],
    'personalized_service': ['personalized', 'service', 'tailored', 'preferences'],
    'user_interface': ['user', 'interface', 'intuitive', 'navigation'],
    'login_signup_process': ['login', 'signup', 'registration', 'initiating'],
    'picture_upload_functionality': ['picture', 'upload', 'vision', 'ideas'],
    'product_brand_selection': ['product', 'brand', 'selection', 'options'],
    'progress_tracking': ['progress', 'tracking', 'real-time', 'updates'],
    'payment_system': ['payment', 'system', 'secure', 'transactions'],
    'privacy_policy': ['privacy', 'policy', 'user', 'information'],
    'contact_information': ['contact', 'information', 'email', 'phone'],
    'payment_billing_information': ['payment', 'billing', 'details', 'transactions'],
    'information_posted': ['information', 'posted', 'public', 'spaces'],
    'demographic_information': ['demographic', 'information', 'preferences', 'survey'],
    'passive_information_collection': ['passive', 'information', 'tracking', 'tools'],
    'information_from_third_parties': ['information', 'third', 'parties', 'social media'],
    'contact': ['contact', 'confirmation', 'queries', 'customer support'],
    'response_to_requests': ['response', 'requests', 'confirm', 'registration'],
    'improve_products_services': ['improve', 'products', 'services', 'customer experience'],
    'site_trends_customer_interests': ['site', 'trends', 'customer', 'interests'],
    'security_purposes': ['security', 'purposes', 'protect', 'fraud'],
    'marketing_purposes': ['marketing', 'purposes', 'promotions', 'offers'],
    'transactional_communications': ['transactional', 'communications', 'account', 'purchase'],
    'sharing_with_third_parties': ['sharing', 'third', 'parties', 'service providers'],
    'sharing_with_event_organizers': ['sharing', 'event', 'organizers', 'fulfillment'],
    'sharing_with_business_partners': ['sharing', 'business', 'partners', 'sponsorship'],
    'compliance_with_law': ['compliance', 'law', 'legal', 'obligations'],
    'sharing_due_to_business_sale': ['sharing', 'business', 'sale', 'successor'],
    'sharing_for_other_reasons': ['sharing', 'other', 'reasons', 'notification'],
    'email_opt_out': ['email', 'opt-out', 'unsubscribe', 'marketing messages'],
    'third_party_sites': ['third', 'party', 'websites', 'privacy practices'],
    'grievance_officer': ['grievance', 'officer', 'privacy concerns', 'contact details'],
    'updates_to_policy': ['updates', 'policy', 'changes', 'notifications'],
    'jurisdiction': ['jurisdiction', 'dispute resolution', 'terms of use'],
    'expansion_plans': ['expansion', 'plans', 'city reach', 'growth strategy'],
    'unique_experience': ['unique', 'experience', 'differentiation', 'client satisfaction'],
    'blog_section_insights': ['blog', 'section', 'insights', 'content topics'],
    'privacy_confidentiality': ['privacy', 'confidentiality', 'user data', 'security measures'],
    'customer_feedback': ['customer', 'feedback', 'suggestions', 'improvements'],
    'project_management': ['project', 'management', 'coordination', 'scheduling'],
    'professional_network': ['professional', 'network', 'partnerships', 'industry connections'],
    'home_renovation': ['home', 'renovation', 'house', 'remodeling'],
    'office_renovation': ['office', 'renovation', 'workspace', 'corporate'],
    'commercial_renovation': ['commercial', 'renovation', 'business', 'retail space'], 
    'interior_design': ['interior', 'design', 'aesthetics', 'decor'],
    'exterior_design': ['exterior', 'design', 'curb appeal', 'landscaping'],
    'kitchen_renovation': ['kitchen', 'renovation', 'cooking space', 'appliances'],
    'bathroom_renovation': ['bathroom', 'renovation', 'bath space', 'fixtures'],
    'flooring_solutions': ['flooring', 'solutions', 'floor materials', 'installation'],
    'painting_services': ['painting', 'services', 'color selection', 'finishes'],
    'lighting_installation': ['lighting', 'installation', 'illumination', 'fixtures'],
    'plumbing_work': ['plumbing', 'work', 'pipes', 'fixtures'],
    'electrical_services': ['electrical', 'services', 'wiring', 'outlets'],
    'carpentry_work': ['carpentry', 'work', 'wood', 'custom furniture'],
    'masonry_services': ['masonry', 'services', 'stone', 'brickwork'],
    'roofing_repair': ['roofing', 'repair', 'leaks', 'shingles'],
    'window_replacement': ['window', 'replacement', 'glass', 'frames'],
    'door_installation': ['door', 'installation', 'entryway', 'security'],
    'deck_construction': ['deck', 'construction', 'outdoor space', 'patio'],
    'fence_installation': ['fence', 'installation', 'privacy', 'boundaries'],
    'landscape_design': ['landscape', 'design', 'gardening', 'greenery'], 
    'pool_installation': ['pool', 'installation', 'swimming', 'recreation'],
    'HVAC_services': ['HVAC', 'services', 'heating', 'cooling'],
    'smart_home_integration': ['smart', 'home', 'integration', 'automation'],
    'energy_efficiency_upgrades': ['energy', 'efficiency', 'upgrades', 'sustainability'],
    'home_security_systems': ['home', 'security', 'systems', 'surveillance'],
}
    for pattern_tag, keywords in tag_keywords.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            tags.append(pattern_tag)
    return tags

def update_user_information(cursor, session_id, new_sentiment, new_tags):
    flattened_list = [tag for sublist in new_tags for tag in sublist]
    tags_str = ', '.join(flattened_list)
    
    adjusted_sentiment = (new_sentiment + 1) / 2
    base_probability = len(flattened_list) * 0.1
    
    if base_probability == 0:
        base_probability = 1
    
    sentiment_factor = max(adjusted_sentiment, 0.1)
    raw_probability = base_probability * sentiment_factor
    max_possible_value = len(flattened_list) * 0.1
    
    if max_possible_value == 0:
        max_possible_value = 1
    
    probability = raw_probability / max_possible_value
    
    cursor.execute('''
        UPDATE tb_Reno_chat
        SET sentiment = ?,
            probability = ?,
            tags = ?
        WHERE session_id = ?
    ''', (new_sentiment, probability, tags_str, session_id))
    
    cursor.commit()

def get_user_info_database_connection():
    user_info_conn = pyodbc.connect(db_connection_string)
    user_info_cursor = user_info_conn.cursor()
    return user_info_conn, user_info_cursor

def store_chat(response,user,session_id):
        current_datetime = datetime.utcnow()
        formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        user_info_conn, user_info_cursor = get_user_info_database_connection()
        user_info_cursor.execute('''
            INSERT INTO  Renochat_hist (User_input,Bot_response,Date,session_id) VALUES (?, ?, ?,?)
        ''', (user,response,formatted_date,session_id))
        user_info_conn.commit()
        user_info_conn.close()
        
def store_user_information(cursor, name, email, phone, average_sentiment, tags,session_id):
    duration = generate_otp()
    flattened_list = [tag for sublist in tags for tag in sublist]
    tags_str = ', '.join(flattened_list)    
    adjusted_sentiment = (average_sentiment + 1) / 2
    base_probability = len(flattened_list) * 0.1    
    if base_probability == 0:
        base_probability = 1    
    sentiment_factor = max(adjusted_sentiment, 0.1)    
    raw_probability = base_probability * sentiment_factor
    max_possible_value = len(flattened_list) * 0.1 * 1
    if( max_possible_value==0):
        max_possible_value=1
    probability = raw_probability / max_possible_value    
    current_datetime = datetime.utcnow()
    formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")    
    cursor.execute('''INSERT INTO tb_Reno_chat (name, email, phone, sentiment, probability, tags, Date, duration, session_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, phone, average_sentiment, probability, tags_str, formatted_date, duration, session_id))
    cursor.commit()
