# 🧠 Credibility Scoring System – Deliverables 1 & 2  
**Author:** Janet Garcia  
**Course:** Data Science – Applied Machine Learning  
**Instructor:** Yiqiao  
**Date:** October 2025  

---

## 📖 Overview  
This project investigates how machine learning can evaluate the **credibility of online information sources**.  

- **Deliverable 1** created a *rule-based scoring function* using domain names and keyword rules.  
- **Deliverable 2** advances the work into a **data-driven model** using **TF-IDF** text features and **Logistic Regression**, supported by evaluation metrics, cross-validation, and four analytical plots.  

The two deliverables together represent a transition from handcrafted rules to an interpretable supervised-learning model.

---

## 🎯 Objectives  
1. Demonstrate how text features can indicate source credibility.  
2. Build a labeled dataset and extract features using **TF-IDF**.  
3. Train a **Logistic Regression** classifier to predict credible vs. non-credible text.  
4. Evaluate and visualize performance with four key plots.  
5. Compare results to the original rule-based approach.

---

## 🧱 Deliverable 1 Summary – Rule-Based Credibility Function  

| Aspect | Description |
|--------|--------------|
| **Goal** | Provide a simple credibility score using explicit rules. |
| **Method** | Checked domains (`.gov`, `.edu`, `.org`), looked for authors and citations, penalized blogs/opinion sites. |
| **Output** | JSON object: `{"score": 0.90, "explanation": "Government domain (.gov) – highly credible."}` |
| **Limitation** | Static rules cannot learn new patterns or language changes. |

Deliverable 1 served as the baseline for Deliverable 2’s learning-based model.

---

## 🤖 Deliverable 2 – TF-IDF + Logistic Regression Model  

Deliverable 2 builds a **machine-learning pipeline** that automatically learns credibility cues from data.  
The notebook (`Deliverable2.ipynb`) performs all the following steps:

### 1️⃣ Dataset Creation  
A small synthetic dataset was designed to simulate credible vs. non-credible statements.  
- **Credible examples** use factual, research-oriented language (e.g., “According to NIH data…”).  
- **Non-credible examples** use sensational or unsupported phrasing (e.g., “Secret scientists reveal miracle cure!”).  
Each sample is labeled as `1 = credible` or `0 = not credible`.

### 2️⃣ Feature Extraction – TF-IDF  
- Converts text to numeric vectors using `TfidfVectorizer(max_features=50, stop_words='english')`.  
- Highlights uncommon but meaningful words across the dataset.  
- Produces a feature matrix used for training the model.

### 3️⃣ Model Training – Logistic Regression  
- Trains a logistic regression classifier to map TF-IDF features to credibility labels.  
- The model outputs probabilities between 0 and 1, then thresholds them at 0.5 for binary predictions.  
- Uses 70 % of data for training and 30 % for testing.

### 4️⃣ Evaluation Metrics  
After prediction, the notebook prints:  
