import re
from urllib.parse import urlparse
import tldextract

def extract_features(url):
    features = {}
    
    # Parses the URL
    parsed = urlparse(url)
    
    # Gets length features (phishing URLs are often abnormally long)
    features['url_length'] = len(url)
    features['hostname_length'] = len(parsed.netloc)
    features['path_length'] = len(parsed.path)
    
    # Gets count features (high counts of special chars are suspicious)
    features['count_dots'] = url.count('.')
    features['count_hyphens'] = url.count('-')
    features['count_at'] = url.count('@') # Often used to obscure the true domain
    features['count_question'] = url.count('?')
    features['count_digits'] = sum(c.isdigit() for c in url)
    
    # Gets binary features (yes/no)
    # Checks if IP address is used instead of domain (e.g., http://192.168.1.1/login)
    ip_pattern = r"(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
    features['use_of_ip'] = 1 if re.search(ip_pattern, url) else 0
    
    # Checks for suspicious keywords in the path
    suspicious_keywords = ['login', 'secure', 'account', 'update', 'banking']
    features['sus_keyword'] = 1 if any(word in url.lower() for word in suspicious_keywords) else 0
    
    return features