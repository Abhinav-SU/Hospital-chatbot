#!/bin/bash

# 🎬 Demo Pre-Flight Check
# Run this before recording to ensure all queries work

echo "🚀 Starting Hospital Chatbot Demo Pre-Flight Check..."
echo "=================================================="
echo ""

# Check if server is running
echo "✓ Checking if Streamlit server is running on port 8502..."
if lsof -i :8502 > /dev/null 2>&1; then
    echo "  ✅ Server is running on port 8502"
else
    echo "  ❌ Server is NOT running!"
    echo "  Starting server now..."
    cd /workspaces/Hospital-chatbot
    nohup streamlit run chatbot_ai.py --server.port 8502 > /tmp/streamlit.log 2>&1 &
    sleep 5
    echo "  ✅ Server started!"
fi

echo ""

# Check if Neo4j is accessible
echo "✓ Checking Neo4j connection..."
python3 << 'EOF'
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

try:
    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
    )
    with driver.session() as session:
        result = session.run("MATCH (h:Hospital) RETURN count(h) as count")
        count = result.single()["count"]
        print(f"  ✅ Neo4j connected! Found {count} hospitals in database")
    driver.close()
except Exception as e:
    print(f"  ❌ Neo4j connection failed: {e}")
EOF

echo ""

# Check if web interface is responding
echo "✓ Checking if web interface is responding..."
if curl -s http://localhost:8502 > /dev/null; then
    echo "  ✅ Web interface is responding"
else
    echo "  ❌ Web interface is not responding"
fi

echo ""

# Test demo queries
echo "✓ Testing demo queries..."
python3 << 'EOF'
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
)

queries = {
    "California Hospitals": """
        MATCH (h:Hospital)
        WHERE h.state_name = 'CA'
        RETURN h.name AS Hospital
    """,
    "Patients by Dr. Sarah Johnson": """
        MATCH (p:Patient)-[:HAS]->(v:Visit)-[:TREATS]-(phy:Physician)
        WHERE phy.name = 'Sarah Johnson'
        RETURN DISTINCT p.name AS Patient
    """,
    "Common Diagnoses": """
        MATCH (v:Visit)
        WHERE v.primary_diagnosis IS NOT NULL
        RETURN v.primary_diagnosis AS Diagnosis, COUNT(*) AS Count
        ORDER BY Count DESC LIMIT 5
    """,
    "Highest Paid Physicians": """
        MATCH (p:Physician)
        WHERE p.salary IS NOT NULL
        RETURN p.name AS Physician, p.salary AS Salary
        ORDER BY Salary DESC LIMIT 3
    """,
    "Patient Reviews": """
        MATCH (r:Review)
        RETURN r.review AS Review LIMIT 3
    """
}

with driver.session() as session:
    for name, query in queries.items():
        try:
            result = session.run(query)
            records = [dict(r) for r in result]
            if records:
                print(f"  ✅ {name}: Found {len(records)} results")
            else:
                print(f"  ⚠️  {name}: No results (query worked but no data)")
        except Exception as e:
            print(f"  ❌ {name}: Failed - {str(e)[:50]}")

driver.close()
EOF

echo ""
echo "=================================================="
echo "✅ Pre-Flight Check Complete!"
echo ""
echo "📹 Ready to record! Open: http://localhost:8502"
echo "📝 Follow DEMO_SCRIPT.md for voiceover script"
echo "🎯 Use QUICK_DEMO_GUIDE.md for quick reference"
echo ""
echo "🎬 Good luck with your recording!"
