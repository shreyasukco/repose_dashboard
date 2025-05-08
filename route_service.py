# from geopy.distance import geodesic
# from sklearn.cluster import KMeans
# import pandas as pd
# import numpy as np

# def calculate_total_distance(outlets):
#     total_distance = 0
#     for i in range(1, len(outlets)):
#         point1 = (outlets.iloc[i - 1]['latitude'], outlets.iloc[i - 1]['longitude'])
#         point2 = (outlets.iloc[i]['latitude'], outlets.iloc[i]['longitude'])
#         total_distance += geodesic(point1, point2).km
#     return total_distance

# def is_within_distance(df1, df2, max_distance=20):
#     """Check if any point in df2 is within max_distance from any point in df1."""
#     for _, row1 in df1.iterrows():
#         point1 = (row1['latitude'], row1['longitude'])
#         for _, row2 in df2.iterrows():
#             point2 = (row2['latitude'], row2['longitude'])
#             if geodesic(point1, point2).km <= max_distance:
#                 return True
#     return False

# def merge_routes(df1, df2):
#     """Merge two routes and retain the route name of the first one."""
#     merged_df = pd.concat([df1, df2], ignore_index=True)
#     merged_df["route"] = df1["route"].iloc[0]  # Keep route name from the first dataframe
#     return merged_df

# def create_routes_by_dealer_count(df):
#     df = df.copy()
#     merged_routes = []

#     for (bo, state), group in df.groupby(["name of bo", "state1"]):
#         group = group.copy()
#         routes = list(group["route"].unique())
#         route_points = {
#             r: list(zip(
#                 group[group["route"] == r]["latitude"],
#                 group[group["route"] == r]["longitude"]
#             ))
#             for r in routes
#         }
#         route_counts = {r: len(route_points[r]) for r in routes}

#         new_rows = []
#         skip_routes = set()  # To keep track of merged routes

#         for route_name, route_df in group.groupby("route"):
#             if route_counts[route_name] > 12:
#                 if route_counts[route_name] > 30:
#                     # If the count is more than 30, split into 3 clusters
#                     kmeans = KMeans(n_clusters=3, random_state=42)
#                 else:
#                     # If count is between 12 and 30, split into 2 clusters
#                     kmeans = KMeans(n_clusters=2, random_state=42)

#                 # Perform KMeans clustering based on latitude and longitude
#                 kmeans.fit(route_df[['latitude', 'longitude']])
#                 route_df['cluster'] = kmeans.labels_

#                 # For each cluster, assign a new route name and add to the new rows
#                 for cluster_id in np.unique(kmeans.labels_):
#                     cluster_df = route_df[route_df['cluster'] == cluster_id].copy()
#                     cluster_df['route'] = f"{route_name}_split_{cluster_id + 1}"  # New route name
#                     new_rows.append(cluster_df)
#             else:
#                 # If the route count is less than or equal to 12, keep it as is
#                 new_rows.append(route_df)

#         final_group = pd.concat(new_rows, ignore_index=True)
#         merged_routes.append(final_group)

#     return pd.concat(merged_routes, ignore_index=True)
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from sklearn.preprocessing import StandardScaler

def haversine_vectorized(lat1, lon1, lat2, lon2):
    # Vectorized Haversine function for distance (in km)
    R = 6371  # Earth radius in kilometers
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)

    a = np.sin(dphi / 2.0) ** 2 + \
        np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2.0) ** 2
    return R * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))

def create_routes_by_dealer_count(df, eps_km=35, min_samples=1):
    df = df.copy()
    result = []

    for (bo, state), group in df.groupby(['name of bo', 'state1']):
        coords = group[['latitude', 'longitude']].to_numpy()

        # Convert latitude/longitude to radians
        radians = np.radians(coords)

        # Use haversine distance metric with DBSCAN
        db = DBSCAN(eps=eps_km / 6371.0,  # convert km to radians
                    min_samples=min_samples,
                    algorithm='ball_tree',
                    metric='haversine').fit(radians)

        group['cluster'] = db.labels_

        # Assign route1 names
        group['route1'] = group['cluster'].apply(
            lambda c: f"{bo}_{state}_Route_{c + 1}" if c != -1 else f"{bo}_{state}_Unclustered"
        )
        result.append(group)

    return pd.concat(result, ignore_index=True)
