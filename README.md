# 🧠 SaaS License Optimizer

An AI-powered dashboard that detects **SaaS license waste** and helps organizations **cut costs and optimize usage**.

---

## 🚀 Project Highlights

- 🔍 Predicts underutilized SaaS licenses using ML (RandomForest)
- 📊 Admin dashboard with trends, monthly waste, logs
- ⚙️ Built with **Streamlit**, **Flask**, **JWT Auth**, and **SQLite**
- 🔐 JWT-secured REST API
- ☁️ AWS Lambda-ready architecture

---

## 🧱 Tech Stack

| Frontend     | Backend        | ML/Infra           |
|--------------|----------------|--------------------|
| Streamlit    | Flask + JWT    | Scikit-learn, Pandas |
| Plotly       | SQLite         | Pickle             |

---

## 📂 Project Structure

```bash
SaaS-License-Optimizer/
├── dashboard.py              # Streamlit UI
├── admin_dashboard.py        # Waste analytics
├── lambda/                   # Deployable Streamlit app
├── model.pkl                 # Trained ML model
├── service_costs.csv         # Cost tracking
├── auth_backend/             # JWT-based API backend
├── models/                   # Prediction logic
├── requirements.txt
└── .gitignore
