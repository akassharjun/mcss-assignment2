class Patch:
    """
    Represents a single patch (tile) in the world with a grain resource.
    """

    def __init__(self, x: int, y: int, max_grain: int):
        self.x = x
        self.y = y
        self.max_grain = max_grain
        # Initialize current grain to the maximum (will be modified during diffusion)
        self.current_grain = max_grain

    def grow_grain(self, growth_amount: int = 1) -> None:
        """
        Increase current grain by growth_amount up to the maximum capacity.
        This matches NetLogo's configurable num-grain-grown parameter.
        """
        if self.current_grain < self.max_grain:
            self.current_grain = min(self.max_grain, self.current_grain + growth_amount)


    def harvest(self) -> int:
        """
        Harvest all grain from this patch and reset to zero.
        Returns the amount harvested.
        """
        grain = self.current_grain
        self.current_grain = 0
        return grain

    def get_grain_amount(self) -> int:
        """
        Return the current grain amount on this patch.
        """
        return int(self.current_grain) 
