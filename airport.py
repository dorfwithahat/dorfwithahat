import heapq
import tkinter as tk
from tkinter import messagebox

class Graph:
    def __init__(self, edges_list=None):
        self.nodes = []
        self.edges = []
        if edges_list is not None:
            self.add_edges(edges_list)

    def add_node(self, v):
        self.nodes.append(v)

    def add_edge(self, ab, travel_time, layover_time):
        a, b = ab
        if a not in self.nodes:
            self.nodes.append(a)
        if b not in self.nodes:
            self.nodes.append(b)
        my_new_edge = Edge(ab, travel_time, layover_time)
        self.edges.append(my_new_edge)

    def add_edges(self, e_list):
        for ab, travel_time, layover_time in e_list:
            self.add_edge(ab, travel_time, layover_time)

    def dijkstra(self, start_node):
        # Create a priority queue to store (distance, node) tuples
        queue = []
        heapq.heappush(queue, (0, start_node))  # Use heapq to manage the priority queue

        # Create a dictionary to store the shortest path to each node
        distances = {node: float('infinity') for node in self.nodes}
        distances[start_node] = 0

        # Create a dictionary to store the best previous node to each node
        previous_nodes = {node: None for node in self.nodes}

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            # If we found a shorter path before, skip processing this node
            if current_distance > distances[current_node]:
                continue

            # Look at each neighbor of the current node
            for edge in self.edges:
                if edge._from == current_node:
                    # Add both the travel time and the specific layover time for this edge
                    distance = current_distance + edge._weight + edge._layover_time

                    # If a shorter path is found
                    if distance < distances[edge._to]:
                        distances[edge._to] = distance
                        previous_nodes[edge._to] = current_node
                        heapq.heappush(queue, (distance, edge._to))

        return distances, previous_nodes

    def get_edge_distance(self, from_node, to_node):
        for edge in self.edges:
            if edge._from == from_node and edge._to == to_node:
                return edge._weight + edge._layover_time
        return None  # If no edge exists between the nodes

    def get_shortest_path_with_distances(self, previous_nodes, start_node, target_node):
        path = []
        current_node = target_node

        # Trace back from target node to start node
        while current_node is not None:
            path.append(current_node)
            current_node = previous_nodes[current_node]

        # Reverse the path to get it in the correct order
        path = path[::-1]

        # Check if the start node is in the path (if not, no valid path exists)
        if path[0] != start_node:
            return None, None  # Return None if no valid path exists

        # Output the path along with distances between nodes
        total_distance = 0
        distances_with_path = []
        for i in range(len(path) - 1):
            from_node = path[i]
            to_node = path[i + 1]
            edge_distance = self.get_edge_distance(from_node, to_node)
            if edge_distance is not None:
                distances_with_path.append(f"{from_node} -> {to_node}: {edge_distance} units")
                total_distance += edge_distance
            else:
                distances_with_path.append(f"No direct edge between {from_node} and {to_node}")

        distances_with_path.append(f"Total travel time: {total_distance} units")

        return path, distances_with_path


class Edge:
    def __init__(self, ab, travel_time, layover_time):
        a, b = ab
        self._from = a
        self._to = b
        self._weight = travel_time  # Travel time between cities
        self._layover_time = layover_time  # Layover time for this specific flight

    def get_names(self):
        """Return just the names of the nodes (from and to)."""
        return self._from, self._to

# Example edge list with travel times and layover times
edgelist = [
    (('Atlanta', 'Chicago'), 2.1, 0.5),  # 2.1 is travel time, 0.5 is layover time
    (('Chicago', 'San Francisco'), 4.7, 1.0),
    (('San Francisco', 'Newark'), 6.2, 1.5),
    (('San Diego', 'Newark'), 5.8, 1.0),
    (('Atlanta', 'Newark'), 2.3, 0.3)
]

# Creating graph
g = Graph(edgelist)

# Create the UI
def create_ui():
    root = tk.Tk()
    root.title("Flight Path Finder")

    # Labels for input
    tk.Label(root, text="Starting City:").grid(row=0, column=0, padx=10, pady=10)
    tk.Label(root, text="Destination City:").grid(row=1, column=0, padx=10, pady=10)

    # Input fields
    start_city_var = tk.StringVar()
    target_city_var = tk.StringVar()

    start_city_entry = tk.Entry(root, textvariable=start_city_var)
    start_city_entry.grid(row=0, column=1, padx=10, pady=10)

    target_city_entry = tk.Entry(root, textvariable=target_city_var)
    target_city_entry.grid(row=1, column=1, padx=10, pady=10)

    # Output label for the path
    output_label = tk.Label(root, text="", wraplength=400, justify="left")
    output_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Function to handle finding the shortest path
    def find_path():
        start_city = start_city_var.get()
        target_city = target_city_var.get()

        if not start_city or not target_city:
            messagebox.showerror("Input Error", "Both fields are required!")
            return

        distances, previous_nodes = g.dijkstra(start_city)
        path, distances_with_path = g.get_shortest_path_with_distances(previous_nodes, start_city, target_city)

        if path:
            output_label.config(text="\n".join(distances_with_path))
        else:
            output_label.config(text="No valid path found.")

    # Button to find the path
    find_path_button = tk.Button(root, text="Find Shortest Path", command=find_path)
    find_path_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Run the UI loop
    root.mainloop()

# Call the function to create the UI
create_ui()

#add to kaboom project,
# add a sprite for the bullets
# add a sprite for the gun as well
# way to display ammo
# way to hide ammo before we have the gun item