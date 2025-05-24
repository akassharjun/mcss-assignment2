from typing import List
from .patch import Patch
from .turtle import Turtle
from random import shuffle, randint, sample
from math import floor
from typing import List, Tuple

from .wealth_classifier import WealthClass, WealthClassifier


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
            max_grain=4,
            grain_growth_interval: int = 4
    ):
        self.width = width
        self.height = height
        self.num_turtles = num_turtles
        self.percent_best_land = percent_best_land
        self.max_vision = max_vision
        self.max_metabolism = max_metabolism
        self.min_life_expectancy = min_life_expectancy
        self.max_life_expectancy = max_life_expectancy

        self.grain_growth_interval = grain_growth_interval
        self.max_grain = max_grain
        self.uniform_wealth = uniform_wealth

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
        best_land_positions = set(sample(all_positions, num_best_patches))

        # Initialize the grid row by row
        self.grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                max_grain = self.max_grain if (x, y) in best_land_positions else 1
                patch = Patch(x=x, y=y, max_grain=max_grain)
                row.append(patch)
            self.grid.append(row)

    def _init_turtles(self) -> None:
        """
        Spawn initial turtles with random attributes and initial wealth strategy.
        """
        # Generate and shuffle all valid positions
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        shuffle(all_positions)
        selected_positions = all_positions[:self.num_turtles]

        # Create all turtles first
        for i, (x, y) in enumerate(selected_positions):
            turtle = self._init_turtle(i, x, y)
            self.turtles.append(turtle)
        
        # After all turtles are created, classify them based on wealth distribution
        self.update_all_wealth_classes()

    def _init_turtle(self, i, x, y) -> Turtle:
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
            initial_wealth=randint(metabolism, 50)
        )

        return turtle

    def get_max_wealth(self) -> float:
        """
        Calculates and returns the maximum wealth among all turtles.

        Returns:
            float: The maximum wealth found.
                   Returns 0.0 if there are no turtles (assuming wealth is non-negative).
        """
        if not self.turtles:
            return 0.0
        return max(turtle.wealth for turtle in self.turtles)

    def get_min_wealth(self) -> float:
        """
        Calculates and returns the minimum wealth among all turtles.

        Returns:
            float: The minimum wealth found.
                   Returns 0.0 if there are no turtles (this might be ambiguous
                   if 0 is a valid minimum wealth for a non-empty set;
                   consider float('inf') or raising an error if more specific
                   behavior is needed for an empty set and wealth can be anything).
                   Assuming non-negative wealth, 0.0 is a common default.
        """
        if not self.turtles:
            # If wealth could be negative, float('inf') would be a better default,
            # or raising a ValueError. For non-negative wealth, 0.0 is often okay.
            return 0.0
        return min(turtle.wealth for turtle in self.turtles)

    def get_total_wealth(self) -> float:
        """
        Calculates and returns the sum of wealth of all turtles.

        Returns:
            float: The total wealth. Returns 0.0 if there are no turtles.
        """
        # sum() on an empty generator expression or list conveniently returns 0
        return sum(turtle.wealth for turtle in self.turtles)

    def calculate_gini_index(self) -> float:
        """
        Calculates the Gini index, a measure of wealth inequality.
        Requires non-negative wealth values for standard interpretation.
        Returns a float between 0 (perfect equality) and 1 (maximal inequality).
        """
        if not self.turtles or len(self.turtles) < 2:
            # Gini is undefined or 0 for a single individual or no individuals.
            # For a single individual, they have 100% of the wealth, Lorenz is (0,0) -> (1,1).
            # Gini would be 0.
            return 0.0

        # Use non-negative wealths, sorted
        # Standard Gini calculation assumes non-negative values.
        wealths = sorted([max(0, turtle.wealth) for turtle in self.turtles])
        n = len(wealths)
        total_wealth = sum(wealths)

        if total_wealth == 0:
            # If all wealths are 0 (after capping), it's perfect equality.
            return 0.0

        # Using the formula: Gini = ( Σ (2i - n - 1) * y_i ) / ( n * Σ y_i )
        # where y_i are the sorted wealths (1-indexed for 'i' in formula)
        numerator = 0
        for i, wealth_val in enumerate(wealths):
            # i is 0-indexed here, formula uses 1-indexed 'i'
            # So, the rank 'r' (1-indexed) is i + 1
            numerator += (2 * (i + 1) - n - 1) * wealth_val

        denominator = n * total_wealth

        if denominator == 0:  # Should be caught by total_wealth == 0 earlier, but good check
            return 0.0

        gini = numerator / denominator
        return gini

    # Pass the current maximum wealth of the system and the max x value to plot
    def calculate_lorenz_list(self, total_wealth, max_x=100) -> List[Tuple[float, float]]:
        group_size = floor(self.num_turtles / max_x)
        sorted_agents = sorted(self.turtles, key=lambda t: t.wealth)

        acc_wealth = 0
        result = [(0.0, 0.0)]  # Start from origin

        for i in range(1, max_x + 1):
            start_idx = (i - 1) * group_size
            end_idx = i * group_size
            agent_group = sorted_agents[start_idx:end_idx]

            acc_wealth += sum(agent.wealth for agent in agent_group)

            pop_fraction = i / max_x
            wealth_fraction = acc_wealth / total_wealth
            result.append((pop_fraction, wealth_fraction))

        return result

    def update_all_wealth_classes(self) -> None:
        """
        Update wealth classes for all turtles based on current wealth distribution.
        This should be called after any simulation step that changes turtle wealth.
        """
        if not self.turtles:
            return

        # Calculate max wealth
        max_wealth = max(turtle.wealth for turtle in self.turtles)

        # Update each turtle's wealth class
        for turtle in self.turtles:
            turtle.wealth_class = WealthClassifier.classify_agent(turtle.wealth, max_wealth)

    def get_wealth_class_distribution(self) -> dict:
        """
        Get the current distribution of wealth classes.

        Returns:
            dict: Dictionary with class names as keys and counts as values
        """
        wealth_classes = [turtle.wealth_class for turtle in self.turtles]
        return WealthClassifier.get_class_distribution(wealth_classes)

    def get_wealth_class_percentages(self) -> dict:
        """
        Get the current percentage distribution of wealth classes.

        Returns:
            dict: Dictionary with class names as keys and percentages as values
        """
        wealth_classes = [turtle.wealth_class for turtle in self.turtles]
        return WealthClassifier.get_class_percentages(wealth_classes)

    def get_turtles_by_class(self, wealth_class: WealthClass) -> List[Turtle]:
        """
        Get all turtles belonging to a specific wealth class.

        Args:
            wealth_class: The wealth class to filter by

        Returns:
            List[Turtle]: List of turtles in the specified wealth class
        """
        return [turtle for turtle in self.turtles if turtle.wealth_class == wealth_class]

    def tick(self, tick_count: int) -> dict:
        # patch actions
        # check
        if tick_count % self.grain_growth_interval == 0:
            for coord in self.grid:
                for patch in coord:
                    patch.grow_grain()

        # turtle actions
        # move, harvest, eat, check death
        for turtle in list(self.turtles):
            turtle.move(self)
            turtle.harvest_and_eat(self)

            if turtle.is_dead():
                self.turtles.remove(turtle)
                turtle = self._init_turtle(turtle.id, turtle.x, turtle.y)
                self.turtles.append(turtle)

        # Update wealth classes after all turtles have acted
        self.update_all_wealth_classes()

        total_wealth = self.get_total_wealth()
        max_wealth = self.get_max_wealth()
        min_wealth = self.get_min_wealth()

        return {
            'min_wealth': min_wealth,
            'total_wealth': total_wealth,
            'max_wealth': max_wealth,
            'gini_index': self.calculate_gini_index(),
            'lorenz_list': self.calculate_lorenz_list(total_wealth),
        }
