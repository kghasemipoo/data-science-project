import streamlit as st
import pandas as pd
import math
import geopandas as gpd
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
from geodatasets import get_path

# Title and Sidebar Configuration
st.title("Warmest Route Finder")
st.sidebar.title("Configuration")

# Sidebar Inputs
csv_file_path = "dataset/GlobalLandTemperaturesByCity.csv"
specific_date = st.sidebar.text_input("Enter a specific date (YYYY-MM-DD):", value="1849-04-01")
c1 = st.sidebar.text_input("Enter the start city:", value="London")
c2 = st.sidebar.text_input("Enter the destination city:", value="Los Angeles")

# Button to trigger the execution
if st.sidebar.button("Find Warmest Route"):

    # Load and preprocess data
    try:
        data = pd.read_csv(csv_file_path)
        data['dt'] = pd.to_datetime(data['dt'])
        data = data.dropna()


        # Convert coordinates
        def convert_coords(coord):
            """Convert coordinate strings to numeric."""
            if 'N' in coord or 'E' in coord:
                return float(coord[:-1])
            elif 'S' in coord or 'W' in coord:
                return -float(coord[:-1])
            return float(coord)


        data['Latitude'] = data['Latitude'].apply(convert_coords)
        data['Longitude'] = data['Longitude'].apply(convert_coords)

        # Filter data for the specific date
        data_in_specific_date = data[data['dt'] == specific_date].reset_index(drop=True)

        if data_in_specific_date.empty:
            st.error(f"No data available for the date {specific_date}. Please try another date.")
        else:
            # Find city indices
            try:
                c1_index = data_in_specific_date['City'].loc[lambda x: x == c1].index[0]
                c2_index = data_in_specific_date['City'].loc[lambda x: x == c2].index[0]
            except:
                st.error(f"One or both cities ({c1}, {c2}) are not present in the dataset for the given date.")
                st.stop()

            #Stores the number of rows in the filtered dataset (number of cities on that date).
            row_length = data_in_specific_date.shape[0]

            #calculate the distance between two cities based on their latitude and longitude indices (i and j).
            def calc_distance_between_cities(i, j):
                p1 = (data_in_specific_date['Longitude'][i], data_in_specific_date['Latitude'][i])
                p2 = (data_in_specific_date['Longitude'][j], data_in_specific_date['Latitude'][j])
                return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

            # Calculate distance matrix
            distance_matrix = [
                [
                    0 if i == j else calc_distance_between_cities(i, j) for j in range(row_length)
                ] for i in range(row_length)
            ]
            #Converts the AverageTemperature column into a list for easy access.
            temp_list = list(data_in_specific_date['AverageTemperature'])

            # Function to find the warmest route
            def warmest_route(dist, temp, start, end):
                n = len(dist)
                visited = set()
                route = [start]
                current = start

                while current != end:
                    visited.add(current)

                    # Find all unvisited neighbors with distances
                    neighbors = [(i, dist[current][i]) for i in range(n) if i not in visited]

                    # Sort neighbors by distance (ascending)
                    neighbors.sort(key=lambda x: x[1])

                    # Pick the three nearest neighbors
                    nearest_three = neighbors[:3]

                    # Select the city with the highest temperature among the three
                    current = max(nearest_three, key=lambda x: temp[x[0]])[0]

                    # Move to the warmest city
                    route.append(current)

                return route


            # Get the warmest route
            result = warmest_route(distance_matrix, temp_list, c1_index, c2_index)

            # Get route city names and coordinates
            #Converts the route (indices) into city names and prints the result.
            results_names = [data_in_specific_date['City'][idx] for idx in result]
            coords = [(data_in_specific_date['Longitude'][idx], data_in_specific_date['Latitude'][idx]) for idx in
                      result]

            st.success(f"Warmest route from {c1} to {c2}:")
            st.write(results_names)

            # Geopandas Visualization
            # Step 1: Create GeoDataFrame for all cities
            geometry_cities = [Point(lon, lat) for lon, lat in
                               zip(data_in_specific_date['Longitude'], data_in_specific_date['Latitude'])]
            gdf_cities = gpd.GeoDataFrame(data_in_specific_date, geometry=geometry_cities)

            # Step 2: Create GeoDataFrame for route
            geometry_route = LineString(coords)
            gdf_route = gpd.GeoDataFrame([{'geometry': geometry_route, 'Route': 'Warmest Route'}])

            # Step 3: Plot the map
            world = gpd.read_file(get_path("naturalearth.land"))

            fig, ax = plt.subplots(figsize=(90,70))  # Adjusted for Streamlit
            world.plot(ax=ax, color='lightgrey')  # Base map
            gdf_cities.plot(ax=ax, color='blue', markersize=20, label='Cities')  # Cities
            gdf_route.plot(ax=ax, color='red', linewidth=2, label='Warmest Route')  # Route

            # Add labels only for the cities in the route
            for idx, (x, y, label) in enumerate(zip(data_in_specific_date['Longitude'],
                                                    data_in_specific_date['Latitude'],
                                                    data_in_specific_date['City'])):
                if idx in result:  # Check if the city is part of the route
                    ax.text(x, y, label, fontsize=5, color='black', ha='right', va='bottom')

            plt.title(f"Warmest Route from {c1} to {c2}")
            plt.legend()
            st.pyplot(fig)

    except FileNotFoundError:
        st.error(f"The file '{csv_file_path}' was not found. Please ensure the file exists in the specified location.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
