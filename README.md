# Weather Data Science Project 🌍

### University of Milan  
**Author:** Kasra Ghasemipoo  
**Date:** November 25, 2024  

---

## Project Overview  
This project analyzes global temperature data from 1750 to the present. It includes two major objectives:  
1. **Visualization of Temperature Changes Over Time:**  
   A graphical representation of temperature variations in major cities worldwide, highlighting cities with the largest temperature ranges in different historical periods.  

2. **Optimal Travel Route Suggestion:**  
   For a traveler moving from Beijing to Los Angeles, the program suggests the warmest path step by step, considering the three nearest neighboring cities at each step.  

**Dataset URL:** [Kaggle: Climate Change Earth Surface Temperature Data](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data)  
---

## Features  
### Part A: Temperature Visualization  
- **Objective:** Display the change in temperatures over time on a map and highlight cities with significant temperature ranges.  
- **Files:**  
  - `majorCitiesOnMap.py`: Maps major cities and their temperature data.  
  - `rangeCity.py`: Computes and identifies cities with the largest temperature ranges during specific periods.  
  - `streamlit_app.py`: Provides an interactive visualization using Streamlit.  

### Part B: Optimal Route Suggestion  
- **Objective:** Determine the warmest travel route from Beijing to Los Angeles based on greedy selection.  
- **Files:**  
  - `routing.py`: Implements the route-finding algorithm.  
  - `routingPlot.py`: Generates a graphical representation of the suggested route.  
  - `streamlit_app2.py`: Streamlit app for interactive route visualization.  

---

## Algorithm Details: Greedy Route Selection  
The algorithm identifies the warmest route between cities using the following approach:  

1. **Initialization:** Start from Beijing and move towards Los Angeles.  
2. **Greedy Decision:** At each step, select the warmest city among the three nearest neighbors.  
3. **Termination:** Stop when Los Angeles is reached, recording the full travel route.

### Why Greedy?  
- **Local Optimization:** Maximizes warmth at every step.  
- **Feasibility:** Ensures progression towards the destination.  
- While it may not guarantee the globally warmest or shortest route, it adheres to the problem's constraints effectively.

### Example Execution  
Given a distance matrix and temperature list:  
```text
dist = [
 [0, 10, 20, 30],
 [10, 0, 15, 25],
 [20, 15, 0, 35],
 [30, 25, 35, 0]
]

temp = [20, 25, 30, 35]
start = 0  # Beijing
end = 3    # Los Angeles
