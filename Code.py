import pandas as pd
import sqlite3
from datetime import datetime
import random
from sklearn.ensemble import IsolationForest
import numpy as np

# --- Load CSVs ---
safety_df = pd.read_csv(r"C:\Users\nithi\Downloads\Dataset\Dataset\[Usecase 4] AI for Elderly Care and Support\safety_monitoring.csv")
reminder_df = pd.read_csv(r"C:\Users\nithi\Downloads\Dataset\Dataset\[Usecase 4] AI for Elderly Care and Support\daily_reminder.csv")
health_df = pd.read_csv(r"C:\Users\nithi\Downloads\Dataset\Dataset\[Usecase 4] AI for Elderly Care and Support\health_monitoring.csv")

# --- Clean & Prepare Data ---
# Remove unnamed columns
safety_df = safety_df.loc[:, ~safety_df.columns.str.contains('^Unnamed')]
reminder_df = reminder_df.loc[:, ~reminder_df.columns.str.contains('^Unnamed')]
health_df = health_df.loc[:, ~health_df.columns.str.contains('^Unnamed')]

# Convert time columns
safety_df['Timestamp'] = pd.to_datetime(safety_df['Timestamp'])
reminder_df['Scheduled Time'] = pd.to_datetime(reminder_df['Scheduled Time'])
health_df['Timestamp'] = pd.to_datetime(health_df['Timestamp'])

# Add control columns
if 'Delivered' not in reminder_df.columns:
    reminder_df['Delivered'] = 0

# --- Save to SQLite ---
conn = sqlite3.connect("elderly_care.db")
safety_df.to_sql("safety", conn, if_exists="replace", index=False)
reminder_df.to_sql("reminders", conn, if_exists="replace", index=False)
health_df.to_sql("health", conn, if_exists="replace", index=False)

# --- Agents ---
class SafetyAgent:
    def __init__(self, conn):
        self.conn = conn
        self.model = IsolationForest(contamination=0.01)

    def detect_anomalies(self):
        df = pd.read_sql("SELECT * FROM safety", self.conn)
        df['duration'] = pd.to_numeric(df['Post-Fall Inactivity Duration (Seconds)'], errors='coerce')
        df_clean = df[['duration']].dropna()

        if len(df_clean) < 10:
            return "Insufficient data"

        self.model.fit(df_clean)
        df['anomaly'] = self.model.predict(df[['duration']])
        anomalies = df[df['anomaly'] == -1]
        return anomalies[['Timestamp', 'Post-Fall Inactivity Duration (Seconds)', 'Location']]

class ReminderAgent:
    def __init__(self, conn):
        self.conn = conn

    def get_due_reminders(self):
        now = datetime.now()
        query = f"""
        SELECT rowid, * FROM reminders
        WHERE "Scheduled Time" <= ? AND Delivered = 0
        """
        return pd.read_sql(query, self.conn, params=(now,))

    def mark_delivered(self, rowid):
        cur = self.conn.cursor()
        cur.execute("UPDATE reminders SET Delivered = 1 WHERE rowid = ?", (rowid,))
        self.conn.commit()

class HealthAgent:
    def __init__(self, conn):
        self.conn = conn

    def check_latest_vitals(self):
        df = pd.read_sql("SELECT * FROM health ORDER BY Timestamp DESC LIMIT 1", self.conn)
        if df.empty:
            return "No health data available"

        vitals = df.iloc[0]
        alerts = []

        try:
            if float(vitals["Heart Rate"]) < 50 or float(vitals["Heart Rate"]) > 100:
                alerts.append("⚠️ Abnormal heart rate")
            if float(vitals["Glucose Levels"]) > 180:
                alerts.append("⚠️ High glucose level")
            if float(vitals["Oxygen Saturation (SpO₂%)"]) < 92:
                alerts.append("⚠️ Low SpO₂")
        except Exception as e:
            alerts.append(f"Error parsing vitals: {e}")

        return alerts or ["Vitals normal."]

class LLM_Ollama:
    def ask(self, prompt):
        return f"Ollama: [Response to: '{prompt}']"  # Stub; replace with real API if needed

# --- Coordinator ---
class Coordinator:
    def __init__(self):
        self.safety_agent = SafetyAgent(conn)
        self.reminder_agent = ReminderAgent(conn)
        self.health_agent = HealthAgent(conn)
        self.llm_agent = LLM_Ollama()

    def run_cycle(self):
        print("🔍 Safety Monitoring:")
        safety_alerts = self.safety_agent.detect_anomalies()
        if isinstance(safety_alerts, str):
            print(" -", safety_alerts)
        else:
            print(safety_alerts)

        print("\n📢 Reminders:")
        due_reminders = self.reminder_agent.get_due_reminders()
        if not due_reminders.empty:
            for _, row in due_reminders.iterrows():
                print(f"Reminder: {row['Reminder Type']} at {row['Scheduled Time']}")
                self.reminder_agent.mark_delivered(row['rowid'])
        else:
            print("No due reminders.")

        print("\n🧪 Health Check:")
        alerts = self.health_agent.check_latest_vitals()
        for alert in alerts:
            print(alert)

        print("\n🧠 LLM Advice:")
        print(self.llm_agent.ask("Give fall prevention tips for elderly."))

# --- Run System ---
if __name__ == "__main__":
    system = Coordinator()
    system.run_cycle()
