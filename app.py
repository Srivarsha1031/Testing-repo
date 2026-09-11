"""
Number guessing game.
The computer picks a secret number and you try to guess it.
Tracks attempts, gives hints, and lets you play again.
"""

import random


def choose_difficulty():
    print("Pick a difficulty:")
    print("  1. Easy   (1-10, 5 guesses)")
    print("  2. Medium (1-50, 7 guesses)")
    print("  3. Hard   (1-100, 8 guesses)")

    while True:
        choice = input("Your choice: ").strip()
        if choice == "1":
            return 10, 5
        if choice == "2":
            return 50, 7
        if choice == "3":
            return 100, 8
        print("Please enter 1, 2 or 3.")


def play_round():
    max_number, max_guesses = choose_difficulty()
    secret = random.randint(1, max_number)
    guesses_left = max_guesses
    previous_guesses = []

    print(f"\nI'm thinking of a number between 1 and {max_number}.")
    print(f"You have {max_guesses} guesses. Good luck!\n")

    while guesses_left > 0:
        text = input(f"Guess ({guesses_left} left): ").strip()

        if not text.isdigit():
            print("Please type a whole number.")
            continue

        guess = int(text)

        if guess < 1 or guess > max_number:
            print(f"Stay between 1 and {max_number}.")
            continue

        if guess in previous_guesses:
            print("You already tried that one!")
            continue

        previous_guesses.append(guess)
        guesses_left -= 1

        if guess == secret:
            used = max_guesses - guesses_left
            print(f"\nCorrect! You got it in {used} guess{'es' if used != 1 else ''}.")
            return True

        difference = abs(secret - guess)
        if difference <= 3:
            hint = "Very close!"
        elif difference <= 10:
            hint = "Getting warm."
        else:
            hint = "Way off."

        direction = "higher" if guess < secret else "lower"
        print(f"{hint} Try {direction}.")

    print(f"\nOut of guesses! The number was {secret}.")
    return False


def main():
    print("===== NUMBER GUESSING GAME =====\n")
    wins = 0
    rounds = 0

    while True:
        rounds += 1
        if play_round():
            wins += 1

        print(f"\nScore: {wins} win(s) out of {rounds} round(s).")
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break
        print()


if __name__ == "__main__":
    main()
