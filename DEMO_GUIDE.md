# 🏥 Hospital Chatbot Demo Guide

## Welcome to Your Hospital Chatbot Demo!

This guide will help you test the Hospital Chatbot system in VS Code's browser.

---

## 📋 Project Overview

The Hospital Chatbot is a Neo4j-powered healthcare data management system that demonstrates:
- ✅ Graph database relationships between hospitals, patients, physicians, and visits
- ✅ Automated ETL pipeline for loading healthcare data
- ✅ Real-time data querying with Cypher
- ✅ Docker containerization for easy deployment

---

## 🚀 Quick Start Guide

### Step 1: Start the System

The services are configured with Docker Compose. Start them with:

```bash
cd /workspaces/Hospital-chatbot
docker compose up -d
```

### Step 2: Access Neo4j Browser

Once the services are running, open the Neo4j Browser:

**URL:** http://localhost:7474

**Login Credentials:**
- Username: `neo4j`
- Password: `hospital_demo_2026`

### Step 3: View the Demo Page

Open the demo HTML page in VS Code's Simple Browser:

**File:** `/workspaces/Hospital-chatbot/demo.html`

---

## 📊 Sample Data Overview

The database contains:
- **5 Hospitals** across different states
- **10 Patients** with complete medical records
- **5 Physicians** from top medical schools
- **10 Hospital Visits** with diagnoses and treatments
- **10 Patient Reviews** with feedback
- **5 Insurance Payers** (Blue Cross, UnitedHealthcare, etc.)

---

## 🔍 Demo Cypher Queries

Try these queries in the Neo4j Browser:

### Query 1: View All Hospitals
```cypher
MATCH (h:Hospital)
RETURN h.name AS Hospital, h.state_name AS State
ORDER BY h.name
```

### Query 2: Find Patients Treated by Dr. Sarah Johnson
```cypher
MATCH (patient:Patient)-[:HAS]->(visit:Visit)<-[:TREATS]-(physician:Physician {name: "Dr. Sarah Johnson"})
RETURN patient.name AS Patient, 
       visit.date_of_admission AS AdmissionDate,
       visit.primary_diagnosis AS Diagnosis
```

### Query 3: Hospitals with Most Visits
```cypher
MATCH (visit:Visit)-[:AT]->(hospital:Hospital)
RETURN hospital.name AS Hospital, 
       COUNT(visit) AS TotalVisits
ORDER BY TotalVisits DESC
```

### Query 4: Average Billing by Insurance Provider
```cypher
MATCH (visit:Visit)-[:COVERED_BY]->(payer:Payer)
RETURN payer.name AS InsuranceProvider,
       AVG(visit.billing_amount) AS AverageBilling,
       COUNT(visit) AS TotalClaims
ORDER BY AverageBilling DESC
```

### Query 5: Emergency Visits with Patient Reviews
```cypher
MATCH (visit:Visit {admission_type: "Emergency"})-[:WRITES]->(review:Review)
MATCH (visit)-[:AT]->(hospital:Hospital)
RETURN hospital.name AS Hospital,
       visit.chief_complaint AS Complaint,
       review.review AS PatientReview
LIMIT 5
```

### Query 6: Visualize the Hospital Network
```cypher
MATCH (h:Hospital)<-[:AT]-(v:Visit)-[:TREATS]-(p:Physician)
RETURN h, v, p
LIMIT 20
```

---

## 🎥 Recording Your Demo Video

### Preparation Checklist

Before recording:
- [ ] Services are running (`docker compose ps`)
- [ ] Neo4j Browser is accessible at http://localhost:7474
- [ ] You're logged in to Neo4j
- [ ] Demo page is open in a browser

### Demo Script (Voice Over)

Here's a suggested narration for your video:

#### Introduction (15 seconds)
> "Welcome to the Hospital Chatbot demonstration. This is a healthcare data management system built with Neo4j graph database, demonstrating how we can manage complex relationships between hospitals, patients, physicians, and medical visits."

