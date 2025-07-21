import osmnx as ox
import geopandas as gpd

G = ox.graph_from_place("Macau, China", network_type="walk")
edges = ox.graph_to_gdfs(G, nodes=False)
edges_proj = edges.to_crs(epsg=3857)
minx, miny, _, _ = edges_proj.total_bounds
edges_proj["geometry"] = edges_proj["geometry"].translate(xoff=-minx, yoff=-miny)
edges_proj["wkt"] = edges_proj["geometry"].apply(lambda g: g.wkt)
edges_proj["wkt"].to_csv("macau_streets_for_the_one.wkt", index=False, header=False)
