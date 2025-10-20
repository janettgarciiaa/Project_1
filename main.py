import os
import re
import numpy as np
import requests
import streamlit as st

# ---------------------------------
# 🌐 Perplexity Chatbot + Balanced Credibility Ratings
# ---------------------------------

st.set_page_config(page_title="Perplexity Chatbot", page_icon="🌐")
st.title("Perplexity Chatbot 🌐")

# Load API key
PPLX_KEY = st.secrets.get("PERPLEXITY_API_KEY", os.getenv("PERPLEXITY_API_KEY", ""))
if not PPLX_KEY:
    st.error("❌ Missing Perplexity API key. Add it in Settings → Secrets or your .env file.")
    st.stop()

# Maintain chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar info
with st.sidebar:
    st.header("Chat Settings")
    st.caption("💡 Model: sonar-pro")
    st.success("✅ Connected to Perplexity API")
    st.caption("⭐ Balanced Credibility Mode Active")

# -----------------------------
# Perplexity API call
# -----------------------------
def ask_perplexity(prompt):
    """Ask Perplexity for a detailed, source-rich answer."""
    headers = {
        "Authorization": f"Bearer {PPLX_KEY}",
        "Content-Type": "application/json",
    }

    # Enforce structured responses with credible sources
    full_prompt = (
        f"{prompt.strip()}\n\n"
        "Provide your answer with **clearly cited links from multiple credibility levels**: "
        "at least one .gov or .edu, one .org, and one .com source. "
        "Format your output in readable bullet points with the full URLs visible."
    )

    payload = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": full_prompt}],
    }

    try:
        res = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=60,
        )
        if res.status_code != 200:
            return f"⚠️ API Error {res.status_code}: {res.text}"
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ API Error: {e}"

# -----------------------------
# Credibility scoring logic
# -----------------------------
def credibility_score(url: str):
    """Balanced scoring between .gov, .edu, .org, .com"""
    domain = url.lower()
    score = 0
    reasons = []

    # --- Domain types ---
    if domain.endswith(".gov"):
        score += 4.9
        reasons.append("Government or official agency (.gov)")
    elif domain.endswith(".edu"):
        score += 4.7
        reasons.append("Academic or university (.edu)")
    elif domain.endswith(".org"):
        score += 4.4
        reasons.append("Nonprofit or research organization (.org)")
    elif domain.endswith(".com"):
        score += 3.8
        reasons.append("Commercial or media site (.com)")
    else:
        score += 3.2
        reasons.append("General web domain")

    # --- Known trusted sites ---
    trusted = [
        "who.int", "cdc.gov", "nasa.gov", "energy.gov", "nih.gov", "un.org",
        "bbc", "reuters", "nytimes", "forbes", "nature.com", "webmd",
        "mayo", "britannica", "nationalgeographic", "apa.org"
    ]
    if any(site in domain for site in trusted):
        score += 0.4
        reasons.append("Trusted, verified source")

    # --- Questionable / user-generated sites ---
    low_trust = ["reddit", "quora", "tiktok", "blogspot", "wordpress", "x.com"]
    if any(site in domain for site in low_trust):
        score -= 0.8
        reasons.append("User-generated or discussion forum")

    # --- SEO-style content ---
    if any(k in url for k in ["best-", "top-", "ranking", "review", "compare"]):
        score -= 0.3
        reasons.append("SEO or marketing-oriented phrasing")

    # --- Minor variability ---
    np.random.seed(abs(hash(domain)) % (10**6))
    score += np.random.uniform(-0.1, 0.1)

    score = round(np.clip(score, 0, 5), 2)
    reason = ", ".join(reasons[:2]) + "."
    return score, reason

# -----------------------------
# Star display function
# -----------------------------
def star_rating(score):
    stars = int(round(score))
    gold = "⭐" * stars
    gray = "✩" * (5 - stars)
    return f"<span style='color:gold'>{gold}</span>{gray}"

# -----------------------------
# Inject inline ratings next to URLs
# -----------------------------
def inject_inline_ratings(reply):
    urls = re.findall(r"https?://[^\s\]\)]+", reply)
    for url in urls:
        score, reason = credibility_score(url)
        stars = star_rating(score)

        if score >= 4.5:
            label = "🟢 High Credibility"
        elif score >= 3.8:
            label = "🟡 Moderate Credibility"
        else:
            label = "🔴 Low Credibility"

        inline_text = (
            f" — {stars} ({score}/5) {label}<br>"
            f"<span style='font-size:13px;color:gray'>{reason}</span>"
        )
        reply = reply.replace(url, f"{url}{inline_text}")
    return reply

# -----------------------------
# Display chat history
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# -----------------------------
# Handle user prompt
# -----------------------------
if prompt := st.chat_input("Ask something..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Retrieving and analyzing sources..."):
            reply = ask_perplexity(prompt)
            reply_with_ratings = inject_inline_ratings(reply)
        st.markdown(reply_with_ratings, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": reply_with_ratings})

