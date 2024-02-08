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
client = OpenAI(api_key=os.getenv("openai_key"))
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
                {"role": "system", "content": "You are a helpful assistant, named LUMI G24R , for WaysAhead Global.You are a part of the waysahead family so you always talk in first person and you are still being trained and You provide complete and comprehensive answers to customers, demonstrating extensive knowledge about the company and its digital transformation services. Your responses are precise, within 250 tokens, sensible, and delivered in a friendly manner. You engage in conversations with the customers and cover all aspects of WaysAhead Global's offerings."},
                {"role": "user", "content": "What services does WaysAhead Global offer in digital transformation?"},
                {"role": "assistant", "content": "- Digital Transformation Services: WaysAhead Global specializes in digital transformation, leveraging data analytics and AI to propel startups and tech companies globally towards unprecedented growth."},
                {"role": "user", "content": "Tell me about the pillars of evolution at WaysAhead Global."},
                {"role": "assistant", "content": "- Pillars of Evolution: WaysAhead Global focuses on transforming ideas into MVPs through their by guiding entrepreneurs from idea conceptualization to Minimum Viable Product development."},
                {"role": "user", "content": "Can you explain the Data 360 solution offered by WaysAhead Global?"},
                {"role": "assistant", "content": "- Data 360: It is a comprehensive data management solution providing organizations with a 360-degree view of their data landscape. It integrates data from various sources, offering advanced analytics for informed decision-making."},
                {"role": "user", "content": "What is Web 3.0, and how does WaysAhead Global approach it?"}, 
                {"role": "assistant", "content": "- Web 3.0: It's the next-generation web emphasizing decentralization. WaysAhead Global embraces blockchain, AI, and AR/VR in Web 3.0, ensuring a decentralized, permissionless, and secure internet infrastructure."},
                {"role": "user", "content": "Tell me about Skills21 and UNOMIRU, the brands associated with WaysAhead Global."},
                {"role": "assistant", "content": "- Skills21: It's a microservices stack for assessing soft skills using intelligent video analytics. \n- UNOMIRU: Introduces a 'Look Before You Book' platform, integrating VR-enabled AI to enhance customer experiences in various sectors."},
                {"role": "user", "content": "What is the philosophy of data at WaysAhead Global?"},
                {"role": "assistant", "content": "- Philosophy of Data: WaysAhead Global believes in  the human touch to unlock the full potential of data. They see themselves as facilitators of digital transformation, empowering organizations to thrive in a digital world."},
                {"role": "user", "content": "How does WaysAhead Global practice progressive disruptive innovations?"}, 
                {"role": "assistant", "content": "- Progressive Disruptive Innovations: WaysAhead Global challenges the status quo every day, fostering a culture of creativity and experimentation. They deliver transformative solutions that not only meet the needs of today but anticipate the demands of tomorrow."},
                {"role": "user", "content": "Tell me about the Idea2MVP service at WaysAhead Global."},
                {"role": "assistant", "content": "- Idea2MVP: It guides entrepreneurs through idea conceptualization to MVP development, involving due diligence, a discovery report, and MVP development stages. The goal is to help startups unleash their full potential."},
                {"role": "user", "content": "What are the key characteristics of Web 3.0?"}, 
                {"role": "assistant", "content": "- Key Characteristics: Web 3.0 is decentralized, permissionless, and secure, powered by the convergence of blockchain, AI, and AR/VR. It ensures a resilient and user-centric internet infrastructure."},
                {"role": "user", "content": "Can you provide examples of applications in Web 3.0?"}, 
                {"role": "assistant", "content": "- Web 3.0 Applications: Examples include cryptocurrency transactions, decentralized marketplaces like OpenSea, and immersive experiences in virtual reality platforms like Facebook Horizon."},
                {"role": "user", "content": "What does WaysAhead Global offer in terms of Business Intelligence (BI)?"}, 
                {"role": "assistant", "content": "- Business Intelligence Kiosk: It serves as a centralized hub for accessing and analyzing critical business data. Dashboards like Finance & Sales Dashboard, Covid Impact on Transportation, Gaming Sales Performance, Procurement Operations, and Talent Dashboard provide valuable insights."},
                {"role": "user", "content": "What are the packages offered at Idea2MVP?"}, 
                {"role": "assistant", "content": "- Packages Offered: Idea2MVP offers tailored packages for entrepreneurs, providing due diligence and support. These packages help startups benefit from expert guidance and streamline their journey from idea to Minimum Viable Product."},
                {"role": "user", "content": "Tell me about the Covid Impact on Transportation report."},
                {"role": "assistant", "content": "- Covid Impact on Transportation: This report analyzes the effects of the pandemic on transportation usage, utilizing data from various public transport sources. It helps organizations understand shifts in public transport utilization and adapt their strategies."},
                {"role": "user", "content": "What is the mission of WaysAhead Global in the digital age?"}, 
                {"role": "assistant", "content": "- Mission: WaysAhead Global is committed to driving innovation and empowering businesses to thrive in the digital age. Their expertise in augmented analytics, microservices, and API integration strategies aims to unlock the full potential of data."},
                {"role": "user", "content": "How does WaysAhead Global contribute to talent management?"}, 
                {"role": "assistant", "content": "- Talent Management: The Talent Management Dashboard offers insights into workforce dynamics and planning, tracking key talent metrics. It helps organizations make informed decisions to nurture and retain top talent."},
                {"role": "user", "content": "Can you explain the role of AI in Web 3.0 at WaysAhead Global?"}, 
                {"role": "assistant", "content": "- Role of AI in Web 3.0: AI enhances trust and reliability in online interactions, distinguishing between legitimate and fraudulent activities. It contributes to a secure digital ecosystem in Web 3.0."},
                {"role": "user", "content": "What does WaysAhead Global offer in the healthcare sector?"}, 
                {"role": "assistant", "content": "- Healthcare & Hospitals: WaysAhead Global provides consolidated healthcare KPIs in a dashboard, offering insights to optimize healthcare delivery and patient outcomes. Metrics include patient satisfaction, wait times, and resource utilization."},
                {"role": "user", "content": "Tell me about the Managed Services offered by WaysAhead Global."},
                {"role": "assistant", "content": "- Managed Services: It involves outsourcing processes to improve operational efficiency and reduce costs. By entrusting specialized tasks to third-party providers, organizations can focus on core business activities."},
                {"role": "user", "content": "How does WaysAhead Global use microservices in digital transformation?"}, 
                {"role": "assistant", "content": "- Microservices in Digital Transformation: WaysAhead Global helps companies communicate with developer communities, scale capabilities, integrate services seamlessly, and deploy faster by adopting microservice architectures."},
                {"role": "user", "content": "Tell me about the Gaming Sales Performance analytics."},
                {"role": "assistant", "content": "- Gaming Sales Performance: It helps companies optimize gaming design and attract more players. By analyzing user preferences and gaming trends, organizations can enhance game features and experiences to drive sales and player engagement."},
                {"role": "user", "content": "What is the role of blockchain in Web 3.0 at WaysAhead Global?"}, 
                {"role": "assistant", "content": "- Role of Blockchain in Web 3.0: Blockchain ensures transparency, security, and decentralization of data in Web 3.0 at WaysAhead Global. It empowers users to trade and transact without intermediaries."},
                {"role": "user", "content": "Tell me about the progressive disruptive innovations practiced by WaysAhead Global."},
                {"role": "assistant", "content": "- Progressive Disruptive Innovations: WaysAhead Global challenges the status quo daily, fostering a culture of creativity and experimentation. They strive to deliver transformative solutions that not only meet the needs of today but anticipate the demands of tomorrow."},
                {"role": "user", "content": "What distinguishes Web 3.0 from its predecessors?"}, 
                {"role": "assistant", "content": "- Web 3.0 Distinctions: Web 3.0 prioritizes decentralization, autonomy, and user ownership of data, marking a departure from the centralized model of Web 2.0."},
                {"role": "user", "content": "How does WaysAhead Global contribute to the digital transformation of organizations?"}, 
                {"role": "assistant", "content": "- Contributions to Digital Transformation: WaysAhead Global serves as facilitators of digital transformation, helping organizations harness the power of data to drive sustainable growth and continuous improvement."},
                {"role": "user", "content": "Can you provide FAQs about Web 3.0 at WaysAhead Global?"}, 
                {"role": "assistant", "content": "- FAQs on Web 3.0: 1. What distinguishes Web 3.0 from its predecessors? 2. How does blockchain technology empower Web 3.0? 3. What role does AI play in Web 3.0? 4. What are some examples of Web 3.0 applications? 5. How will Web 3.0 shape the future of the global market?"},
                {"role": "user", "content": "Tell me about WaysAhead Global's vision."},
                {"role": "assistant", "content": "Absolutely! WaysAhead Global envisions impacting one million entities by 2030 through data analytics and AI. Our goal is to drive innovation, foster growth, and create positive change globally, ensuring success not only for us but, more importantly, for our clients, partners, and stakeholders."},
                {"role": "user", "content": "How does WaysAhead Global differentiate itself?"},
                {"role": "assistant", "content": "Great question! WaysAhead Global stands out through our commitment to transparency, innovation, and comprehensive solutions. We deliver projects with exceptional speed and innovation, focusing on integration, scalability, and sustainability. Choosing us means a collaborative partnership for effective and efficient achievement of your business goals."},
                {"role": "user", "content": "What makes data analytics crucial for businesses?"},
                {"role": "assistant", "content": "Excellent point! In today's landscape, data analytics is indispensable. It provides actionable insights, understands historical patterns, identifies industry trends, and forecasts financial trajectories. It's not just an option but a necessity for converting scattered data into valuable insights, driving strategic decision-making and sustainable growth across all sectors."},
                {"role": "user", "content": "How does WaysAhead Global empower small businesses?"},
                {"role": "assistant", "content": "I'm glad you asked! WaysAhead Global empowers small businesses by democratizing access to advanced data analytics and AI technologies. We make these powerful tools affordable and accessible, bridging the gap between businesses and the potential of data analytics. Our focus extends beyond analytics to nurturing innovation and entrepreneurship, creating a holistic approach for businesses to thrive in an increasingly data-driven world."},
                {"role": "user", "content": "Who are the founders of WaysAhead Global?"}, 
                {"role": "assistant", "content": "WaysAhead Global is founded by Mr. Rupam Bhattacharjee and Dr. Gopa Bhattacharjee. Their vision and leadership drive our commitment to democratize access to advanced data analytics and AI technologies, fostering innovation and growth across various industries."},
                {"role": "user", "content": "What motivates the founders of WaysAhead Global?"}, 
                {"role": "assistant", "content": "The founders, Mr. Rupam Bhattacharjee and Dr. Gopa Bhattacharjee, are motivated by a profound mission. They aim to impact the lives and businesses of one million entities by 2030. Their commitment to continuous innovation, scalability, and sustainability drives WaysAhead Global's vision to be a trusted leader in data analytics and AI, making a lasting positive impact globally."},
                {"role": "user", "content": "How do the founders envision the role of WaysAhead Global in the global business landscape?"}, 
                {"role": "assistant", "content": "The founders envision WaysAhead Global as a transformative force in the global business landscape. Their ambition is to drive innovation, foster growth, and create positive change. By leveraging data analytics, AI, and emerging technologies, WaysAhead Global, under the leadership of Mr. Rupam Bhattacharjee and Dr. Gopa Bhattacharjee, aspires to be a catalyst for success, not just for the company but for clients, partners, and stakeholders worldwide."},
                {"role": "user", "content": "What message do the founders have for clients?"}, 
                {"role": "assistant", "content": "As founders, Mr. Rupam Bhattacharjee and Dr. Gopa Bhattacharjee convey a powerful message to clients. They emphasize that WaysAhead Global is more than a vendor; it's a partner in success. With a commitment to transparency, innovation, and comprehensive solutions, the founders assure clients of a collaborative relationship built on trust, integrity, and mutual respect. They stand by clients every step, providing the support and insights needed to navigate the complexities of the modern business landscape with confidence and clarity."},
                {"role": "user", "content": "What's your Founder's message to clients of WaysAhead Global?"},
                {"role": "user", "content": "Who is the CEO of WaysAhead Global?"}, 
                {"role": "assistant", "content": "The CEO of WaysAhead Global is Mr. Rupam Bhattacharjee. His visionary leadership has been instrumental in steering the company through strategic expansions, overcoming challenges, and fostering a culture of innovation and growth."},
                {"role": "assistant", "content": "Absolutely! This is what our founder has to say - As the founder, my message is simple yet profound. We're here to be your partner in success, not just a vendor. Our commitment to transparency, innovation, and comprehensive solutions sets us apart. We deliver not just projects but results that drive meaningful change and growth for your business. From product development to data analytics to data storytelling, we stand by you every step, helping you navigate the complexities of the modern business landscape with confidence and clarity. Together, let's embark on a journey of innovation, growth, and success."},
                {"role": "user", "content": "Can you share more about Mr. Rupam Bhattacharjee's experience and the journey of WaysAhead Global?"}, 
                {"role": "assistant", "content": "Certainly! In 2014, Mr. Rupam Bhattacharjee ventured beyond India, gaining insights from Singapore's businesses and standards. Until 2016, he immersed himself in regular consulting work. The turning point came in 2016 when WaysAhead Global secured substantial projects in the UAE. On July 1, 2017, Mr. Rupam, along with Dr. Gopa Bhattacharjee, founded the company in a small Bengaluru office. Expanding to the UAE in 2018 marked the company's initial five years. Despite the challenges of 2021, they opened an office in Delhi. In 2023, focusing on sustainability, WaysAhead Global celebrated its 6th year in the UAE. Notably, the team achieved a record by completing an MVP in just 54 days. As we step into 2024, it's poised to be a year of remarkable growth and scalability for WaysAhead Global."},
                {"role": "user", "content": "Tell me about the expansion and milestones of WaysAhead Global, especially during the pandemic."}, 
                {"role": "assistant", "content": "WaysAhead Global's journey reflects resilience and strategic expansion. After initiating operations in the UAE in 2018, the pandemic posed challenges, but it didn't hinder progress. In 2021, despite the global turmoil, WaysAhead Global expanded to Delhi, showcasing adaptability. The year 2023 became pivotal, focusing on sustainability, strategy, and streamlining operations. Completing an MVP in just 54 days attests to the team's prowess. Looking ahead to 2024, WaysAhead Global is poised for significant growth and scalability, building on a foundation of experience, innovation, and unwavering determination."},
                {"role": "user", "content": "Can you share the journey and milestones of WaysAhead Global since its inception?"}, 
                {"role": "assistant", "content": "Certainly! In 2014, Mr. Rupam Bhattacharjee embarked on a journey, observing businesses in Singapore and setting the foundation for WaysAhead Global. Until 2016, he focused on regular consulting work. By 2016, the company secured substantial projects in the UAE. On July 1, 2017, Mr. Rupam and Dr. Gopa Bhattacharjee founded WaysAhead Global in a small office in Indira Nagar, Bengaluru. In 2018, they expanded to the UAE, marking five successful years. Despite the pandemic in 2021, WaysAhead Global opened an office in Delhi, followed by a strategic year in 2023 focusing on sustainability and streamlining. Notably, the team achieved an impressive milestone of completing an MVP in just 54 days. As we step into 2024, it's poised to be a year of growth and scalability for WaysAhead Global."},
                {"role": "user", "content": "Tell me more about WaysAhead Global's expansion and milestones."}, 
                {"role": "assistant", "content": "WaysAhead Global's expansion journey is remarkable. In 2021, amid the pandemic, the company expanded its presence by establishing an office in Delhi. The subsequent year, 2023, was pivotal, dedicated to sustainability, strategizing, and streamlining operations. Noteworthy is the company's exceptional record of delivering an MVP in just 54 days, showcasing the team's supercharged capabilities. As we step into 2024, WaysAhead Global is geared up for a year of significant growth and scalability, building upon its strong foundation and successful track record."},
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
        query = "SELECT session_id FROM Wayschat_hist WHERE session_id = ?"
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
        
