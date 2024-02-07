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

@app.route("/generate_sessionid",methods=['GET'])
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
                {"role": "system", "content": "You are a helpful assistant, named WA-BOT , for WaysAhead Global.You are a part of the waysahead family so you always talk in first person and you are still being trained and You provide complete and comprehensive answers to customers, demonstrating extensive knowledge about the company and its digital transformation services. Your responses are precise, within 250 tokens, sensible, and delivered in a friendly manner. You engage in conversations with the customers and cover all aspects of WaysAhead Global's offerings."},
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
        query = "SELECT session_id FROM Kalaachat_hist WHERE session_id = ?"
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
        nonlocal c       
        user_input_processed = preprocess_text(user_input)        
        fetched_data = fetch_session_id_from_database(session) 
        if not fetched_data:
            sentiment_scores = []
            conversation_history = []
            tags=[]
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
        'kalaaplanet_info': ['Kalaaplanet', 'art', 'Indian arts', 'art forms', 'products'],
        'art_categories': ['paintings', 'sculptures', 'crafts', 'traditional art', 'contemporary art', 'fusion art'],
        'buying_process': ['purchase', 'buying', 'Get Quote', 'art acquisition'],
        'delivery_time': ['delivery time', 'shipping', 'estimated delivery date'],
        'shipping_costs': ['shipping costs', 'shipping expenses', 'cost calculation'],
        'art_collaborations': ['collaborations', 'international artists', 'artist-in-residence', 'cultural exchanges'],
        'sustainable_art_practices': ['sustainable art practices', 'eco-friendly', 'environmental impact'],
        'art_education_advocacy': ['art education advocacy', 'collaboration with educational institutions', 'sponsorship'],
        'traditional_contemporary_fusion': ['traditional and contemporary art', 'global dialogue', 'artistic expressions'],
        'empowering_young_artists': ['empowering young artists', 'scholarships', 'mentorship programs'],
        'technology_in_art_creation': ['technology in art creation', 'digital tools', 'augmented reality'],
        'promoting_art_career_choice': ['promoting art as a career choice', 'career counseling', 'art institutions'],
        'supporting_public_art_installations': ['supporting public art installations', 'local authorities', 'urban landscapes'],
        'celebrating_traditional_festivals': ['celebrating traditional festivals through art', 'festive collections'],
        'collaboration_with_educational_institutions': ['collaboration with educational institutions', 'art workshops'],
        'preservation_of_architectural_heritage': ['preservation of architectural heritage through art', 'artworks'],
        'art_therapy_for_mental_well-being': ['art therapy for mental well-being', 'mental health professionals'],
        'celebrating_diversity_of_indian_folklore': ['celebrating diversity of Indian folklore through art', 'thematic collections'],
        'supporting_artists_with_disabilities': ['supporting artists with disabilities', 'inclusive initiative'],
        'promoting_art_as_tool_for_social_change': ['promoting art as a tool for social change', 'social impact organizations'],
        'art_exhibition_events': ['art exhibition events', 'gallery showcases', 'public exhibitions'],
        'artistic_collaborations_community': ['artistic collaborations with the community', 'community engagement projects'],
        'art_awards_recognition': ['art awards and recognition', 'artist accolades', 'excellence in art'],
        'art_fairs_participation': ['participation in art fairs', 'national and international art events'],
        'digital_platform_showcases': ['digital platform showcases', 'online exhibitions', 'virtual art experiences'],
        'art_curation_process': ['art curation process', 'curatorial decisions', 'exhibition planning'],
        'art_collection_investment': ['art collection as an investment', 'collectible artworks', 'art market trends'],
        'customer_feedback_art_purchases': ['customer feedback on art purchases', 'testimonials', 'satisfied buyers'],
        'artist_profiles_and_interviews': ['artist profiles and interviews', 'behind-the-art stories', 'creative insights'],
        'artistic_merchandise_offers': ['artistic merchandise offers', 'limited edition products', 'exclusive art items'],
        'art_in_social_media': ['art presence in social media', 'online art communities', 'creative platforms'],
        'art_and_culture_discussions': ['art and culture discussions', 'panel talks', 'cultural forums'],
        'art_market_trends': ['art market trends', 'collectors',' preferences', 'market analysis'],
        'art_influencers_collaborations': ['art influencers collaborations', 'social media influencers', 'creative partnerships'],
        'art_and_wellness_connections': ['art and wellness connections', 'mindfulness through art', 'creative therapies'],
        'art_in_public_spaces_projects': ['art in public spaces projects', 'city beautification', 'public art initiatives'],
        'art_and_technology_integration': ['art and technology integration', 'interactive art installations', 'tech-driven art'],
        'art_commissions_customizations': ['art commissions and customizations', 'bespoke artworks', 'personalized art'],
        'art_and_philanthropy': ['art and philanthropy', 'charity auctions', 'art for a cause'],
        'art_in_hospitality_industry': ['art in hospitality industry', 'hotel collaborations', 'creative ambiance'],
        'art_and_environmental_consciousness': ['art and environmental consciousness', 'eco-friendly initiatives', 'green art'],
        'art_and_historical_narratives': ['art and historical narratives', 'historical themes', 'cultural storytelling'],
        'art_and_literature_connections': ['art and literature connections', 'visual storytelling', 'literary collaborations'],
        'art_as_corporate_gifts': ['art as corporate gifts', 'customized corporate artworks', 'business partnerships'],
        'art_and_emerging_technologies': ['art and emerging technologies', 'innovative art forms', 'experimental artworks'],
        'art_for_interior_design': ['art for interior design', 'home decor solutions', 'art in living spaces'],
        'art_and_religious_cultural_celebrations': ['art and religious/cultural celebrations', 'festive art collections'],
        'art_for_social_media_campaigns': ['art for social media campaigns', 'visual content creation', 'digital marketing'],
        'art_and_pop_culture_references': ['art and pop culture references', 'contemporary trends', 'cultural influences'],
        'art_and_educational_programs': ['art and educational programs', 'creative learning initiatives', 'art workshops'],
        'art_in_rehabilitation_centers': ['art in rehabilitation centers', 'therapeutic art programs', 'healing through art'],
        'art_and_gender_representation': ['art and gender representation', 'gender equality in art', 'diverse artistic voices'],
        'art_and_technology_collaborative_projects': ['art and technology collaborative projects', 'tech-art experiments', 'innovation fusion'],
        'art_and_intercultural_dialogue': ['art and intercultural dialogue', 'cross-cultural art projects', 'global artistic exchange'],
        'art_in_corporate_workspaces': ['art in corporate workspaces', 'office art installations', 'creative workplace culture'],
        'art_and_digital_reproduction': ['art and digital reproduction', 'limited edition prints', 'digital art accessibility'],
        'art_and_sustainability_projects': ['art and sustainability projects', 'eco-friendly art initiatives', 'environmental awareness through art'],
        'art_in_political_activism': ['art in political activism', 'social justice art', 'creative protest expressions'],
        'art_and_community_regeneration': ['art and community regeneration', 'urban art projects', 'neighborhood revitalization'],
        'art_and_aging_population': ['art and aging population', 'creative aging programs', 'art for seniors'],
        'art_and_corporate_branding': ['art and corporate branding', 'brand collaboration through art', 'visual brand identity'],
        'art_and_sensory_experiences': ['art and sensory experiences', 'multi-sensory art installations', 'interactive art displays'],
        'art_and_culinary_collaborations': ['art and culinary collaborations', 'food and art fusion', 'culinary art experiences'],
        'art_and_space_design': ['art and space design', 'architectural collaborations', 'artistic spatial concepts'],
        'art_and_personal_expression': ['art and personal expression', 'individualistic art creation', 'self-discovery through art'],
        'art_and_virtual_reality': ['art and virtual reality', 'VR art experiences', 'immersive digital artworks'],
        'art_in_prison_reformation': ['art in prison reformation', 'inmate art programs', 'rehabilitative art practices'],
        'art_and_civic_engagement': ['art and civic engagement', 'community art projects', 'public involvement through art'],
        'art_and_body_positivity': ['art and body positivity', 'inclusive body image representations', 'celebrating diverse beauty'],
        'art_and_social_entrepreneurship': ['art and social entrepreneurship', 'creative ventures for social impact', 'artistic solutions for societal issues'],
        'art_and_emotional_wellbeing': ['art and emotional wellbeing', 'expressive art therapy', 'mental health awareness through art'],
        'art_and_historical_preservation': ['art and historical preservation', 'cultural heritage conservation', 'historical restoration through art'],
        'art_and_disability_inclusion': ['art and disability inclusion', 'accessible art programs', 'inclusive artistic spaces'],
        'art_and_experiential_marketing': ['art and experiential marketing', 'brand experiences through art', 'event marketing with a creative touch'],
        'art_and_nature_conservation': ['art and nature conservation', 'environmental art projects', 'wildlife awareness through art'],
        'art_and_language_of_creativity': ['art and language of creativity', 'expressive arts communication', 'visual storytelling'],
        'art_in_digital_advertising': ['art in digital advertising', 'visual content for ads', 'creative advertising campaigns'],
        'art_and_internet_culture': ['art and internet culture', 'online art communities', 'digital art trends'],
        'art_and_consumer_behavior': ['art and consumer behavior', 'psychology of art in marketing', 'visual appeal in consumer choices'],
        'art_and_religious_spirituality': ['art and religious spirituality', 'sacred art traditions', 'spiritual symbolism in art']
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
    cursor.execute('''INSERT INTO  tb_Ways_chat (name, email, phone, sentiment, probability, tags, Date, duration, session_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, phone, average_sentiment, probability, tags_str, formatted_date, duration, session_id))
    cursor.commit()



chatbot_model= klaaplanet_bot()

@app.route('/')
def index():
    return render_template("frontendupdated (3).html")

@app.route('/api/chat', methods=['POST'])
def chat():
    global conversation_history
    global session_start_time
    start_time = time.time()
    session=request.headers["session-id"]
    user_input = request.form['user_input']
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
    query = """UPDATE Kalaachat_hist 
               SET response_time = ?  
               WHERE session_id = ?"""
    cursor.execute(query,time_taken,session)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'response': response})


if __name__ == "__main__":
    app.run(debug=False)