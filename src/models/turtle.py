from src.models.world import World


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
        Look in the four cardinal directions up to vision distance,
        choose one of the patches with the highest grain, and move there.
        """


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