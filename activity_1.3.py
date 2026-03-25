import csv
import heapq
import os
import itertools

# ============================================================
# Activity 1.3 - Railway Route Planning System
# UFCFYR-15-2 Advanced Algorithms Coursework
# ============================================================
# This program finds the LOWEST COST route for a logistics
# container to visit a given set of UK railway stations.
#
# Rules (from the brief):
#   - Each destination station can be visited ONCE only
#   - Exception: the start and final destination CAN be the same
#     (making the route a loop/cycle)
#   - The route must visit ALL specified stations
#
# Algorithm overview:
#   Step 1 — Build a graph from the CSV railway network data
#   Step 2 — Use DIJKSTRA'S ALGORITHM to find the shortest path
#             between every pair of required stations
#   Step 3 — Use BRUTE-FORCE PERMUTATION to find the optimal
#             visiting order (Travelling Salesman Problem variant)
#   Step 4 — Reconstruct the full detailed route and save it
#
# Extra feature: Partial/fuzzy station name matching so the user
# does not need to type exact station names.
# ============================================================

NETWORK_FILE = os.path.join("activity1_3", "activity1_3_railnetwork_data.csv")
OUTPUT_FILE  = os.path.join("activity1_3", "route_result.txt")


# ============================================================
# SECTION 1: Graph Construction
# ============================================================

def load_graph(filepath):
    """
    Load the railway network CSV into an adjacency list (dictionary).

    CSV format per row:  StationA, StationB, Cost

    An adjacency list is chosen because:
      - It uses less memory than a matrix for sparse graphs
        (most stations only connect to a few neighbours)
      - Neighbour lookup is O(degree) which is fast for Dijkstra's

    The graph is UNDIRECTED — if A connects to B, B also connects to A
    (trains run both ways, and the cost is the same either direction).

    Returns:
        dict  {station_name: {neighbour_name: cost, ...}, ...}
    """
    graph = {}

    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3 or not row[0].strip():
                continue  # skip empty or malformed rows

            station_a = row[0].strip()
            station_b = row[1].strip()

            try:
                weight = int(row[2].strip())
            except ValueError:
                continue  # skip rows with non-numeric weights

            # Ensure both stations exist as keys in the graph
            if station_a not in graph:
                graph[station_a] = {}
            if station_b not in graph:
                graph[station_b] = {}

            # Add edge in BOTH directions (undirected graph)
            graph[station_a][station_b] = weight
            graph[station_b][station_a] = weight

    return graph


# ============================================================
# SECTION 2: Dijkstra's Shortest Path Algorithm
# ============================================================

def dijkstra(graph, start):
    """
    Find the shortest path from 'start' to every other station.

    Dijkstra's Algorithm works by maintaining a priority queue of
    (distance, station) pairs.  We always process the station with
    the smallest known distance first (greedy choice), which
    guarantees we find the global shortest path.

    Data structures used:
      - distances  : dict mapping each station to its shortest known
                     distance from 'start' (initialised to infinity)
      - previous   : dict recording which station we came from on
                     the optimal path (used to reconstruct the route)
      - pq         : a MIN-HEAP (priority queue) — heapq in Python
                     gives O(log n) insert and O(log n) extract-min,
                     making this implementation O((V + E) log V)

    Parameters:
        graph (dict) : adjacency list of the full railway network
        start (str)  : name of the station to start from

    Returns:
        distances (dict) : {station: shortest_distance_from_start}
        previous  (dict) : {station: previous_station_on_best_path}
    """
    # Initialise all distances to infinity (unknown/unreachable)
    distances = {node: float('inf') for node in graph}
    distances[start] = 0  # distance from start to itself is 0

    # Track which station we arrived from on the best known path
    previous = {node: None for node in graph}

    # Priority queue: (distance, station_name)
    # heapq always gives us the smallest distance first (min-heap)
    pq = [(0, start)]

    visited = set()  # stations whose shortest path is finalised

    while pq:
        current_dist, current_node = heapq.heappop(pq)  # get closest unvisited station

        # If already finalised, skip (stale entry in the heap)
        if current_node in visited:
            continue
        visited.add(current_node)

        # Explore each neighbour of the current station
        for neighbour, edge_weight in graph[current_node].items():
            new_dist = current_dist + edge_weight

            # If we found a shorter route to this neighbour, update it
            if new_dist < distances[neighbour]:
                distances[neighbour] = new_dist
                previous[neighbour] = current_node
                heapq.heappush(pq, (new_dist, neighbour))

    return distances, previous


def reconstruct_path(previous, start, end):
    """
    Walk backwards through the 'previous' dict to rebuild the
    full station-by-station path from 'start' to 'end'.

    Returns:
        list of station names from start to end,
        or an empty list if no path exists.
    """
    path = []
    current = end

    while current is not None:
        path.append(current)
        current = previous.get(current)

    path.reverse()  # we built it backwards, so reverse it

    # Verify the path actually starts at 'start'
    if not path or path[0] != start:
        return []  # no valid path found

    return path


