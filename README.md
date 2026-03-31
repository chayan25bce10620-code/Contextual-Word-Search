# Contextual Word Search

A context aware synonym suggester that ranks the alternatives by context.

---

## The Problem

When writing, often one wishes to change a word that doesn't fit the tone of the sentence. Searching a thesaurus for the perfect word is a time consuming process this tool aims to fix.

---

## How It Works

The app takes in both the word and the original sentence as inputs and passes it through a small LLM to generate a ranked list which is then displayed.

---

## Installation

​```bash
git clone https://github.com/chayan25bce10620-code/Contextual-Word-Search 
cd Contextual-Word-Search
pip install -r requirements.txt
​```

---

## Usage

​```bash
streamlit run app.py 
​```

Enter your original setence, Word to be replaced, and click suggest. The ranked list will then be generated below.

**Example output:**
```
Sentence : I am drunk.
Word     : drunk
1. drink — 0.86
2. drunkard  — 0.79
3. booze    — 0.76
```

---

## Project Structure

​```
├── app.py                # Streamlit UI
├── suggester.py          # synonym suggester logic
├── requirements.txt
└── README.md
​```

---

## Course Context

Built as a BYOP project for CSA2001 — Fundamentals in AI and ML, VIT Bhopal (2025–26).