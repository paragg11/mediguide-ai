
import unittest

from src.knowledge_base import load_documents, split_documents


class KnowledgeBaseTests(unittest.TestCase):

    def test_documents_load(self):
        documents = load_documents()

        self.assertGreater(len(documents), 0)
        self.assertIn("text", documents[0])
        self.assertIn("metadata", documents[0])

    def test_chunks_have_metadata(self):
        documents = load_documents()
        chunks = split_documents(documents)

        self.assertGreater(len(chunks), 0)

        for chunk in chunks:
            self.assertTrue(chunk["text"].strip())
            self.assertIn("source", chunk["metadata"])
            self.assertIn("chunk_id", chunk["metadata"])


if __name__ == "__main__":
    unittest.main()
