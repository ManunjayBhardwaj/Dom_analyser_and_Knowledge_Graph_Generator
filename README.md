# 🧠 Knowledge Graph Generator using LLM + Web Scraping

This project demonstrates how to extract structured knowledge from a live webpage (e.g., Wikipedia) and visualize it as a knowledge graph using:

- 🌐 Web scraping (Selenium + BeautifulSoup)
- 🧠 LLM-based triple extraction (Ollama with LLaMA 3)
- 📊 Knowledge graph visualization (NetworkX + Matplotlib)

---

## 📌 Project Overview

Given a URL (e.g., [Trivago Wikipedia](https://en.wikipedia.org/wiki/Trivago)), this pipeline:

1. Scrapes meaningful structured content (headings, paragraphs)
2. Sends the content to a local LLM (via Ollama) for triple extraction
3. Parses subject-predicate-object (SPO) triples using regex
4. Visualizes the results as a directed knowledge graph

---
## Sample Output 

<img width="1280" alt="Screenshot 2025-06-10 at 1 43 39 PM" src="https://github.com/user-attachments/assets/7f3ce3f0-1c37-4311-947a-46b0a1455574" />

---

## 📦 Requirements

- Python 3.7+
- [Ollama](https://ollama.com) installed locally (use `llama3`, `mistral`, etc.)
- Google Chrome
- ChromeDriver (automatically handled with `webdriver-manager`)

Install Python dependencies:

```bash
pip install selenium beautifulsoup4 requests networkx matplotlib webdriver-manager



