# check_env.py
import sys
import streamlit as st

st.title("🛠 Python Environment Checker")
st.write("✅ Python Executable Being Used:")
st.code(sys.executable)