def precompute_paths(graph, stations):
    """
    Run Dijkstra's from each required station to build:
      - cost_matrix : cost_matrix[A][B] = cheapest travel cost from A to B
      - path_matrix : path_matrix[A][B] = list of all stations on that route

    This avoids running Dijkstra's repeatedly during route search.

    Time complexity: O(n × (V + E) log V)
      where n = number of required stations,
            V = total stations in network,
            E = total connections.

    Returns:
        cost_matrix (dict of dict)
        path_matrix (dict of dict)
    """
    cost_matrix = {}
    path_matrix = {}

    for station in stations:
        distances, previous = dijkstra(graph, station)
        cost_matrix[station] = {}
        path_matrix[station] = {}

        for other in stations:
            if other == station:
                continue
            cost_matrix[station][other] = distances[other]
            path_matrix[station][other] = reconstruct_path(previous, station, other)

    return cost_matrix, path_matrix


# ============================================================
# SECTION 3: Optimal Route Search (TSP variant)
# ============================================================

def find_optimal_route(required_stations, start, end, cost_matrix):
    """
    Find the minimum-cost order to visit all required stations
    from 'start' to 'end', visiting each station exactly once.

    This is a variant of the Travelling Salesman Problem (TSP).
    We solve it by trying ALL possible orderings of the intermediate
    stations (brute-force permutation search).

    Why brute force is acceptable here:
      - The number of required stations is typically small (5-10)
      - For n intermediate stations, we check n! orderings
      - For n=8 intermediates: 8! = 40,320 — extremely fast
      - For larger sets, Held-Karp DP (O(n² × 2^n)) could be used

    Parameters:
        required_stations : all stations the container must visit
        start             : the starting station
        end               : the final destination
        cost_matrix       : precomputed shortest costs between stations

    Returns:
        (min_cost, best_route)
          min_cost   : total cost of the optimal route (int)
          best_route : ordered list of required stations to visit
    """
    # Intermediate stations = everything except start and end
    if start == end:
        # It's a loop — start and end are the same station
        intermediates = [s for s in required_stations if s != start]
    else:
        intermediates = [s for s in required_stations if s != start and s != end]

    min_cost   = float('inf')
    best_route = None

    # Try every possible ordering of the intermediate stations
    for permutation in itertools.permutations(intermediates):

        # Build the full candidate route: start → intermediates... → end
        route = [start] + list(permutation) + [end]

        # Calculate the total cost for this ordering
        total_cost = 0
        valid = True

        for i in range(len(route) - 1):
            leg_cost = cost_matrix[route[i]].get(route[i + 1], float('inf'))

            if leg_cost == float('inf'):
                valid = False  # no path between these two stations
                break

            total_cost += leg_cost

        # Keep this route if it's valid and cheaper than the best so far
        if valid and total_cost < min_cost:
            min_cost   = total_cost
            best_route = route

    return min_cost, best_route


# ============================================================
# SECTION 4: Route Reconstruction
# ============================================================

def build_full_route(best_route, path_matrix):
    """
    Expand the high-level visiting order into a full step-by-step
    route listing every station the container passes through,
    including intermediate stops not in the required list.

    Example:
        best_route  = [London, Bristol, Oxford]
        full_route  = [London, Reading, Swindon, Bristol, ...Oxford]

    Returns:
        list of all station names in travel order
    """
    full_route = []

    for i in range(len(best_route) - 1):
        segment = path_matrix[best_route[i]][best_route[i + 1]]

        if i == 0:
            full_route.extend(segment)          # first segment: include start
        else:
            full_route.extend(segment[1:])      # subsequent: skip first (already added)

    return full_route


# ============================================================
# SECTION 5: Station Name Matching (Extra Feature)
# ============================================================

def find_station(query, all_stations):
    """
    Match a user's input to a station name in the network.

    Matching priority:
      1. Exact match (case-insensitive)
      2. Partial match — user's text appears anywhere in the station name
      3. If multiple partial matches: list them and let user choose

    This means users can type 'Bristol' instead of
    'BRISTOL TEMPLE MEADS', or 'Manchester P' for
    'MANCHESTER PICCADILLY'.

    Returns:
        str  : matched station name, or None if not found
    """
    query_clean = query.strip().lower()

    # 1. Exact match (ignoring case)
    for station in all_stations:
        if station.lower() == query_clean:
            return station

    # 2. Partial match
    matches = [s for s in all_stations if query_clean in s.lower()]

    if len(matches) == 1:
        return matches[0]  # only one match — use it automatically

    elif len(matches) > 1:
        # Multiple matches — ask the user to choose
        print(f"  Multiple stations match '{query}':")
        for i, m in enumerate(matches, 1):
            print(f"    {i}. {m}")
        try:
            choice = int(input("  Enter number to select: "))
            return matches[choice - 1]
        except (ValueError, IndexError):
            print("  Invalid choice.")
            return None

    # No match found
    print(f"  WARNING: No station found matching '{query}'.")
    return None