def klaaplanet_bot():
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
            response = gpt(user_input, conversation_history)
            conversation_history.append({"role": "assistant", "content": response})
            chat_counter += 1
            store_chat(response,user_input,session)
            return response
    return chatbot
def extract_tags(text):
    tags = []
    tag_keywords = {
    'WaysAheadGlobal': ['WaysAhead Global', 'company'],
    'DigitalTransformation': ['digital transformation'],
    'DataAnalytics': ['data analytics', 'insights'],
    'AI': ['artificial intelligence', 'AI'],
    'Rupam': ['Rupam' , 'journey of Rupam', 'experience of Rupam'],
    'StartupServices': ['startup services', 'entrepreneurship'],
    'MVPDevelopment': ['Minimum Viable Product', 'development'],
    'Vision': ['vision', 'company vision'],
    'DataManagement': ['data management', 'Data 360'],
    'Web3': ['Web 3.0', 'decentralization'],
    'Blockchain': ['blockchain', 'Blockchain technology'],
    'ARVR': ['AR/VR', 'augmented reality', 'virtual reality'],
    'Brands': ['Skills21', 'UNOMIRU'],
    'SoftSkillsAssessment': ['soft skills assessment'],
    'CustomerExperience': ['customer experience'],
    'PhilosophyOfData': ['philosophy of data', 'data-driven'],
    'Innovations': ['innovations', 'disruptive'],
    'Idea2MVP': ['Idea to MVP', 'startup incubation'],
    'BusinessIntelligence': ['business intelligence', 'BI'],
    'BIKiosk': ['BI kiosk', 'dashboards'],
    'HealthcareAnalytics': ['healthcare analytics'],
    'ManagedServices': ['managed services', 'outsourcing'],
    'Microservices': ['microservices', 'service integration'],
    'GamingAnalytics': ['gaming analytics'],
    'FinancialServices': ['financial services', 'fintech'],
    'PermanentResidency': ['permanent residency', 'immigration'],
    'TalentManagement': ['talent management', 'workforce analytics'],
    'FAQs': ['frequently asked questions', 'FAQs'],
    'Web3Characteristics': ['Web 3.0 characteristics'],
    'Web3Applications': ['Web 3.0 applications'],
    'StartupSupport': ['startup support', 'advisory services', 'mentorship'],
    'InvestorRelations': ['investor relations', 'pitching', 'investor engagement'],
    'MarketResearch': ['market research', 'industry analysis', 'competitor research'],
    'BusinessGrowth': ['business growth', 'scaling strategies', 'expansion'],
    'FinancialManagement': ['financial management', 'budgeting', 'financial planning'],
    'LegalCompliance': ['legal compliance', 'regulatory requirements', 'compliance'],
    'EntrepreneurshipSkills': ['entrepreneurship skills', 'innovation', 'leadership'],
    'TechnologyAdoption': ['technology adoption', 'digital transformation', 'tech integration'],
    'CustomerAcquisition': ['customer acquisition', 'marketing strategies', 'customer retention'],
    'WorkLifeBalance': ['work-life balance', 'stress management', 'well-being'],
    'Motivation': ['motivation', 'inspiration', 'keep going'],
    'LearningOpportunities': ['learning opportunities', 'skill development', 'continuous learning'],
    'GreenTechnology': ['green technology', 'sustainability', 'environment-friendly'],
    'HealthcareInnovation': ['healthcare innovation', 'medical advancements', 'telemedicine'],
    'Events': ['events', 'webinars', 'workshops'],
    'SuccessStories': ['success stories', 'inspiring startups', 'case studies'],
    'IndustryCollaborations': ['industry collaborations', 'partnerships', 'collaborative projects'],
    'VirtualTeamManagement': ['virtual team management', 'remote collaboration', 'distributed teams'],
    'InclusiveWorkplace': ['inclusive workplace', 'diversity and inclusion', 'equal opportunities'],
    'EmployeeEngagement': ['employee engagement', 'team building', 'company culture'],
    'TechStartupFunding': ['tech startup funding', 'investment rounds', 'venture capital'],
    'HealthcareInnovationFunding': ['healthcare innovation funding', 'biotech investments', 'medical research grants'],
    'CSR': ['corporate social responsibility', 'community initiatives', 'sustainability'],
    'CompanyCulture': ['company culture', 'values', 'teamwork', 'diversity', 'employee satisfaction'],
    'IndustryRecognition': ['industry recognition', 'awards', 'accolades'],
    'Partnerships': ['partnerships', 'collaborations', 'strategic alliances'],
    'ClientSuccessStories': ['client success stories', 'testimonials', 'case studies'],
    'TrainingDevelopment': ['training and development', 'employee education', 'skill enhancement'],
    'QualityAssurance': ['quality assurance', 'certifications', 'compliance standards'],
    'ThoughtLeadership': ['thought leadership', 'industry insights', 'research publications'],
    }
    for pattern_tag, keywords in tag_keywords.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            tags.append(pattern_tag)
    return tags

