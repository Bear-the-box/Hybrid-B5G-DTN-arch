import osmnx as ox

file_path = "map.osm"
G = ox.graph_from_xml(file_path)
edges = ox.graph_to_gdfs(G, nodes=False)
edges["wkt"] = edges["geometry"].apply(lambda geom: geom.wkt)
edges["wkt"].to_csv("the_one_map.wkt", index=False, header=False)