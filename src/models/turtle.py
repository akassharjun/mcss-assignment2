from __future__ import annotations

from random import choice

from .wealth_classifier import WealthClass


class Turtle:
    """
    Represents a turtle with vision, metabolism, life expectancy, and wealth.
    Each turtle is assigned to a wealth class (poor, middle class, rich) based on their wealth
    relative to the richest turtle in the population.
    """

    def __init__(self,
                 id: int,
                 x: int,
                 y: int,
                 metabolism: int,
                 vision: int,
                 life_expectancy: int,
                 initial_wealth: int = 0,
                 wealth_class: WealthClass = WealthClass.POOR):
        self.id = id
        self.x = x
        self.y = y
        self.metabolism = metabolism
        self.vision = vision
        self.life_expectancy = life_expectancy
        self.age = 0
        self.wealth = initial_wealth
        self.wealth_class = wealth_class

    def move(self, world: "World") -> None:
        """
        Look in the four cardinal directions up to vision distance,
        choose one of the patches with the highest grain, and move there.
        """
        candidates = []

        directions = [
            (1, 0),    # Right
            (-1, 0),   # Left
            (0, -1),   # Up
            (0, 1)     # Down
        ]

        for dx, dy in directions:
            for dist in range(1, self.vision + 1):
                nx = self.x + dx * dist
                ny = self.y + dy * dist

                if 0 <= nx < world.width and 0 <= ny < world.height:
                    patch = world.grid[ny][nx]
                    grain = patch.get_grain_amount()
                    candidates.append(((nx, ny), grain))

        # Include current location as a candidate
        current_grain = world.grid[self.y][self.x].get_grain_amount()
        candidates.append(((self.x, self.y), current_grain))

        max_grain = max(grain for _, grain in candidates)
        best_positions = [pos for pos, grain in candidates if grain == max_grain]

        self.x, self.y = choice(best_positions)

    def harvest_and_eat(self, world: "World") -> None:
        """
        Harvest grain on current patch, add to wealth, then consume metabolism.
        After metabolism, update the wealth class based on new wealth.
        """
        patch = world.grid[self.y][self.x]
        gained = patch.harvest()
        self.wealth += gained
        self.wealth -= self.metabolism

    def increment_age(self) -> None:
        """
        Increment the turtle's age by one tick.
        """
        self.age += 1

    def is_dead(self) -> bool:
        """
        Returns True if the turtle has zero or negative wealth or exceeded life expectancy.
        """
        return self.wealth <= 0 or self.age > self.life_expectancy

    def get_wealth_class_name(self) -> str:
        """
        Get the string representation of the turtle's wealth class.

        Returns:
            str: The wealth class name ('poor', 'middle_class', or 'rich')
        """
        return self.wealth_class.value
