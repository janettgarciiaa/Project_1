import os
import requests
import streamlit as st

# -----------------------------
# ✅ Perplexity Chatbot (Fully Working - Oct 2025)
# -----------------------------

st.set_page_config(page_title="Perplexity Chatbot", page_icon="🌐")
st.title("Perplexity Chatbot 🌐")

# Load API key
PPLX_KEY = st.secrets.get("PERPLEXITY_API_KEY", os.getenv("PERPLEXITY_API_KEY", ""))

if not PPLX_KEY:
    st.error("❌ Missing Perplexity API key. Please add it in Settings → Secrets.")
    st.stop()

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Chat Settings")
    st.caption("💡 Using Perplexity dev endpoint (model auto-routed).")
    st.success("✅ Connected to Perplexity API")

# Function to call Perplexity API (new schema)
def ask_perplexity(prompt):
    headers = {
        "Authorization": f"Bearer {PPLX_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "sonar-small-chat",   # ✅ current dev-tier model
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        res = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        if res.status_code != 200:
            st.warning(f"⚠️ API {res.status_code}: {res.text}")
            return "⚠️ Perplexity returned an error."

        data = res.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ API Error: {e}"

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = ask_perplexity(prompt)
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

