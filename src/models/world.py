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
            width: int = 51,
            height: int = 51,
            num_turtles: int = 250,
            percent_best_land: float = 10.0,
            max_vision: int = 5,
            max_metabolism: int = 15,
            min_life_expectancy: int = 1,
            max_life_expectancy: int = 83,
            uniform_wealth: int = 50,
            max_grain=50,
            grain_growth_interval: int = 1,
            num_grain_grown: int = 4,
            inheritance_flag: bool = False,
            uniform_wealth_flag: bool = False,
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
        self.max_grain = max_grain  # Global maximum grain value
        self.num_grain_grown = num_grain_grown  # How much grain grows each interval

        self.uniform_wealth = uniform_wealth

        self.grid: List[List[Patch]] = []
        self.turtles: List[Turtle] = []
        self.current_tick: int = 0
        self.lorenz_list: List[List[float]] = []

        self.inheritance_flag = inheritance_flag
        self.uniform_wealth_flag = uniform_wealth_flag

        self._init_grid()
        self._init_turtles()

    def _init_grid(self) -> None:
        """
        Initialize the grid of patches with NetLogo-style diffusion setup.
        """
        # Calculate how many patches are considered best land
        total_patches = self.width * self.height
        num_best_patches = int(
            total_patches * (self.percent_best_land / 100.0))

        # Initialize all patches with 0 grain first
        self.grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                patch = Patch(x=x, y=y, max_grain=0)
                row.append(patch)
            self.grid.append(row)

        # Randomly select positions for best land patches
        all_positions = [(x, y) for x in range(self.width)
                         for y in range(self.height)]
        best_land_positions = set(sample(all_positions, num_best_patches))

        # Set best land patches to have maximum grain capacity
        for x, y in best_land_positions:
            self.grid[y][x].max_grain = self.max_grain
            self.grid[y][x].current_grain = self.max_grain

        # Apply NetLogo-style diffusion during setup
        self._apply_setup_diffusion()

        # Set max_grain for each patch based on final grain amounts after diffusion
        for y in range(self.height):
            for x in range(self.width):
                patch = self.grid[y][x]
                patch.max_grain = patch.current_grain  # Maximum capacity = initial amount

    def _apply_setup_diffusion(self) -> None:
        """
        Apply NetLogo-style diffusion during setup to create grain gradients.
        This replicates the NetLogo setup-patches procedure.
        """
        # Phase 1: Repeat 5 times - restore best land and diffuse
        for _ in range(5):
            # Restore best land patches to full grain
            for y in range(self.height):
                for x in range(self.width):
                    patch = self.grid[y][x]
                    if patch.max_grain == self.max_grain:  # This is best land
                        patch.current_grain = self.max_grain

            # Diffuse with factor 0.25
            self._diffuse_grain(0.25)

        # Phase 2: Repeat 10 more times - just diffuse
        for _ in range(10):
            self._diffuse_grain(0.25)

        # Round grain levels to whole numbers and ensure non-negative
        for y in range(self.height):
            for x in range(self.width):
                patch = self.grid[y][x]
                patch.current_grain = max(0, int(patch.current_grain))

    def _diffuse_grain(self, diffusion_rate: float) -> None:
        """
        Implement NetLogo-style diffusion algorithm.
        Each patch shares a portion of its grain with its 4 neighbors.
        """
        # Create a copy of current grain values
        new_grain = [[0.0 for _ in range(self.width)]
                     for _ in range(self.height)]

        # Calculate new grain values based on diffusion
        for y in range(self.height):
            for x in range(self.width):
                current_grain = self.grid[y][x].current_grain

                # Amount this patch keeps
                kept_grain = current_grain * (1.0 - diffusion_rate)

                # Amount to distribute to neighbors
                diffused_grain = current_grain * diffusion_rate

                # Find valid neighbors (4-connected)
                neighbors = []
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        neighbors.append((nx, ny))

                # This patch keeps its portion
                new_grain[y][x] += kept_grain

                # Distribute to neighbors
                if neighbors:
                    grain_per_neighbor = diffused_grain / len(neighbors)
                    for nx, ny in neighbors:
                        new_grain[ny][nx] += grain_per_neighbor

        # Update all patches with new grain values
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x].current_grain = new_grain[y][x]

    def _init_turtles(self) -> None:
        """
        Spawn initial turtles with random attributes and initial wealth strategy.
        """
        # Generate and shuffle all valid positions
        all_positions = [(x, y) for x in range(self.width)
                         for y in range(self.height)]
        shuffle(all_positions)
        selected_positions = all_positions[:self.num_turtles]

        # Create all turtles first
        for i, (x, y) in enumerate(selected_positions):
            turtle = self._init_turtle(i, x, y, 0)
            self.turtles.append(turtle)

        # After all turtles are created, classify them based on wealth distribution
        self.update_all_wealth_classes()

    def _init_turtle(self, i, x, y, inheritance) -> Turtle:
        """
        Initialize turtle with compatible parameters.
        """
        # Generate random attributes
        metabolism = randint(1, self.max_metabolism)
        vision = randint(1, self.max_vision)
        life_expectancy = randint(
            self.min_life_expectancy, self.max_life_expectancy)

        if self.uniform_wealth_flag:
            initial_wealth = self.uniform_wealth
        elif inheritance > 0:
            initial_wealth = inheritance
        else:
            initial_wealth = metabolism + randint(0, 50)

        turtle = Turtle(
            id=i,
            x=x,
            y=y,
            metabolism=metabolism,
            vision=vision,
            life_expectancy=life_expectancy,
            initial_wealth=initial_wealth,
        )

        return turtle

    def get_max_wealth(self) -> float:
        """
        Calculates and returns the maximum wealth among all turtles.
        """
        if not self.turtles:
            return 0.0
        return max(turtle.wealth for turtle in self.turtles)

    def get_min_wealth(self) -> float:
        """
        Calculates and returns the minimum wealth among all turtles.
        """
        if not self.turtles:
            return 0.0
        return min(turtle.wealth for turtle in self.turtles)

    def get_total_wealth(self) -> float:
        """
        Calculates and returns the sum of wealth of all turtles.

        Returns:
            float: The total wealth. Returns 0.0 if there are no turtles.
        """
        return sum(turtle.wealth for turtle in self.turtles)

    def calculate_gini_index(self) -> float:
        """
        Calculates the Gini index, a measure of wealth inequality.
        """
        if not self.turtles or len(self.turtles) < 2:
            return 0.0

        wealths = sorted([max(0, turtle.wealth) for turtle in self.turtles])
        n = len(wealths)
        total_wealth = sum(wealths)

        if total_wealth == 0:
            return 0.0

        # Using the formula: Gini = ( Σ (2i - n - 1) * y_i ) / ( n * Σ y_i )
        # where y_i are the sorted wealths (1-indexed for 'i' in formula)
        numerator = 0
        for i, wealth_val in enumerate(wealths):
            # i is 0-indexed here, formula uses 1-indexed 'i'
            # So, the rank 'r' (1-indexed) is i + 1
            numerator += (2 * (i + 1) - n - 1) * wealth_val

        denominator = n * total_wealth
        if denominator == 0:
            return 0.0

        gini = numerator / denominator
        return gini

    # Pass the current maximum wealth of the system and the max x value to plot
    def calculate_lorenz_list(self, total_wealth, max_x=100) -> List[Tuple[float, float]]:
        if not self.turtles or total_wealth <= 0:
            return [(0.0, 0.0), (100.0, 100.0)]

        # Sort turtles by wealth (poorest to richest)
        sorted_turtles = sorted(self.turtles, key=lambda t: t.wealth)
        n_turtles = len(sorted_turtles)

        result = [(0.0, 0.0)]  # Start from origin

        for i in range(1, max_x + 1):
            # Find turtle index for this population percentage
            turtle_index = int((i * n_turtles) / max_x) - 1
            turtle_index = min(turtle_index, n_turtles - 1)

            # Sum actual individual wealths (no averaging!)
            cumulative_wealth = sum(
                turtle.wealth for turtle in sorted_turtles[:turtle_index + 1])

            pop_percent = (i / max_x) * 100
            wealth_percent = (cumulative_wealth / total_wealth) * 100

            result.append((pop_percent, wealth_percent))

        return result

    def update_all_wealth_classes(self) -> None:
        """
        Update wealth classes for all turtles based on current wealth distribution.
        """
        if not self.turtles:
            return

        max_wealth = max(turtle.wealth for turtle in self.turtles)

        for turtle in self.turtles:
            turtle.wealth_class = WealthClassifier.classify_agent(
                turtle.wealth, max_wealth)

    def get_wealth_class_distribution(self) -> dict:
        """
        Get the current distribution of wealth classes.
        """
        wealth_classes = [turtle.wealth_class for turtle in self.turtles]
        return WealthClassifier.get_class_distribution(wealth_classes)

    def get_wealth_class_percentages(self) -> dict:
        """
        Get the current percentage distribution of wealth classes.
        """
        wealth_classes = [turtle.wealth_class for turtle in self.turtles]
        return WealthClassifier.get_class_percentages(wealth_classes)

    def get_turtles_by_class(self, wealth_class: WealthClass) -> List[Turtle]:
        """
        Get all turtles belonging to a specific wealth class.
        """
        return [turtle for turtle in self.turtles if turtle.wealth_class == wealth_class]

    def harvest_grain(self) -> None:
        """
        Shared harvesting where multiple turtles split grain on same patch.
        """
        # Group turtles by their location
        patch_turtles = {}
        for turtle in self.turtles:
            key = (turtle.x, turtle.y)
            if key not in patch_turtles:
                patch_turtles[key] = []
            patch_turtles[key].append(turtle)

        # For each patch with turtles, split the grain among them
        for (x, y), turtles_on_patch in patch_turtles.items():
            patch = self.grid[y][x]
            total_grain = patch.current_grain

            if total_grain > 0 and turtles_on_patch:
                grain_per_turtle = total_grain / len(turtles_on_patch)

                # Give each turtle their share
                for turtle in turtles_on_patch:
                    turtle.wealth += grain_per_turtle

                # Patch is now empty
                patch.current_grain = 0

    def tick(self, tick_count: int) -> dict:
        """
        Execute one simulation step following NetLogo order of operations.
        """

        # 1. Turtle movement phase
        for turtle in self.turtles:
            turtle.move(self)

        # 2. Harvesting phase (shared harvesting like NetLogo)
        self.harvest_grain()

        # 3. Eating and aging phase
        dead_turtles = []
        for turtle in list(self.turtles):
            turtle.eat()  # Consume metabolism
            turtle.increment_age()

            if turtle.is_dead():
                dead_turtles.append(turtle)

        # 4. Death and rebirth phase
        for turtle in dead_turtles:
            self.turtles.remove(turtle)

            offspring_wealth = turtle.wealth if self.inheritance_flag and turtle.wealth > 0 else 0

            new_turtle = self._init_turtle(
                turtle.id, turtle.x, turtle.y, offspring_wealth)

            self.turtles.append(new_turtle)

        # 5. Patch grain growth
        if tick_count % self.grain_growth_interval == 0:
            for row in self.grid:
                for patch in row:
                    patch.grow_grain(self.num_grain_grown)

        # Update wealth classes after all changes
        self.update_all_wealth_classes()

        # Calculate metrics
        total_wealth = self.get_total_wealth()
        max_wealth = self.get_max_wealth()
        min_wealth = self.get_min_wealth()
        
        wealth_classes = self.get_wealth_class_distribution()
        

        return {
            'min_wealth': min_wealth,
            'total_wealth': total_wealth,
            'max_wealth': max_wealth,
            'gini_index': self.calculate_gini_index(),
            'lorenz_list': self.calculate_lorenz_list(total_wealth),
            'poor' : wealth_classes['poor'],
            'middle_class' : wealth_classes['middle_class'],
            'rich' : wealth_classes['rich']
        }
