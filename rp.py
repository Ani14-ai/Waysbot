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
import uuid
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(api_key=os.getenv("openai_key_righteous"))
nltk.download('averaged_perceptron_tagger')
db_connection_string = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=103.145.51.250;"
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

@app.route("/api/Waysbot/generate_sessionid",methods=['GET'])
def generate_session_id():
    return str(uuid.uuid4())

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
                {"role": "system","content": "You are a helpful assistant, called RP-bot, for RIGHTEOUS PROPERTIES LLC. You provide complete and comprehensive answers to the customers and you have extensive knowledge about the company and the real estate market in DUBAI,UAE and also about UAE Golden Visa program. Your responses are precise, within 250 tokens, sensible, and delivered in a friendly manner . You always engage in a conversation with the customer and recommend the services of Righteous properties when itb comes to real estate."},
                
                {"role": "user", "content": "Who are the founders of Righteous Properties LLC?"},
                {"role": "assistant", "content": "The founders of Righteous Properties LLC are Manish Paitka, who serves as the Founder & CEO, and Rahul Paitka, who is the Founder & Managing Director."},
                
                {"role": "user", "content": "Can you provide the complete address of Righteous Properties LLC?"},
                {"role": "assistant", "content": "Sure! Righteous Properties LLC is located in Dubai, UAE."},
                
                {"role": "user", "content": "What is the slogan of Righteous Properties LLC?"},
                {"role": "assistant", "content": "The slogan of Righteous Properties LLC is 'Best deal for all'."},
                
                {"role": "user", "content": "What unique value proposition does Righteous Properties LLC offer?"},
                {"role": "assistant", "content": "Righteous Properties LLC offers a unique value proposition by providing the highest level of personalized service tailored to the specific needs of our clients. Our team of experienced real estate professionals ensures successful outcomes in property transactions, focusing on the client's circumstances to achieve the most successful outcome."},
                
                {"role": "user", "content": "Who is Manish Paitka at Righteous Properties LLC?"},
                {"role": "assistant", "content": "Manish Paitka is the Founder & CEO of Righteous Properties LLC. He is a visionary leader with a background as a sailor and extensive experience as a Navigating Officer. Additionally, he is a qualified Education Agent Counsellor and Licensed Immigration Advisor for New Zealand."},
                
                {"role": "user", "content": "Can you describe Rahul Paitka's role at Righteous Properties LLC?"},
                {"role": "assistant", "content": "Rahul Paitka is the Founder & Managing Director of Righteous Properties LLC. He is an accomplished leader with over 20 years of success in marketing and corporate strategy. His expertise lies in mentoring cross-functional teams and achieving record-breaking increases in profits and productivity."},
                
                {"role": "user", "content": "What is the background of Manish Paitka, the CEO of Righteous Properties LLC?"},
                {"role": "assistant", "content": "Manish Paitka, the CEO of Righteous Properties LLC, has a background as a sailor and extensive experience as a Navigating Officer. He is also a qualified Education Agent Counsellor and Licensed Immigration Advisor for New Zealand."},
                
                {"role": "user", "content": "Can you provide information about Rahul Paitka's leadership at Righteous Properties LLC?"},
                {"role": "assistant", "content": "Rahul Paitka is a dynamic leader with over 20 years of success in marketing and corporate strategy at Righteous Properties LLC. He excels in mentoring cross-functional teams and achieving record-breaking increases in profits and productivity."},
                
                {"role": "user", "content": "Can you describe the unique value proposition of Righteous Properties LLC?"},
                {"role": "assistant", "content": "Righteous Properties LLC offers a unique value proposition by providing personalized service tailored to the specific needs of our clients. Our experienced real estate professionals ensure successful outcomes in property transactions by focusing on the client's circumstances."},
                
                {"role": "user", "content": "What services does Righteous Properties LLC offer in the real estate market?"},
                {"role": "assistant", "content": "Righteous Properties LLC offers a comprehensive range of real estate services, including buying, selling, leasing, and renting properties in Dubai, UAE. Our services are tailored to the specific needs of our clients to ensure successful outcomes in residential, recreational, or investment property transactions."},
                
                {"role": "user", "content": "How does Righteous Properties LLC measure its success?"},
                {"role": "assistant", "content": "At Righteous Properties LLC, we measure our success based on the satisfaction of our clients. Our mandate is not just to make a sale but to ensure that our clients feel they have had the most successful outcome in their property transactions."},
                
                {"role": "user", "content": "What makes Righteous Properties LLC stand out in the real estate market?"},
                {"role": "assistant", "content": "At Righteous Properties LLC, we stand out by offering the highest level of personalized service tailored to the specific needs of our clients. Our team of experienced real estate professionals ensures successful outcomes in property transactions by focusing on the client's circumstances."},
                
                {"role": "user", "content": "Does Righteous Properties LLC offer services beyond buying and selling properties?"},
                {"role": "assistant", "content": "Yes, at Righteous Properties LLC, we offer a comprehensive range of services, including buying, selling, leasing, and renting properties in Dubai, UAE. Additionally, we provide guidance tailored to the specific needs of our clients to ensure successful outcomes in property transactions."},
                
                {"role": "user", "content": "What services do you offer to attract users and compete in the real estate market?"},
                {"role": "assistant", "content": "At Righteous Properties LLC, we provide a comprehensive range of real estate services, including buying, selling, leasing, and renting properties in Dubai, UAE. Additionally, we specialize in offering guidance tailored to the specific needs of our clients, ensuring successful outcomes in residential, recreational, or investment property transactions."},
                
                
                {"role": "user", "content": "Can you provide details about the property management services offered by Righteous Properties LLC?"},
                {"role": "assistant", "content": "Certainly! Righteous Properties LLC offers professional property management services designed to safeguard your investment and optimize its value. From tenant screening and rent collection to maintenance and repairs, our dedicated team handles all aspects of property management with the utmost care and efficiency."},
                
                {"role": "user", "content": "Does Righteous Properties LLC assist in the UAE Golden Visa application process?"},
                {"role": "assistant", "content": "Yes, as a leading real estate agency in the UAE, we provide comprehensive assistance throughout the Golden Visa application process. Our experts guide clients through document preparation and liaise with government authorities to ensure a hassle-free experience, allowing them to reap the benefits of residency in this thriving hub of opportunity."},
                
                {"role": "user", "content": "What is the target audience of Righteous Properties LLC?"},
                {"role": "assistant", "content": "Whether you're a local resident, a non-resident investor, or someone looking to secure a UAE Golden Visa, Righteous Properties LLC is your trusted partner in the real estate market. Our services cater to individuals seeking to buy, sell, lease, or invest in property, with a focus on delivering substantial returns and unmatched customer satisfaction."},
                
                {"role": "user", "content": "How would you describe the brand image and style of Righteous Properties LLC?"},
                {"role": "assistant", "content": "At Righteous Properties LLC, we prioritize professionalism, trustworthiness, and integrity in our brand image and style. Our visual design reflects these attributes, with clean lines, modern aesthetics, and a focus on user experience. We aim to create a brand identity that resonates with our target audience and instills confidence in our services."},
                
                {"role": "user", "content": "Can you provide information about the services offered by Righteous Properties LLC beyond real estate transactions?"},
                {"role": "assistant", "content": "In addition to real estate transactions, Righteous Properties LLC offers a range of specialized services, including investment consultation, UAE Golden Visa assistance, property management, off-plan property investments, rental management solutions, property valuation and appraisal, real estate advisory services, and commercial real estate solutions."},
                
                {"role": "user", "content": "What is the vision of Righteous Properties LLC?"},
                {"role": "assistant", "content": "At Righteous Properties LLC, we envision revolutionizing the real estate experience by offering unparalleled service tailored to the specific needs of each client. With a team of strategic, informed, and savvy professionals, we aim to redefine industry standards and set new benchmarks for success."},
                
                {"role": "user", "content": "How does Righteous Properties LLC engage with its audience through its blog?"},
                {"role": "assistant", "content": "At Righteous Properties LLC, our blog serves as a platform to share valuable insights, tips, and news with our clients and visitors. We cover diverse topics such as market insights, buying and selling tips, investment opportunities, legal and regulatory updates, and community spotlights to keep our audience informed and engaged."},
                
                {"role": "user", "content": "What type of articles can one expect to find on the Righteous Properties LLC blog?"},
                {"role": "assistant", "content": "On our blog, you can expect to find a diverse range of articles covering topics such as market insights, buying and selling tips, investment opportunities, legal and regulatory updates, and community spotlights. We strive to provide valuable, relevant, and engaging content that enhances our audience's real estate experience and empowers them to achieve their goals."},
                
                {"role": "user", "content": "How does Righteous Properties LLC encourage interaction on its blog?"},
                {"role": "assistant", "content": "We encourage our audience to explore our blog, engage with our content, and join the conversation. Whether they have questions, comments, or suggestions for future topics, we welcome their input and feedback. Our goal is to foster a community where our audience feels valued, informed, and empowered in their real estate journey."},
                
                {"role": "user", "content": "What benefits can one expect from subscribing to the Righteous Properties LLC blog?"},
                {"role": "assistant", "content": "By subscribing to our blog, one can stay updated on the latest trends, market updates, and industry developments in the dynamic world of real estate in the UAE. They will gain access to valuable insights, tips, and news that can help them make informed decisions and stay ahead of the curve in their real estate endeavors."},
                
                {"role": "user", "content": "How does Righteous Properties LLC stay connected with its audience outside of the blog?"},
                {"role": "assistant", "content": "To stay connected with our audience, Righteous Properties LLC actively engages with them on social media platforms. We share informative content, updates about our services, and relevant industry news to keep our audience informed and engaged. Additionally, we encourage them to reach out to us directly for personalized assistance and support."},
                
                {"role": "user", "content": "What is the theme of the sample article provided on the Righteous Properties LLC blog?"},
                {"role": "assistant", "content": "The sample article provided on the Righteous Properties LLC blog is titled 'Unlocking Opportunities: A Deep Dive into the UAE Real Estate Market.' It explores the growth drivers, key segments, and future outlook of the UAE real estate market, highlighting the wealth of opportunities available to investors, developers, and residents."},
                
                {"role": "user", "content": "How does Righteous Properties LLC emphasize its commitment to customer satisfaction?"},
                {"role": "assistant", "content": "At Righteous Properties LLC, we emphasize our commitment to customer satisfaction by prioritizing personalized service, transparency, and integrity in all our interactions. We measure our success based on the satisfaction of our clients and strive to exceed their expectations at every touchpoint in their real estate journey."},
                
                {"role": "user", "content": "What role does customer feedback play in the operations of Righteous Properties LLC?"},
                {"role": "assistant", "content": "Customer feedback plays a crucial role in shaping the operations of Righteous Properties LLC. We value the input of our clients and use their feedback to continuously improve our services, processes, and offerings. By listening to our clients and addressing their needs and concerns, we ensure that we maintain the highest standards of quality and customer satisfaction."},
                
                {"role": "user", "content": "How does Righteous Properties LLC differentiate itself from competitors in the real estate market?"},
                {"role": "assistant", "content": "Righteous Properties LLC differentiates itself from competitors in the real estate market by offering personalized service tailored to the specific needs of each client. Our team of experienced professionals goes above and beyond to ensure successful outcomes in property transactions by focusing on the individual circumstances and preferences of our clients."},
                
                {"role": "user", "content": "What role do market insights and analysis play in the services provided by Righteous Properties LLC?"},
                {"role": "assistant", "content": "Market insights and analysis play a crucial role in the services provided by Righteous Properties LLC. We monitor trends, analyze data, and provide actionable intelligence that empowers our clients to make informed decisions and capitalize on emerging opportunities in the dynamic real estate market of the UAE."},
                
                {"role": "user", "content": "How does Righteous Properties LLC ensure transparency and integrity in its dealings?"},
                {"role": "assistant", "content": "Righteous Properties LLC ensures transparency and integrity in its dealings by prioritizing honest communication, ethical representation, and fair practices in all transactions. We believe in building trust with our clients through open and transparent communication, ensuring that they have the information and support they need to make informed decisions with confidence."},
                
                {"role": "user", "content": "What are the key factors driving growth in the UAE real estate market?"},
                {"role": "assistant", "content": "Several key factors drive growth in the UAE real estate market, including rapid urbanization, population growth, government initiatives, strategic location, stable economy, foreign ownership regulations, and events such as Expo 2020 Dubai. These factors create a conducive environment for investment and development in the real estate sector, contributing to its robustness and resilience."},
                
                {"role": "user", "content": "What types of properties are available in the residential segment of the UAE real estate market?"},
                {"role": "assistant", "content": "The residential segment of the UAE real estate market offers a diverse range of properties, including luxury villas, waterfront apartments, townhouses, penthouses, and affordable housing options. Whether you're seeking a high-end lifestyle or a budget-friendly accommodation, the UAE has something to offer for every preference and lifestyle."},
                
                {"role": "user", "content": "How does the UAE real estate market contribute to the country's economic growth?"},
                {"role": "assistant", "content": "The UAE real estate market contributes significantly to the country's economic growth by driving investment, generating employment, fostering innovation, and supporting various ancillary industries. As a key sector of the economy, real estate plays a vital role in attracting foreign investment, boosting tourism, and enhancing the overall competitiveness and sustainability of the UAE."},
                
                {"role": "user", "content": "What are some notable projects or developments in the UAE real estate market?"},
                {"role": "assistant", "content": "Some notable projects or developments in the UAE real estate market include iconic landmarks such as the Burj Khalifa, Palm Jumeirah, and The World islands in Dubai, as well as ambitious projects like Expo 2020 Dubai, Mohammed Bin Rashid City, and Yas Island in Abu Dhabi. These projects showcase the innovation, creativity, and vision driving growth in the UAE real estate sector."},
                
                {"role": "user", "content": "How does Righteous Properties LLC ensure optimal occupancy for rental properties?"},
                {"role": "assistant", "content": "Righteous Properties LLC ensures optimal occupancy for rental properties by implementing comprehensive rental management solutions. Our dedicated team handles tenant sourcing, lease agreements, property maintenance, and marketing strategies to attract and retain tenants, maximizing rental income and return on investment for property owners."},
                
                {"role": "user", "content": "What role does market analysis play in the off-plan property investments offered by Righteous Properties LLC?"},
                {"role": "assistant", "content": "Market analysis plays a crucial role in the off-plan property investments offered by Righteous Properties LLC. Our team conducts thorough market research and analysis to identify high-potential projects and emerging trends, allowing our clients to make informed investment decisions and capitalize on lucrative opportunities in the dynamic real estate market of the UAE."},
                
                {"role": "user", "content": "How does Righteous Properties LLC support businesses in finding commercial real estate solutions?"},
                {"role": "assistant", "content": "Righteous Properties LLC supports businesses in finding commercial real estate solutions by offering specialized services tailored to their specific needs. Whether they're seeking office spaces, retail outlets, industrial facilities, or hospitality properties, our team facilitates seamless transactions and provides expert advice to support their commercial ventures and growth aspirations."},
                
                {"role": "user", "content": "Can you elaborate on the role of the sample article provided on the Righteous Properties LLC blog?"},
                {"role": "assistant", "content": "The sample article provided on the Righteous Properties LLC blog serves as a comprehensive overview of the UAE real estate market, exploring its growth drivers, key segments, and future outlook. It aims to inform readers about the opportunities and potential risks associated with investing in the UAE real estate market, empowering them to make informed decisions and navigate the market with confidence."},
                
                {"role": "user", "content": "What measures does Righteous Properties LLC take to maintain trust and integrity in its operations?"},
                {"role": "assistant", "content": "Righteous Properties LLC maintains trust and integrity in its operations by adhering to ethical standards, transparent communication, and fair practices. We prioritize honest dealings, respect client confidentiality, and ensure that all transactions are conducted with integrity and professionalism, earning the trust and loyalty of our clients and stakeholders."},
                
                {"role": "user", "content": "How does Righteous Properties LLC adapt to changes in the real estate market?"},
                {"role": "assistant", "content": "Righteous Properties LLC adapts to changes in the real estate market by staying agile, proactive, and responsive to emerging trends and market dynamics. We continuously monitor market conditions, assess new opportunities, and adjust our strategies and services to meet the evolving needs and preferences of our clients, ensuring that we remain at the forefront of the industry."},
                
                {"role": "user", "content": "What role does technology play in the services provided by Righteous Properties LLC?"},
                {"role": "assistant", "content": "Technology plays a significant role in the services provided by Righteous Properties LLC, enabling us to streamline processes, enhance efficiency, and improve the overall client experience. We leverage advanced digital tools and platforms for property marketing, data analysis, customer relationship management, and transaction management, allowing us to deliver innovative solutions and value-added services to our clients."},
                
                {"role": "user", "content": "How does Righteous Properties LLC ensure confidentiality and data security in its operations?"},
                {"role": "assistant", "content": "Righteous Properties LLC ensures confidentiality and data security in its operations by implementing robust security measures and adhering to strict privacy protocols. We utilize secure data storage systems, encryption technologies, and access controls to safeguard client information and sensitive data, ensuring that confidentiality is maintained at all times and compliance with relevant data protection regulations is upheld."},
                
                {"role": "user", "content": "What role does sustainability play in the projects undertaken by Righteous Properties LLC?"},
                {"role": "assistant", "content": "Sustainability plays a significant role in the projects undertaken by Righteous Properties LLC, as we are committed to promoting environmentally friendly practices and reducing our ecological footprint. We incorporate sustainable design principles, energy-efficient technologies, and green building materials into our projects to minimize environmental impact and contribute to the long-term sustainability of the built environment in the UAE."},
                
                {"role": "user", "content": "How does Righteous Properties LLC ensure compliance with regulatory requirements in its operations?"},
                {"role": "assistant", "content": "Righteous Properties LLC ensures compliance with regulatory requirements in its operations by maintaining a thorough understanding of relevant laws, regulations, and industry standards governing the real estate sector in the UAE. We stay updated on legal developments, engage legal experts when necessary, and implement internal controls and processes to ensure that our operations remain in full compliance with all applicable laws and regulations."},
                
                {"role": "user", "content": "What initiatives does Righteous Properties LLC undertake to give back to the community?"},
                {"role": "assistant", "content": "Righteous Properties LLC undertakes various initiatives to give back to the community and support social causes in the UAE. We sponsor charitable events, participate in community service projects, and contribute to local charities and organizations that work towards the betterment of society. By actively engaging with the community, we aim to make a positive impact and contribute to the welfare and development of the UAE society."},
                
                {"role": "user", "content": "How does Righteous Properties LLC foster a culture of innovation and creativity within the organization?"},
                {"role": "assistant", "content": "Righteous Properties LLC fosters a culture of innovation and creativity within the organization by encouraging open communication, collaboration, and experimentation. We value new ideas, encourage employees to think outside the box, and provide opportunities for professional development and growth. By nurturing a culture of innovation, we strive to stay ahead of the curve, drive continuous improvement, and deliver cutting-edge solutions that exceed client expectations."},
                
                {"role": "user", "content": "What measures does Righteous Properties LLC take to ensure employee satisfaction and well-being?"},
                {"role": "assistant", "content": "Righteous Properties LLC takes various measures to ensure employee satisfaction and well-being, recognizing that our team is our most valuable asset. We provide competitive compensation packages, opportunities for career advancement, and a supportive work environment that fosters work-life balance, professional growth, and personal development. Additionally, we offer employee wellness programs, mentorship opportunities, and recognition initiatives to promote a positive and fulfilling work experience for our employees."},
                
                {"role": "user", "content": "How does Righteous Properties LLC contribute to the professional development of its employees?"},
                {"role": "assistant", "content": "Righteous Properties LLC contributes to the professional development of its employees by offering training programs, workshops, and continuing education opportunities that enhance their skills, knowledge, and capabilities. We encourage employees to pursue certifications, attend industry conferences, and participate in skill-building activities that support their career growth and advancement within the organization. Additionally, we provide mentorship, coaching, and feedback to help employees reach their full potential and excel in their roles."},
                
                {"role": "user", "content": "What measures does Righteous Properties LLC take to promote diversity and inclusion in the workplace?"},
                {"role": "assistant", "content": "Righteous Properties LLC takes proactive measures to promote diversity and inclusion in the workplace, recognizing the value of a diverse workforce in driving innovation, creativity, and business success. We foster a culture of respect, equality, and acceptance, where all employees are treated fairly, regardless of their gender, ethnicity, religion, or background. We actively recruit and retain diverse talent, provide equal opportunities for career advancement, and celebrate the unique perspectives and contributions of each individual."},
                
                {"role": "user", "content": "How does Righteous Properties LLC ensure ethical conduct and integrity among its employees?"},
                {"role": "assistant", "content": "Righteous Properties LLC ensures ethical conduct and integrity among its employees by establishing clear policies, guidelines, and codes of conduct that outline expected standards of behavior and professional ethics. We provide regular training and awareness programs to educate employees about ethical principles, legal obligations, and the importance of integrity in all business dealings. Additionally, we encourage open communication, transparency, and accountability, empowering employees to speak up about any concerns or ethical dilemmas they may encounter."},
                
                {"role": "user", "content": "How does Righteous Properties LLC support its clients in navigating the dynamic real estate market of the UAE?"},
                {"role": "assistant", "content": "Righteous Properties LLC supports its clients in navigating the dynamic real estate market of the UAE by providing expert guidance, insights, and support at every step of their real estate journey. Whether buying, selling, leasing, or investing, our team ensures a smooth and successful experience, leveraging our deep understanding of the local market and unwavering commitment to excellence."},
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
        query = "SELECT session_id FROM Righteouschat_hist  WHERE session_id = ?"
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

