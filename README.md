# 🧠 Credibility Scoring System – Deliverables 1 & 2  

**Author:** Janet Garcia  
**Course:** Data Science – Applied Machine Learning  
**Instructor:** Yiqiao  
**Date:** October 2025  

---

## 📖 Overview  
This project evaluates the **credibility of online information sources** using Python.  

- **Deliverable 1:** Introduced a *rule-based system* that scored websites and text based on domains (e.g., `.gov`, `.edu`, `.org`) and surface-level cues (authors, citations, tone).  
- **Deliverable 2:** Expanded the project into a *data-driven machine-learning model* using **TF-IDF text features** and **Logistic Regression** to classify sources as credible or non-credible.  

Together, these deliverables show the evolution from a heuristic approach to an interpretable supervised model.

---

## 🎯 Project Goals  
1. Build a Python program that determines how trustworthy a given source or article is.  
2. Compare the effectiveness of rule-based scoring vs. data-driven modeling.  
3. Apply key data-science steps: data creation, feature extraction, training, and evaluation.  
4. Visualize and interpret model results through charts and metrics.  

---

## 🧩 Project Structure  

| File | Description |
|------|--------------|
| `Deliverable1.ipynb` | Rule-based credibility scoring function (heuristics + JSON output). |
| `Deliverable2.ipynb` | TF-IDF + Logistic Regression model with 4 visualizations. |
| `README.md` | Combined documentation for both deliverables. |
| `plots/` | Optional folder to store ROC, PR, and feature-importance charts. |

---

## 🧱 Deliverable 1 – Rule-Based Credibility Function  

**Concept:**  
Implements fixed rules to assess credibility by domain type, accessibility, and content structure.

**Logic Summary:**  
- Checks if source domain ends in `.gov`, `.edu`, `.org`, or `.com`.  
- Rewards credible domains and the presence of “References” or “By” author tags.  
- Penalizes blog-style or opinion sites (e.g., “wordpress,” “medium,” “substack”).  
- Outputs a JSON-style dictionary like:  

```json
{"score": 0.90, "explanation": "Government domain (.gov) – highly credible."}

