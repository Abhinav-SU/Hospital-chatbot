# 🏥 Hospital Chatbot

A hospital data management system that uses Neo4j graph database to store and query healthcare data, built for intelligent chatbot integration.

## 📋 Overview

This project provides an ETL (Extract, Transform, Load) pipeline to import structured hospital data from CSV files into a Neo4j graph database. The data model includes hospitals, patients, physicians, payers, visits, and reviews - creating a comprehensive healthcare knowledge graph with relationships between all entities.

## 🏗️ Architecture

```
Hospital-Chatbot/
├── data/                          # CSV data files (excluded from git)
│   ├── healthcare_dataset.csv
│   ├── hospitals.csv
│   ├── patients.csv
│   ├── physicians.csv
│   ├── payers.csv
│   ├── visits.csv
│   └── reviews.csv
├── hospital_neo4j_etl/           # Neo4j ETL package
│   ├── src/
│   │   ├── hospital_bulk_csv_write.py  # Main ETL script
│   │   └── entrypoint.sh               # Docker entrypoint
│   ├── Dockerfile                      # Docker image definition
│   └── pyproject.toml                  # Python package config
├── analysis.py                    # Data analysis using Polars
├── docker-compose.yml            # Docker orchestration (ETL service)
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md
```

## 📊 Data Model

### Nodes (Entities)
- **Hospital**: Healthcare facilities (ID, name, state)
- **Patient**: Patient records (ID, name, sex, DOB, blood type)
- **Physician**: Medical staff (ID, name, DOB, graduation year, medical school, salary)
- **Payer**: Insurance providers (ID, name)
- **Visit**: Patient hospital visits (ID, room number, admission type, dates, diagnosis, treatment)
- **Review**: Hospital reviews (ID, review text, patient/physician/hospital names)

### Relationships
- **AT**: `(Visit)-[:AT]->(Hospital)` - Visit occurred at a hospital
- **WRITES**: `(Visit)-[:WRITES]->(Review)` - Visit resulted in a review
- **TREATS**: `(Physician)-[:TREATS]->(Visit)` - Physician treated a visit
- **COVERED_BY**: `(Visit)-[:COVERED_BY {service_date, billing_amount}]->(Payer)` - Visit covered by insurance
- **HAS**: `(Patient)-[:HAS]->(Visit)` - Patient had a visit
- **EMPLOYS**: `(Hospital)-[:EMPLOYS]->(Physician)` - Hospital employs physician

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+** (recommended: 3.11)
- **Docker Desktop** (for containerized deployment)
- **Neo4j Database** (optional if using Docker)

### Installation

1. **Clone the repository**
   ```powershell
   git clone <your-repo-url>
   cd Hospital-Chatbot
   ```

2. **Create and activate virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Prepare your data**
   - Place your CSV files in the `data/` directory
   - Ensure CSV files match the expected schema (see CSV File Requirements below)

### Usage

#### Option 1: Docker Deployment (Recommended)

**Note**: The current `docker-compose.yml` includes only the ETL service. You'll need to run Neo4j separately or add it to the compose file.

1. **Create `.env` file** in project root:
   ```env
   # Neo4j Configuration
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_password_here
   
   # CSV File Paths (use file:/// URI format for Neo4j)
   HOSPITALS_CSV_PATH=file:///data/hospitals.csv
   PAYERS_CSV_PATH=file:///data/payers.csv
   PHYSICIANS_CSV_PATH=file:///data/physicians.csv
   PATIENTS_CSV_PATH=file:///data/patients.csv
   VISITS_CSV_PATH=file:///data/visits.csv
   REVIEWS_CSV_PATH=file:///data/reviews.csv
   ```

2. **Build and run**:
   ```powershell
   docker compose up --build
   ```

#### Option 2: Local Python Execution

1. **Start Neo4j** (install separately or use Docker)
   ```powershell
   # Using Docker for Neo4j only
   docker run -d \
     --name neo4j \
     -p 7474:7474 -p 7687:7687 \
     -e NEO4J_AUTH=neo4j/password123 \
     neo4j:5.14.0
   ```

2. **Set environment variables** and run ETL:
   ```powershell
   # Set environment variables (or use .env file with python-dotenv)
   $env:NEO4J_URI="bolt://localhost:7687"
   $env:NEO4J_USERNAME="neo4j"
   $env:NEO4J_PASSWORD="password123"
   # ... set CSV paths ...
   
   python hospital_neo4j_etl/src/hospital_bulk_csv_write.py
   ```

#### Data Analysis

Analyze CSV data before loading into Neo4j:

```powershell
python analysis.py
```

This will display:
- Dataset dimensions (rows, columns)
- First 5 rows of hospital data
- First 5 rows of physician data

## 🔒 Security

- ✅ **No hardcoded credentials** - All secrets use environment variables
- ✅ **`.env` excluded** - Environment files not tracked in git
- ✅ **Patient data protected** - CSV files in `data/` folder excluded from version control
- ✅ **Virtual environment ignored** - `venv/` not tracked
- ⚠️ **Change default passwords** - Update Neo4j password in production

