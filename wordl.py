# # ...
# import pathlib
# import random
# from string import ascii_letters
# from rich.console import Console
# from rich.theme import Theme

# console = Console(width=40, theme=Theme({"warning": "red on yellow"}))  

# console = Console(width=40)


# def get_random_word(word_list):
#     """Get a random five-letter word from a list of strings.

#     ## Example:

#     >>> get_random_word(["snake", "worm", "it'll"])
#     'SNAKE'
#     """
#     words = [
#         word.upper()
#         for word in word_list
#         if len(word) == 5 and all(letter in ascii_letters for letter in word)
#     ]
#     return random.choice(words)


# # def show_guess(guess, word):
# #     """Show the user's guess on the terminal and classify all letters.

# #     ## Example:

# #     >>> show_guess("CRANE", "SNAKE")
# #     Correct letters: A, E
# #     Misplaced letters: N
# #     Wrong letters: C, R
# #     """
# #     correct_letters = {
# #         letter for letter, correct in zip(guess,word) if letter == correct 
# #     }
# #     misplaced_letters = set(guess) & set(word) - correct_letters
# #     wrong_letters = set(guess) - set(word)

# #     print("Correct letters:",", ".join(sorted(correct_letters)))
# #     print("Misplaced letters:",", ".join(sorted(misplaced_letters)))
# #     print("Wrong letters:",", ".join(sorted(wrong_letters)))

# def show_guesses(guesses, word):
#     for guess in guesses:
#         styled_guess = []
#         for letter, correct in zip(guess, word):
#             if letter == correct:
#                 style = "bold white on green"
#             elif letter in word:
#                 style = "bold white on yellow"
#             elif letter in ascii_letters:
#                 style = "white on #666666"
#             else:
#                 style = "dim"
#             styled_guess.append(f"[{style}]{letter}[/]")

#         console.print("".join(styled_guess), justify="center")


# def game_over(word):
#     print(f"The word was {word}")


# def main():
#     words_path = pathlib.Path(__file__).parent / "wordlist.txt"
#     word = get_random_word(words_path.read_text(encoding="utf-8").split("\n"))
#     guesses = ["_" * 5] * 6

#     for idx in range(6):
#         refresh_page(headline=f"Guess {idx + 1}")
#         show_guesses(guesses, word)

#         guesses[idx] = input("\nGuess word: ").upper()
#         if guesses[idx] == word:
#             break

#     else:
#         game_over(word)

# if __name__ == "__main__":
#     main()


# def refresh_page(headline):
#     console.clear()
#     console.rule(f"[bold blue]:leafy_green: {headline} :leafy_green:[/]\n")

# # ...


# wyrdl.py

import contextlib
import pathlib
import random
from string import ascii_letters, ascii_uppercase

from rich.console import Console
from rich.theme import Theme

console = Console(width=40, theme=Theme({"warning": "red on yellow"}))

NUM_LETTERS = 5
NUM_GUESSES = 6
WORDS_PATH = pathlib.Path(__file__).parent / "wordlist.txt"

def main():
    # Pre-process
    word = get_random_word(WORDS_PATH.read_text(encoding="utf-8").split("\n"))
    guesses = ["_" * NUM_LETTERS] * NUM_GUESSES

    # Process (main loop)
    with contextlib.suppress(KeyboardInterrupt):
        for idx in range(NUM_GUESSES):
            refresh_page(headline=f"Guess {idx + 1}")
            show_guesses(guesses, word)

            guesses[idx] = guess_word(previous_guesses=guesses[:idx])
            if guesses[idx] == word:
                break

    # Post-process
    game_over(guesses, word, guessed_correctly=guesses[idx] == word)

def refresh_page(headline):
    console.clear()
    console.rule(f"[bold blue]:leafy_green: {headline} :leafy_green:[/]\n")

def get_random_word(word_list):
    # words = [
    #     word.upper()
    #     for word in word_list
    #     if len(word) == 5 and all(letter in ascii_letters for letter in word)
    # ]
    # return random.choice(words)
    if words := [
        word.upper()
        for word in word_list
        if len(word) == NUM_LETTERS and all(letter in ascii_letters for letter in word)
    ]:
        return random.choice(words)
    else:
        console.print("No words of length ${NUM_LETTERS} in the word list", style="warning")
        raise SystemExit()

def show_guesses(guesses, word):
    letter_status = {letter: letter for letter in ascii_uppercase}
    for guess in guesses:
        styled_guess = []
        for letter, correct in zip(guess, word):
            if letter == correct:
                style = "bold white on green"
            elif letter in word:
                style = "bold white on yellow"
            elif letter in ascii_letters:
                style = "white on #666666"
            else:
                style = "dim"
            styled_guess.append(f"[{style}]{letter}[/]")
            if letter != "_":
                letter_status[letter] = f"[{style}]{letter}[/]"

        console.print("".join(styled_guess), justify="center")
    console.print("\n" + "".join(letter_status.values()), justify="center")

def game_over(guesses, word, guessed_correctly):
    refresh_page(headline="Game Over")
    show_guesses(guesses, word)

    if guessed_correctly:
        console.print(f"\n[bold white on green]Correct, the word is {word}[/]")
    else:
        console.print(f"\n[bold white on red]Sorry, the word was {word}[/]")

def guess_word(previous_guesses):
    guess = console.input("\nGuess word: ").upper()

    if guess in previous_guesses:
        console.print(f"You've already guessed {guess}.", style="warning")
        return guess_word(previous_guesses)
    
    if len(guess) != NUM_LETTERS:
        console.print("Your guess must be ${NUM_LETTERS} letters.", style="warning")
        return guess_word(previous_guesses)
    
    if any((invalid := letter) not in ascii_letters for letter in guess):
        console.print(
            f"Invalid letter: '{invalid}'. Please use English letters.",
            style="warning",
        )
        return guess_word(previous_guesses)


    return guess

if __name__ == "__main__":
    main()