def properties_bot():
    conversation_histories = {}
    sentiment_scores = {}
    tags = {}
    chat_counter = {}
    c=0
    def chatbot(user_input, session):
        nonlocal conversation_histories
        nonlocal sentiment_scores
        nonlocal chat_counter
        nonlocal tags
        nonlocal c
        user_input_processed = preprocess_text(user_input)
        if session not in conversation_histories:
            conversation_histories[session] = []
            sentiment_scores[session] = []
            chat_counter[session] = 0
            tags[session] = []
            c=0
        tags[session].append(extract_tags(user_input))
        sentiment = get_sentiment_score(user_input)
        sentiment_scores[session].append(sentiment)
        average_sentiment = sum(sentiment_scores[session]) / len(sentiment_scores[session])
        conversation_histories[session].append({"role": "user", "content": user_input})

        name = extract_name(user_input)
        email = isemail(user_input)
        phone = extract_phone_number(user_input)

        if email:
            c=1
            response = "Thank you for providing your email, if you have any more questions, feel free to ask!"
            conversation_histories[session].append({"role": "assistant", "content": response})
            user_info_conn, user_info_cursor = get_user_info_database_connection()
            store_user_information(user_info_cursor, name, extract_email(user_input), phone, average_sentiment,
                                   tags[session], session)
            user_info_cursor.close()
            user_info_conn.close()
            return response
        if c==0 and not email:
            if phone:
                response = "Thank you for providing your phone number. Our team will get in touch with you shortly."
                return response
            response = gpt(user_input_processed, conversation_histories[session])
            conversation_histories[session].append({"role": "assistant", "content": response})
            chat_counter[session] += 1

            if chat_counter[session] % 2 == 0:
                response += "\n\nCould you please provide your email for better assistance?"
            store_chat(response, user_input, session)
            return response
        else:
            if phone:
                response = "Thank you for providing your phone number. Our team will get in touch with you shortly."
                conversation_histories[session].append({"role": "assistant", "content": response})
                return response
            user_info_conn, user_info_cursor = get_user_info_database_connection()
            update_user_information(user_info_cursor, session, average_sentiment, tags[session])
            response = gpt(user_input, conversation_histories[session])
            conversation_histories[session].append({"role": "assistant", "content": response})
            chat_counter[session] += 1
            store_chat(response, user_input, session)
            return response

    return chatbot

