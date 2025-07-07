import streamlit as st
import pandas as pd
import pickle
import os
import plotly.express as px
from datetime import datetime

# --------------- CONFIG ----------------
st.set_page_config(page_title="SaaS Waste Analyzer", layout="wide")
st.title("📊 SaaS License Waste Analyzer")

# --------------- Load ML Model ----------------
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")

if not os.path.exists(model_path):
    st.error("❌ model.pkl not found. Please upload the model file.")
    st.stop()

model = pickle.load(open(model_path, "rb"))

# --------------- Upload CSV ----------------
st.markdown("### 📥 Upload Your SaaS License Usage CSV")

uploaded_file = st.file_uploader("Upload a CSV file with columns: License Count, Monthly Cost, Active Users", type=["csv"])

if uploaded_file is not None:
    try:
        user_df = pd.read_csv(uploaded_file)

        required_cols = {"License Count", "Monthly Cost", "Active Users"}
        if not required_cols.issubset(user_df.columns):
            st.error(f"❌ CSV must contain these columns: {required_cols}")
            st.stop()

        # --------------- Predict Waste ----------------
        input_features = user_df[["License Count", "Monthly Cost", "Active Users"]]
        user_df["Prediction"] = model.predict(input_features)

        # --------------- Simulate Hourly Time Series ----------------
        user_df["Date"] = pd.date_range(end=datetime.today(), periods=len(user_df), freq="H")
        user_df["Hour"] = user_df["Date"].dt.strftime("%H:%M")
        user_df["Month"] = user_df["Date"].dt.strftime("%b %Y")

        # --------------- Summary KPIs ----------------
        st.markdown("---")
        st.subheader("📊 Prediction Summary")

        waste_count = user_df[user_df["Prediction"] == 1].shape[0]
        no_waste_count = user_df[user_df["Prediction"] == 0].shape[0]
        total_waste_cost = user_df[user_df["Prediction"] == 1]["Monthly Cost"].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("🔍 Total Services", len(user_df))
        col2.metric("⚠️ Waste Detected", waste_count)
        col3.metric("💸 Potential Monthly Savings", f"₹{total_waste_cost:,.0f}")

        # --------------- PIE CHART ----------------
        st.subheader("📊 Waste vs No Waste Breakdown")
        pie_data = pd.DataFrame({
            "Type": ["Waste", "No Waste"],
            "Count": [waste_count, no_waste_count]
        })
        fig_pie = px.pie(pie_data, names="Type", values="Count", color_discrete_sequence=["#EF553B", "#00CC96"])
        fig_pie.update_traces(textinfo="label+percent")
        st.plotly_chart(fig_pie, use_container_width=True)

        # --------------- HOURLY TREND CHART ----------------
        st.subheader("📈 Hourly Waste Detection Trend (Simulated)")
        hourly = (
            user_df[user_df["Prediction"] == 1]
            .groupby("Hour")["Monthly Cost"]
            .sum()
            .reset_index()
        )
        fig_line = px.line(hourly, x="Hour", y="Monthly Cost", markers=True,
                           title="📉 Predicted Waste by Hour (Demo)")
        fig_line.update_layout(xaxis_title="Hour", yaxis_title="₹ Waste", title_x=0.3)
        st.plotly_chart(fig_line, use_container_width=True)

        # --------------- TABLE ----------------
        st.subheader("📄 Full Prediction Table")
        st.dataframe(user_df, use_container_width=True)

        # --------------- DOWNLOAD RESULTS ----------------
        st.download_button(
            label="⬇️ Download Prediction CSV",
            data=user_df.to_csv(index=False).encode(),
            file_name="predicted_waste_output.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")

else:
    st.info("📁 Upload a CSV file to begin analyzing your SaaS license waste.")
    st.markdown("""
        **Expected Format:**
        ```
        License Count,Monthly Cost,Active Users
        10,150,3
        25,300,20
        12,120,12
        ```
    """)

# --------------- FOOTER ----------------
st.markdown("---")
st.caption("© 2025 SaaS Optimizer · Built with 💡 by Yash Tandle")
