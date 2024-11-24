import pandas as pd
import math

# Load the dataset
data = pd.read_csv('dataset/GlobalLandTemperaturesByCity.csv')
data['dt'] = pd.to_datetime(data['dt'])
# data['Year'] = data['dt'].dt.year
data = data.dropna()
# print(data['City'].loc[lambda x: x == 'Beijing'].index[0])
# exit(0)

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

specific_data = '1849-04-01'

data_in_specific_date = data[ (data['dt'] == specific_data) ].reset_index(drop=True)

row_length = data_in_specific_date.shape[0]


def calcDistanceBetweenTwoCities(i,j):
    p1 =(data_in_specific_date['Longitude'][i],data_in_specific_date['Latitude'][i])
    p2 =(data_in_specific_date['Longitude'][j],data_in_specific_date['Latitude'][j])
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    )

c1='London'
c2='Los Angeles'

try:
    c1_index = data_in_specific_date['City'].loc[lambda x: x == c1].index[0]
    c2_index = data_in_specific_date['City'].loc[lambda x: x == c2].index[0]
except:
    print('No record of cities in',specific_data)
    exit(0)

temp_list = list(data_in_specific_date['AverageTemperature'])

distance_matrix  = [
    [
        0 if i == j else calcDistanceBetweenTwoCities(i,j)  for j in range(row_length)
    ] for i in range(row_length)
]


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

result = warmest_route(distance_matrix, temp_list, c1_index, c2_index)
print("Route:", result)

print(len(list(set(result))) , len(result))

for idx in result:
    print(data_in_specific_date['City'][idx])


