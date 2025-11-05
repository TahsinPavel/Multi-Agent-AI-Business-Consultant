import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Multi-Agent AI Business Consultant", layout="wide")

st.title("Multi-Agent AI Business Consultant")

st.markdown("Enter a business request and choose the type of consultation.")

request_text = st.text_area("Business request", height=200)

col1, col2, col3 = st.columns(3)

with col1:
	if st.button("Market Analysis"):
		if not request_text.strip():
			st.warning("Please enter a business request first.")
		else:
			with st.spinner("Contacting backend..."):
				resp = requests.post(f"{BACKEND_URL}/consult/market", json={"request": request_text})
				st.subheader("Market Analysis")
				if resp.ok:
					st.text(resp.json().get("response", resp.text))
				else:
					st.error(f"Error: {resp.status_code} {resp.text}")

with col2:
	if st.button("Financial Analysis"):
		if not request_text.strip():
			st.warning("Please enter a business request first.")
		else:
			with st.spinner("Contacting backend..."):
				resp = requests.post(f"{BACKEND_URL}/consult/financial", json={"request": request_text})
				st.subheader("Financial Analysis")
				if resp.ok:
					st.text(resp.json().get("response", resp.text))
				else:
					st.error(f"Error: {resp.status_code} {resp.text}")

with col3:
	if st.button("Strategy"):
		if not request_text.strip():
			st.warning("Please enter a business request first.")
		else:
			with st.spinner("Contacting backend..."):
				resp = requests.post(f"{BACKEND_URL}/consult/strategy", json={"request": request_text})
				st.subheader("Strategy")
				if resp.ok:
					st.text(resp.json().get("response", resp.text))
				else:
					st.error(f"Error: {resp.status_code} {resp.text}")

st.markdown("---")
if st.button("Comprehensive Consultation (All Agents)"):
	if not request_text.strip():
		st.warning("Please enter a business request first.")
	else:
		with st.spinner("Contacting backend for comprehensive consultation..."):
			resp = requests.post(f"{BACKEND_URL}/consult/comprehensive", json={"request": request_text})
			if resp.ok:
				data = resp.json()
				for key, val in data.items():
					st.subheader(f"{key.capitalize()} Agent")
					st.text(val.get("response", ""))
			else:
				st.error(f"Error: {resp.status_code} {resp.text}")

st.caption("Backend URL can be overridden with BACKEND_URL environment variable.")
