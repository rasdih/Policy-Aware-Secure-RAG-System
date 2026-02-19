def decide_action(risk_score):
    if risk_score >= 0.9:
        return "BLOCK"
    else:
        return "ALLOW"
