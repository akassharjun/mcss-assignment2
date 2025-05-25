from models.world import World
from visualization.interactive_visualizer import create_interactive_simulation
import sys


def print_welcome():
    """Print welcome message."""
    print("=" * 60)
    print("INTERACTIVE WEALTH DISTRIBUTION SIMULATION")
    print("NetLogo-Style Interface with Start/Stop Controls")
    print("=" * 60)
    print()
    print("Features:")
    print("• Real-time visualization with four plots")
    print("• START/STOP button control")
    print("• Speed control slider")
    print("• RESET button to restart simulation")
    print("• Interactive NetLogo-style interface")
    print()


def main():
    """Main function - creates interactive simulation interface."""
    
    print_welcome()
    
    # Initialize world
    print("Initializing simulation world...")
    world = World()
    
    # Display world parameters
    print("World Parameters:")
    print(f"• Size: {world.width} × {world.height}")
    print(f"• Population: {world.num_turtles} turtles")
    print(f"• Best Land: {world.percent_best_land * 100:.1f}%")
    print(f"• Vision: 1-{world.max_vision}")
    print(f"• Metabolism: 1-{world.max_metabolism}")
    print(f"• Life Expectancy: {world.min_life_expectancy}-{world.max_life_expectancy}")
    print()
    
    # Create interactive interface
    print("Creating interactive interface...")
    print("The simulation window will open with START/STOP controls.")
    print("Click START to begin the simulation!")
    print()
    
    try:
        # Create and show interactive visualizer
        visualizer = create_interactive_simulation(world)
     
        print("Interface created successfully!")
        print("Controls:")
        print("• START/STOP: Begin/pause simulation")
        print("• SETUP: Restart from beginning") 
        print("• Speed slider: Control simulation speed")
        print("• Close window to exit")
        print()
        print("Opening simulation window... (this may take a moment)")
        
        # Show the interface (this will block until window is closed)
        visualizer.show()
        
    except Exception as e:
        print(f"Error creating interface: {e}")
        print("Try running with --help flag for usage information")
        import traceback
        traceback.print_exc()
    
    finally:
        print("Simulation ended.")


if __name__ == "__main__":
        main()