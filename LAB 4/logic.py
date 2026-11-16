from collections import Counter


def feedback(code, guess):
    """Return exact and partial matches using each code position at most once."""
    exact = 0
    remaining_code = Counter()

    for code_symbol, guess_symbol in zip(code, guess):
        if code_symbol == guess_symbol:
            exact += 1
        else:
            remaining_code[code_symbol] += 1

    partial = 0
    for guess_symbol in guess:
        if guess_symbol in remaining_code and remaining_code[guess_symbol] > 0:
            partial += 1
            remaining_code[guess_symbol] -= 1

    return exact, partial