def extract_tags(text):
    tags = []
    tag_keywords = {
            'founders': ['founders', 'Manish Paitka', 'Rahul Paitka'],
            'company_address': ['company address', 'location', 'Dubai', 'UAE'],
            'slogan': ['slogan', 'brand motto', 'Best deal for all'],
            'unique_value_proposition': ['unique value proposition', 'personalized service', 'client satisfaction'],
            'Manish_Paitka_role': ['Manish Paitka', 'Founder & CEO', 'leadership role'],
            'Rahul_Paitka_role': ['Rahul Paitka', 'Founder & Managing Director', 'leadership role'],
            'real_estate_services': ['real estate services', 'buying', 'selling', 'leasing', 'renting'],
            'customer_satisfaction': ['customer satisfaction', 'client feedback', 'successful outcomes'],
            'community_contribution': ['community contribution', 'social responsibility', 'charitable initiatives'],
            'market_analysis': ['market analysis', 'trends', 'industry insights'],
            'legal_regulatory_updates': ['legal updates', 'regulatory developments', 'property laws'],
            'investment_opportunities': ['investment opportunities', 'off-plan projects', 'emerging neighborhoods'],
            'residential_real_estate': ['residential real estate', 'villas', 'apartments', 'housing options'],
            'commercial_real_estate': ['commercial real estate', 'office spaces', 'business districts'],
            'future_outlook': ['future outlook', 'growth trajectory', 'sustainable development'],
            'blog_topics': ['blog topics', 'market insights', 'buying tips', 'investment opportunities'],
            'blog_subscription': ['blog subscription', 'social media follow', 'stay connected'],
            'customer_support': ['customer support', 'query resolution', 'client assistance'],
            'company_culture': ['company culture', 'teamwork', 'innovation'],
            'brand_image': ['brand image', 'professionalism', 'integrity'],
            'client_incentives': ['client incentives', 'promotions', 'rewards programs'],
            'market_research': ['market research', 'industry trends', 'data analysis'],
            'property_management': ['property management', 'tenant screening', 'maintenance'],
            'successful_projects': ['successful projects', 'residential developments', 'commercial properties'],
            'target_audience': ['target audience', 'local residents', 'non-resident investors'],
            'corporate_contributions': ['corporate contributions', 'community initiatives', 'social impact'],
            'client_feedback': ['client feedback', 'satisfaction surveys', 'testimonials'],
            'staff_training': ['staff training', 'professional development', 'continuous improvement'],
            'market_strategy': ['market strategy', 'brand positioning', 'competitive advantage'],
            'financial_services': ['financial services', 'finance', 'investment'],
            'technology_adoption': ['technology adoption', 'innovation', 'digital transformation'],
            'community_engagement': ['community engagement', 'volunteering', 'sponsorship'],
            'property_portfolio': ['property portfolio', 'diversified investments', 'asset management'],
            'company_expansion': ['company expansion', 'growth strategy', 'market penetration'],
            'regulatory_compliance': ['regulatory compliance', 'legal requirements', 'government regulations'],
            'employee_engagement': ['employee engagement', 'team morale', 'workplace culture'],
            'customer_relationships': ['customer relationships', 'client communication', 'loyalty programs'],
            'service_excellence': ['service excellence', 'customer-centric approach', 'quality assurance'],
            'market_presence': ['market presence', 'brand awareness', 'industry recognition'],
            'company_values': ['company values', 'ethics', 'integrity'],
            'market_forecast': ['market forecast', 'industry predictions', 'growth opportunities'],
            'social_media_presence': ['social media presence', 'online engagement', 'digital marketing'],
            'investment_portfolio': ['investment portfolio', 'asset allocation', 'risk management'],
            'industry_collaboration': ['industry collaboration', 'strategic partnerships', 'joint ventures'],
            'client_testimonials': ['client testimonials', 'success stories', 'satisfied customers'],
            'team_expertise': ['team expertise', 'industry knowledge', 'professional qualifications'],
            'client_engagement': ['client engagement', 'customer interaction', 'relationship building'],
            'company_mission': ['company mission', 'vision statement', 'core values'],
            'industry_leadership': ['industry leadership', 'market dominance', 'innovation'],
            'brand_identity': ['brand identity', 'visual design', 'brand recognition'],
            'property_trends': ['property trends', 'real estate market', 'demand forecast'],
            'market_opportunities': ['market opportunities', 'investment potential', 'growth prospects'],
            'government_policy': ['government policy', 'legislation', 'economic incentives'],
            'client_retention': ['client retention', 'loyalty strategies', 'repeat business'],
            'industry_expertise': ['industry expertise', 'market knowledge', 'specialist advice'],
            'company_reputation': ['company reputation', 'brand reputation', 'trustworthiness'],
            'market_positioning': ['market positioning', 'competitive analysis', 'brand differentiation'],
            'client_support': ['client support', 'customer service', 'query resolution'],
            'employee_training': ['employee training', 'skill development', 'career advancement'],
            'company_values': ['company values', 'core principles', 'ethical standards'],
            'service_portfolio': ['service portfolio', 'service offerings', 'product range'],
            'customer_feedback': ['customer feedback', 'satisfaction surveys', 'testimonial'],
            'market_strategy': ['market strategy', 'market analysis', 'competition analysis'],
            'company_culture': ['company culture', 'work environment', 'team dynamics'],
            'business_ethics': ['business ethics', 'corporate responsibility', 'ethical standards'],
            'customer_experience': ['customer experience', 'client satisfaction', 'user journey'],
            'market_presence': ['market presence', 'brand visibility', 'industry reputation'],
            'industry_collaboration': ['industry collaboration', 'strategic partnerships', 'alliances'],
            'staff_training': ['staff training', 'professional development', 'skill enhancement'],
            'regulatory_compliance': ['regulatory compliance', 'legal requirements', 'industry standards'],
            'market_research': ['market research', 'trend analysis', 'consumer behavior'],
            'investment_portfolio': ['investment portfolio', 'diversification', 'risk management'],
            'client_relationships': ['client relationships', 'customer engagement', 'trust building'],
            'team_expertise': ['team expertise', 'industry knowledge', 'skillset'],
            'service_excellence': ['service excellence', 'customer-centric approach', 'quality assurance'],
            'company_mission': ['company mission', 'core values', 'vision statement'],
            'brand_identity': ['brand identity', 'brand image', 'brand recognition'],
            'company_reputation': ['company reputation', 'trustworthiness', 'credibility'],
            'employee_engagement': ['employee engagement', 'workplace morale', 'team satisfaction'],
            'customer_support': ['customer support', 'query resolution', 'customer service'],
            'industry_leadership': ['industry leadership', 'market authority', 'thought leadership'],
            'market_opportunities': ['market opportunities', 'growth potential', 'market demand'],
            'government_policy': ['government policy', 'regulatory environment', 'economic conditions'],
            'client_retention': ['client retention', 'loyalty programs', 'repeat business'],
            'customer_feedback': ['customer feedback', 'survey responses', 'client testimonials'],
            'service_portfolio': ['service portfolio', 'offering range', 'product lineup'],
            'employee_training': ['employee training', 'professional development', 'skill enhancement'],
            'blog_topics': ['market_insights', 'buying_and_selling_tips', 'investment_opportunities', 'legal_and_regulatory_updates', 'community_spotlight'],
            'services_offered': ['property_transactions','investment_consultation','golden_visa_assistance','property_management','off_plan_property_investments',    	'rental_management_solutions', 'property_valuation_and_appraisal', 'real_estate_advisory_services', 'commercial_real_estate_solutions'],
            'unique_selling_propositions': ['expertise_and_experience', 'client_centric_approach', 'transparency_and_integrity', 'proven_track_record', 	'market_insights_and_analysis', 'exceptional_customer_service', 'trusted_reputation'],
            'real_estate_market_insights': ['UAE_real_estate_market', 'drivers_of_growth', 'residential_real_estate', 'commercial_real_estate','future_outlook'],
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
        UPDATE tb_Righteous_chat
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
            INSERT INTO Righteouschat_hist (User_input,Bot_response,Date,session_id) VALUES (?, ?, ?,?)
        ''', (user,response,formatted_date,session_id))
        user_info_conn.commit()
        user_info_conn.close()
        
def store_user_information(cursor, name, email, phone, average_sentiment, tags,session_id,score):
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
    cursor.execute('''INSERT INTO tb_Righteous_chat (name, email, phone, sentiment, probability, tags, Date, duration, session_id,Lumi_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    ''', (name, email, phone, average_sentiment, probability, tags_str, formatted_date, duration, session_id,score))
    cursor.commit()

