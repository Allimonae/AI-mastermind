# Fall 2024 CSCI 350 Artificial Intelligence
# Created by Allison Lee on October 27, 2024
# Group Project - Deadline 2
#
# Baseline 3: Make your first c – 1 guesses monochromatic: "all A’s," "all B’s,"… for all but one of the c colors. That will
# tell you how many pegs of each color are in the answer. (You don't need to actually guess the last color; you can
# compute how many of those there are from the other answers.) Then you generate and test only answers consistent
# with that known color distribution.

from abc import ABC, abstractmethod

class Player(ABC):
    """Player for Mastermind"""

    def __init__(self):
        """Constructor for Player"""

        self.player_name = ""

    @abstractmethod
    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],
    ) -> str:
        """Makes a guess of the secret code for Mastermind

        Args:
            board_length (int): Number of pegs of secret code.
            colors (list[str]]): All possible colors that can be used to generate a code.
            scsa_name (str): Name of SCSA used to generate secret code.
            last_response (tuple[int, int, int]): (First element in tuple is the number of pegs that match exactly with the secret
                                           code for the previous guess, the second element is the number of pegs that are
                                           the right color, but in the wrong location for the previous guess, and the third
                                           element is the number of guesses so far.)

        Raises:
            NotImplementedError: Function must be implemented by subclasses.
        """

        raise NotImplementedError

class Baseline3(Player):
    def __init__(self) -> None:
        self.player_name = "Baseline3"
        self.guess: list[str] = []
        self.color_counts: dict[str, int] = {}  # Track count of each color
        self.final_color = False  # Flag to start consistent guesses
        self.guess_index = 0  # Initialize guess index

    def make_guess(
        self,
        board_length: int,
        colors: list[str],
        scsa_name: str,
        last_response: tuple[int, int, int],
    ) -> str:
        """Makes a guess of the secret code for Mastermind."""
        
        # Monochromatic guesses for each color in c-1
        if len(self.color_counts) < len(colors) - 1:
            curr_color = colors[len(self.color_counts)]
            self.guess = [curr_color] * board_length
            self.color_counts[curr_color] = last_response[0] + last_response[1]  # Store number of times color comes up
            print(f"Guess: {self.guess}, Color Counts: {self.color_counts}")
            return "".join(self.guess)

        # Calculate count of last color and clean color_counts
        if not self.final_color:
            last_color_count = board_length - sum(self.color_counts.values())
            self.color_counts[colors[-1]] = last_color_count
            self.final_color = True

            # Clean color_counts to remove colors with zero counts
            self.color_counts = {color: count for color, count in self.color_counts.items() if count > 0}

        # Generate valid guesses based on known color distribution
        possible_codes = self.generate_possible_codes(board_length, colors)
        if self.guess_index < len(possible_codes):
            self.guess = possible_codes[self.guess_index]
            self.guess_index += 1
            print(f"Generated Guess: {self.guess}")
            return "".join(self.guess)

        # Return last guess if no new guesses are available
        return "".join(self.guess)

    def generate_possible_codes(self, board_length: int, colors: list[str]) -> list[list[str]]:
        """Generate all possible codes based on the known color distribution."""
        from itertools import permutations

        # Create a list of colors based on their counts
        color_pool = []
        for color, count in self.color_counts.items():
            color_pool.extend([color] * count)

        # Generate unique permutations of the color pool that match board_length
        possible_codes = set(permutations(color_pool, board_length))
        return [list(code) for code in possible_codes]

    def generate_next_guess_based_on_counts(self, board_length: int, colors: list[str]) -> str:
        """Generate the next guess based on known color counts."""
        
        # Initialize the guess based on the known color counts
        guess_as_list = []
        for color in colors:
            guess_as_list.extend([color] * self.color_counts.get(color, 0))

        # Ensure the guess length matches the board length
        while len(guess_as_list) < board_length:
            for color in colors:
                if guess_as_list.count(color) < self.color_counts.get(color, 0):
                    guess_as_list.append(color)
                    if len(guess_as_list) == board_length:
                        break

        self.guess = ''.join(guess_as_list)
        return self.guess