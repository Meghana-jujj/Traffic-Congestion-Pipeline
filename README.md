# Traffic-Congestion-Pipeline
## 🚦 Real-Time Traffic Congestion Monitoring & Alerting System

This project simulates real-time traffic data using Kafka and processes it using PySpark before storing results in a PostgreSQL database. The final visualizations are created in Tableau and Power BI. Everything is run locally, with no AWS or paid tools required — ideal for showcasing **end-to-end data engineering skills**.

## 💡 Key Features

- 🔄 **Kafka Producer** for streaming traffic data in real time  
- ⚡ **PySpark Structured Streaming** to clean, filter, and transform incoming data  
- 🛢️ **PostgreSQL** for storing processed data  
- 📊 **Dashboards** in Power BI and Tableau to monitor congestion  
- 🧱 **Modular architecture** built like a real-world project  
- 🖼️ Includes diagrams, SQL scripts, code, and sample data   

# Project Structure
traffic-congestion-pipeline/
├── data/ # Simulated traffic CSV data files
├── kafka_producer/ # Python script to stream data into Kafka
├── spark_processor/ # PySpark streaming application
├── database/ # PostgreSQL setup scripts and SQL files
├── dashboards/
│ ├── tableau/ # Tableau dashboards and screenshots
│ └── powerbi/ # Power BI dashboards and screenshots
├── diagrams/ # Architecture diagrams and flowcharts
├── requirements.txt # Python dependencies file
├── .gitignore # Files to be ignored by Git
└── README.md # Project documentation and overview

---

## 📦 Tech Stack

| Layer             | Tools                      |
|------------------|----------------------------|
| Data Streaming   | Apache Kafka + Python      |
| Processing       | PySpark                    |
| Storage          | PostgreSQL                 |
| Visualization    | Tableau, Power BI          |
| Diagramming      | draw.io / Excalidraw       |

---

## 🛠️ How to Run This Project

This project is still in development, and each step will be implemented in a separate folder with code, instructions, and visual outputs.

 ✅ Step 1: Setup Kafka, Zookeeper locally  
 ✅ Step 2: Create sample traffic data (CSV)  
 ✅ Step 3: Kafka Producer to stream traffic data  
 ✅ Step 4: PySpark consumer to process data  
 ✅ Step 5: Save output to PostgreSQL  
 ✅ Step 6: Build Tableau/Power BI dashboards  
 ✅ Step 7: Draw full architecture diagram  

---

## 📊 Sample Use Case

This project can simulate:
- Monitor city-wide traffic using IoT and GPS data  
- Identify slow-moving traffic in key areas  
- Trigger alerts when average speed drops below thresholds  
- Aggregate and visualize historical traffic trends

---

## 🧠 Learnings & Goals

This project was created to showcase real-world data engineering skills including:
- Working with real-time streaming data
- Building a Kafka → Spark → Database pipeline
- Creating professional, job-ready dashboards
- Documenting and deploying projects like a developer


# Link to Streamlit 
https://traffic-congestion-pipeline-sxgjydzmcptlfpzg5xzj6b.streamlit.app/

---

## 🧑‍💻 Author

**Meghana Jujjavarapu**  



