# main.py
import streamlit as st
import requests
import os
import json

# --- PAGE SETUP ---
st.set_page_config(page_title="Claude Chatbot", page_icon="🤖")
st.title("Claude Chatbot with Web Search 🌐")

# --- DEFINE STATE ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# --- BASIC SETTINGS ---
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Claude system behavior
system_prompt = (
    "You are Claude, a helpful, factual assistant. "
    "Always provide clear, accurate, and sourced answers. "
    "If web search context is available, use it."
)

# --- DEFINE FUNCTIONS ---

# Claude REST call (no SDK errors)
def ask_claude_via_rest(prompt: str):
    if not ANTHROPIC_API_KEY:
        return "Error: Anthropic API key not found."
    try:
        headers = {
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01"
        }
        data = {
            "model": "claude-3-sonnet-20240229",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}]
        }
        resp = requests.post("https://api.anthropic.com/v1/messages",
                             headers=headers, data=json.dumps(data))
        if resp.status_code == 200:
            content = resp.json()
            return content["content"][0]["text"]
        else:
            return f"Error from Claude API: {resp.text}"
    except Exception as e:
        return f"Claude API error: {str(e)}"


# Optional: Web search via Perplexity (if enabled)
def run_web_search(query: str):
    if not PERPLEXITY_API_KEY:
        return None, None, None
    try:
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"model": "pplx-7b-online", "messages": [{"role": "user", "content": query}]}
        r = requests.post("https://api.perplexity.ai/chat/completions",
                          headers=headers, json=payload)
        if r.status_code == 200:
            result = r.json()
            context = result["choices"][0]["message"]["content"]
            sources = result["choices"][0].get("sources", [])
            sources_md = "\n".join([f"- [{s['title']}]({s['url']})" for s in sources]) if sources else None
            search_note = "Results provided by Perplexity Search API."
            return context, sources_md, search_note
        else:
            return None, f"Error: {r.text}", None
    except Exception as e:
        return None, f"Search error: {str(e)}", None


# --- UI SECTION ---

user_input = st.chat_input("Ask Claude anything...")
sources_md = None
search_note = None
context_from_search = None

if user_input:
    # Append user message to session
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Try web search first
    context_from_search, sources_md, search_note = run_web_search(user_input)

    # Prepare full Claude prompt
    full_prompt = f"{system_prompt}\n\nUser: {user_input}"
    if context_from_search:
        full_prompt += f"\n\nWeb context:\n{context_from_search}"

    # Get Claude response
    response_text = ask_claude_via_rest(full_prompt)

    # Display assistant output
    with st.chat_message("assistant"):
        if sources_md:
            st.markdown(sources_md)
            st.markdown("---")
        st.markdown(response_text)
        if search_note:
            st.caption(search_note)

    # Save Claude response to session
    st.session_state["messages"].append({
        "role": "assistant",
        "content": response_text if response_text else "(no response)"
    })

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

