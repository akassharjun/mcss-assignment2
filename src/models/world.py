from typing import List, Tuple
from src.models.patch import Patch
from src.models.turtle import Turtle
from random import shuffle, randint

class World:
    """
    Simulation environment containing patches and turtles.
    Collects metrics (Lorenz curve, Gini index, class distributions).
    """

    def __init__(
            self,
            width: int = 50,
            height: int = 50,
            num_turtles: int = 100,
            percent_best_land: float = 0.2,
            max_vision: int = 6,
            max_metabolism: int = 3,
            min_life_expectancy: int = 60,
            max_life_expectancy: int = 100,
            uniform_wealth: int = 50,
    ):
        self.width = width
        self.height = height
        self.num_turtles = num_turtles
        self.percent_best_land = percent_best_land
        self.max_vision = max_vision
        self.max_metabolism = max_metabolism
        self.min_life_expectancy = min_life_expectancy
        self.max_life_expectancy = max_life_expectancy

        self.grid: List[List[Patch]] = []
        self.turtles: List[Turtle] = []
        self.current_tick: int = 0
        self.lorenz_list: List[List[float]] = []
        self.gini_list: List[float] = []

        self._init_grid()
        self._init_turtles()

    def _init_grid(self) -> None:
        """
        Initialize the grid of patches, assigning high-resource (best land)
        to a percentage of patches.
        """
        # Calculate how many patches are considered best land
        total_patches = self.width * self.height
        num_best_patches = int(total_patches * self.percent_best_land)

        # Randomly select unique positions for best land
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        best_land_positions = set(random.sample(all_positions, num_best_patches))

        # Initialize the grid row by row
        self.grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                max_grain = 4 if (x, y) in best_land_positions else 1
                patch = Patch(x=x, y=y, max_grain=max_grain)
                row.append(patch)
            self.grid.append(row)    

    def _init_turtles(self) -> None:
        
        # Generate and shuffle all valid positions
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        shuffle(all_positions)
        selected_positions = all_positions[:self.num_turtles]

        for i, (x, y) in enumerate(selected_positions):
            metabolism = randint(1, self.max_metabolism)
            vision = randint(1, self.max_vision)
            life_expectancy = randint(self.min_life_expectancy, self.max_life_expectancy)

        turtle = Turtle(
            id=i,
            x=x,
            y=y,
            metabolism=metabolism,
            vision=vision,
            life_expectancy=life_expectancy,
            initial_wealth=self.uniform_wealth
        )
        self.turtles.append(turtle)    
        
        """
        Spawn initial turtles with random attributes and initial wealth strategy.
        """
