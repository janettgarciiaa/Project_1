import os
import requests
import streamlit as st

# -----------------------------
# 💬 Perplexity Chatbot (Working Developer API Version - Oct 2025)
# -----------------------------

st.set_page_config(page_title="Perplexity Chatbot", page_icon="🌐")
st.title("Perplexity Chatbot 🌐")

# Load API key
PPLX_KEY = st.secrets.get("PERPLEXITY_API_KEY", os.getenv("PERPLEXITY_API_KEY", ""))

if not PPLX_KEY:
    st.error("❌ Missing Perplexity API key. Please add it in Settings → Secrets.")
    st.stop()

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Chat Settings")
    st.caption("💡 Using Perplexity developer endpoint (auto model selection).")
    st.success("✅ Connected to Perplexity API")

# Function to call Perplexity API
def ask_perplexity(prompt):
    headers = {
        "Authorization": f"Bearer {PPLX_KEY}",
        "Content-Type": "application/json",
    }

    # ✅ This format works for developer keys — no model field required
    payload = {
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            st.warning(f"⚠️ API {response.status_code}: {response.text}")
            return "⚠️ Perplexity returned an error."

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = ask_perplexity(prompt)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

