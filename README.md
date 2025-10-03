# 🏥 Hospital Chatbot

A hospital data management system that uses Neo4j graph database to store and query healthcare data, built for intelligent chatbot integration.

## 📋 Overview

This project provides an ETL (Extract, Transform, Load) pipeline to import structured hospital data from CSV files into a Neo4j graph database. The data model includes hospitals, patients, physicians, payers, visits, and reviews - creating a comprehensive healthcare knowledge graph.

## 🏗️ Architecture

```
Hospital-Chatbot/
├── data/                          # CSV data files (not tracked in git)
│   ├── hospitals.csv
│   ├── patients.csv
│   ├── physicians.csv
│   ├── payers.csv
│   ├── visits.csv
│   └── reviews.csv
├── hospital_neo4j_etl/           # Neo4j ETL package
│   ├── src/
│   │   ├── hospital_bulk_csv_write.py
│   │   └── entrypoint.sh
│   └── pyproject.toml
├── analysis.py                    # Data analysis utilities
├── docker-compose.yml            # Docker orchestration
└── .gitignore
```

## 📊 Data Model

The graph database contains the following node types:

- **Hospital**: Healthcare facilities with ID, name, and location
- **Patient**: Patient records
- **Physician**: Medical staff information
- **Payer**: Insurance and payment providers
- **Visit**: Patient visit records
- **Review**: Hospital reviews and ratings

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Neo4j Database
- Docker & Docker Compose (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Hospital-Chatbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   # or
   source venv/bin/activate      # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   # Neo4j Configuration
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_password_here
   
   # CSV File Paths (use file:/// URI format)
   HOSPITALS_CSV_PATH=file:///data/hospitals.csv
   PAYERS_CSV_PATH=file:///data/payers.csv
   PHYSICIANS_CSV_PATH=file:///data/physicians.csv
   PATIENTS_CSV_PATH=file:///data/patients.csv
   VISITS_CSV_PATH=file:///data/visits.csv
   REVIEWS_CSV_PATH=file:///data/reviews.csv
   ```

### Usage

#### Run the ETL Pipeline

```bash
python hospital_neo4j_etl/src/hospital_bulk_csv_write.py
```

This will:
1. Connect to Neo4j database
2. Set uniqueness constraints on all node types
3. Load CSV data into the graph database

#### Data Analysis

```bash
python analysis.py
```

Analyzes the healthcare dataset using Polars.

## 🐳 Docker Deployment

*(To be configured in docker-compose.yml)*

```bash
docker-compose up -d
```

## 🔒 Security

- All sensitive credentials are stored in environment variables
- `.env` files are excluded from version control
- Patient data (CSV files) is not tracked in git
- Use strong passwords for Neo4j database

## 📦 Dependencies

- `neo4j` - Neo4j Python driver
- `polars` - Fast DataFrame library for data analysis
- `retry` - Retry decorator for handling transient failures
- `python-dotenv` - Environment variable management (recommended)

## 🛠️ Features

- **Retry Logic**: Automatic retry (up to 100 attempts) for database connection failures
- **Uniqueness Constraints**: Ensures data integrity with unique ID constraints
- **Bulk CSV Import**: Efficient data loading using Neo4j's `LOAD CSV` feature
- **Graph Relationships**: Ready for relationship creation between nodes (patients-visits, visits-hospitals, etc.)

## 📝 CSV File Requirements

Your CSV files should have the following columns:

- **hospitals.csv**: `hospital_id`, `hospital_name`, `state`
- **patients.csv**: TBD
- **physicians.csv**: TBD
- **payers.csv**: TBD
- **visits.csv**: TBD
- **reviews.csv**: TBD

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is for educational purposes.

## 🐛 Troubleshooting

### Connection Issues
- Ensure Neo4j is running on `bolt://localhost:7687`
- Check your credentials in `.env` file
- Verify firewall settings

### CSV Loading Errors
- Ensure CSV file paths use `file:///` URI format
- Check that CSV column names match the query expectations
- Verify CSV files are accessible to Neo4j

### Module Not Found
```bash
pip install polars neo4j retry
```

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Built with ❤️ for healthcare data management**
