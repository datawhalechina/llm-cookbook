from pathlib import Path
import unittest


GUIDE = Path(__file__).resolve().parents[1] / "Env-Setup.md"


class MiniMaxConfigurationDocumentationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guide = GUIDE.read_text(encoding="utf-8")

    def test_regional_endpoints_are_current(self):
        for endpoint in (
            "https://api.minimax.io/v1",
            "https://api.minimax.io/anthropic",
            "https://api.minimaxi.com/v1",
            "https://api.minimaxi.com/anthropic",
        ):
            self.assertIn(endpoint, self.guide)

    def test_model_metadata_is_current(self):
        expected_rows = (
            "| `MiniMax-M3` | 1,000,000 | text, image, video | adaptive, disabled | $0.60 | $2.40 | $0.12 | Not listed |",
            "| `MiniMax-M2.7` | 204,800 | text | always on | $0.30 | $1.20 | $0.06 | $0.375 |",
        )
        for row in expected_rows:
            self.assertIn(row, self.guide)


if __name__ == "__main__":
    unittest.main()
