import streamlit as st
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Neo4j Connection
class HospitalChatbot:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def query_database(self, cypher_query):
        """Execute a Cypher query and return results"""
        try:
            with self.driver.session() as session:
                result = session.run(cypher_query)
                return [dict(record) for record in result]
        except Exception as e:
            return {"error": str(e)}
    
    def natural_language_to_cypher(self, question):
        """Convert natural language question to Cypher query using pattern matching"""
        question_lower = question.lower()
        
        # Pattern matching for common questions - ORDER MATTERS!
        
        # Statistics query - must come before generic hospital
        if "statistics" in question_lower or "stats" in question_lower or "count" in question_lower:
            return """
                MATCH (h:Hospital)
                OPTIONAL MATCH (v:Visit)-[:AT]->(h)
                RETURN h.name AS Hospital,
                       COUNT(DISTINCT v) AS Total_Visits
                ORDER BY Total_Visits DESC
            """
        
        # California/state-specific hospitals
        elif "california" in question_lower or "ca" in question_lower:
            return """
                MATCH (h:Hospital)
                WHERE h.state_name = 'CA'
                RETURN h.name AS Hospital, h.state_name AS State
            """
        
        # Patients treated by specific physician
        elif ("patient" in question_lower or "treated" in question_lower) and ("sarah johnson" in question_lower):
            return """
                MATCH (patient:Patient)-[:HAS]->(visit:Visit)<-[:TREATS]-(physician:Physician)
                WHERE physician.name CONTAINS 'Dr. Sarah Johnson'
                RETURN DISTINCT patient.name AS Patient, 
                       physician.name AS Physician,
                       COUNT(visit) AS Visits
                ORDER BY Visits DESC
            """
        
        elif ("patient" in question_lower or "treated" in question_lower) and ("michael chen" in question_lower):
            return """
                MATCH (patient:Patient)-[:HAS]->(visit:Visit)<-[:TREATS]-(physician:Physician)
                WHERE physician.name CONTAINS 'Dr. Michael Chen'
                RETURN DISTINCT patient.name AS Patient, 
                       physician.name AS Physician,
                       COUNT(visit) AS Visits
                ORDER BY Visits DESC
            """
        
        # Patient medical history
        elif "history" in question_lower and "john smith" in question_lower:
            return """
                MATCH (patient:Patient)-[:HAS]->(visit:Visit)
                WHERE patient.name CONTAINS 'John Smith'
                MATCH (visit)-[:AT]->(hospital:Hospital)
                MATCH (visit)<-[:TREATS]-(physician:Physician)
                RETURN patient.name AS Patient,
                       visit.admission_date AS Date,
                       hospital.name AS Hospital,
                       physician.name AS Physician,
                       visit.diagnosis AS Diagnosis
                ORDER BY visit.admission_date DESC
            """
        
        elif "history" in question_lower and "mary johnson" in question_lower:
            return """
                MATCH (patient:Patient)-[:HAS]->(visit:Visit)
                WHERE patient.name CONTAINS 'Mary Johnson'
                MATCH (visit)-[:AT]->(hospital:Hospital)
                MATCH (visit)<-[:TREATS]-(physician:Physician)
                RETURN patient.name AS Patient,
                       visit.admission_date AS Date,
                       hospital.name AS Hospital,
                       physician.name AS Physician,
                       visit.diagnosis AS Diagnosis
                ORDER BY visit.admission_date DESC
            """
        
        # Common diagnoses
        # List physicians with salaries
        elif ("physician" in question_lower or "doctor" in question_lower) and "salary" in question_lower:
            return """
                MATCH (p:Physician)
                RETURN p.name AS Physician, p.school AS School, p.salary AS Salary
                ORDER BY p.salary DESC
            """
        
        # Highest paid physicians
        elif "highest" in question_lower and ("paid" in question_lower or "salary" in question_lower):
            return """
                MATCH (p:Physician)
                RETURN p.name AS Physician, p.salary AS Salary
                ORDER BY p.salary DESC
                LIMIT 5
            """
        
        # Generic diagnosis query
        elif "diagnosis" in question_lower or "disease" in question_lower or "condition" in question_lower:
            return """
                MATCH (visit:Visit)
                RETURN visit.diagnosis AS Diagnosis, COUNT(*) AS Count
                ORDER BY Count DESC
                LIMIT 10
            """
        
        # Patient reviews
        elif "review" in question_lower:
            return """
                MATCH (visit:Visit)-[:WRITES]->(review:Review)
                MATCH (visit)-[:AT]->(hospital:Hospital)
                RETURN hospital.name AS Hospital,
                       review.text AS Review,
                       review.patient_name AS Patient
                LIMIT 10
            """
        
        # List all hospitals (default/generic)
        elif "hospital" in question_lower and ("all" in question_lower or "show" in question_lower or "list" in question_lower):
            return """
                MATCH (h:Hospital)
                RETURN h.name AS Hospital, h.state_name AS State
                ORDER BY h.name
            """
        
        # Default fallback
        else:
            # Default: show database summary
            return """
                MATCH (h:Hospital)
                RETURN h.name AS Hospital, h.state_name AS State
                LIMIT 5
            """
    
    def format_response(self, data, question):
        """Format the query results into a natural language response"""
        if not data:
            return "I couldn't find any information matching your query. Please try rephrasing your question."
        
        if isinstance(data, dict) and "error" in data:
            return f"Sorry, I encountered an error: {data['error']}"
        
        # Format based on the type of data
        if len(data) > 0:
            keys = list(data[0].keys())
            
            if "Hospital" in keys and "State" in keys:
                response = f"I found {len(data)} hospital(s):\n\n"
                for item in data:
                    response += f"• **{item['Hospital']}** - {item['State']}\n"
                return response
            
            elif "Patient" in keys and "Physician" in keys:
                response = f"Here are the patients:\n\n"
                for item in data:
                    response += f"• **{item['Patient']}** treated by {item['Physician']}"
                    if 'Visits' in item:
                        response += f" ({item['Visits']} visits)"
                    response += "\n"
                return response
            
            elif "Physician" in keys and "Salary" in keys:
                response = f"Here are the physicians:\n\n"
                for item in data:
                    response += f"• **{item['Physician']}** - ${item['Salary']:,.0f}\n"
                    if 'School' in item:
                        response += f"   School: {item['School']}\n"
                return response
            
            elif "Diagnosis" in keys:
                if "Count" in keys:
                    response = f"Most common diagnoses:\n\n"
                    for item in data:
                        response += f"• **{item['Diagnosis']}** - {item['Count']} cases\n"
                else:
                    response = f"Patient medical information:\n\n"
                    for item in data:
                        response += f"Date: {item.get('Date', 'N/A')}\n"
                        response += f"  Diagnosis: {item['Diagnosis']}\n"
                        response += f"  Hospital: {item.get('Hospital', 'N/A')}\n\n"
                return response
            
            elif "Review" in keys:
                response = f"Patient reviews:\n\n"
                for item in data[:5]:
                    response += f"• \"{item['Review']}\"\n"
                    response += f"  - {item.get('Patient', 'Anonymous')}\n\n"
                return response
            
            elif "Total_Visits" in keys:
                response = f"Hospital statistics:\n\n"
                for item in data:
                    response += f"• **{item['Hospital']}** - {item['Total_Visits']} visits\n"
                return response
            
            else:
                # Generic formatting
                response = f"Found {len(data)} result(s):\n\n"
                for item in data:
                    for key, value in item.items():
                        response += f"**{key}:** {value}\n"
                    response += "\n"
                return response
        
        return "No results found."

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
    connection_status = "Connected to Neo4j"
except Exception as e:
    st.error(f"Could not connect to Neo4j: {e}")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar - exactly like RealPython tutorial
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with a hospital system database. 
        The system uses Neo4j graph database to answer questions about 
        hospitals, patients, visits, physicians, and insurance payers.
        """
    )

    st.header("Example Questions")
    st.markdown("- Which hospitals are in the hospital system?")
    st.markdown("- Show me all hospitals in California")
    st.markdown("- Which patients were treated by Dr. Sarah Johnson?")
    st.markdown("- What is the visit history for patient John Smith?")
    st.markdown("- Show me the most common diagnoses")
    st.markdown("- Which physicians have the highest salaries?")
    st.markdown("- What are the hospital statistics?")
    st.markdown("- Show me patient reviews")
    st.markdown("- List all available physicians")

# Main UI - exactly like RealPython tutorial
st.title("Hospital System Chatbot")
st.info(
    "Ask me questions about patients, visits, insurance payers, hospitals, "
    "physicians, and reviews!"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What do you want to know?"):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get bot response
    cypher_query = bot.natural_language_to_cypher(prompt)
    results = bot.query_database(cypher_query)
    response = bot.format_response(results, prompt)
    
    # Display assistant message
    st.chat_message("assistant").markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

