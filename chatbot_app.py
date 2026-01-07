"""
🏥 Hospital Chatbot - Interactive Query Interface
-------------------------------------------------
A conversational chatbot interface for querying hospital data from Neo4j.
"""

import streamlit as st
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🏥 Hospital Chatbot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .query-result {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Neo4j Connection
class HospitalChatbot:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def find_hospitals(self):
        """Get all hospitals"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (h:Hospital)
                RETURN h.name AS name, h.state_name AS state
                ORDER BY h.name
            """)
            return [dict(record) for record in result]
    
    def find_patients_by_physician(self, physician_name):
        """Find all patients treated by a specific physician"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (patient:Patient)-[:HAS]->(visit:Visit)<-[:TREATS]-(physician:Physician)
                WHERE physician.name CONTAINS $name
                RETURN DISTINCT patient.name AS patient, 
                       physician.name AS physician,
                       COUNT(visit) AS visit_count
                ORDER BY visit_count DESC
            """, name=physician_name)
            return [dict(record) for record in result]
    
    def get_hospital_stats(self, hospital_name):
        """Get statistics for a specific hospital"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (h:Hospital {name: $name})
                OPTIONAL MATCH (v:Visit)-[:AT]->(h)
                OPTIONAL MATCH (h)-[:EMPLOYS]->(p:Physician)
                RETURN h.name AS hospital,
                       h.state_name AS state,
                       COUNT(DISTINCT v) AS total_visits,
                       COUNT(DISTINCT p) AS total_physicians
            """, name=hospital_name)
            return result.single()
    
    def get_patient_history(self, patient_name):
        """Get full medical history for a patient"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (patient:Patient)-[:HAS]->(visit:Visit)
                WHERE patient.name CONTAINS $name
                MATCH (visit)-[:AT]->(hospital:Hospital)
                MATCH (visit)<-[:TREATS]-(physician:Physician)
                OPTIONAL MATCH (visit)-[:COVERED_BY]->(payer:Payer)
                RETURN patient.name AS patient,
                       visit.admission_date AS date,
                       hospital.name AS hospital,
                       physician.name AS physician,
                       visit.diagnosis AS diagnosis,
                       visit.chief_complaint AS complaint,
                       payer.name AS insurance
                ORDER BY visit.admission_date DESC
            """, name=patient_name)
            return [dict(record) for record in result]
    
    def search_by_diagnosis(self, diagnosis):
        """Search visits by diagnosis"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (visit:Visit)-[:AT]->(hospital:Hospital)
                MATCH (patient:Patient)-[:HAS]->(visit)
                WHERE visit.diagnosis CONTAINS $diagnosis
                RETURN patient.name AS patient,
                       hospital.name AS hospital,
                       visit.diagnosis AS diagnosis,
                       visit.admission_date AS date
                ORDER BY visit.admission_date DESC
                LIMIT 10
            """, diagnosis=diagnosis)
            return [dict(record) for record in result]
    
    def get_all_physicians(self):
        """Get all physicians"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Physician)
                RETURN p.name AS name, p.school AS school, p.salary AS salary
                ORDER BY p.name
            """)
            return [dict(record) for record in result]
    
    def get_reviews_by_hospital(self, hospital_name):
        """Get patient reviews for a hospital"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (visit:Visit)-[:AT]->(hospital:Hospital {name: $name})
                MATCH (visit)-[:WRITES]->(review:Review)
                RETURN review.text AS review,
                       review.patient_name AS patient,
                       review.physician_name AS physician
                LIMIT 10
            """, name=hospital_name)
            return [dict(record) for record in result]

# Initialize chatbot
@st.cache_resource
def init_chatbot():
    return HospitalChatbot(
        uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        user=os.getenv("NEO4J_USERNAME", "neo4j"),
        password=os.getenv("NEO4J_PASSWORD", "hospital_demo_2026")
    )

try:
    bot = init_chatbot()
    connection_status = "✅ Connected"
except Exception as e:
    st.error(f"❌ Could not connect to Neo4j: {e}")
    st.stop()

