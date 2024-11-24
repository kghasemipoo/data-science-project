import pandas as pd
import geopandas
import matplotlib.pyplot as plt
from geodatasets import get_path

# Load the dataset
data = pd.read_csv('dataset/GlobalLandTemperaturesByMajorCity.csv')
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

# Calculate the temperature range (max temperature - min temperature) for each city
temperature_range = data.groupby(['City', 'Country'])['AverageTemperature'].agg(['max', 'min'])

# DEBUG
# print(temperature_range)
# exit(0)

temperature_range['range'] = temperature_range['max'] - temperature_range['min']

# Sort cities by temperature range in descending order
top_cities_range = temperature_range.sort_values(by='range', ascending=False).head(
    20)  # Top 20 cities with largest range

# Merge with the original data to get coordinates
top_cities_data = data[data.set_index(['City', 'Country']).index.isin(top_cities_range.index)]

# Remove duplicates to only show one entry per city
top_cities_data_unique = top_cities_data.drop_duplicates(subset=['City', 'Country'])

# Create GeoDataFrame for the top cities
gdf = geopandas.GeoDataFrame(
    top_cities_data_unique,
    geometry=geopandas.points_from_xy(top_cities_data_unique.Longitude, top_cities_data_unique.Latitude),
    crs="EPSG:4326"
)

# Load the world map using GeoPandas built-in dataset
world = geopandas.read_file(get_path("naturalearth.land"))

# Plot the map with distinguished countries
fig, ax = plt.subplots(figsize=(90, 70))
world.plot(ax=ax, cmap='tab20', legend=True, edgecolor="black", linewidth=0.5)

# Plot the top cities with the largest temperature range
for idx, row in gdf.iterrows():
    city = row['City']
    country = row['Country']
    temp_range = top_cities_range.loc[(city, country), 'range']
    ax.scatter(row['Longitude'], row['Latitude'], color='red', s=5)
    ax.annotate(f"{city}, {country}\nRange: {temp_range:.2f}°C",
                (row['Longitude'], row['Latitude']),
                textcoords="offset points",
                xytext=(5, 5),  # Adjust the position of the text
                ha='center', fontsize=8, color='black')

plt.title("Cities with the Largest Temperature Range")
plt.legend()
plt.show()
