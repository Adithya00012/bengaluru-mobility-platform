import pandas as pd
import geopandas as gpd
import sqlite3
import folium

conn = sqlite3.connect("data/processed/mobility.db")

query = """
SELECT
    loc.zone_id,
    loc.zone_name,
    loc.center_lat,
    loc.center_lon,
    COUNT(f.trip_id) as trip_count
FROM dim_location loc
LEFT JOIN fact_trips f ON loc.zone_id = f.pickup_zone_id
GROUP BY loc.zone_id, loc.zone_name, loc.center_lat, loc.center_lon
"""
zones_with_counts = pd.read_sql(query, conn)
conn.close()

print("Zones with trip counts:")
print(zones_with_counts)

geometry = gpd.points_from_xy(
    zones_with_counts["center_lon"], zones_with_counts["center_lat"]
)
gdf = gpd.GeoDataFrame(zones_with_counts, geometry=geometry, crs="EPSG:4326")

print("\nGeoDataFrame created. Geometry column:")
print(gdf[["zone_name", "geometry"]])

bengaluru_center = [12.9716, 77.5946]
m = folium.Map(location=bengaluru_center, zoom_start=11)

for _, row in gdf.iterrows():
    folium.CircleMarker(
        location=[row["center_lat"], row["center_lon"]],
        radius=5 + (row["trip_count"] * 3),  
        popup=f"{row['zone_name']}: {row['trip_count']} trips",
        color="crimson",
        fill=True,
        fill_opacity=0.6,
    ).add_to(m)

m.save("dashboards/zone_demand_map.html")
print("\nMap saved to dashboards/zone_demand_map.html")
