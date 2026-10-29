
"""MediGuide AI: basic specialist directory search tool."""

SPECIALTIES = {
    "dermatologist": "Dermatology",
    "skin specialist": "Dermatology",
    "cardiologist": "Cardiology",
    "heart specialist": "Cardiology",
    "neurologist": "Neurology",
    "orthopedic": "Orthopedics",
    "orthopaedic": "Orthopedics",
    "pediatrician": "Pediatrics",
    "paediatrician": "Pediatrics",
    "psychiatrist": "Psychiatry",
    "dentist": "Dentistry",
}


def identify_specialty(question: str) -> str | None:
    """Identify a supported specialty mentioned in a question."""

    normalized_question = question.lower().strip()

    for phrase, specialty in SPECIALTIES.items():
        if phrase in normalized_question:
            return specialty

    return None


def search_specialists(question: str, location: str) -> dict:
    """
    Validate a specialist-search request.

    This first version does not contact a provider directory.
    It prepares a validated request for a future real API.
    """

    location = location.strip()
    specialty = identify_specialty(question)

    if not question.strip():
        return {
            "status": "invalid_request",
            "message": "Please enter a specialist type or question.",
            "results": [],
        }

    if not specialty:
        return {
            "status": "unsupported_specialty",
            "message": (
                "I couldn't identify a supported specialty. "
                "Please specify the type of specialist you need."
            ),
            "results": [],
        }

    if not location:
        return {
            "status": "location_required",
            "message": "Please provide a city or area to search.",
            "results": [],
        }

    return {
        "status": "ready_for_provider_lookup",
        "specialty": specialty,
        "location": location,
        "message": (
            "The request is validated, but no provider directory "
            "is connected yet. No doctors have been looked up."
        ),
        "results": [],
    }


if __name__ == "__main__":
    example = search_specialists(
        "Find a dermatologist",
        "Pune",
    )
    print(example)
