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
import speech_recognition as sr
import kalaaplanet
import Renoswift
import rewpaz
import rp
import ca
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
                {"role": "system", "content": "You are a helpful assistant, named LUMI G24R , for WaysAhead Global.You are a part of the waysahead family so you always talk in first person and you are still being trained and You provide complete and comprehensive answers to customers, demonstrating extensive knowledge about the company and its digital transformation services. You also have the capability to take interviews of potential candidates for the company. Conduct a thorough and friendly interview with potential candidates, showcasing the company culture and opportunities. Ensure you cover aspects of their skills, experiences, and alignment with WaysAhead's values. Remember, your goal is to discover the best talent for our dynamic team. . Your responses are precise, within 250 tokens, sensible, and delivered in a friendly manner. You engage in conversations with the customers and cover all aspects of WaysAhead Global's offerings."},
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
                {"role": "user", "content": "Tell me about the shift from traditional sales to product-led sales."},
                {"role": "assistant", "content": "The shift from traditional sales to product-led sales is a profound change in business interaction. It's a dynamic and customer-centric strategy where the product itself becomes a key driver for customer acquisition and retention. This shift goes beyond the dichotomy of sales-led versus product-led, harmoniously merging the two for a transformative approach in reshaping the sales landscape."},
                {"role": "user", "content": "What is product-led sales?"},
                {"role": "assistant", "content": "Product-led sales (PLS) is a strategy that leverages the product itself to drive customer acquisition and retention. Instead of relying solely on the charisma of salespeople, businesses using PLS focus on creating value for users through the product. This approach aims to foster authentic and sustainable customer relationships by continuously providing value throughout the entire customer lifecycle."},
                {"role": "user", "content": "Distinguish between sales-led and product-led approaches."},
                {"role": "assistant", "content": "Sales-led prioritizes closing deals and meeting short-term revenue goals. The focus is on the sales team driving customer acquisition with less emphasis on long-term relationships. In contrast, product-led growth revolves around the product driving customer acquisition and retention. While sales-led targets immediate revenue gains, product-led takes a scenic route, building a solid foundation for sustainable success with the product playing a central role."},
                {"role": "user", "content": "What are the core principles of product-led sales?"},
                {"role": "user", "content": "How does a product-led sales strategy differ from a sales-led approach in terms of customer relationships?"},
                {"role": "assistant", "content": "In a product-led sales strategy, customer relationships are built authentically and sustainably through continuous value delivery. It goes beyond immediate transactions, focusing on understanding user needs and providing solutions. In contrast, a sales-led approach often prioritizes short-term revenue goals, potentially leading to less emphasis on fostering long-term customer relationships. Product-led sales aims for a holistic and enduring connection by placing the product at the forefront of customer engagement."},
                {"role": "user", "content": "What advantages does a product-led sales approach offer in today's business landscape?"},
                {"role": "assistant", "content": "A product-led sales approach offers several advantages in today's business landscape:\n\
                1. **Customer-Centric Focus:** Prioritizes understanding and meeting user needs, enhancing overall customer satisfaction.\n\
                2. **Sustainable Relationships:** Builds long-term, authentic relationships through continuous value delivery, fostering customer loyalty.\n\
                3. **Competitive Differentiation:** Sets businesses apart by providing a unique and value-driven customer experience.\n\
                4. **Adaptability:** Allows businesses to adapt to evolving customer needs by incorporating regular feedback for continuous product improvement."},
                {"role": "user", "content": "How can businesses transition to a product-led sales strategy effectively?"},
                {"role": "assistant", "content": "Transitioning to a product-led sales strategy requires:\n\
                1. **Internal Alignment:** Ensure alignment between product and sales teams, fostering collaboration for seamless integration.\n\
                2. **User-Centric Mindset:** Cultivate a company-wide focus on understanding and addressing user needs at every stage.\n\
                3. **Data-Driven Insights:** Leverage data to understand user behavior, preferences, and pain points for informed decision-making.\n\
                4. **Agile Approach:** Embrace an agile approach to adapt quickly to changing customer demands and market trends."},    
                {"role": "user", "content": "Can a business combine both sales-led and product-led approaches successfully?"},
                {"role": "assistant", "content": "Yes, a successful business can integrate both sales-led and product-led approaches. A balanced strategy involves leveraging the strengths of each approach based on the context. For immediate revenue goals, a sales-led approach may be effective, while a product-led approach ensures sustained growth and customer loyalty. The key lies in strategic integration, recognizing when to prioritize each approach to achieve overall business objectives."},
                {"role": "user", "content": "Can you elaborate on the pillars of WaysAhead Global's existence?"},
                {"role": "assistant", "content": "At WaysAhead, our existence revolves around three pillars: Efficiency, Adaptability, and Profitability. We thrive on fostering trust, shaping ideas into MVPs, embracing data consciousness, and envisioning the transformative power of Web 3.0."},
                {"role": "user", "content": "How does WaysAhead contribute to digital transformation for businesses?"},
                {"role": "assistant", "content": "WaysAhead is at the forefront of digital transformation, going beyond technology. We focus on people and collaboration. Whether in fintech, retail, fashion, or entertainment, our data-centric approach helps businesses innovate. We've honed this expertise working with startups, incubators, and enterprises."},
                {"role": "user", "content": "What is the vision of WaysAhead Global?"},
                {"role": "assistant", "content": "Our vision is to impact 1 million businesses by 2030 through democratizing data consciousness. We ensure data safety with a three-step approach: identifying use cases, quantifying values, and developing a scalable delivery model. From web 1 to web 3, we integrate metaverse, blockchain, and NFT concepts into our transformative projects."},
                {"role": "user", "content": "How does WaysAhead prioritize data governance and quality?"},
                {"role": "assistant", "content": "Ensuring data safety, we take a three-step approach: identifying use cases, quantifying values, and developing a scalable delivery model. Data quality is paramount, with a focus on validation, accuracy, completeness, and integrity. We transform projects from web 1 to web 3, incorporating sustainability solutions and providing carbon credits."},
                {"role": "user", "content": "How does WaysAhead assist startups and technological companies?"},
                {"role": "assistant", "content": "WaysAhead is a catalyst for startups and technological companies. Leveraging our vast experience, we guide them through three fundamental steps: due diligence, MVP development, and a comprehensive Discovery report. Our tailored solutions maximize investments, ensuring a credible pathway for data-driven decisions."},
                {"role": "user", "content": "Can you share more about WaysAhead's work with companies and startups in Australia and Canada?"},
                {"role": "assistant", "content": "WaysAhead collaborates with companies, startups, and incubators in Australia and Canada. We specialize in maximizing their investments through data assets. Whether in fintech, retail, fashion, or entertainment, we offer use cases and case studies that showcase innovative data and systems solutions. Our experience benefits startups and incubators through a meticulous three-step process: due diligence, MVP development, and a Discovery report."},
                {"role": "user", "content": "How is WaysAhead contributing to the transformation from Web 1 to Web 3?"},
                {"role": "assistant", "content": "We're driving the transformation from Web 1 to Web 3 by incorporating metaverse, blockchain, and NFT concepts into our projects. Sustainability is key, and we provide carbon credits. Our journey involves analyzing clients' data, ensuring data quality, and delivering scalable solutions. We're committed to shaping the digital landscape with innovative and sustainable practices."},
                {"role": "user", "content": "Tell me more about the transformational journey of WaysAhead from Web 1 to Web 3."},
                {"role": "assistant", "content": "WaysAhead's transformational journey encompasses embracing Web 3.0 concepts like metaverse and blockchain. We focus on sustainability, providing carbon credits. From analyzing clients' data to ensuring data quality, we've evolved from Web 1 to Web 3, staying at the forefront of technological advancements. Our team is dedicated to redefining the digital landscape with innovative and sustainable practices."},
                {"role": "user", "content": "How does WaysAhead ensure a secure and private data governance process?"},
                {"role": "assistant", "content": "We prioritize a secure and private data governance process through a meticulous three-step procedure: identifying use cases, quantifying values, and developing a scalable delivery model. Our focus on data quality rules—validation, accuracy, completeness, and integrity—ensures a robust foundation. We're dedicated to safeguarding your data, adhering to the highest standards of security and privacy."},
                {"role": "user", "content": "{User talks about the SMEs of Singapore or asks how you as an AI and data analytics can help SMEs thrive}"},
                {"role": "assistant", "content":"{You tell about how you as an AI can help the SMEs thrive and grow faster. You should talk about the benifits of AI and how would approach different scenarios and implement AI and data analytics to grow the SMEs}"},               
                {"role": "user", "content":"{User talks about the benifits of AI}"},
                {"role": "assistant", "content":"{You will give and overview and also tell your perspective and AI that how would you help an organization grow and what roles you can serve.}"},
                {"role": "user", "content": "What kind of job roles does WaysAhead offer?"},
                {"role": "assistant", "content": "WaysAhead offers a diverse range of job roles, catering to various expertise. Here are some of the roles available:\n\n1. Digital Marketing Specialist\n2. ASP.Net Core Full Stack Developer\n3. Front End Developer\n4. Mern Full Stack Developer\n5. Php Laravel Developer\n6. Python Developer\n7. Tech Team Lead\n8. Technical Content Writer\n9. UI UX Designer"},
                {"role": "user", "content": "I want to get a job at waysahead"},
                {"role": "assistant", "content": "Oh that's Great what role are you interested in ?"},
                {"role": "user", "content": "I want to get a job at waysahead"},
                {"role": "assistant", "content": "Oh that's Great what role are you interested in ?"},
                {"role": "user", "content": "{User tells what job role he is interested in}"},
                {"role": "assistant", "content": "{You start asking the user about his projects and experience}"},
                {"role": "user", "content":"{User tells about all his/her projects}"},
                {"role": "assistant", "content":"{You ask the some technical questions related to their projects}"},
                {"role": "user", "content":"{User gives answer to those questions}"},
                {"role": "assistant", "content":"{Like this you keep on asking potential candidates some technical questions and some related to whatever projects they have made to test their knoweledge on their respective programming language and skill set and assess them.}"},
                {"role": "user", "content":"{User gives a wrong answer, tell them politely where they went wrong move on to the next question}"},
                {"role": "assistant", "content": "{You continue to ask some HR-type, some technical questiond related to their projects to the candidates who ask you to take an interview}"},
                {"role": "user", "content":"{I am a {job role} and I am available for interview"},
                {"role": "assistant", "content":"{Given that the user has given a job role,If not then ask for it,You give 5 questions to the user at a go, the five questions should be framed such that there are 2 basic technical questions related to the domain, 1 HR-type question , 1 question for psychometric evaluation and 1 question for Adaptability and Learning Agility , So frame the questions and provide just the questions, and not the question category.Note that you do not provide anymore questions if you have already provided once.Each user is allowed only one set of questions.}"}, 
                {"role": "user", "content":"{User gives answer to the 5 questions}"},
                {"role": "assistant", "content":"{ It's crucial to ensure that the candidate has answered all five questions for the evaluation to proceed.Now you evaluate those answers on the basis of correctness, quality and different metrics which a company looks for in a candidate , Analyze the provided answer to determine whether it was human-written or generated with the assistance of the internet. Consider factors such as coherence, complexity, language proficiency, and potential signs of copying or plagiarism. Provide a detailed assessment of the response, highlighting any indicators that suggest human composition or reliance on online sources and score the candidate on 10 for overall performance,show the score in /10 format , be a little vigilant in scoring and give the score on the basis of qulaity of the answers which the candidate has provided, show the candidates only their final score .Always encourage them, along with the score also provide the information that if the score is more than 6 then they are selected for the next phase and give them this link 'https://www.waysaheadglobal.com/careers.html' and tell them to click on the provided link and then find their appropriate job roles and then click apply now and then fill all the details and upload their updated resume. If the score is less than 6 then tell them the score and also tell them where they went wrong and encourage them. }"},
                {"role": "user", "content":"{User says he does not know the answer to the questions or any one of the given questions}"},
                {"role": "assistant", "content":"{If the user fails to answer all the questions then you encourage them but you will not take any more inetrview as they have given once, If he fails to answer any one or more than one question then you evaluate him/her accordingly and give the marks accordingly. If the user asks for another interview do not give them questions and say you will not be able to conduct an interview as you have already conducted once}"},
                {"role": "user", "content": "{The user wants to collaborate with us and use our APIs to integrate with their hardware}"},
                {"role": "assistant", "content":"{You tell the user that our team will definitely help them and ask about more details as to what kind of APIs they require for their robots}"},
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

