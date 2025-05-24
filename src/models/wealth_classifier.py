from enum import Enum
from typing import List


class WealthClass(Enum):
    """
    Enum representing the three wealth classes based on the NetLogo Wealth Distribution model.
    """
    POOR = "poor"
    MIDDLE_CLASS = "middle_class"
    RICH = "rich"


class WealthClassifier:
    """
    Utility class for classifying agents into wealth classes based on their wealth
    relative to the richest agent in the population.

    This follows the NetLogo Wealth Distribution model classification:
    - Poor: wealth <= max_wealth / 3
    - Middle Class: max_wealth / 3 < wealth <= (max_wealth * 2 / 3)
    - Rich: wealth > (max_wealth * 2 / 3)
    """

    @staticmethod
    def classify_agent(agent_wealth: int, max_wealth: int) -> WealthClass:
        """
        Classify a single agent based on their wealth relative to the maximum wealth.

        Args:
            agent_wealth: The wealth of the agent to classify
            max_wealth: The maximum wealth in the population

        Returns:
            WealthClass: The wealth class (POOR, MIDDLE_CLASS, or RICH)
        """
        if max_wealth == 0:
            return WealthClass.POOR

        if agent_wealth <= max_wealth / 3:
            return WealthClass.POOR
        elif agent_wealth <= (max_wealth * 2 / 3):
            return WealthClass.MIDDLE_CLASS
        else:
            return WealthClass.RICH

    @staticmethod
    def get_class_distribution(wealth_classes: List[WealthClass]) -> dict:
        """
        Get the distribution count of each wealth class.

        Args:
            wealth_classes: List of wealth classes

        Returns:
            dict: Dictionary with class names as keys and counts as values
        """
        distribution = {
            WealthClass.POOR.value: 0,
            WealthClass.MIDDLE_CLASS.value: 0,
            WealthClass.RICH.value: 0
        }

        for wealth_class in wealth_classes:
            distribution[wealth_class.value] += 1

        return distribution

    @staticmethod
    def get_class_percentages(wealth_classes: List[WealthClass]) -> dict:
        """
        Get the percentage distribution of each wealth class.

        Args:
            wealth_classes: List of wealth classes

        Returns:
            dict: Dictionary with class names as keys and percentages as values
        """
        if not wealth_classes:
            return {
                WealthClass.POOR.value: 0.0,
                WealthClass.MIDDLE_CLASS.value: 0.0,
                WealthClass.RICH.value: 0.0
            }

        distribution = WealthClassifier.get_class_distribution(wealth_classes)
        total = len(wealth_classes)

        return {
            class_name: (count / total) * 100
            for class_name, count in distribution.items()
        }