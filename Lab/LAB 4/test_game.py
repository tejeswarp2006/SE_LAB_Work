import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from game import Mastermind


class GameLifecycleTests(unittest.TestCase):
    def test_win_records_history_and_stops_after_the_guess(self):
        game = Mastermind(code=["1", "2", "3", "4"], turns=10)

        with patch("builtins.input", side_effect=["1234"]):
            with redirect_stdout(io.StringIO()) as output:
                game.run()

        self.assertTrue(game.finished)
        self.assertEqual(game.result, "win")
        self.assertEqual(game.turns, 9)
        self.assertEqual(game.history, [("1234", 4, 0)])
        self.assertIn("Cracked the code!", output.getvalue())

    def test_loss_uses_all_guesses_and_preserves_history(self):
        game = Mastermind(code=["1", "2", "3", "4"], turns=2)

        with patch("builtins.input", side_effect=["5555", "6666"]):
            with redirect_stdout(io.StringIO()) as output:
                game.run()

        self.assertTrue(game.finished)
        self.assertEqual(game.result, "loss")
        self.assertEqual(game.turns, 0)
        self.assertEqual(game.history, [("5555", 0, 0), ("6666", 0, 0)])
        self.assertIn("The code was 1234", output.getvalue())

    def test_invalid_guess_does_not_consume_a_turn(self):
        game = Mastermind(code=["1", "2", "3", "4"], turns=2)

        with patch("builtins.input", side_effect=["12", "1234"]):
            with redirect_stdout(io.StringIO()) as output:
                game.run()

        self.assertEqual(game.turns, 1)
        self.assertEqual(game.history, [("1234", 4, 0)])
        self.assertIn("Enter exactly 4 symbols from 1 to 6.", output.getvalue())

    def test_game_ends_without_accepting_more_state_changes(self):
        game = Mastermind(code=["1", "2", "3", "4"], turns=1)

        with patch("builtins.input", side_effect=["1234", "2222"]):
            with redirect_stdout(io.StringIO()) as output:
                game.run()

        self.assertEqual(game.history, [("1234", 4, 0)])
        self.assertIn("Cracked the code!", output.getvalue())
        self.assertNotIn("2222", output.getvalue())

    def test_history_is_presented_readably_and_in_order(self):
        game = Mastermind(code=["1", "2", "3", "4"], turns=3)

        with patch("builtins.input", side_effect=["1111", "1234"]):
            with redirect_stdout(io.StringIO()) as output:
                game.run()

        self.assertIn("Guess 1: 1111 — 1 exact, 0 partial", output.getvalue())
        self.assertIn("Guess 2: 1234 — 4 exact, 0 partial", output.getvalue())

    def test_invalid_guesses_are_rejected_without_consuming_a_turn(self):
        game = Mastermind(code=["1", "2", "3", "4"], turns=2)

        with patch("builtins.input", side_effect=[" 12 ", "1234"]):
            with redirect_stdout(io.StringIO()) as output:
                game.run()

        self.assertEqual(game.turns, 1)
        self.assertEqual(game.history, [("1234", 4, 0)])
        self.assertIn("Enter exactly 4 symbols from 1 to 6.", output.getvalue())

    def test_quit_marks_the_game_as_finished(self):
        game = Mastermind(code=["1", "2", "3", "4"], turns=10)

        with patch("builtins.input", side_effect=["q"]):
            with redirect_stdout(io.StringIO()) as output:
                game.run()

        self.assertTrue(game.finished)
        self.assertEqual(game.result, "quit")
        self.assertEqual(game.history, [])
        self.assertIn("You quit the game.", output.getvalue())


if __name__ == "__main__":
    unittest.main()
