from src.models.world import World
from random import choice

class Turtle:
    """
    Represents a turtle with vision, metabolism, life expectancy, and wealth.
    """
    def __init__(self,
                 id: int,
                 x: int,
                 y: int,
                 metabolism: int,
                 vision: int,
                 life_expectancy: int,
                 initial_wealth: int = 0):
        self.id = id
        self.x = x
        self.y = y
        self.metabolism = metabolism
        self.vision = vision
        self.life_expectancy = life_expectancy
        self.age = 0
        self.wealth = initial_wealth

    def move(self, world: World) -> None:
        """
        Look in all directions up to vision distance (Manhattan distance),
        choose one of the patches with the highest grain, and move there.
        """
        candidates = []

        for dx in range(-self.vision, self.vision + 1):
            for dy in range(-self.vision, self.vision + 1):
                # Use Manhattan distance to filter
                if abs(dx) + abs(dy) > self.vision:
                    continue

                nx = self.x + dx
                ny = self.y + dy

                if 0 <= nx < world.width and 0 <= ny < world.height:
                    patch = world.grid[ny][nx]
                    grain = patch.get_grain_amount()
                    candidates.append(((nx, ny), grain))

        # Find patch(es) with highest grain
        max_grain = max(grain for _, grain in candidates)
        best_positions = [pos for pos, grain in candidates if grain == max_grain]

        # Move to one of the best patches (randomly if tied)
        self.x, self.y = choice(best_positions)

    def harvest_and_eat(self, world: World) -> None:
        """
        Harvest grain on current patch, add to wealth, then consume metabolism.
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