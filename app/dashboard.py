import streamlit as st
import pickle
import os
import csv
from datetime import datetime

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="SaaS License Optimizer",
    page_icon="💡",
    layout="centered"
)

# ----------------- Sidebar -----------------
with st.sidebar:
    st.image("https://avatars.githubusercontent.com/u/116947480?v=4", width=120)
    st.markdown("### 👤 Yash Tandle")
    st.caption("Cloud & DevOps | AI Builder | Future Architect")
    st.markdown("---")
    st.markdown("🚀 This project uses AI to help reduce your SaaS license waste.")
    st.markdown("💡 Powered by machine learning with a focus on real-time cost optimization.")
    st.markdown("---")
    st.info("Project: SaaS License Optimizer v1", icon="🧠")

# ----------------- CSS -----------------
st.markdown("""
    <style>
        .big-font {
            font-size: 30px !important;
            font-weight: bold;
        }
        .sub-font {
            font-size: 16px;
            color: #888;
        }
        .rounded-box {
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .footer {
            text-align: center;
            font-size: 13px;
            color: #aaa;
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- Title Area -----------------
st.markdown("<div class='big-font'>🧠 SaaS License Waste Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-font'>Predict unused license waste and optimize your SaaS spend like a pro.</div><br>", unsafe_allow_html=True)

# ----------------- Load ML Model -----------------
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

if not os.path.exists(model_path):
    st.error("❌ model.pkl not found. Please ensure it's uploaded correctly.")
    st.stop()

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.stop()

# ----------------- Input Form -----------------
with st.form("predict_form", clear_on_submit=False):
    st.markdown("### 📥 Enter SaaS Usage Metrics")

    col1, col2 = st.columns(2)
    with col1:
        license_count = st.number_input("🔢 Total Licenses Purchased", min_value=1)
        active_users = st.number_input("👥 Active Users Last 30 Days", min_value=0)
        department = st.selectbox("🏢 Department", ["Engineering", "Sales", "Marketing", "HR", "Finance", "Other"])
    with col2:
        monthly_cost = st.number_input("💰 Monthly Cost (₹)", min_value=0.0, step=0.1)
        usage_frequency = st.slider("📈 Usage Frequency (%)", 0, 100, 60)
        contract_lockin = st.selectbox("📄 Under Contract Lock-in?", ["Yes", "No"])

    notes = st.text_area("📝 Any special notes for this service?", placeholder="E.g., Critical tool, may reduce usage next quarter...")

    submitted = st.form_submit_button("🚀 Predict Waste")

# ----------------- Prediction -----------------
if submitted:
    input_data = [[license_count, monthly_cost, active_users]]

    try:
        prediction = model.predict(input_data)[0]

        st.markdown("### 📣 Prediction Summary")

        if prediction == 1:
            st.markdown(
                "<div class='rounded-box' style='background-color:#ffe6e6;'>"
                "<h4 style='color:#d9534f;'>⚠️ Waste Detected</h4>"
                "This service shows signs of <strong>underutilization</strong>. Consider reducing license count or reallocating."
                "</div>", unsafe_allow_html=True)
        else:
            st.markdown(
                "<div class='rounded-box' style='background-color:#e6ffe6;'>"
                "<h4 style='color:#5cb85c;'>✅ No Waste Detected</h4>"
                "Good job! Your current license setup appears optimized."
                "</div>", unsafe_allow_html=True)

        # ----------------- Save to waste_log.csv -----------------
        log_data = {
            "Date": datetime.today().strftime("%Y-%m-%d"),
            "Service Name": department + " Tool",
            "Monthly Cost": monthly_cost,
            "Prediction": prediction
        }

        log_file = os.path.join(os.path.dirname(__file__), "waste_log.csv")
        file_exists = os.path.exists(log_file)

        with open(log_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=log_data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(log_data)

        # 📊 Debug Info
        with st.expander("🔍 Show Prediction Details"):
            st.json({
                "License Count": license_count,
                "Monthly Cost": monthly_cost,
                "Active Users": active_users,
                "Usage Frequency (%)": usage_frequency,
                "Department": department,
                "Lock-in": contract_lockin,
                "Prediction": "Waste" if prediction == 1 else "No Waste"
            })

    except Exception as e:
        st.error(f"Prediction failed: {e}")

# ----------------- Footer -----------------
st.markdown("<div class='footer'>© 2025 SaaS License Optimizer | Designed by Yash Tandle 💼</div>", unsafe_allow_html=True)
