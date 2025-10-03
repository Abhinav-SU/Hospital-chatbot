"""
Hospital Graph ETL Pipeline
----------------------------
This script loads healthcare data from CSV files into a Neo4j graph database.
It creates nodes (hospitals, patients, physicians, etc.) and relationships between them.

Graph Structure:
- Nodes: Hospital, Payer, Physician, Patient, Visit, Review
- Relationships: AT, WRITES, TREATS, COVERED_BY, HAS, EMPLOYS
"""

import logging
import os

from neo4j import GraphDatabase
from retry import retry

# ============================================================================
# CONFIGURATION: Load paths and credentials from environment variables
# ============================================================================
# CSV file paths (should be in file:/// URI format for Neo4j)
HOSPITALS_CSV_PATH = os.getenv("HOSPITALS_CSV_PATH")
PAYERS_CSV_PATH = os.getenv("PAYERS_CSV_PATH")
PHYSICIANS_CSV_PATH = os.getenv("PHYSICIANS_CSV_PATH")
PATIENTS_CSV_PATH = os.getenv("PATIENTS_CSV_PATH")
VISITS_CSV_PATH = os.getenv("VISITS_CSV_PATH")
REVIEWS_CSV_PATH = os.getenv("REVIEWS_CSV_PATH")

# Neo4j database connection settings
NEO4J_URI = os.getenv("NEO4J_URI")  # e.g., bolt://localhost:7687
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")  # e.g., neo4j
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")  # your secure password

# ============================================================================
# LOGGING SETUP: Configure logging format and level
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOGGER = logging.getLogger(__name__)

# List of all node types in our graph database
NODES = ["Hospital", "Payer", "Physician", "Patient", "Visit", "Review"]


# ============================================================================
# HELPER FUNCTION: Set uniqueness constraints
# ============================================================================
def _set_uniqueness_constraints(tx, node):
    """
    Create a uniqueness constraint on a node type's ID property.
    
    This ensures:
    1. No two nodes of the same type can have the same ID
    2. An index is automatically created for fast lookups
    3. Data integrity is maintained
    
    Args:
        tx: Neo4j transaction object
        node: Node type name (e.g., "Hospital", "Patient")
    
    Example:
        For node="Hospital", creates: 
        CREATE CONSTRAINT FOR (n:Hospital) REQUIRE n.id IS UNIQUE
    """
    query = f"""CREATE CONSTRAINT IF NOT EXISTS FOR (n:{node})
        REQUIRE n.id IS UNIQUE;"""
    _ = tx.run(query, {})


