import os
import requests
import streamlit as st

# -----------------------------
# Perplexity-Only Chatbot (2025 Stable Format)
# -----------------------------

st.set_page_config(page_title="Claude Chatbot with Web Search", page_icon="🌐")
st.title("Claude Chatbot with Web Search 🌐")

# Load the Perplexity API key
PPLX_KEY = st.secrets.get("PERPLEXITY_API_KEY", os.getenv("PERPLEXITY_API_KEY", ""))

if not PPLX_KEY:
    st.error("Missing Perplexity API key. Please add it in Settings → Secrets.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Web Search Settings")
    use_web = st.checkbox("Enable Web Search", value=True)
    st.caption("When enabled, Perplexity fetches live information from the web.")

# Function to call Perplexity API
def ask_perplexity(prompt, web_enabled=True):
    # ✅ Use the current supported model names
    model = "llama-3.1-sonar-small-128k-online" if web_enabled else "llama-3.1-sonar-small-128k-chat"
    headers = {
        "Authorization": f"Bearer {PPLX_KEY}",
        "Content-Type": "application/json",
    }
    # ✅ Updated payload structure
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500,
        "temperature": 0.2,
        "top_p": 0.9,
        "stream": False,  # Perplexity now requires this key explicitly
    }

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        # ✅ Correct field path (as of Oct 2025)
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ API Error: {e}"

# Display chat history
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

