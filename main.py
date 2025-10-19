from dotenv import load_dotenv
import os
import requests
import streamlit as st
from anthropic import Anthropic

load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
from anthropic import Anthropic

client = Anthropic(api_key=anthropic_api_key, max_retries=None)

def perplexity_search(query):
    """Perform a web search using Perplexity API"""
    url = "https://api.perplexity.ai/search"
    headers = {
        "Authorization": f"Bearer {perplexity_api_key}",
        "Content-Type": "application/json"
    }
    data = {"query": query}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if not results:
            return "No search results found."
        formatted = "\n\n".join(
            [f"🔹 **{r['title']}**\n{r['url']}" for r in results[:3]]
        )
        return f"### Top Search Results\n{formatted}"
    else:
        return f"Error: {response.status_code} - {response.text}"

import os
import streamlit as st
import anthropic
from dotenv import load_dotenv
from serpapi import GoogleSearch

# ----------------------------
# Load environment variables
# ----------------------------
load_dotenv()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SERPAPI_API_KEY   = os.getenv("SERPAPI_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Claude Chatbot (Web Search Edition)", page_icon="🤖")
import streamlit as st
from dotenv import load_dotenv
import os
import requests
from anthropic import Anthropic

# Load API keys
load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
client = Anthropic(api_key=anthropic_api_key)

# Define Perplexity Search Function
def perplexity_search(query):
    url = "https://api.perplexity.ai/search"
    headers = {
        "Authorization": f"Bearer {perplexity_api_key}",
        "Content-Type": "application/json"
    }
    data = {"query": query}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        results = response.json().get("results", [])
        if not results:
            return "No search results found."
        formatted = "\n\n".join(
            [f"🔹 **{r.get('title', 'No title')}**\n{r.get('url', '')}" for r in results[:3]]
        )
        return f"### Top Search Results\n{formatted}"
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit UI
st.title("Claude Chatbot")

checkbox_state = st.checkbox("Enable Web Search")
user_input = st.text_input("What would you like to talk about?")

if st.button("Submit") and user_input:
    if checkbox_state:
        st.write("🔍 Searching the web with Perplexity...")
        search_results = perplexity_search(user_input)
        st.markdown(search_results)
    else:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=300,
            messages=[{"role": "user", "content": user_input}]
        )
        st.write(message.content[0].text)

# ----------------------------
# Chat history
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ----------------------------
# Helper: run SerpAPI search
# ----------------------------
def do_serpapi_search(query: str, num: int = 5):
    """Run a Google search via SerpAPI and return a list of {title, link, snippet}."""
    if not SERPAPI_API_KEY:
        return [], "No SERPAPI_API_KEY set. Skipping search."

    try:
        params = {
            "engine": "google",
            "q": query,
            "num": num,
            "api_key": SERPAPI_API_KEY,
        }
        results = GoogleSearch(params).get_dict()
        items = []
        for r in results.get("organic_results", [])[:num]:
            items.append({
                "title": r.get("title", "(no title)"),
                "link": r.get("link", ""),
                "snippet": r.get("snippet", ""),
            })
        return items, None
    except Exception as e:
        return [], f"Search error: {e}"

# ----------------------------
# Chat input
# ----------------------------
prompt = st.chat_input("What would you like to talk about?")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    sources_md = ""
    search_items = []
    search_note = None

    st.write(message.content[0].text)

    system_prompt = (
        "You are a helpful assistant. "
        "If web sources are provided, use them to answer factually and cite them as [1], [2], etc."
    )

    context_from_search = ""
    if search_items:
        lines = []
        for i, it in enumerate(search_items, start=1):
            lines.append(f"[{i}] {it['title']}\nURL: {it['link']}\nSummary: {it['snippet']}\n")
        context_from_search = "Here are relevant web results:\n\n" + "\n".join(lines)

    claude_messages = []
    if context_from_search:
        claude_messages.append({"role": "user", "content": f"{prompt}\n\n{context_from_search}"})
    else:
        claude_messages.append({"role": "user", "content": prompt})

    assistant_text = None
    error_text = None

    if client:
        try:
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                system=system_prompt,
                messages=claude_messages
            )
            assistant_text = ""
            for block in message.content:
                if block.type == "text":
                    assistant_text += block.text
        except Exception as e:
            error_text = str(e)
    else:
        error_text = "No Anthropic API key found."

    with st.chat_message("assistant"):
        if assistant_text:
            if sources_md:
                st.markdown(sources_md)
                st.markdown("---")
            st.markdown(assistant_text)
        else:
            if sources_md:
                st.markdown(sources_md)
                st.info("Showing sources only — Claude response unavailable.")
            else:
                st.error("Could not generate a response. " + (error_text or ""))
            if search_note:
                st.caption(search_note)

    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_text if assistant_text else (sources_md or "(no response)")
    })