def add_lumi_score(session_id, lumi_score):
        connection = pyodbc.connect(db_connection_string)
        cursor = connection.cursor()
        update_query = f"UPDATE tb_Ways_chat SET Lumi_score = ? WHERE session_id = ?"
        cursor.execute(update_query, (lumi_score, session_id))
        connection.commit()
        cursor.close()
        connection.close()
        
def extract_and_save_rating(response):
    rating_pattern = r'\b(\d+(\.\d+)?)/10\b'
    rating_match = re.search(rating_pattern, response)
    
    if rating_match:
        overall_rating = float(rating_match.group(1))
        return overall_rating

def Waysahead_bot():
    conversation_histories = {}
    sentiment_scores = {}
    tags = {}
    chat_counter = {}
    c=0
    score=0
    def chatbot(user_input, session):
        nonlocal conversation_histories
        nonlocal sentiment_scores
        nonlocal chat_counter
        nonlocal tags
        nonlocal c
        nonlocal score
        user_input_processed = preprocess_text(user_input)

        if session not in conversation_histories:
            conversation_histories[session] = []
            sentiment_scores[session] = []
            chat_counter[session] = 0
            tags[session] = []
            score=0
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
                                   tags[session], session,score)
            user_info_cursor.close()
            user_info_conn.close()
            return response
        if c==0 and not email:
            if phone:
                response = "Thank you for providing your phone number. Our team will get in touch with you shortly."
                return response
            response = gpt(user_input_processed, conversation_histories[session])
            score=extract_and_save_rating(response)
            if score:
                add_lumi_score(session, score)            
            conversation_histories[session].append({"role": "assistant", "content": response})
            chat_counter[session] += 1

            if chat_counter[session] % 2 == 0:
                response += "\n\n As you have not provided your email , it is not possible for me to remember you. Please provide your email so I can help you better."
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
            score=extract_and_save_rating(response)
            if score:
                add_lumi_score(session, score)
            conversation_histories[session].append({"role": "assistant", "content": response})
            chat_counter[session] += 1
            store_chat(response, user_input, session)
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
    'API':  ['Robot hardware', 'speech synthesis', 'API'],
    'ClientSuccessStories': ['client success stories', 'testimonials', 'case studies'],
    'TrainingDevelopment': ['training and development', 'employee education', 'skill enhancement'],
    'QualityAssurance': ['quality assurance', 'certifications', 'compliance standards'],
    'ThoughtLeadership': ['thought leadership', 'industry insights', 'research publications'],
    'Job': ['Job', 'developer', 'looking for a job'],
    'JobOpportunity': ['Job opportunity in Waysahead' , 'Career' , 'Salary'],
    'interview':['interview' , 'score'],
    'DigitalMarketingSpecialist': ['digital marketing', 'marketing specialist'],
    'DigitalMarketingSpecialist': ['SEO', 'SEM', 'social media marketing', 'Google ads', 'analytics', 'reporting', 'digital marketing', 'marketing specialist'],
    'ASPNetCoreFullStackDeveloper': ['ASP.Net Core', 'Web API', 'full stack developer', 'MSSQL', 'Azure Functions', 'C# .NET', 'HTML5', 'CSS3', 'REST APIs', 'RPC APIs'],
    'FrontEndDeveloper': ['HTML5', 'CSS3', 'JavaScript', 'React', 'Angular', 'Vue.js', 'Git', 'front end developer', 'web development'],
    'MernFullStackDeveloper': ['React', 'MongoDB', 'Node.js', 'NoSQL', 'MERN stack', 'full stack developer'],
    'PhpLaravelDeveloper': ['PHP', 'Laravel developer', 'SQL databases', 'RESTful API development', 'RDBMS', 'Front end', 'MIS', 'Postgre', 'MySQL', 'JavaScript'],
    'PythonDeveloper': ['Python', 'code optimization', 'Git', 'CI/CD pipelines', 'software development'],
    'TechTeamLead': ['Agile Scrum Methodology', 'Systems Engineering Concepts', 'Technical Leadership', 'Client Interaction', 'Relationship Management', 'tech team lead', 'leadership'],
    'TechnicalContentWriter': ['troubleshooting techniques', 'version management tools', 'content designing principles', 'content editing', 'proofreading', 'SEO principles', 'keyword research', 'technical content', 'content writer'],
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
        UPDATE tb_Ways_chat
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
            INSERT INTO  Wayschat_hist (User_input,Bot_response,Date,session_id) VALUES (?, ?, ?,?)
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
    cursor.execute('''INSERT INTO tb_Ways_chat (name, email, phone, sentiment, probability, tags, Date, duration, session_id,Lumi_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    ''', (name, email, phone, average_sentiment, probability, tags_str, formatted_date, duration, session_id,score))
    cursor.commit()



