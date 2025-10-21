# 🌐 Perplexity Chatbot with Balanced Credibility Ratings

This Streamlit web app connects to the **Perplexity AI API** to deliver detailed, source-rich answers with **inline credibility ratings** for each cited link.  
It was developed as part of **Project 1: Deliverable 2** for the Data Science program.

---

## ✨ Features

- 💬 Real-time conversational responses via Perplexity (`sonar-pro` model)
- 🔍 Inline credibility scoring for each cited source
- ⭐ Star-based visualization and trust color indicators  
- 🟢🟡🔴 Highlights high, moderate, and low credibility domains
- 📜 Persistent chat history during active Streamlit sessions

---

## 🧠 Credibility Scoring Function

The core scoring logic is implemented in the function:

```python
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
        reasons.append("General or unknown web domain")

    # --- Known trusted sources ---
    trusted = [
        "who.int", "cdc.gov", "nasa.gov", "nih.gov", "un.org",
        "bbc", "reuters", "nytimes", "forbes", "nature.com", "webmd",
        "mayo", "britannica", "nationalgeographic", "apa.org"
    ]
    if any(site in domain for site in trusted):
        score += 0.4
        reasons.append("Trusted, verified source")

    # --- Low trust or SEO content ---
    low_trust = ["reddit", "quora", "tiktok", "blogspot", "wordpress", "x.com"]
    if any(site in domain for site in low_trust):
        score -= 0.8
        reasons.append("User-generated or discussion forum")

    if any(k in url for k in ["best-", "top-", "ranking", "review", "compare"]):
        score -= 0.3
        reasons.append("SEO or marketing-oriented phrasing")

    return round(max(0, min(score, 5)), 2), ", ".join(reasons[:2]) + "."
