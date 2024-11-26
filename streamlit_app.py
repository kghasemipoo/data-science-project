import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from geodatasets import get_path
import os

# Sidebar navigation
st.sidebar.title("Navigation")
app_choice = st.sidebar.radio(
    "Go to",
    ("Temperature Analysis", "Routing between 2 cities"),
)

# Temperature Analysis App
if app_choice == "Temperature Analysis":
    st.title("Temperature Range Analysis for Major Cities")
    st.sidebar.header("Configuration")

    # Sidebar options for this app
    top_n = st.sidebar.slider("Number of Top Cities", min_value=5, max_value=50, value=20)

    # Load the specific CSV file
    csv_file_path = "dataset/GlobalLandTemperaturesByMajorCity.csv"

    try:
        # Load and preprocess data
        data = pd.read_csv(csv_file_path)
        data['dt'] = pd.to_datetime(data['dt'])
        data['Year'] = data['dt'].dt.year
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

        # Calculate temperature range
        temperature_range = data.groupby(['City', 'Country'])['AverageTemperature'].agg(['max', 'min'])
        temperature_range['range'] = temperature_range['max'] - temperature_range['min']

        # Sort and get top cities
        top_cities_range = temperature_range.sort_values(by='range', ascending=False).head(top_n)
        top_cities_data = data[data.set_index(['City', 'Country']).index.isin(top_cities_range.index)]
        top_cities_data_unique = top_cities_data.drop_duplicates(subset=['City', 'Country'])

        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(
            top_cities_data_unique,
            geometry=gpd.points_from_xy(top_cities_data_unique.Longitude, top_cities_data_unique.Latitude),
            crs="EPSG:4326"
        )

        # Visualization
        st.subheader("World Map with Top Cities")
        world = gpd.read_file(get_path("naturalearth.land"))

        fig, ax = plt.subplots(figsize=(90,70))  # Adjusted figure size for Streamlit
        world.plot(ax=ax, cmap='tab20', legend=True, edgecolor="black", linewidth=0.5)

        # Plot the top cities
        for idx, row in gdf.iterrows():
            city = row['City']
            country = row['Country']
            temp_range = top_cities_range.loc[(city, country), 'range']
            ax.scatter(row['Longitude'], row['Latitude'], color='red', s=50)
            ax.annotate(f"{city}, {country}\nRange: {temp_range:.2f}°C",
                        (row['Longitude'], row['Latitude']),
                        textcoords="offset points",
                        xytext=(5, 5),
                        ha='center', fontsize=10, color='black')

        plt.title("Cities with the Largest Temperature Range")
        st.pyplot(fig)

        # Display table of results
        st.subheader("Top Cities with Largest Temperature Range")
        st.dataframe(top_cities_range, use_container_width=True)
    except FileNotFoundError:
        st.error(f"The file '{csv_file_path}' was not found. Please ensure the file exists in the specified location.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# The Routing App
elif app_choice == "Routing between 2 cities":
    os.system("streamlit run streamlit_app2.py")


