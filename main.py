import pandas as pd
import geopandas
import matplotlib.pyplot as plt
from geodatasets import get_path
data =pd.read_csv('dataset/GlobalLandTemperaturesByMajorCity.csv'
)

# Drop rows with missing values
data = data.dropna()

# Convert latitude and longitude to numeric
def convert_coords(coord):
    """Convert coordinate strings to numeric."""
    if 'N' in coord or 'E' in coord:
        return float(coord[:-1])
    elif 'S' in coord or 'W' in coord:
        return -float(coord[:-1])
    return float(coord)

data['Latitude'] = data['Latitude'].apply(convert_coords)
data['Longitude'] = data['Longitude'].apply(convert_coords)

gdf = geopandas.GeoDataFrame(data, geometry=geopandas.points_from_xy(data.Longitude, data.Latitude), crs="EPSG:4326")
print(gdf)

world = geopandas.read_file(get_path("naturalearth.land"))


# Plot the map with distinguished countries
fig, ax = plt.subplots(figsize=(15, 10))

# Plot cities and annotate them with country and city names
# Remove duplicates based on City and Country
data_unique = data.drop_duplicates(subset=['City', 'Country'])

# Create GeoDataFrame for cities
gdf = geopandas.GeoDataFrame(
    data_unique, geometry=geopandas.points_from_xy(data_unique.Longitude, data_unique.Latitude), crs="EPSG:4326"
)

# Load the world map using GeoPandas built-in dataset

# Plot the map with distinguished countries
fig, ax = plt.subplots(figsize=(100, 70))
world.plot(ax=ax, cmap='tab20', legend=True, edgecolor="black", linewidth=0.5)

# Plot cities and annotate them with country and city names
for idx, row in gdf.iterrows():
    city = row['City']
    country = row['Country']
    ax.scatter(row['Longitude'], row['Latitude'], color='red', s=5)
    ax.annotate(f"{city}, {country}",
                (row['Longitude'], row['Latitude']),
                textcoords="offset points",
                xytext=(5, 5),  # Adjust the position of the text
                ha='center', fontsize=8, color='black')

plt.title("Global Land Temperatures by Major City")
plt.legend()
plt.show()