# ============================================================================
# MAIN ETL FUNCTION: Load all hospital data into Neo4j
# ============================================================================
@retry(tries=100, delay=10)  # Retry up to 100 times with 10 sec delay (waits for Neo4j to start)
def load_hospital_graph_from_csv() -> None:
    """
    Load structured hospital CSV data into Neo4j graph database.
    
    Process:
    1. Connect to Neo4j database
    2. Set uniqueness constraints on all node types
    3. Load nodes (hospitals, patients, physicians, payers, visits, reviews)
    4. Create relationships between nodes
    
    The @retry decorator handles cases where Neo4j isn't ready yet (e.g., Docker startup).
    """

    # ========================================================================
    # STEP 1: Connect to Neo4j Database
    # ========================================================================
    driver = GraphDatabase.driver(
        NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    # ========================================================================
    # STEP 2: Set Uniqueness Constraints
    # ========================================================================
    # Create constraints for all 6 node types to ensure unique IDs
    LOGGER.info("Setting uniqueness constraints on nodes")
    with driver.session(database="neo4j") as session:
        for node in NODES:
            session.execute_write(_set_uniqueness_constraints, node)

    # ========================================================================
    # STEP 3: Load Node Data from CSV Files
    # ========================================================================
    
    # --- Load Hospital Nodes ---
    # Creates nodes like: (:Hospital {id: 1, name: "City General", state_name: "CA"})
    LOGGER.info("Loading hospital nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{HOSPITALS_CSV_PATH}' AS hospitals
        MERGE (h:Hospital {{id: toInteger(hospitals.hospital_id),
                            name: hospitals.hospital_name,
                            state_name: hospitals.hospital_state}});
        """
        _ = session.run(query, {})

    # --- Load Payer Nodes (Insurance Companies) ---
    # Creates nodes like: (:Payer {id: 1, name: "Blue Cross"})
    LOGGER.info("Loading payer nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{PAYERS_CSV_PATH}' AS payers
        MERGE (p:Payer {{id: toInteger(payers.payer_id),
        name: payers.payer_name}});
        """
        _ = session.run(query, {})

    # --- Load Physician Nodes ---
    # Creates nodes with physician details (name, DOB, school, salary, etc.)
    LOGGER.info("Loading physician nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{PHYSICIANS_CSV_PATH}' AS physicians
        MERGE (p:Physician {{id: toInteger(physicians.physician_id),
                            name: physicians.physician_name,
                            dob: physicians.physician_dob,
                            grad_year: physicians.physician_grad_year,
                            school: physicians.medical_school,
                            salary: toFloat(physicians.salary)
                            }});
        """
        _ = session.run(query, {})

    # --- Load Visit Nodes ---
    # Visit = a patient's hospital visit record
    # ON CREATE/MATCH SET allows updating properties if visit already exists
    LOGGER.info("Loading visit nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS FROM '{VISITS_CSV_PATH}' AS visits
        MERGE (v:Visit {{id: toInteger(visits.visit_id),
                            room_number: toInteger(visits.room_number),
                            admission_type: visits.admission_type,
                            admission_date: visits.date_of_admission,
                            test_results: visits.test_results,
                            status: visits.visit_status
        }})
            ON CREATE SET v.chief_complaint = visits.chief_complaint
            ON MATCH SET v.chief_complaint = visits.chief_complaint
            ON CREATE SET v.treatment_description =
            visits.treatment_description
            ON MATCH SET v.treatment_description = visits.treatment_description
            ON CREATE SET v.diagnosis = visits.primary_diagnosis
            ON MATCH SET v.diagnosis = visits.primary_diagnosis
            ON CREATE SET v.discharge_date = visits.discharge_date
            ON MATCH SET v.discharge_date = visits.discharge_date
         """
        _ = session.run(query, {})

    # --- Load Patient Nodes ---
    # Creates nodes with patient demographics (name, sex, DOB, blood type)
    LOGGER.info("Loading patient nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{PATIENTS_CSV_PATH}' AS patients
        MERGE (p:Patient {{id: toInteger(patients.patient_id),
                        name: patients.patient_name,
                        sex: patients.patient_sex,
                        dob: patients.patient_dob,
                        blood_type: patients.patient_blood_type
                        }});
        """
        _ = session.run(query, {})

    # --- Load Review Nodes ---
    # Patient reviews/feedback about their hospital experience
    LOGGER.info("Loading review nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{REVIEWS_CSV_PATH}' AS reviews
        MERGE (r:Review {{id: toInteger(reviews.review_id),
                         text: reviews.review,
                         patient_name: reviews.patient_name,
                         physician_name: reviews.physician_name,
                         hospital_name: reviews.hospital_name
                        }});
        """
        _ = session.run(query, {})

    # ========================================================================
    # STEP 4: Create Relationships Between Nodes
    # ========================================================================
    # This is where we build the graph structure by connecting related nodes
    
    # --- AT Relationship: Visit -> Hospital ---
    # Connects each visit to the hospital where it occurred
    # Graph: (Visit)-[:AT]->(Hospital)
    LOGGER.info("Loading 'AT' relationships")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS FROM '{VISITS_CSV_PATH}' AS row
        MATCH (source: `Visit` {{ `id`: toInteger(trim(row.`visit_id`)) }})
        MATCH (target: `Hospital` {{ `id`:
        toInteger(trim(row.`hospital_id`))}})
        MERGE (source)-[r: `AT`]->(target)
        """
        _ = session.run(query, {})

    # --- WRITES Relationship: Visit -> Review ---
    # Links a visit to any reviews written about that visit
    # Graph: (Visit)-[:WRITES]->(Review)
    LOGGER.info("Loading 'WRITES' relationships")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS FROM '{REVIEWS_CSV_PATH}' AS reviews
            MATCH (v:Visit {{id: toInteger(reviews.visit_id)}})
            MATCH (r:Review {{id: toInteger(reviews.review_id)}})
            MERGE (v)-[writes:WRITES]->(r)
        """
        _ = session.run(query, {})

    # --- TREATS Relationship: Physician -> Visit ---
    # Shows which physician treated each visit
    # Graph: (Physician)-[:TREATS]->(Visit)
    LOGGER.info("Loading 'TREATS' relationships")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS FROM '{VISITS_CSV_PATH}' AS visits
            MATCH (p:Physician {{id: toInteger(visits.physician_id)}})
            MATCH (v:Visit {{id: toInteger(visits.visit_id)}})
            MERGE (p)-[treats:TREATS]->(v)
        """
        _ = session.run(query, {})

    # --- COVERED_BY Relationship: Visit -> Payer ---
    # Links visits to insurance payers, with billing information
    # Graph: (Visit)-[:COVERED_BY {service_date, billing_amount}]->(Payer)
    # Note: This relationship has properties (service_date and billing_amount)
    LOGGER.info("Loading 'COVERED_BY' relationships")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS FROM '{VISITS_CSV_PATH}' AS visits
            MATCH (v:Visit {{id: toInteger(visits.visit_id)}})
            MATCH (p:Payer {{id: toInteger(visits.payer_id)}})
            MERGE (v)-[covered_by:COVERED_BY]->(p)
            ON CREATE SET
                covered_by.service_date = visits.discharge_date,
                covered_by.billing_amount = toFloat(visits.billing_amount)
        """
        _ = session.run(query, {})

    # --- HAS Relationship: Patient -> Visit ---
    # Connects patients to their hospital visits
    # Graph: (Patient)-[:HAS]->(Visit)
    LOGGER.info("Loading 'HAS' relationships")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS FROM '{VISITS_CSV_PATH}' AS visits
            MATCH (p:Patient {{id: toInteger(visits.patient_id)}})
            MATCH (v:Visit {{id: toInteger(visits.visit_id)}})
            MERGE (p)-[has:HAS]->(v)
        """
        _ = session.run(query, {})

    # --- EMPLOYS Relationship: Hospital -> Physician ---
    # Shows which hospitals employ which physicians
    # Graph: (Hospital)-[:EMPLOYS]->(Physician)
    LOGGER.info("Loading 'EMPLOYS' relationships")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS FROM '{VISITS_CSV_PATH}' AS visits
            MATCH (h:Hospital {{id: toInteger(visits.hospital_id)}})
            MATCH (p:Physician {{id: toInteger(visits.physician_id)}})
            MERGE (h)-[employs:EMPLOYS]->(p)
        """
        _ = session.run(query, {})


# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    """
    When this script is run directly (not imported), execute the ETL pipeline.
    
    Usage:
        python hospital_bulk_csv_write.py
    
    Prerequisites:
        - Environment variables must be set (NEO4J_URI, NEO4J_USERNAME, etc.)
        - Neo4j database must be running
        - CSV files must be accessible at the specified paths
    """
    load_hospital_graph_from_csv()