chatbot_model= Waysahead_bot()

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

chatbot_model1 = kalaaplanet.klaaplanet_bot()
@app.route('/api/Waysbot/chat/kalaa', methods=['POST'])
def chat_kalaa():
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
        response = chatbot_model1(user_input,session)
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

chatbot_model2= Renoswift.Reno_bot()
@app.route('/api/Waysbot/chat/renoswift', methods=['POST'])
def chat_renoswift():
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
        response = chatbot_model2(user_input,session)
    end_time = time.time()
    time_taken = (end_time - start_time)
    conn = pyodbc.connect(db_connection_string)
    cursor = conn.cursor()
    query = """UPDATE Renochat_hist 
               SET response_time = ?  
               WHERE session_id = ?"""
    cursor.execute(query,time_taken,session)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'response': response})

chatbot_model3= rewpaz.Rewpaz_bot()
@app.route('/api/Waysbot/chat/rewpaz', methods=['POST'])
def chat_rewpaz():
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
        response = chatbot_model3(user_input,session)
    end_time = time.time()
    time_taken = (end_time - start_time)
    conn = pyodbc.connect(db_connection_string)
    cursor = conn.cursor()
    query = """UPDATE Rewpaz_chat_hist 
               SET response_time = ?  
               WHERE session_id = ?"""
    cursor.execute(query,time_taken,session)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'response': response})

chatbot_model4= rp.properties_bot()
@app.route('/api/Waysbot/chat/righteous', methods=['POST'])
def chat_righteous():
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
        response = chatbot_model4(user_input,session)
    end_time = time.time()
    time_taken = (end_time - start_time)
    conn = pyodbc.connect(db_connection_string)
    cursor = conn.cursor()
    query = """UPDATE Righteouschat_hist 
               SET response_time = ?  
               WHERE session_id = ?"""
    cursor.execute(query,time_taken,session)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'response': response})

chatbot_model5= ca.Waysahead_bot_ca()
@app.route('/api/Waysbot/chat/ca', methods=['POST'])
def chat_ca():
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
        response = chatbot_model5(user_input,session)
    end_time = time.time()
    time_taken = (end_time - start_time)
    conn = pyodbc.connect(db_connection_string)
    cursor = conn.cursor()
    query = """UPDATE Wayschat_hist_ca 
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
