
import unittest

from src.safety import check_emergency


class TestEmergencyChecker(unittest.TestCase):

    def test_difficulty_breathing_triggers_warning(self):
        result = check_emergency(
            "I am having difficulty breathing"
        )

        self.assertTrue(result["emergency_detected"])
        self.assertIn(
            "difficulty breathing",
            result["matched_phrases"],
        )

    def test_chest_pain_triggers_warning(self):
        result = check_emergency("I have chest pain")

        self.assertTrue(result["emergency_detected"])

    def test_case_insensitive_matching(self):
        result = check_emergency(
            "I HAVE SEVERE CHEST PAIN"
        )

        self.assertTrue(result["emergency_detected"])

    def test_unmatched_question_returns_no_match(self):
        result = check_emergency(
            "What are common causes of a mild headache?"
        )

        self.assertFalse(result["emergency_detected"])
        self.assertEqual(result["matched_phrases"], [])

    def test_empty_question_returns_no_match(self):
        result = check_emergency("")

        self.assertFalse(result["emergency_detected"])


if __name__ == "__main__":
    unittest.main()
