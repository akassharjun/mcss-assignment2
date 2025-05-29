# Wealth Distribution Model - Python Replication

A Python implementation and extension of the NetLogo Wealth Distribution model for SWEN90004: Modelling Complex Software Systems at The University of Melbourne.

## 📋 Project Overview

This project replicates the classic NetLogo Wealth Distribution model in Python and extends it to investigate how different inheritance and wealth initialization mechanisms affect economic inequality patterns. The model simulates agents foraging for resources in a spatial environment, demonstrating how wealth inequality emerges naturally from simple competitive behaviors.

### Key Features

- ✅ **Accurate NetLogo Replication**: Faithful reproduction of the original model mechanics
- ✅ **Standard Library Only**: Core simulation uses only Python built-in modules (assignment compliant)
- ✅ **Optional Visualization**: Interactive GUI available for verification and demonstration
- ✅ **Statistical Analysis**: Gini coefficient, Lorenz curves, and wealth class distributions
- ✅ **Model Extensions**: Investigation of inheritance and uniform wealth scenarios
- ✅ **CSV Data Export**: Results exportable for external analysis

## 🚀 Quick Start

### Prerequisites

- **Core Simulation**: Python 3.13+ only (no external dependencies)
- **Optional GUI**: matplotlib (for interactive visualization)

### Installation

```bash
# Clone or download the project
git clone [repo-url]
cd wealth-distribution-model

# Core simulation - no additional setup needed!
# Optional: Install matplotlib for GUI visualization
pip install matplotlib
```

### Running the Simulation

#### Command Line Mode (Assignment Compliant)

```bash
# Run default world - outputs CSV data
python src/simulation_runner.py --scenario default --ticks 500 --runs 10

# Run with inheritance enabled
python src/simulation_runner.py --scenario inheritance --ticks 500 --runs 10

# Run with uniform wealth initialization
python src/simulation_runner.py --scenario uniform --ticks 500 --runs 10
```

#### Interactive GUI Mode (Optional - Requires matplotlib)

```bash
# Run default world with visualization
python src/simulation_gui_runner.py --scenario default

# Run inheritance world with GUI
python src/simulation_gui_runner.py --scenario inheritance

# Run uniform wealth world with GUI
python src/simulation_gui_runner.py --scenario uniform
```

## 📊 Output and Analysis

### Command Line Output

The core simulation produces:

- **Console Progress**: Real-time tick progress and key metrics
- **CSV Results**: Detailed data exported to `results/` directory
- **Summary Statistics**: Final Gini coefficients and wealth distributions

Example output:

```
Running default scenario:
  • 10 simulation runs
  • 500 ticks per run
  • Output: results/default_results.csv

Simulation Complete: All runs finished
Results exported to: results/default_results.csv
```

### Optional GUI Features

When matplotlib is available, the interactive visualization provides:

- **Real-time Plots**: Class distributions, Lorenz curves, Gini evolution
- **Control Interface**: START/STOP, SETUP, speed control
- **NetLogo-style Display**: Familiar interface for model verification

## 📊 Model Scenarios

### 1. Default World (`--scenario default`)

Replicates the original NetLogo model:

- Random initial wealth (metabolism + 0-50 grain)
- No inheritance (offspring get random wealth from population range)
- Demonstrates emergence of wealth inequality

### 2. Inheritance World (`--scenario inheritance`)

Modified inheritance mechanism:

- Children inherit their parent's full wealth
- Investigates impact of true wealth inheritance
- Compare inequality patterns with default model

### 3. Uniform Wealth World (`--scenario uniform`)

Equal starting conditions:

- All agents start with same wealth (50 grain)
- Tests whether uniform initialization prevents inequality
- Demonstrates role of individual differences vs. initial conditions

## 🏗️ Project Structure

```
src/
├── models/
│   ├── patch.py           # Grid cell with grain resources
│   ├── turtle.py          # Agent with foraging behavior
│   ├── world.py           # Main simulation engine
│   └── wealth_classifier.py # Wealth class categorization
├── utility/
    ├── averager.py        # Util Averager
│   └── runner.py          # Batch simulation utilities
├── visualization/         # GUI visualization components
├── results/               # CSV output directory
├── simulation_runner.py   # Command-line simulation (CORE)
└── simulation_gui_runner.py # Interactive GUI runner
```

## 🔧 Core Model Parameters

| Parameter       | Default Value | Description                         |
| --------------- | ------------- | ----------------------------------- |
| Grid Size       | 51 × 51       | World dimensions                    |
| Population      | 250           | Number of agents                    |
| Best Land       | 10%           | Percentage of high-resource patches |
| Max Grain       | 50            | Maximum grain per patch             |
| Vision Range    | 1-5           | Agent sight distance (random)       |
| Metabolism      | 1-15          | Resource consumption rate (random)  |
| Life Expectancy | 1-83          | Maximum agent lifespan (random)     |
| Grain Growth    | 4 units/tick  | Resource regeneration rate          |

