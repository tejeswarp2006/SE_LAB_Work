from game import Mastermind

if __name__ == "__main__":
    difficulty = Mastermind.select_difficulty()
    Mastermind(difficulty=difficulty).run()
