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


class Baseline1(Player):
    def __init__(self) -> None:
        self.player_name = "Baseline1"
        self.guess: list[str] = []

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
            last_response (tuple[int, int, int]):
            First element in tuple is the number of pegs that match exactly with the secret
            code for the previous guess, the second element is the number of pegs that are
            the right color, but in the wrong location for the previous guess, and the third
            element is the number of guesses so far.

        Returns:
            str: Returns guess
        """
        # initialization of guess (base c number)
        if not self.guess:
            self.guess = ["A"] * board_length
            return "".join(self.guess)

        # adds 1 to guess (base c number)
        # update digit by digit with carrying
        c = len(colors)
        for digit in range(1, board_length + 1):
            new_value: int = (ord(self.guess[-digit]) + 1) % (c + ord("A"))
            if new_value == 0:  # 0 should map to "A"
                new_value = ord("A")
            self.guess[-digit] = chr(new_value)
            if self.guess[-digit] != "A":  # no more carry
                break

        return "".join(self.guess)
