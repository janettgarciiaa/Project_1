import os
import requests
import streamlit as st

# -----------------------------
# Perplexity Chatbot (Developer Key Version)
# -----------------------------

st.set_page_config(page_title="Perplexity Chatbot", page_icon="🌐")
st.title("Perplexity Chatbot 🌐")

# Load the Perplexity API key
PPLX_KEY = st.secrets.get("PERPLEXITY_API_KEY", os.getenv("PERPLEXITY_API_KEY", ""))

# Stop if no key
if not PPLX_KEY:
    st.error("❌ Missing Perplexity API key. Please add it in Settings → Secrets.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Web Search Settings")
    use_web = st.checkbox("Enable Web Search", value=True)
    st.caption("When enabled, Perplexity will fetch real-time info from the web.")

# Function to call Perplexity API (developer key version)
def ask_perplexity(prompt, web_enabled=True):
    model = "llama-3.1-sonar-small-128k-online" if web_enabled else "llama-3.1-sonar-small-128k-chat"
    headers = {
        "Authorization": f"Bearer {PPLX_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        # ✅ Correct endpoint for developer keys
        response = requests.post(
            "https://api.perplexity.ai/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        data = response.json()

        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["text"]
        else:
            return "⚠️ No response content returned."

    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

# Display previous messages
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
            reply = ask_perplexity(prompt, use_web)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

