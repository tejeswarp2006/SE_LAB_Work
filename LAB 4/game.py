import random
from logic import feedback


class Mastermind:
    DIFFICULTIES = {
        "easy": {"length": 4, "symbols": "123456", "turns": 10},
        "medium": {"length": 5, "symbols": "12345678", "turns": 8},
        "hard": {"length": 6, "symbols": "123456789", "turns": 6},
    }

    def __init__(self, code=None, turns=None, difficulty="easy"):
        self.difficulty = difficulty.lower()
        if self.difficulty not in self.DIFFICULTIES:
            raise ValueError("Difficulty must be easy, medium, or hard.")

        config = self.DIFFICULTIES[self.difficulty]
        self.symbols = config["symbols"]
        self.code_length = config["length"]
        self.turns = config["turns"] if turns is None else turns

        if code is None:
            self.code = [random.choice(self.symbols) for _ in range(self.code_length)]
        else:
            self.code = list(code)

        self.history = []
        self.finished = False
        self.result = None

    def _finish(self, result):
        self.finished = True
        self.result = result

    def _process_guess(self, raw):
        if self.finished:
            return

        guess = list(raw)
        exact, partial = feedback(self.code, guess)
        self.history.append((raw, exact, partial))
        self.turns -= 1
        print(f"Guess {len(self.history)}: {raw} — {exact} exact, {partial} partial")

        if exact == len(self.code):
            self._finish("win")
            print("Cracked the code!")
        elif self.turns == 0:
            self._finish("loss")

    @classmethod
    def select_difficulty(cls):
        print("Select difficulty:")
        for number, name in enumerate(cls.DIFFICULTIES, start=1):
            config = cls.DIFFICULTIES[name]
            print(f"  {number}. {name.title()} "
                  f"({config['length']} symbols, {config['turns']} turns)")

        while True:
            choice = input("Difficulty > ").strip().lower()
            try:
                index = int(choice) - 1
            except ValueError:
                print("Choose 1, 2, or 3.")
                continue

            if 0 <= index < len(cls.DIFFICULTIES):
                return list(cls.DIFFICULTIES)[index]

            print("Choose 1, 2, or 3.")

    def run(self):
        print(f"Difficulty: {self.difficulty.title()} — "
              f"enter {self.code_length} symbols from {self.symbols[0]} to {self.symbols[-1]}.")
        while not self.finished and self.turns > 0:
            raw = input(f"{self.turns} turns left > ").strip()
            if raw.lower() == "q":
                self._finish("quit")
                print("You quit the game.")
                return
            if len(raw) != len(self.code) or any(ch not in self.symbols for ch in raw):
                print(f"Enter exactly {self.code_length} symbols from {self.symbols[0]} to {self.symbols[-1]}.")
                continue
            self._process_guess(raw)

        if self.finished and self.result == "loss":
            print("The code was", "".join(self.code))