## 📈 Data Collection

### Standard Library Implementation

All core functionality uses only Python built-in modules:

- **CSV Module**: For data export and analysis
- **Random Module**: For stochastic processes
- **Math Module**: For statistical calculations
- **Collections**: For data aggregation

### Exported Data Format

CSV files contain per-tick data:

```csv
tick,gini_index,poor_count,middle_count,rich_count,total_wealth,min_wealth,max_wealth
1,0.123,200,45,5,12500,0,250
2,0.134,198,47,5,12600,0,255
...
```

## 🧪 Experimental Validation

### Command Line Batch Processing

```bash
# Run comprehensive comparison experiment
python src/simulation_runner.py --scenario default --ticks 1000 --runs 100
python src/simulation_runner.py --scenario inheritance --ticks 1000 --runs 100
python src/simulation_runner.py --scenario uniform --ticks 1000 --runs 100

# This executes:
# - Multiple runs of each scenario (default, inheritance, uniform)
# - Configurable ticks per run
# - Results exported to results/ directory
```

### Quick Analysis of results

Run the `utility/averager.py` script to calculate and display the averaged values from your simulation results. This script requires `pandas` to be installed, and you will need to provide the path to your CSV results file (e.g., `/path/to/your/results.csv`).

## 🎯 Key Findings

1. **Successful Replication**: Python model reproduces NetLogo inequality emergence
2. **Inheritance Impact**: True inheritance increases inequality (higher Gini coefficients)
3. **Uniform Wealth Limits**: Equal starting wealth alone cannot prevent inequality
4. **Individual Differences Matter**: Agent characteristics (metabolism, vision) drive long-term outcomes

## 🛠️ Technical Implementation

### NetLogo Compatibility Features

- **Patch diffusion algorithm**: Replicates NetLogo's grain spreading mechanism
- **Agent movement**: Four-directional optimal foraging behavior
- **Shared harvesting**: Multiple agents split resources on same patch
- **Death/birth cycle**: Population replacement with NetLogo inheritance rules

### Code Quality Standards

- ✅ **No external dependencies** for core functionality (assignment requirement)
- ✅ **Comprehensive documentation** for all classes and methods
- ✅ **Modular design** for easy extension and testing
- ✅ **Python 3.13 compatibility** verified
- ✅ **Clear variable names** and consistent formatting

## 🚨 Troubleshooting

### Assignment Submission Mode (Standard Library Only)

**Core simulation not running**

```bash
# Check Python version
python --version  # Should be 3.13+

# Test basic functionality
python -c "import csv, random, math; print('Standard library OK')"

# Run minimal test
python src/models/world.py  # Should run basic test
```

**CSV files not generated**

- Check `results/` directory exists
- Ensure write permissions in project folder
- Try running with full path: `python /full/path/to/simulation_runner.py`

### Optional GUI Mode Issues

**"No module named 'matplotlib'"**

```bash
# Install matplotlib for GUI features
pip install matplotlib

# Or skip GUI and use command line mode
python src/simulation_runner.py --scenario default --ticks 100 --runs 5
```

**GUI window doesn't appear**

- Try different matplotlib backends
- Check your Python GUI libraries installation
- Use command line mode instead: fully functional without GUI

**Memory issues with long runs**

- Reduce ticks: `--ticks 200` instead of 500
- Reduce runs: `--runs 5` instead of 10
- Use command line mode for batch processing

### Performance Tips

- **Command Line Mode**: Much faster for batch experiments
- **GUI Mode**: Use for verification and demonstration only
- **Long Experiments**: Always use command line with CSV export
- **Testing**: Start with `--ticks 50 --runs 5` for quick validation

## 📋 Assignment Compliance

This project structure ensures full SWEN90004 requirements compliance:

## 👥 Authors

**Group Members:**

- Akassharjun Shanmugarajah (1641203)
- David Relacion (1571930)
- Kamal Kumar (1534816)

**SWEN90004 - Modelling Complex Software Systems**
**The University of Melbourne**

## 📄 License

This project is submitted as coursework for SWEN90004. Code is provided for educational purposes and assignment evaluation.

## 🙏 Acknowledgments

- Based on the NetLogo Wealth Distribution model by Uri Wilensky
- NetLogo Models Library: https://ccl.northwestern.edu/netlogo/models/
- SWEN90004 teaching team for project guidance
- Matplotlib for optional visualization capabilities

---

**Note**: This README provides comprehensive guidance for running and understanding the project. For detailed experimental results and analysis, please refer to the accompanying project report.