# ============================================================
# SECTION 6: Output
# ============================================================

def display_and_save(output_path, required_stations, start, end,
                     min_cost, best_route, full_route, cost_matrix):
    """
    Print the results to the console and save them to a text file.

    Output includes:
      - The required stations and start/end
      - The optimal visiting order of required stations
      - The cost of each leg between required stations
      - The complete step-by-step route through all intermediate stops
      - The total cost
    """
    lines = []
    lines.append("=" * 65)
    lines.append("  RAILWAY LOGISTICS ROUTE PLANNER — RESULT")
    lines.append("=" * 65)
    lines.append("")
    lines.append(f"  Required stations : {', '.join(required_stations)}")
    lines.append(f"  Start             : {start}")
    lines.append(f"  Destination       : {end}")
    lines.append("")
    lines.append("  Optimal visiting order (required stations only):")

    # Show each leg with its cost
    for i in range(len(best_route) - 1):
        leg_cost = cost_matrix[best_route[i]][best_route[i + 1]]
        lines.append(f"    {best_route[i]}")
        lines.append(f"        ↓  (cost: {leg_cost})")
    lines.append(f"    {best_route[-1]}")
    lines.append("")
    lines.append(f"  Total cost : {min_cost}")
    lines.append("")
    lines.append(f"  Full route including all intermediate stops ({len(full_route)} stations):")
    lines.append("  " + " → ".join(full_route))
    lines.append("")
    lines.append("=" * 65)

    # Print to console
    for line in lines:
        print(line)

    # Save to file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\n  Results saved to: {output_path}")


# ============================================================
# SECTION 7: Main Entry Point
# ============================================================

def main():
    """
    Orchestrates the full route planning system:
      1. Load the railway network graph
      2. Get required stations from the user
      3. Precompute shortest paths between required stations
      4. Find optimal visiting order
      5. Display and save the result
    """
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    network_path = os.path.join(script_dir, NETWORK_FILE)
    output_path  = os.path.join(script_dir, OUTPUT_FILE)

    # --- Step 1: Load the railway network ---
    print("Loading railway network...")
    graph = load_graph(network_path)
    all_stations = list(graph.keys())
    print(f"  Network loaded: {len(all_stations)} stations.\n")

    # --- Step 2: Get the list of stations to visit from the user ---
    print("Enter the stations the container must visit (comma-separated).")
    print("Tip: partial names are accepted, e.g. 'Bristol' or 'Manchester P'")
    print("Example: London, Oxford, Bristol, Birmingham, Exeter\n")

    raw_input = input("Stations: ").split(',')

    required_stations = []
    for name in raw_input:
        match = find_station(name.strip(), all_stations)
        if match:
            if match not in required_stations:       # avoid duplicates
                required_stations.append(match)
                print(f"  Matched: {match}")
        # else: warning already printed inside find_station()

    if len(required_stations) < 2:
        print("\nNeed at least 2 valid stations. Exiting.")
        return

    # --- Get start and end stations ---
    print(f"\nEnter the START station (must be one of the stations above):")
    start = find_station(input("Start: ").strip(), required_stations)

    print(f"Enter the DESTINATION station (must be one of the stations above):")
    end = find_station(input("Destination: ").strip(), required_stations)

    if not start or not end:
        print("Invalid start or destination station. Exiting.")
        return

    if start == end:
        print(f"\nStart and destination are the same ({start}) — planning a round trip.")

    # --- Step 3: Precompute shortest paths between required stations ---
    print("\nComputing shortest paths between required stations (Dijkstra's)...")
    cost_matrix, path_matrix = precompute_paths(graph, required_stations)

    # Check all pairs are reachable
    for a in required_stations:
        for b in required_stations:
            if a != b and cost_matrix[a].get(b, float('inf')) == float('inf'):
                print(f"  WARNING: No path found between {a} and {b}.")

    # --- Step 4: Find optimal visiting order ---
    print("Finding optimal route (testing all permutations)...")
    min_cost, best_route = find_optimal_route(
        required_stations, start, end, cost_matrix
    )

    if best_route is None:
        print("No valid route found connecting all required stations. Exiting.")
        return

    # --- Step 5: Build the full detailed route ---
    full_route = build_full_route(best_route, path_matrix)

    # --- Step 6: Display and save ---
    print()
    display_and_save(
        output_path, required_stations, start, end,
        min_cost, best_route, full_route, cost_matrix
    )


if __name__ == "__main__":
    main()
