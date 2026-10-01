def detect_escalation(message):
    text = message.lower()

    escalation_phrases = [
        "human",
        "recruiter",
        "talk to someone",
        "speak to someone",
        "human agent",
        "real person",
        "contact recruiter",
        "recruitment team"
    ]

    return any(phrase in text for phrase in escalation_phrases)
