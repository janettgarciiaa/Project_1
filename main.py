import os
import requests
import streamlit as st

# -----------------------------
# Perplexity-Only Chatbot (Final 2025 Spec)
# -----------------------------

st.set_page_config(page_title="Claude Chatbot with Web Search", page_icon="🌐")
st.title("Claude Chatbot with Web Search 🌐")

# Load the Perplexity API key
PPLX_KEY = st.secrets.get("PERPLEXITY_API_KEY", os.getenv("PERPLEXITY_API_KEY", ""))

# Stop if no key
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
    st.caption("When enabled, Perplexity will fetch real-time information from the web.")

# Function to call Perplexity API
def ask_perplexity(prompt, web_enabled=True):
    model = "llama-3.1-sonar-small-128k-online" if web_enabled else "llama-3.1-sonar-small-128k-chat"
    headers = {
        "Authorization": f"Bearer {PPLX_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_output_tokens": 512,
        "return_related_questions": False,
    }

    try:
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            json=data,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"⚠️ Network or API error: {str(e)}"
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle new user input
if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = ask_perplexity(prompt, use_web)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

