# route_optimizer.py
# Route optimization using Dijkstra Algorithm

import heapq

# Graph representing Delhi NCR road network
graph = {

    "AIIMS": {
        "Ring Road": 4,
        "Lodhi Road": 6
    },

    "Ring Road": {
        "Connaught Place": 5,
        "Noida Sector 62": 8
    },

    "Lodhi Road": {
        "Connaught Place": 3
    },

    "Connaught Place": {
        "Gurgaon Cyber City": 10
    },

    "Noida Sector 62": {
        "Gurgaon Cyber City": 6
    },

    "Gurgaon Cyber City": {}
}


def find_fastest_route(start, end):

    queue = [(0, start, [])]

    visited = set()

    while queue:

        cost, node, path = heapq.heappop(queue)

        if node in visited:
            continue

        visited.add(node)

        path = path + [node]

        if node == end:
            return path, cost

        # FIX: use .items()
        for neighbor, weight in graph.get(node, {}).items():

            heapq.heappush(queue, (cost + weight, neighbor, path))

    return None, None