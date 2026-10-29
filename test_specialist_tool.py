
import unittest

from src.specialist_tool import (
    identify_specialty,
    search_specialists,
)


class TestSpecialistTool(unittest.TestCase):

    def test_identifies_dermatology(self):
        self.assertEqual(
            identify_specialty("I need a dermatologist"),
            "Dermatology",
        )

    def test_identifies_heart_specialist(self):
        self.assertEqual(
            identify_specialty("I need a heart specialist"),
            "Cardiology",
        )

    def test_requires_location(self):
        result = search_specialists(
            "Find a dermatologist",
            "",
        )

        self.assertEqual(result["status"], "location_required")

    def test_rejects_unknown_specialty(self):
        result = search_specialists(
            "Find a specialist",
            "Pune",
        )

        self.assertEqual(
            result["status"],
            "unsupported_specialty",
        )

    def test_does_not_invent_provider_results(self):
        result = search_specialists(
            "Find a dermatologist",
            "Pune",
        )

        self.assertEqual(result["results"], [])
        self.assertEqual(
            result["status"],
            "ready_for_provider_lookup",
        )


if __name__ == "__main__":
    unittest.main()