## 📦 Dependencies

### Core Dependencies
```
neo4j==5.14.1          # Neo4j Python driver
polars==0.19.19        # Fast DataFrame library
retry==0.9.2           # Retry decorator for fault tolerance
python-dotenv==1.0.0   # Environment variable management
```

### Development Dependencies
```
ipython==8.18.1        # Enhanced Python shell
black                  # Code formatter
flake8                 # Linting
```

## 🛠️ Features

- ✅ **Comprehensive ETL Pipeline**: Loads 6 node types and 6 relationship types
- ✅ **Automatic Retry Logic**: Retries up to 100 times with 10-second delays (handles Neo4j startup)
- ✅ **Data Integrity**: Uniqueness constraints on all node IDs
- ✅ **Bulk CSV Import**: Efficient loading using Neo4j's `LOAD CSV WITH HEADERS`
- ✅ **Dockerized Deployment**: Containerized ETL service
- ✅ **Comprehensive Logging**: Track pipeline progress with detailed logs
- ✅ **Well-Documented Code**: Extensive inline comments explaining each step

## 📝 CSV File Requirements

### Required CSV Files and Columns:

#### `hospitals.csv`
- `hospital_id` (integer)
- `hospital_name` (string)
- `hospital_state` (string)

#### `payers.csv`
- `payer_id` (integer)
- `payer_name` (string)

#### `physicians.csv`
- `physician_id` (integer)
- `physician_name` (string)
- `physician_dob` (date string)
- `physician_grad_year` (year)
- `medical_school` (string)
- `salary` (float)

#### `patients.csv`
- `patient_id` (integer)
- `patient_name` (string)
- `patient_sex` (string)
- `patient_dob` (date string)
- `patient_blood_type` (string)

#### `visits.csv`
- `visit_id` (integer)
- `room_number` (integer)
- `admission_type` (string)
- `date_of_admission` (date string)
- `test_results` (string)
- `visit_status` (string)
- `chief_complaint` (string)
- `treatment_description` (text)
- `primary_diagnosis` (string)
- `discharge_date` (date string)
- `hospital_id` (integer - foreign key)
- `physician_id` (integer - foreign key)
- `patient_id` (integer - foreign key)
- `payer_id` (integer - foreign key)
- `billing_amount` (float)

#### `reviews.csv`
- `review_id` (integer)
- `review` (text)
- `patient_name` (string)
- `physician_name` (string)
- `hospital_name` (string)
- `visit_id` (integer - foreign key)

## 🎯 Example Queries

Once data is loaded, you can query the graph using Cypher (Neo4j Browser at http://localhost:7474):

```cypher
// Find all patients treated by a specific physician
MATCH (patient:Patient)-[:HAS]->(visit:Visit)<-[:TREATS]-(physician:Physician {name: "Dr. Smith"})
RETURN patient.name, visit.admission_date, visit.diagnosis

// Find hospitals with the most visits
MATCH (visit:Visit)-[:AT]->(hospital:Hospital)
RETURN hospital.name, COUNT(visit) AS total_visits
ORDER BY total_visits DESC
LIMIT 10

// Calculate average billing by insurance payer
MATCH (visit:Visit)-[coverage:COVERED_BY]->(payer:Payer)
RETURN payer.name, 
       AVG(coverage.billing_amount) AS avg_billing,
       COUNT(visit) AS total_visits
ORDER BY avg_billing DESC

// Find patient visit history with full context
MATCH (patient:Patient {name: "John Doe"})-[:HAS]->(visit:Visit)
MATCH (visit)-[:AT]->(hospital:Hospital)
MATCH (visit)<-[:TREATS]-(physician:Physician)
MATCH (visit)-[:COVERED_BY]->(payer:Payer)
RETURN patient.name, 
       visit.admission_date, 
       hospital.name, 
       physician.name,
       payer.name,
       visit.diagnosis
ORDER BY visit.admission_date DESC
```

## 🐛 Troubleshooting

### Docker Issues
**Error**: `docker compose: command not found`
- **Solution**: Install Docker Desktop or use `docker-compose` (older version)

**Error**: `unexpected end of JSON input`
- **Solution**: Clean Docker cache: `docker system prune -f`
- Ensure Docker Desktop is running

### Connection Issues
**Error**: `Unable to connect to Neo4j`
- Check Neo4j is running: `docker ps` or check Neo4j Desktop
- Verify `NEO4J_URI` in `.env` matches your Neo4j instance
- Default: `bolt://localhost:7687`

### Build Errors
**Error**: `invalid pyproject.toml config`
- ✅ **Fixed**: Typo corrected (`dependecies` → `dependencies`)

**Error**: Module not found
```powershell
pip install -r requirements.txt
```

### CSV Loading Errors
- Ensure CSV files exist in `data/` directory
- Check column names match requirements exactly
- Verify CSV encoding (UTF-8 recommended)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is for educational purposes.

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Built with ❤️ for healthcare data management**
