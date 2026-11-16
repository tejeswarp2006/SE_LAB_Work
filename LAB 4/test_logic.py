import unittest

from logic import feedback


class FeedbackTests(unittest.TestCase):
    def test_exact_matches_are_counted_first(self):
        self.assertEqual(feedback("1122", "1122"), (4, 0))

    def test_repeated_code_symbols_are_not_double_counted(self):
        self.assertEqual(feedback("1122", "2211"), (0, 4))

    def test_mixed_exact_and_partial_matches_use_remaining_occurrences(self):
        self.assertEqual(feedback("1222", "2123"), (1, 3))

    def test_no_matches_returns_zero_counts(self):
        self.assertEqual(feedback("1234", "5678"), (0, 0))


if __name__ == "__main__":
    unittest.main()
