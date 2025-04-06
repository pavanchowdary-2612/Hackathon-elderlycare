
# 🧠 Sanjeevani AI – Multi-Agent Elderly Care System

Sanjeevani AI is an intelligent, multi-agent system designed to proactively assist in elderly care. Built for a real-time environment, it monitors health vitals, manages medication reminders, detects emergencies, and generates alerts — all coordinated via AI agents and local LLMs.

---

## 📌 Problem Statement

Elderly individuals often face challenges in managing health, safety, and daily routines, especially in the absence of continuous caregiving. Sanjeevani AI addresses this by providing:

- Real-time monitoring of vitals and activity
- Personalized reminders
- Emergency detection and alerts
- A multi-agent system to ensure modular, scalable responses

---

## 🏗️ Technologies Used

| Category | Tools / Technologies |
|----------|----------------------|
| **Multi-Agent System** | LangGraph |
| **LLM (Local)** | Ollama |
| **Data Handling** | pandas, numpy |
| **Machine Learning** | scikit-learn (Isolation Forest), rule-based logic |
| **Backend/Storage** | SQLite |
| **Custom Tools** | Python-based Reminder/Alert APIs |
| **Frontend (Optional)** | Streamlit / Flask |
| **Visualization** | matplotlib, seaborn (for trends) |

---

## ⚙️ System Architecture

The system consists of specialized agents:

### 🧩 Agent Roles

- **Health Monitor Agent**: Analyzes real-time health vitals like blood pressure, pulse, SpO2.
- **Safety Agent**: Detects emergencies (e.g., falls, inactivity).
- **Reminder Agent**: Sends reminders for medication, hydration, doctor visits.
- **Alert Agent**: Dispatches alerts via SMS/email/dashboard in emergency or non-compliance.
- **Scheduler Agent**: Coordinates agent flow based on data and LLM-generated logic.

---

## 🗂️ Dataset Columns

**Health Monitoring**: `heart_rate`, `bp_sys`, `bp_dia`, `spo2`, `body_temp`  
**Safety Monitoring**: `fall_detected`, `motion`, `emergency_button`  
**Reminders**: `medication_time`, `medication_name`, `status`

---

## 🔁 Flow Overview

```
1. Load data from CSVs
2. Pass through respective agents:
   - Health anomalies → Alert
   - Missed reminders → Alert
   - Emergency events → Alert
3. Agents interact through Scheduler
4. Output: Notifications, logs, alerts
5. Logged in SQLite and visualized on UI (optional)
```

---

## ✅ Features

- 🔍 **Continuous Monitoring**: Real-time analysis of elderly vitals and activities  
- ⏰ **Smart Reminders**: Scheduled notifications based on dataset  
- 🚨 **Emergency Alerts**: Fall/inactivity detection & alerts  
- 🧠 **LLM-Driven Decisions**: Agents adapt behavior based on context  
- 📊 **Historical Logs**: Stored for caregiver review and analytics  

---

## 🚀 Getting Started

```bash
# Install dependencies
pip install pandas numpy scikit-learn langgraph flask streamlit sqlite3

# Launch the system
python main.py
```

Optional: Run the UI dashboard  
```bash
streamlit run dashboard.py
```

---

## 📚 References / Other Details

- LangGraph documentation: https://docs.langgraph.dev
- Ollama LLM setup: https://ollama.com
- Dataset: Provided by Hackathon organizers
- Built during [Hackathon Name], 2025
