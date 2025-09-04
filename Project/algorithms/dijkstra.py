# dijkstra.py
import math
import json
import heapq

class PriorityQueue:
    def __init__(self):
        self.collection = []

    def enqueue(self, element):
        if self.is_empty():
            self.collection.append(element)
        else:
            added = False
            for i in range(len(self.collection)):
                if element[1] < self.collection[i][1]:
                    self.collection.insert(i, element)
                    added = True
                    break
            if not added:
                self.collection.append(element)

    def dequeue(self):
        return self.collection.pop(0)

    def is_empty(self):
        return len(self.collection) == 0

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in km

def dijkstra(source_index, edges):
    n = len(edges)
    distances = [float('inf')] * n
    distances[source_index] = 0
    visited = [False] * n
    priority_queue = [(0, source_index)]

    while priority_queue:
        current_distance, current_index = heapq.heappop(priority_queue)
        
        if visited[current_index]:
            continue

        visited[current_index] = True

        for edge in edges[current_index]:
            neighbor_index = edge['node']
            weight = edge['distance']

            if distances[current_index] + weight < distances[neighbor_index]:
                distances[neighbor_index] = distances[current_index] + weight
                heapq.heappush(priority_queue, (distances[neighbor_index], neighbor_index))

    return distances
