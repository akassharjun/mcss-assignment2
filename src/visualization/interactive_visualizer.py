import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from matplotlib.animation import FuncAnimation
from typing import Dict

from src.models.world import World


class InteractiveWealthVisualizer:
    """
    Interactive visualizer with start/stop controls and real-time updates.
    Handles all visualization logic and GUI controls.
    """
    
    def __init__(self, world, figsize=(16, 10)):
        """
        Initialize interactive visualizer.
        
        Args:
            world: World instance to visualize
            figsize: Figure size as (width, height) tuple
        """
        self.world = world
        self.is_running = False
        self.current_tick = 0
        self.animation = None
        
        # Data storage for time series
        self.time_data = []
        self.poor_history = []
        self.middle_history = []  
        self.rich_history = []
        self.gini_history = []
        self.current_lorenz_points = []
        
        # NetLogo color scheme
        self.colors = {
            'poor': '#d62728',        # Red
            'middle_class': '#2ca02c', # Green
            'rich': '#1f77b4'         # Blue
        }
        
        # Setup matplotlib for interactive mode
        try:
            # Try to use a GUI backend
            import matplotlib
            current_backend = matplotlib.get_backend()
            print(f"Current matplotlib backend: {current_backend}")
            
            # Only change backend if we're using a non-GUI backend
            if current_backend in ['Agg', 'svg', 'pdf', 'ps']:
                try:
                    matplotlib.use('TkAgg')
                    print("Switched to TkAgg backend")
                except:
                    try:
                        matplotlib.use('Qt5Agg')
                        print("Switched to Qt5Agg backend")
                    except:
                        print("Using default backend")
        except Exception as e:
            print(f"Backend setup warning: {e}")
        
        plt.rcParams['figure.raise_window'] = True
        
        
        if world.uniform_wealth_flag:
            title = 'Uniform Wealth World Simulation'
        elif world.inheritance_flag:
            title = 'Inheritance World Simulation'
        else:
            title = 'Default World Simulation'
            
        # Create the interface
        self._create_interface(figsize, title)
        
    def _create_interface(self, figsize, title):
        """Create the complete interface with plots and controls."""
        
        # Create figure with subplots
        self.fig, self.axes = plt.subplots(2, 2, figsize=figsize)
        self.fig.canvas.manager.set_window_title(title)
        self.fig.suptitle('Interactive Wealth Distribution Simulation - NetLogo Style', 
                         fontsize=14, fontweight='bold')
        
        # Adjust layout to make room for controls at bottom
        plt.subplots_adjust(left=0.08, bottom=0.15, right=0.95, top=0.92, 
                           wspace=0.25, hspace=0.35)
        
        # Set up window close event handler
        self.fig.canvas.mpl_connect('close_event', self._on_window_close)
        
        # Create control buttons
        self._create_controls()
        
        # Setup initial plots
        self._setup_all_plots()
        
        # Enable interactive mode
        plt.ion()
        
        # Create animation for smooth updates
        try:
            self.animation = FuncAnimation(self.fig, self._animation_update, 
                                         interval=100, blit=False, cache_frame_data=False)
        except Exception as e:
            print(f"Warning: Could not create animation: {e}")
            self.animation = None
        
        # Force the figure to be drawn
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
    def _animation_update(self, frame):
        """Animation update function called by matplotlib timer."""
        if self.is_running:
            try:
                # Get speed from slider
                speed = self.speed_slider.val
                
                # Run simulation steps based on speed
                steps = max(1, int(speed))
                for _ in range(steps):
                    if self.is_running:
                        self.current_tick += 1
                        data = self.world.tick(self.current_tick)
                        
                        # Print progress every 50 ticks
                        if self.current_tick % 50 == 0:
                            class_dist = self.world.get_wealth_class_distribution()
                            gini = data.get('gini_index', 0)
                            print(f"Tick {self.current_tick:4d}: Gini={gini:.3f} | "
                                  f"Classes: P={class_dist.get('poor', 0):3d} "
                                  f"M={class_dist.get('middle_class', 0):3d} "
                                  f"R={class_dist.get('rich', 0):3d}")
                
                # Update plots
                self._update_plots()
                self._update_tick_display()
                
            except Exception as e:
                print(f"Simulation error at tick {self.current_tick}: {e}")
                self.is_running = False
        
        return []  # Return empty list for blit (not used but required)
        
    def _create_controls(self):
        """Create start/stop and other control buttons."""
        
        # Start/Stop button
        start_stop_ax = plt.axes([0.1, 0.02, 0.12, 0.05])
        self.start_stop_button = Button(start_stop_ax, 'START', color='lightgreen')
        self.start_stop_button.on_clicked(self._toggle_simulation)
        
        # Setup button (formerly Reset)
        setup_ax = plt.axes([0.25, 0.02, 0.12, 0.05])
        self.setup_button = Button(setup_ax, 'SETUP', color='lightcoral')
        self.setup_button.on_clicked(self._setup_simulation)
        
        # Speed control slider
        speed_ax = plt.axes([0.45, 0.03, 0.25, 0.03])
        self.speed_slider = Slider(speed_ax, 'Speed', 0.1, 5.0, valinit=1.0)
        self.speed_slider.label.set_size(10)
        
        # Tick counter display
        tick_ax = plt.axes([0.75, 0.02, 0.15, 0.05])
        tick_ax.text(0.5, 0.5, f'Tick: {self.current_tick}', 
                    ha='center', va='center', fontsize=11, fontweight='bold')
        tick_ax.axis('off')
        self.tick_display = tick_ax
        
    def _setup_all_plots(self):
        """Configure the initial setup for all four plots."""
        
        # Top-left: Class Plot (time series)
        ax_class = self.axes[0, 0]
        ax_class.set_title('Class Plot', fontweight='bold', fontsize=11)
        ax_class.set_xlabel('Time')
        ax_class.set_ylabel('Turtles')
        ax_class.grid(True, alpha=0.3)
        ax_class.set_xlim(0, 100)
        ax_class.set_ylim(0, 300)
        
        # Top-right: Class Histogram
        ax_hist = self.axes[0, 1]
        ax_hist.set_title('Class Histogram', fontweight='bold', fontsize=11)
        ax_hist.set_xlabel('Classes')
        ax_hist.set_ylabel('Turtles')
        ax_hist.set_xlim(-0.5, 2.5)
        ax_hist.set_xticks([0, 1, 2])
        ax_hist.set_xticklabels(['low', 'mid', 'up'])
        
        # Bottom-left: Lorenz Curve
        ax_lorenz = self.axes[1, 0]
        ax_lorenz.set_title('Lorenz Curve', fontweight='bold', fontsize=11)
        ax_lorenz.set_xlabel('Pop %')
        ax_lorenz.set_ylabel('Wealth %')
        ax_lorenz.set_xlim(0, 100)
        ax_lorenz.set_ylim(0, 100)
        ax_lorenz.grid(True, alpha=0.3)
        ax_lorenz.plot([0, 100], [0, 100], 'k-', linewidth=1, 
                      label='equal', alpha=0.7)
        
        # Bottom-right: Gini Index vs Time
        ax_gini = self.axes[1, 1]
        ax_gini.set_title('Gini-Index v. Time', fontweight='bold', fontsize=11)
        ax_gini.set_xlabel('Time')
        ax_gini.set_ylabel('Gini')
        ax_gini.set_xlim(0, 100)
        ax_gini.set_ylim(0, 1)
        ax_gini.grid(True, alpha=0.3)
        
    def _toggle_simulation(self, event):
        """Start or stop the simulation."""
        if not self.is_running:
            self._start_simulation()
        else:
            self._stop_simulation()
            
    def _start_simulation(self):
        """Start the simulation."""
        if not self.is_running:
            self.is_running = True
            self.start_stop_button.label.set_text('STOP')
            self.start_stop_button.color = 'lightcoral'
            
            print("✓ Simulation started!")
            
    def _stop_simulation(self):
        """Stop the simulation."""
        if self.is_running:
            self.is_running = False
            self.start_stop_button.label.set_text('START')
            self.start_stop_button.color = 'lightgreen'
            print("⚠ Simulation stopped!")
            
    def _setup_simulation(self, event):
        """Reset the simulation to initial state and clear all graphs."""
        # Stop simulation if running
        if self.is_running:
            self._stop_simulation()
            
        # Reset data
        self.current_tick = 0
        self.time_data.clear()
        self.poor_history.clear()
        self.middle_history.clear()
        self.rich_history.clear()
        self.gini_history.clear()
        self.current_lorenz_points.clear()
        
        # Reset world
        self.world = World()
        
        # Clear and reset all plots immediately
        self._clear_all_plots()
        self._setup_all_plots()
        self._update_tick_display()
        
        # Force immediate redraw
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        
        print("🔄 Simulation setup complete!")
        
    def _clear_all_plots(self):
        """Clear all plot data and reset to initial state."""
        for i in range(2):
            for j in range(2):
                self.axes[i, j].clear()
        
    def _update_plots(self):
        """Update all plots with current simulation data."""
        try:
            # Get current data from world
            class_distribution = self.world.get_wealth_class_distribution()
            gini_coefficient = self.world.calculate_gini_index()
            total_wealth = self.world.get_total_wealth()
            
            # Store historical data
            self.time_data.append(self.current_tick)
            self.poor_history.append(class_distribution.get('poor', 0))
            self.middle_history.append(class_distribution.get('middle_class', 0))
            self.rich_history.append(class_distribution.get('rich', 0))
            self.gini_history.append(gini_coefficient)
            
            # Get Lorenz curve points
            if total_wealth > 0:
                self.current_lorenz_points = self.world.calculate_lorenz_list(total_wealth)
            
            # Update each plot
            self._update_class_plot()
            self._update_class_histogram(class_distribution)
            self._update_lorenz_curve()
            self._update_gini_plot()
            
        except Exception as e:
            print(f"Error updating plots: {e}")
        
    def _update_class_plot(self):
        """Update the time series plot of wealth class populations."""
        ax = self.axes[0, 0]
        ax.clear()
        ax.set_title('Class Plot', fontweight='bold', fontsize=11)
        ax.set_xlabel('Time')
        ax.set_ylabel('Turtles')
        ax.grid(True, alpha=0.3)
        
        if len(self.time_data) > 1:
            ax.plot(self.time_data, self.poor_history, 
                   color=self.colors['poor'], linewidth=2, label='low')
            ax.plot(self.time_data, self.middle_history, 
                   color=self.colors['middle_class'], linewidth=2, label='mid')
            ax.plot(self.time_data, self.rich_history, 
                   color=self.colors['rich'], linewidth=2, label='up')
            
            # Dynamic axis limits
            max_time = max(self.time_data)
            max_population = max(max(self.poor_history), 
                               max(self.middle_history), 
                               max(self.rich_history))
            
            ax.set_xlim(0, max_time * 1.05)
            ax.set_ylim(0, max_population * 1.1)
            ax.legend(loc='upper right', fontsize=9)
            
    def _update_class_histogram(self, class_dist: Dict):
        """Update the bar chart of current wealth class distribution."""
        ax = self.axes[0, 1]
        ax.clear()
        ax.set_title('Class Histogram', fontweight='bold', fontsize=11)
        ax.set_xlabel('Classes')
        ax.set_ylabel('Turtles')
        ax.set_xlim(-0.5, 2.5)
        ax.set_xticks([0, 1, 2])
        ax.set_xticklabels(['low', 'mid', 'up'])
        
        classes = ['poor', 'middle_class', 'rich']
        colors = [self.colors['poor'], self.colors['middle_class'], self.colors['rich']]
        values = [class_dist.get(cls, 0) for cls in classes]
        
        ax.bar([0, 1, 2], values, color=colors, alpha=0.8, width=0.6)
        
        if max(values) > 0:
            ax.set_ylim(0, max(values) * 1.1)
            
    def _update_lorenz_curve(self):
        """Update the Lorenz curve showing wealth inequality."""
        ax = self.axes[1, 0]
        ax.clear()
        ax.set_title('Lorenz Curve', fontweight='bold', fontsize=11)
        ax.set_xlabel('Pop %')
        ax.set_ylabel('Wealth %')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)
        
        # Perfect equality line
        ax.plot([0, 100], [0, 100], 'k-', linewidth=1, 
               label='equal', alpha=0.7)
        
        # Actual Lorenz curve
        if len(self.current_lorenz_points) > 1:
            pop_percentages = [point[0] for point in self.current_lorenz_points]
            wealth_percentages = [point[1] for point in self.current_lorenz_points]
            ax.plot(pop_percentages, wealth_percentages, 
                   color='#d62728', linewidth=3, label='lorenz')
            
        ax.legend(loc='upper left', fontsize=9)
        
    def _update_gini_plot(self):
        """Update the Gini coefficient time series plot."""
        ax = self.axes[1, 1]
        ax.clear()
        ax.set_title('Gini-Index v. Time', fontweight='bold', fontsize=11)
        ax.set_xlabel('Time')
        ax.set_ylabel('Gini')
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        
        if len(self.time_data) > 1:
            ax.plot(self.time_data, self.gini_history, 
                   color='#1f77b4', linewidth=2)
            
            max_time = max(self.time_data)
            ax.set_xlim(0, max_time * 1.05)
            
    def _update_tick_display(self):
        """Update the tick counter display."""
        self.tick_display.clear()
        self.tick_display.text(0.5, 0.5, f'Tick: {self.current_tick}', 
                              ha='center', va='center', fontsize=11, fontweight='bold')
        self.tick_display.axis('off')
        
    def save_plots(self, filename: str = None):
        """Save current plots to file."""
        if filename is None:
            filename = f'wealth_distribution_tick_{self.current_tick}.png'
        
        try:
            self.fig.savefig(filename, dpi=300, bbox_inches='tight', 
                            facecolor='white', edgecolor='none')
            print(f"Plots saved to {filename}")
        except Exception as e:
            print(f"Error saving plots: {e}")
        
    def show(self):
        """Display the interactive interface and keep it open."""
        try:
            # Make sure the window is visible and stays open
            plt.interactive(True)
            plt.show(block=True)
        except KeyboardInterrupt:
            print("\nInterface closed by user")
        except Exception as e:
            print(f"Interface closed: {e}")
        finally:
            if self.is_running:
                self.is_running = False
            plt.ioff()
        
    def close(self):
        """Clean shutdown of the visualizer."""
        if self.is_running:
            self._stop_simulation()
        if self.animation and hasattr(self.animation, 'event_source'):
            try:
                self.animation.event_source.stop()
            except:
                pass  # Ignore errors during shutdown
        try:
            plt.close(self.fig)
        except:
            pass  # Ignore errors during shutdown
            
    def _on_window_close(self, event):
        """Handle window close event for smooth shutdown."""
        print("\nClosing simulation window...")
        if self.is_running:
            self._stop_simulation()
        if self.animation and hasattr(self.animation, 'event_source'):
            try:
                self.animation.event_source.stop()
            except:
                pass  # Ignore errors during shutdown
        plt.ioff()
        print("Simulation window closed successfully.")


# Simple function to create and run the interactive visualizer
def create_interactive_simulation(world):
    """
    Create and display interactive simulation interface.
    
    Args:
        world: World instance to simulate
        
    Returns:
        InteractiveWealthVisualizer instance
    """
    visualizer = InteractiveWealthVisualizer(world)
    return visualizer


if __name__ == "__main__":
    print("Interactive Wealth Distribution Visualizer")
    print("This module provides interactive visualization with start/stop controls.")
    print("Import and use with your World class:")
    print()
    print("Example:")
    print("  from interactive_visualizer import create_interactive_simulation")
    print("  from models.world import World")
    print("  world = World()")
    print("  visualizer = create_interactive_simulation(world)")
    print("  visualizer.show()")