#### System Overview (20 seconds)
> "The system uses Docker containers to run Neo4j and an automated ETL pipeline. We have sample data including 5 hospitals, 10 patients, 5 physicians, and 10 hospital visits with complete medical records."

#### Neo4j Browser Tour (30 seconds)
> "Let's log into the Neo4j Browser. Here we can see our graph database. Let me run a query to show all hospitals in our system... As you can see, we have hospitals across California, New York, Texas, Florida, and Illinois."

#### Data Relationships (40 seconds)
> "Now let's explore the relationships. This query shows all patients treated by Dr. Sarah Johnson... You can see the patient name, admission date, and diagnosis. The power of a graph database is in these relationships."

> "Let me show you a more complex query - finding hospitals with the most visits... City General Hospital and Memorial Healthcare lead with 2 visits each in our sample data."

#### Visual Graph (20 seconds)
> "Here's the real power - let's visualize the hospital network. This query shows the connections between hospitals, visits, and physicians. You can see how everything is interconnected in a graph structure."

#### Conclusion (15 seconds)
> "This demonstrates how a graph database can effectively manage healthcare data with complex relationships. The system is containerized, scalable, and ready for integration with chatbot interfaces. Thank you for watching!"

---

## 🛠️ Troubleshooting

### Services Not Starting
```bash
docker compose down
docker compose up -d
```

### Check Service Status
```bash
docker compose ps
docker compose logs neo4j
docker compose logs hospital_neo4j_etl
```

### Cannot Connect to Neo4j
- Ensure port 7474 and 7687 are not in use
- Wait 30 seconds for Neo4j to fully start
- Check logs: `docker compose logs neo4j`

### Data Not Loading
```bash
# Check ETL logs
docker compose logs hospital_neo4j_etl

# Restart ETL
docker compose restart hospital_neo4j_etl
```

---

## 📁 Project Structure

```
Hospital-Chatbot/
├── data/                      # CSV sample data
│   ├── hospitals.csv
│   ├── patients.csv
│   ├── physicians.csv
│   ├── payers.csv
│   ├── visits.csv
│   └── reviews.csv
├── hospital_neo4j_etl/       # ETL Docker service
│   ├── Dockerfile
│   └── src/
│       └── hospital_bulk_csv_write.py
├── docker-compose.yml        # Service orchestration
├── demo.html                 # Interactive demo page
├── .env                      # Environment configuration
└── DEMO_GUIDE.md            # This file
```

---

## 🎯 Key Features to Highlight in Demo

1. **Graph-Based Data Model** - Complex healthcare relationships
2. **Automated ETL** - CSV to Neo4j data loading
3. **Docker Containerization** - Easy deployment
4. **Interactive Queries** - Real-time Cypher queries
5. **Data Visualization** - Graph network visualization
6. **Production-Ready** - Environment variables, health checks

---

## 🌐 Opening Demo in VS Code Browser

1. Right-click on `demo.html`
2. Select "Open with Live Server" or "Preview in Browser"
3. Or use VS Code's Simple Browser

---

## 📝 Notes for Your Video

- **Screen Resolution**: Record at 1920x1080 for best quality
- **Audio**: Use a good microphone, speak clearly and at a moderate pace
- **Duration**: Aim for 2-3 minutes total
- **Tools**: OBS Studio, Loom, or built-in screen recording
- **Highlights**: Focus on the graph visualizations and query results

---

## 🎬 Post-Production Tips

- Add subtle background music (royalty-free)
- Include text overlays for key points
- Add a title slide at the beginning
- Include your contact information at the end
- Export in MP4 format (H.264 codec)

---

## ✅ Demo Completion Checklist

- [ ] All services running successfully
- [ ] Can log in to Neo4j Browser
- [ ] Sample queries execute correctly
- [ ] Graph visualizations display properly
- [ ] Demo page loads correctly
- [ ] Screen recording software tested
- [ ] Microphone audio quality checked
- [ ] Demo script reviewed and practiced

---

**Good luck with your demo! 🎉**

For questions or issues, refer to the main [README.md](README.md) file.
