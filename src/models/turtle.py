from __future__ import annotations
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

    def move(self, world) -> None:
        """
        Move one step in the cardinal direction with the most visible grain (wraparound edges).
        """
        directions = [
            (0, -1),   # North
            (1, 0),    # East
            (0, 1),    # South
            (-1, 0)    # West
        ]
        
        best_direction = None
        best_total_grain = -1

        for dx, dy in directions:
            total_grain = self._grain_ahead(world, dx, dy)
            if total_grain > best_total_grain:
                best_total_grain = total_grain
                best_direction = (dx, dy)

        if best_direction:
            self.x = (self.x + best_direction[0]) % world.width
            self.y = (self.y + best_direction[1]) % world.height


    def _grain_ahead(self, world: "World", dx: int, dy: int) -> int:
        """
        Sum all grain visible in a specific direction up to vision distance.
        This replicates NetLogo's grain-ahead reporter.
        
        Args:
            world: The world object
            dx, dy: Direction vector (-1, 0, 1)
            
        Returns:
            Total grain visible in this direction
        """
        total_grain = 0
    
        for distance in range(1, self.vision + 1):
            look_x = (self.x + dx * distance) % world.width
            look_y = (self.y + dy * distance) % world.height

            patch = world.grid[look_y][look_x]
            total_grain += patch.get_grain_amount()
        
        return total_grain
    

    def eat(self) -> None:
        """
        Consume metabolism amount of grain (separate from harvesting).
        """
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
        return self.wealth <= 0 or self.age >= self.life_expectancy

    def get_wealth_class_name(self) -> str:
        """
        Get the string representation of the turtle's wealth class.
        """
        return self.wealth_class.value
