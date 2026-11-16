import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from game import Mastermind


class DifficultyModeTests(unittest.TestCase):
    def test_easy_mode_uses_four_symbols_from_one_to_six(self):
        game = Mastermind(difficulty="easy")

        self.assertEqual(len(game.code), 4)
        self.assertTrue(all(symbol in "123456" for symbol in game.code))
        self.assertEqual(game.turns, 10)

    def test_medium_mode_uses_five_symbols_from_one_to_eight(self):
        game = Mastermind(difficulty="medium")

        self.assertEqual(len(game.code), 5)
        self.assertTrue(all(symbol in "12345678" for symbol in game.code))
        self.assertEqual(game.turns, 8)

    def test_hard_mode_uses_six_symbols_from_one_to_nine(self):
        game = Mastermind(difficulty="hard")

        self.assertEqual(len(game.code), 6)
        self.assertTrue(all(symbol in "123456789" for symbol in game.code))
        self.assertEqual(game.turns, 6)

    def test_run_uses_the_selected_difficulty(self):
        game = Mastermind(code="12345", difficulty="medium", turns=8)

        with patch("builtins.input", side_effect=["2", "12345"]):
            with redirect_stdout(io.StringIO()) as output:
                game.run()

        self.assertTrue(game.finished)
        self.assertEqual(game.result, "win")
        self.assertEqual(game.history, [("12345", 5, 0)])
        self.assertIn("Difficulty", output.getvalue())


if __name__ == "__main__":
    unittest.main()
