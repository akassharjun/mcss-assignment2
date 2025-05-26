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
        NetLogo-compatible movement algorithm.
        Look in 4 cardinal directions, sum grain in each direction up to vision distance,
        then move one step toward the direction with the most total grain.
        """
        # Four cardinal directions: North, East, South, West (0°, 90°, 180°, 270°)
        directions = [
            (0, -1),   # North (up)
            (1, 0),    # East (right) 
            (0, 1),    # South (down)
            (-1, 0)    # West (left)
        ]
        
        best_direction = None
        best_total_grain = -1
        
        # Check each direction
        for dx, dy in directions:
            total_grain = self._grain_ahead(world, dx, dy)
            
            if total_grain > best_total_grain:
                best_total_grain = total_grain
                best_direction = (dx, dy)
        
        # Move one step in the best direction (if valid)
        if best_direction:
            new_x = self.x + best_direction[0]
            new_y = self.y + best_direction[1]
            
            # Check boundaries
            if 0 <= new_x < world.width and 0 <= new_y < world.height:
                self.x = new_x
                self.y = new_y
        
        # If no valid direction or best direction is blocked, stay in place


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
        
        # Look ahead in this direction up to vision distance
        for distance in range(1, self.vision + 1):
            look_x = self.x + dx * distance
            look_y = self.y + dy * distance
            
            # Check if position is within world bounds
            if 0 <= look_x < world.width and 0 <= look_y < world.height:
                patch = world.grid[look_y][look_x]
                total_grain += patch.get_grain_amount()
            else:
                # Can't see outside world boundaries
                break
                
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
