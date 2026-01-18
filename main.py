from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import tldextract
from features import extract_features

# Loads the trained model
model = joblib.load('malicious_url_model.pkl')

app = FastAPI()

# List of trusted domains
ALLOWLIST = {
    "google", "youtube", "facebook", "amazon", "wikipedia", 
    "linkedin", "twitter", "instagram", "github", "microsoft"
}

class URLRequest(BaseModel):
    url: str

@app.post("/scan")
def scan_url(item: URLRequest):
    # Extracts the domain to check against allow list
    extracted = tldextract.extract(item.url)
    domain_name = extracted.domain.lower()

    if domain_name in ALLOWLIST:
        return {
            "url": item.url,
            "is_malicious": False,
            "confidence_score": 0.0,
            "explanation": f"Trusted Domain (Allowlisted: {domain_name})"
        }

    # Extracts features from the input URL
    features_dict = extract_features(item.url)
    
    # Converts features to DataFrame (model expects a 2D array)
    features_df = pd.DataFrame([features_dict.values()])
    
    # Predicts safety/maliciousness of URL
    prediction = model.predict(features_df)[0]
    probability = model.predict_proba(features_df)[0][1] # Probability of being malicious
    
    # Explainability - if it's malicious, tell us which features were high
    reason = "Safe"
    if prediction == 1:
        reasons = []
        if features_dict['use_of_ip'] == 1: reasons.append("Uses IP Address")
        if features_dict['url_length'] > 75: reasons.append("URL extremely long")
        if features_dict['count_dots'] > 3: reasons.append("Too many subdomains")
        if features_dict['sus_keyword'] == 1: reasons.append("Suspicious keywords found")
        reason = ", ".join(reasons) if reasons else "Heuristic Pattern Match"

    return {
        "url": item.url,
        "is_malicious": bool(prediction),
        "confidence_score": float(probability),
        "explanation": reason
    }