from os import environ
import sys
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import copy
from queue import Queue
import random

def shortest_path(maze, start, end):
    rows = len(maze)
    cols = len(maze[0])

    def find_path(row, col, length, path):
        if row == end[0] and col == end[1]:
            return length, path + [(row, col)]
        if maze[row][col] == 1:
            return float('inf'), None
        maze[row][col] = 1
        path.append((row, col))
        min_length = float('inf')
        min_path = None
        if row > 0:
            l, p = find_path(row-1, col, length+1, path)
            if l < min_length:
                min_length = l
                min_path = p
        if row < rows-1:
            l, p = find_path(row+1, col, length+1, path)
            if l < min_length:
                min_length = l
                min_path = p
        if col > 0:
            l, p = find_path(row, col-1, length+1, path)
            if l < min_length:
                min_length = l
                min_path = p
        if col < cols-1:
            l, p = find_path(row, col+1, length+1, path)
            if l < min_length:
                min_length = l
                min_path = p
        path.pop()
        maze[row][col] = 0
        return min_length, min_path
    
    min_length, path = find_path(start[0], start[1], 0, [])
    return min_length, path

def generate_maze(M, entry, exit):
    # Create the maze grid with all walls intact
    maze = [[1 for j in range(M)] for i in range(M)]
    
    # Mark the entry and exit points as visited
    maze[0][entry] = 0
    maze[M-1][exit] = 0
    
    # Recursively explore the maze
    explore_maze(maze, 0, entry)
    
    # Check if there is a valid path from entry to exit
    if not check_valid_path(maze, entry, exit):
        return generate_maze(M, entry, exit)
    
    return maze

def explore_maze(maze, i, j):
    # Define the four possible directions to move
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # Randomly shuffle the directions
    random.shuffle(directions)
    
    # Explore each direction
    for d_i, d_j in directions:
        # Calculate the new position
        new_i, new_j = i + 2*d_i, j + 2*d_j
        
        # Check if the new position is inside the maze
        # if 0 <= new_i < len(maze) and 0 <= new_j < len(maze[0]):
        if 0 < new_i < len(maze) and 0 < new_j < len(maze[0]):
            # Check if the new position is unvisited
            if maze[new_i][new_j] == 1:
                # Knock down the wall between the current and new cell
                maze[i+d_i][j+d_j] = 0
                
                # Mark the new cell as visited
                maze[new_i][new_j] = 0

                # Recursively explore the new cell
                explore_maze(maze, new_i, new_j)


def check_valid_path(maze, entry, exit):
    # Define the four possible directions to move
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]    
    # Create a queue for BFS
    q = Queue()
    
    # Add the entry point to the queue
    q.put((0, entry))
    
    # Keep track of visited cells
    visited = set()
    visited.add((0, entry))
    
    # Perform BFS
    while not q.empty():
        i, j = q.get()
        if i == len(maze)-1 and j == exit:
            # Found a path from entry to exit
            return True
        for d_i, d_j in directions:
            new_i, new_j = i + d_i, j + d_j
            if 0 <= new_i < len(maze) and 0 <= new_j < len(maze[0]) and (new_i, new_j) not in visited and maze[new_i][new_j] == 0:
                visited.add((new_i, new_j))
                q.put((new_i, new_j))
    
    # No path from entry to exit
    return False

def animate_path(maze, path):
    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()
    # Set the window size
    size = len(maze)*20
    screen = pygame.display.set_mode((size, size))
    pygame.display.set_caption("Maze Animation")
    # Set the colors
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    # Draw the walls of the maze
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, black, (j*20, i*20, 20, 20))
            else:
                pygame.draw.rect(screen, white, (j*20, i*20, 20, 20))

    # Main loop, run until window closed
    # Run the animation
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            # Draw the path
        for point in path:
            pygame.draw.rect(screen, red, (point[1]*20, point[0]*20, 20, 20))
            pygame.display.update()
            clock.tick(25) #run the loop X tick(s) per second, higher number is faster

if __name__ == "__main__":
    
    # accept user input and check for int value,  round it down to divisible by 2
    # maze_size = 30 
    maze_size = input("Input the size of the maze? Range from 10 to 40: ")
    try:
        maze_size = (int(maze_size)//2)*2
    except ValueError:
        print("This is not a number")
        sys.exit()
        
    if maze_size < 10:
        maze_size = 10
    elif maze_size > 40:
        maze_size = 40
    
    maze_entry = int(maze_size*0.15)
    maze_exit = int(maze_size*0.85)

    maze = generate_maze(maze_size, maze_entry, maze_exit)
    animate_maze = copy.deepcopy(maze)

    start = (0, maze_entry)
    end = (maze_size-1, maze_exit)
    min_length, path = shortest_path(maze, start, end)
    print(f"Minimum Path Length: {min_length}")
    animate_path(animate_maze, path)