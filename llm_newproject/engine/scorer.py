import re

# Critical attack patterns
CRITICAL_PATTERNS = [
    r"ignore previous instructions",
    r"forget all rules",
    r"you are now admin",
    r"reveal system prompt",
    r"show hidden policy",
    r"bypass security",
    r"disable protection"
]

def calculate_risk(text):
    text = text.lower()
    
    for pattern in CRITICAL_PATTERNS:
        if re.search(pattern, text):
            return 1.0   # Immediately mark as critical
    
    return 0.0
