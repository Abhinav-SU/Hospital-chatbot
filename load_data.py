#!/usr/bin/env python3
"""Quick script to load CSV data into Neo4j"""

from neo4j import GraphDatabase
import csv
import os

# Direct connection (use environment variables; no hardcoded secrets)
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def load_csv(filename):
    """Read CSV file from local data/ folder"""
    path = os.path.join("data", filename)
    with open(path, 'r') as f:
        return list(csv.DictReader(f))

print("=" * 60)
print("LOADING HOSPITAL DATA INTO NEO4J")
print("=" * 60)

with driver.session() as session:
    # Clean database
    print("\n0. Cleaning existing data...")
    session.run("MATCH (n) DETACH DELETE n")
    
    # Create constraints
    print("1. Creating constraints...")
    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (h:Hospital) REQUIRE h.id IS UNIQUE")
    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Patient) REQUIRE p.id IS UNIQUE")
    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Physician) REQUIRE p.id IS UNIQUE")
    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (v:Visit) REQUIRE v.id IS UNIQUE")
    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (r:Review) REQUIRE r.id IS UNIQUE")
    session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Payer) REQUIRE p.id IS UNIQUE")
    
    # Load Hospitals
    print("2. Loading Hospitals...")
    hospitals = load_csv('hospitals.csv')
    for h in hospitals:
        session.run("""
            CREATE (h:Hospital {
                id: $id,
                name: $name,
                state_name: $state
            })
        """, id=h['hospital_id'], name=h['hospital_name'], state=h['hospital_state'])
    print(f"   Loaded {len(hospitals)} hospitals")
    
    # Load Payers
    print("3. Loading Payers...")
    payers = load_csv('payers.csv')
    for p in payers:
        session.run("CREATE (p:Payer {id: $id, name: $name})", 
                   id=p['payer_id'], name=p['payer_name'])
    print(f"   Loaded {len(payers)} payers")
    
    # Load Physicians
    print("4. Loading Physicians...")
    physicians = load_csv('physicians.csv')
    for p in physicians:
        session.run("""
            CREATE (p:Physician {
                id: $id,
                name: $name,
                school: $school,
                salary: toFloat($salary)
            })
        """, id=p['physician_id'], name=p['physician_name'], 
            school=p['medical_school'], salary=p['salary'])
    print(f"   Loaded {len(physicians)} physicians")
    
    # Load Patients
    print("5. Loading Patients...")
    patients = load_csv('patients.csv')
    for p in patients:
        session.run("CREATE (p:Patient {id: $id, name: $name})", 
                   id=p['patient_id'], name=p['patient_name'])
    print(f"   Loaded {len(patients)} patients")
    
    # Load Visits
    print("6. Loading Visits...")
    visits = load_csv('visits.csv')
    for v in visits:
        session.run("""
            MATCH (patient:Patient {id: $pid})
            MATCH (hospital:Hospital {id: $hid})
            MATCH (physician:Physician {id: $phid})
            MATCH (payer:Payer {id: $payid})
            CREATE (visit:Visit {
                id: $id,
                admission_date: $date,
                diagnosis: $diagnosis,
                chief_complaint: $complaint
            })
            CREATE (patient)-[:HAS]->(visit)
            CREATE (visit)-[:AT]->(hospital)
            CREATE (physician)-[:TREATS]->(visit)
            CREATE (visit)-[:COVERED_BY]->(payer)
        """, id=v['visit_id'], pid=v['patient_id'], hid=v['hospital_id'],
            phid=v['physician_id'], payid=v['payer_id'], 
            date=v['date_of_admission'], diagnosis=v['primary_diagnosis'],
            complaint=v['chief_complaint'])
    print(f"   Loaded {len(visits)} visits")
    
    # Load Reviews
    print("7. Loading Reviews...")
    reviews = load_csv('reviews.csv')
    for r in reviews:
        session.run("""
            MATCH (visit:Visit {id: $vid})
            CREATE (review:Review {
                id: $id,
                text: $text,
                patient_name: $pname,
                physician_name: $phname
            })
            CREATE (visit)-[:WRITES]->(review)
        """, id=r['review_id'], vid=r['visit_id'], text=r['review'],
            pname=r['patient_name'], phname=r['physician_name'])
    print(f"   Loaded {len(reviews)} reviews")
    
    # Verify
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    result = session.run("MATCH (h:Hospital) RETURN count(h) as count")
    print(f"Hospitals: {result.single()['count']}")
    result = session.run("MATCH (p:Patient) RETURN count(p) as count")
    print(f"Patients: {result.single()['count']}")
    result = session.run("MATCH (p:Physician) RETURN count(p) as count")
    print(f"Physicians: {result.single()['count']}")
    result = session.run("MATCH (v:Visit) RETURN count(v) as count")
    print(f"Visits: {result.single()['count']}")
    result = session.run("MATCH (r:Review) RETURN count(r) as count")
    print(f"Reviews: {result.single()['count']}")
    result = session.run("MATCH (p:Payer) RETURN count(p) as count")
    print(f"Payers: {result.single()['count']}")
    print("\n✅ DATA LOADING COMPLETE!")
    print("=" * 60)

driver.close()
