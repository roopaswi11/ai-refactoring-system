import re
import pandas as pd
from urllib.parse import urlparse

def extract_features(url):

    parsed = urlparse(url)
    domain = parsed.netloc
    scheme = parsed.scheme

    features = {
        # 1. Check IP address in domain
        "having_IP_Address": 1 if re.search(r'(\d{1,3}\.){3}\d{1,3}', domain) else -1,

        # 2. URL Length
        "URL_Length": 1 if len(url) >= 54 else -1,

        # 3. Shortening service
        "Shortining_Service": 1 if re.search(r"bit\.ly|tinyurl|goo\.gl|t\.co", domain) else -1,

        # 4. @ symbol
        "having_At_Symbol": 1 if "@" in url else -1,

        # 5. Double slash redirect
        "double_slash_redirecting": 1 if url.rfind("//") > 7 else -1,

        # 6. Prefix-Suffix (dash in domain)
        "Prefix_Suffix": 1 if "-" in domain else -1,

        # 7. Subdomain count
        "having_Sub_Domain": 1 if domain.count(".") > 1 else -1,

        # 8. HTTPS usage
        "HTTPS_token": 1 if scheme == "https" else -1
    }

    df = pd.DataFrame([features])
    return df