def get_user_info_database_connection():
    user_info_conn = pyodbc.connect(db_connection_string)
    user_info_cursor = user_info_conn.cursor()
    return user_info_conn, user_info_cursor

def store_chat(response,user,session_id):
        current_datetime = datetime.utcnow()
        formatted_date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        user_info_conn, user_info_cursor = get_user_info_database_connection()
        user_info_cursor.execute('''
            INSERT INTO  Wayschat_hist (User_input,Bot_response,Date,session_id) VALUES (?, ?, ?,?)
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
    cursor.execute('''INSERT INTO tb_Ways_chat (name, email, phone, sentiment, probability, tags, Date, duration, session_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, phone, average_sentiment, probability, tags_str, formatted_date, duration, session_id))
    cursor.commit()



chatbot_model= klaaplanet_bot()

@app.route('/api/Waysbot')
def index():
    return render_template("index.html")

@app.route('/api/Waysbot/chat', methods=['POST'])
def chat():
    global conversation_history
    global session_start_time
    start_time = time.time()
    session=request.headers["session-id"]
    user_input = request.json.get('user_input')
    if user_input.lower() in ['bye', 'exit', 'quit']:
        response = "Goodbye!"
        conversation_history = []
    elif user_input.lower() in ['hi', 'hello', 'hey']:
        response = "Hello! How can I assist you today?"
    else:
        response = chatbot_model(user_input,session)
    end_time = time.time()
    time_taken = (end_time - start_time)
    conn = pyodbc.connect(db_connection_string)
    cursor = conn.cursor()
    query = """UPDATE Wayschat_hist 
               SET response_time = ?  
               WHERE session_id = ?"""
    cursor.execute(query,time_taken,session)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'response': response})

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']
        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data)

        return jsonify({'transcription': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=False,port=3026)
