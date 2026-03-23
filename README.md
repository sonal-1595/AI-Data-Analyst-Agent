# 🚀 AI Data Analyst Dashboard

## 📌 Overview

This project is a full-stack AI-powered data analytics system that allows users to:
	•	Upload CSV/Excel files
	•	Visualize data with interactive charts
	•	Generate automatic insights
	•	Ask AI questions about the data
	•	Export AI-generated reports (PDF & TXT)

It consists of:
	•	Frontend: Streamlit dashboard
	•	Backend: FastAPI + LangChain + OpenAI

⸻

## 🏗️ Architecture

Frontend (Streamlit)
        ↓
FastAPI Backend (/analyze)
        ↓
LangChain Pandas Agent
        ↓
OpenAI GPT Model


⸻

## ⚙️ Features

### ✅ Frontend (Streamlit)
	•	File upload (CSV, Excel)
	•	Data preview
	•	KPI metrics (Mean, Max, Min)
	•	Smart chart suggestions
	•	Multiple chart types:
	•	Bar
	•	Line
	•	Scatter
	•	Histogram
	•	Box
	•	Interactive visualization (Plotly)
	•	AI query interface
	•	Report export (PDF & TXT)

### ✅ Backend (FastAPI)
	•	File cleaning & preprocessing
	•	Multi-file merging
	•	AI-powered analysis using LangChain agent
	•	Natural language query handling
	•	Business insights generation

⸻

## 📂 Project Structure

### project/
│
├── frontend/
│   └── app.py          # Streamlit UI
│
├── backend/
│   └── main.py         # FastAPI server
│
├── requirements.txt
└── README.md


⸻

## 🔧 Installation

### 1️⃣ Install Dependencies

pip install -r requirements.txt

⸻

### ▶️ Running the Project

## Start Backend (FastAPI)

cd backend
python main.py

Backend will run on:

http://localhost:8000

⸻

## Start Frontend (Streamlit)

cd frontend
streamlit run app.py

Frontend will run on:

http://localhost:8501


⸻

## 🔑 Configuration

In the Streamlit sidebar:
	•	Enter your OpenAI API Key
	•	Set backend URL (default):

http://localhost:8000/analyze


⸻

# 📊 How It Works

1. File Upload
	•	Users upload CSV or Excel files
	•	Files are cleaned (remove empty rows, fix columns)

2. Data Processing
	•	Multiple files are merged using common columns

3. Visualization
	•	Auto-suggested chart based on data type
	•	User can manually select chart type

4. AI Analysis
	•	Query is sent to backend
	•	LangChain agent analyzes dataframe
	•	GPT model generates insights

5. Report Generation
	•	Output can be downloaded as:
	•	PDF
	•	TXT

⸻

## 🧠 AI Capabilities

The system can:
	•	Answer business questions
	•	Detect trends
	•	Identify anomalies
	•	Generate summary reports
	•	Create tabular insights

⸻

## 🛠️ Tech Stack
	•	Frontend: Streamlit, Plotly
	•	Backend: FastAPI
	•	AI Framework: LangChain
	•	LLM: OpenAI GPT-4o
	•	Data Processing: Pandas
	•	PDF Generation: FPDF
⸻

### 👩🏻‍💻 Author

Sonal Mishra

⸻

🔥 Build your own AI-powered analytics system!