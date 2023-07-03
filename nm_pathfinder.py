import math
from queue import PriorityQueue

def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """


    #initialize required lists
    path = []
    #boxes = mesh['boxes'] 
    #adjacency = mesh['adj']

    print(source_point)
    print(destination_point)

    #check if inside bounds
    if source_point not in boxes or destination_point not in boxes:
        return [], []

    #initialize forward queue and backward queue
    forward_queue = PriorityQueue()
    backward_queue = PriorityQueue()
    forward_queue.put((0, source_point))
    backward_queue.put((0, destination_point))  

    #initialize for storing visited points
    forward_visited = {source_point: None} 
    backward_visited = {destination_point: None} 

    #Initialize variables for visited points
    intersection_point = None
    shortest_distance = math.inf

    #Main search loop
    while not forward_queue.empty() and not backward_queue.empty():
        
        #forward search
        forward_cost, forward_current = forward_queue.get()
        if forward_cost > shortest_distance:
            break

        #check if the point has been visited
        if forward_current in backward_visited:

            #calculate distance from source to destination
            total_distance = forward_cost + backward_visited[forward_current][0]

            #update shortest distance and intersection point
            if total_distance < shortest_distance:
                shortest_distance = total_distance
                intersection_point = forward_current

        #explore neighbor points in forward direction
        for neighbor in adjacency[forward_current]:
            new_cost = forward_cost + distance(forward_current, neighbor)
            if neighbor not in forward_visited or new_cost < forward_visited[neighbor][0]:
                forward_visited[neighbor] = (new_cost, forward_current)
                forward_queue.put((new_cost, neighbor))

        #backward search
        backward_cost, backward_current = backward_queue.get()
        if backward_cost > shortest_distance:
            break

        #check if current point has been visited
        if backward_current in forward_visited:
            #calculate distance from source to destination
            total_distance = backward_cost + forward_visited[backward_current][0]

            #update shortest distance and intersection point
            if total_distance < shortest_distance:
                shortest_distance = total_distance
                intersection_point = backward_current

        #explore neighbor points in backward direction
        for neighbor in adjacency[backward_current]:
            new_cost = backward_cost + distance(backward_current, neighbor)
            if neighbor not in backward_visited or new_cost < backward_visited[neighbor][0]:
                backward_visited[neighbor] = (new_cost, backward_current)
                backward_queue.put((new_cost, neighbor))

    #reconstruct the path
    if intersection_point is not None:
        forward_path = reconstruct_path(intersection_point, forward_visited)
        backward_path = reconstruct_path(intersection_point, backward_visited, reverse=True)
        path = forward_path + backward_path
    
    #return the path
    return path, list(boxes.keys())

def distance(point1, point2):
    """
    Function for returning the distance between two points
    """
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def reconstruct_path(point, visited, reverse=False):
    """
    Function for remaking the path for each new shortest distance found
    """
    path = []
    current = point
    while current:
        path.append(current)
        current = visited[current][1]
    if reverse:
        path.reverse()
    return path