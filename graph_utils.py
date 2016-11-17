from db_utils import *
import snap

# The problem is that artist_id is a string containing letters, but the AddNode(id) function in snap requires that id be an int
# Hence, as a temporary solution before we add another entry to the database is to store a dictionary mapping artist ids to integers
# from 1 to total number of artists


# builds the artists graph for a given year
def build_graph(conn, year, artist_id_to_int):
	graph = snap.PUNGraph.New()
	active_artists = set(get_artist_ids_active_during_year(year, 5, conn)) # set is probably faster
	# Add nodes
	for artist_id in active_artists:
		graph.AddNode(artist_id_to_int[artist_id])
	# Add edges
	for artist_id in active_artists:
		artist_id_int = artist_id_to_int[artist_id]
		neighbors = set(get_sim_artists(artist_id, conn))
		active_neighbors = neighbors.intersection(active_artists)
		
		for neighbor in active_neighbors:
			if artist_id_int != artist_id_to_int[neighbor]:
				graph.AddEdge(artist_id_int, artist_id_to_int[neighbor])
	# delete nodes with noedges so they don't form extra communities
	nodes_to_delete = snap.TIntV()
	for node in graph.Nodes():
		if node.GetDeg() == 0:
			nodes_to_delete.Add(node.GetId())
	snap.DelNodes(graph, nodes_to_delete)
	return graph