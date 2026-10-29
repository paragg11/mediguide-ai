
import unittest
from unittest.mock import patch

from src.rag_pipeline import answer_question


class TestRagSafetyIntegration(unittest.TestCase):

    def test_emergency_skips_llm(self):
        with patch(
            "src.rag_pipeline.search_knowledge_base"
        ) as mock_search:
            result = answer_question(
                "I am having difficulty breathing",
                collection=None,
                embedding_model=None,
            )

        self.assertTrue(result["emergency_detected"])
        self.assertEqual(result["sources"], [])
        mock_search.assert_not_called()

    def test_empty_question_is_rejected(self):
        with patch(
            "src.rag_pipeline.search_knowledge_base"
        ) as mock_search:
            result = answer_question(
                "   ",
                collection=None,
                embedding_model=None,
            )

        self.assertIn("Please enter", result["answer"])
        mock_search.assert_not_called()


if __name__ == "__main__":
    unittest.main()
