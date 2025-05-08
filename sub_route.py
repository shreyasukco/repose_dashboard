import pandas as pd
from sklearn.cluster import DBSCAN
from haversine import haversine
import numpy as np
import string

def haversine_distance_matrix(coords):
    n = len(coords)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dist = haversine(coords[i], coords[j])
            dist_matrix[i][j] = dist_matrix[j][i] = dist
    return dist_matrix

def split_large_route(state_df, max_distance=150):
    dealer_count = len(state_df)
    coords = list(zip(state_df["latitude"], state_df["longitude"]))
    dist_matrix = haversine_distance_matrix(coords)
    max_dist = np.max(dist_matrix)

    if max_dist > max_distance or dealer_count > 15:
        if 15 < dealer_count <= 25:
            n_sub_groups = 2
        elif 25 < dealer_count <= 35:
            n_sub_groups = 3
        elif 35 < dealer_count <= 45:
            n_sub_groups = 4
        elif 45 < dealer_count <= 60:
            n_sub_groups = 5
        else:
            n_sub_groups = 1

        clustering = DBSCAN(eps=20, min_samples=1, metric="precomputed")
        labels = clustering.fit_predict(dist_matrix)

        # Convert label numbers into letters A, B, C,...
        label_map = {}
        for idx, label in enumerate(set(labels)):
            label_map[label] = string.ascii_uppercase[idx]
        state_df["sub_route"] = [f"{state_df['route'].iloc[0]}{label_map[label]}" for label in labels]
    else:
        state_df["sub_route"] = state_df["route"]
    return state_df

def route_service_function(filtered_df):
    result_dfs = []

    for beat, beat_df in filtered_df.groupby("name of bo"):
        for state1, state_df in beat_df.groupby("state1"):
            state_df = state_df.copy()
            coords = list(zip(state_df["latitude"], state_df["longitude"]))
            if not coords:
                continue

            dist_matrix = haversine_distance_matrix(coords)
            clustering = DBSCAN(eps=20, min_samples=1, metric="precomputed")
            labels = clustering.fit_predict(dist_matrix)
            state_df["route"] = [f"{state1}_route{label + 1}" for label in labels]

            # Split large groups
            state_df = state_df.groupby("route").apply(lambda g: split_large_route(g)).reset_index(drop=True)
            result_dfs.append(state_df)

    final_df = pd.concat(result_dfs, ignore_index=True)
    return final_df

def merge_small_routes(df, max_distance=10):
    updated_df = df.copy()
    for bo, bo_df in df.groupby("name of bo"):
        small_routes = {r: g for r, g in bo_df.groupby("sub_route") if len(g) < 5}
        all_routes = {r: g for r, g in bo_df.groupby("sub_route")}

        for route_name, small_group in small_routes.items():
            coords1 = list(zip(small_group["latitude"], small_group["longitude"]))
            for other_name, other_group in all_routes.items():
                if other_name == route_name or len(other_group) < 5:
                    continue
                coords2 = list(zip(other_group["latitude"], other_group["longitude"]))
                if any(haversine(c1, c2) <= max_distance for c1 in coords1 for c2 in coords2):
                    merged_name = route_name.split('_')[0] + "_merged"
                    updated_df.loc[updated_df["sub_route"] == route_name, "sub_route"] = merged_name
                    updated_df.loc[updated_df["sub_route"] == other_name, "sub_route"] = merged_name
                    break
    return updated_df
