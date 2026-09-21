import pandas as pd
import geopandas as gpd
import sqlite3

conn = sqlite3.connect("data/processed/mobility.db")
dim_location = pd.read_sql("SELECT * FROM dim_location", conn)
conn.close()

geometry = gpd.points_from_xy(dim_location["center_lon"], dim_location["center_lat"])
gdf = gpd.GeoDataFrame(dim_location, geometry=geometry, crs="EPSG:4326")

gdf_projected = gdf.to_crs("EPSG:32643")

results = []
for i, zone_a in gdf_projected.iterrows():
    for j, zone_b in gdf_projected.iterrows():
        if zone_a["zone_id"] != zone_b["zone_id"]:
            distance_km = zone_a["geometry"].distance(zone_b["geometry"]) / 1000
            results.append(
                {
                    "zone_a": zone_a["zone_name"],
                    "zone_b": zone_b["zone_name"],
                    "distance_km": round(distance_km, 2),
                }
            )

distances_df = pd.DataFrame(results)

closest = distances_df.loc[distances_df["distance_km"].idxmin()]
print("Closest zone pair:")
print(closest)

print("\nDistances from MG Road / Central to all other zones:")
mg_road_distances = distances_df[
    distances_df["zone_a"] == "MG Road / Central"
].sort_values("distance_km")
print(mg_road_distances[["zone_b", "distance_km"]])
