# Malicious URL Detector

A Machine Learning-powered API that detects phishing and malicious URLs in real-time. This project uses a **Random Forest** classifier to analyze lexical features of URLs and provides an explainable risk assessment.

## Features
* **Real-time Detection:** Distinguishes between benign and malicious URLs.
* **Explainable AI:** Returns *why* a URL was flagged (e.g., "Too many subdomains", "IP address usage").
* **Hybrid Architecture:** Uses an O(1) Allowlist for known safe domains (Google, YouTube) to reduce latency.
* **Production Ready:** API built with **FastAPI** and containerized with **Docker**.

## Tech Stack
* **Language:** Python 3.9
* **ML:** Scikit-Learn, Pandas, NumPy
* **API:** FastAPI, Uvicorn
* **DevOps:** Docker

## How to Run

### Option 1: Using Docker
```bash
docker build -t url-detector .
docker run -p 8000:8000 url-detector
```

### Option 2: Manual Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Train the model:
```bash
python train_model.py
```
3. Start the API:
```bash
uvicorn main:app --reload
```

# Usage

Send a POST request to http://localhost:8000/scan:

### Request:
```json
{
  "url": "[http://paypal-update-security.192.168.1.1.com](http://paypal-update-security.192.168.1.1.com)"
}
```

### Response:
```json
{
  "url": "[http://paypal-update-security.192.168.1.1.com](http://paypal-update-security.192.168.1.1.com)",
  "is_malicious": true,
  "confidence_score": 0.98,
  "explanation": "Uses IP Address, Suspicious keywords found"
}
```