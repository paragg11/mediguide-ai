
"""
MediGuide AI - Basic emergency warning checks.

This is an educational prototype, not a medical triage system.
"""

# Phrases that should trigger an emergency warning.
EMERGENCY_PHRASES = [
    "difficulty breathing",
    "trouble breathing",
    "cannot breathe",
    "can't breathe",
    "severe chest pain",
    "chest pain",
    "loss of consciousness",
    "unconscious",
    "fainted",
    "face drooping",
    "sudden weakness",
    "slurred speech",
    "uncontrolled bleeding",
]


def check_emergency(question: str) -> dict:
    """
    Check a question for configured emergency warning phrases.

    Returns a dictionary containing the result and matched phrases.
    """

    # Normalize the question for case-insensitive matching.
    normalized_question = question.lower().strip()

    # Find all configured phrases present in the question.
    matched_phrases = [
        phrase
        for phrase in EMERGENCY_PHRASES
        if phrase in normalized_question
    ]

    # If any phrase matches, return an emergency warning.
    if matched_phrases:
        return {
            "emergency_detected": True,
            "matched_phrases": matched_phrases,
            "message": (
                "Your message mentions a potential emergency warning "
                "sign. If this is happening now, seek emergency medical "
                "help immediately. In India, call 112 for emergency "
                "assistance. Do not delay care while using this chatbot."
            ),
        }

    # No configured phrase matched. This does NOT rule out an emergency.
    return {
        "emergency_detected": False,
        "matched_phrases": [],
        "message": (
            "No configured emergency phrase was detected. "
            "This does not mean the symptoms are safe or rule out "
            "a medical emergency."
        ),
    }
