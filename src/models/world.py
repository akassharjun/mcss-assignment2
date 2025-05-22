from typing import List, Tuple
from src.models.patch import Patch
from src.models.turtle import Turtle


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

    def _init_turtles(self) -> None:
        """
        Spawn initial turtles with random attributes and initial wealth strategy.
        """