# Header
st.markdown("""
<div class="main-header">
    <h1>🏥 Hospital Chatbot Assistant</h1>
    <p>Ask me anything about hospitals, patients, physicians, and medical visits!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🔍 Quick Actions")
    st.markdown(f"**Status:** {connection_status}")
    
    st.markdown("---")
    st.subheader("Sample Questions")
    st.markdown("""
    - Show all hospitals
    - Find patients treated by Dr. Sarah Johnson
    - Show patient history for John Smith
    - What are the statistics for City General Hospital?
    - Find visits for diagnosis containing pneumonia
    - List all physicians
    - Show reviews for Memorial Healthcare
    """)
    
    st.markdown("---")
    st.subheader("📊 Database Info")
    st.info("""
    - 5 Hospitals
    - 10 Patients  
    - 5 Physicians
    - 10 Visits
    - 5 Payers
    - 10 Reviews
    """)

# Main Content Area
tab1, tab2, tab3 = st.tabs(["💬 Chat", "🏥 Hospitals", "👥 Patients"])

with tab1:
    st.header("Chat with Hospital Assistant")
    
    # Query selector
    query_type = st.selectbox(
        "What would you like to know?",
        ["Custom Query", "List Hospitals", "Find Patients by Physician", 
         "Patient History", "Hospital Statistics", "Search by Diagnosis",
         "List Physicians", "Hospital Reviews"]
    )
    
    result = None
    
    if query_type == "List Hospitals":
        if st.button("🏥 Show All Hospitals"):
            result = bot.find_hospitals()
            if result:
                st.success(f"Found {len(result)} hospitals:")
                for hospital in result:
                    st.markdown(f"""
                    <div class="query-result">
                        <strong>{hospital['name']}</strong><br>
                        📍 State: {hospital['state']}
                    </div>
                    """, unsafe_allow_html=True)
    
    elif query_type == "Find Patients by Physician":
        physician_name = st.text_input("Enter physician name:", "Dr. Sarah Johnson")
        if st.button("🔍 Search"):
            result = bot.find_patients_by_physician(physician_name)
            if result:
                st.success(f"Found {len(result)} patients:")
                for record in result:
                    st.markdown(f"""
                    <div class="query-result">
                        👤 <strong>{record['patient']}</strong><br>
                        👨‍⚕️ Physician: {record['physician']}<br>
                        📊 Visits: {record['visit_count']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"No patients found for {physician_name}")
    
    elif query_type == "Patient History":
        patient_name = st.text_input("Enter patient name:", "John Smith")
        if st.button("📋 Get History"):
            result = bot.get_patient_history(patient_name)
            if result:
                st.success(f"Found {len(result)} visits for {patient_name}:")
                for visit in result:
                    st.markdown(f"""
                    <div class="query-result">
                        📅 <strong>{visit['date']}</strong><br>
                        🏥 Hospital: {visit['hospital']}<br>
                        👨‍⚕️ Physician: {visit['physician']}<br>
                        🩺 Diagnosis: {visit['diagnosis']}<br>
                        💼 Insurance: {visit.get('insurance', 'N/A')}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"No history found for {patient_name}")
    
    elif query_type == "Hospital Statistics":
        hospitals = bot.find_hospitals()
        hospital_names = [h['name'] for h in hospitals]
        hospital_name = st.selectbox("Select hospital:", hospital_names)
        if st.button("📊 Get Stats"):
            result = bot.get_hospital_stats(hospital_name)
            if result:
                st.markdown(f"""
                <div class="query-result">
                    <h3>{result['hospital']}</h3>
                    📍 State: {result['state']}<br>
                    👥 Total Visits: {result['total_visits']}<br>
                    👨‍⚕️ Total Physicians: {result['total_physicians']}
                </div>
                """, unsafe_allow_html=True)
    
    elif query_type == "Search by Diagnosis":
        diagnosis = st.text_input("Enter diagnosis keyword:", "pneumonia")
        if st.button("🔍 Search"):
            result = bot.search_by_diagnosis(diagnosis)
            if result:
                st.success(f"Found {len(result)} visits:")
                for visit in result:
                    st.markdown(f"""
                    <div class="query-result">
                        👤 Patient: {visit['patient']}<br>
                        🏥 Hospital: {visit['hospital']}<br>
                        🩺 Diagnosis: {visit['diagnosis']}<br>
                        📅 Date: {visit['date']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"No visits found for diagnosis: {diagnosis}")
    
    elif query_type == "List Physicians":
        if st.button("👨‍⚕️ Show All Physicians"):
            result = bot.get_all_physicians()
            if result:
                st.success(f"Found {len(result)} physicians:")
                for physician in result:
                    st.markdown(f"""
                    <div class="query-result">
                        👨‍⚕️ <strong>{physician['name']}</strong><br>
                        🎓 School: {physician['school']}<br>
                        💰 Salary: ${physician['salary']:,.2f}
                    </div>
                    """, unsafe_allow_html=True)
    
    elif query_type == "Hospital Reviews":
        hospitals = bot.find_hospitals()
        hospital_names = [h['name'] for h in hospitals]
        hospital_name = st.selectbox("Select hospital:", hospital_names)
        if st.button("⭐ Show Reviews"):
            result = bot.get_reviews_by_hospital(hospital_name)
            if result:
                st.success(f"Found {len(result)} reviews:")
                for review in result:
                    st.markdown(f"""
                    <div class="query-result">
                        ⭐ <em>"{review['review']}"</em><br>
                        👤 Patient: {review['patient']}<br>
                        👨‍⚕️ Physician: {review['physician']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info(f"No reviews found for {hospital_name}")

with tab2:
    st.header("🏥 Hospital Directory")
    hospitals = bot.find_hospitals()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f"Total Hospitals: {len(hospitals)}")
    
    for hospital in hospitals:
        with st.expander(f"🏥 {hospital['name']} - {hospital['state']}"):
            stats = bot.get_hospital_stats(hospital['name'])
            if stats:
                st.write(f"**Total Visits:** {stats['total_visits']}")
                st.write(f"**Total Physicians:** {stats['total_physicians']}")
            
            # Get reviews
            reviews = bot.get_reviews_by_hospital(hospital['name'])
            if reviews:
                st.write(f"**Patient Reviews:** {len(reviews)}")
                for review in reviews[:3]:  # Show first 3
                    st.info(f"⭐ {review['review']}")

with tab3:
    st.header("👥 Patient Records")
    patient_name = st.text_input("Search patient by name:", key="patient_search")
    
    if patient_name:
        history = bot.get_patient_history(patient_name)
        if history:
            st.success(f"Found {len(history)} visits for patients matching '{patient_name}'")
            
            for visit in history:
                with st.expander(f"📅 {visit['date']} - {visit['hospital']}"):
                    st.write(f"**Patient:** {visit['patient']}")
                    st.write(f"**Physician:** {visit['physician']}")
                    st.write(f"**Diagnosis:** {visit['diagnosis']}")
                    st.write(f"**Chief Complaint:** {visit.get('complaint', 'N/A')}")
                    st.write(f"**Insurance:** {visit.get('insurance', 'N/A')}")
        else:
            st.warning(f"No records found for '{patient_name}'")
    else:
        st.info("Enter a patient name to search medical records")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    🏥 Hospital Chatbot System | Powered by Neo4j Graph Database | 2026
</div>
""", unsafe_allow_html=True)
