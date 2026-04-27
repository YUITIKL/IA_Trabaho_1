import heapq
import time


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(pos, grid, tunnels):
    rows, cols = len(grid), len(grid[0])
    x, y = pos

    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    neighbors = []

    for dx, dy in moves:
        nx, ny = x + dx, y + dy

        if 0 <= nx < rows and 0 <= ny < cols:
            cell = grid[nx][ny]

            if cell in ['#', 'F']:
                continue

            if cell == 'T':
                if (nx, ny) in tunnels:
                    neighbors.append(tunnels[(nx, ny)])
                else:
                    neighbors.append((nx, ny))
            else:
                neighbors.append((nx, ny))

    return neighbors


def cost(pos, grid):
    x, y = pos
    cell = grid[x][y]

    if cell == 'S':
        return 3
    return 1


def h1(n, goal):
    return 3 * manhattan(n, goal)


def h2(n, goal):
    return manhattan(n, goal)


def h3(n, goal, tunnels):
    direct = manhattan(n, goal)
    best = direct

    for t1, t2 in tunnels.items():
        dist = manhattan(n, t1) + 1 + manhattan(t2, goal)
        best = min(best, dist)

    return best


def a_star(grid, start, goal, heuristic, tunnels):
    open_set = []
    heapq.heappush(open_set, (0, start))

    g_score = {start: 0}
    came_from = {}

    visited = set()
    max_frontier = 1

    start_time = time.time()

    while open_set:
        max_frontier = max(max_frontier, len(open_set))

        _, current = heapq.heappop(open_set)

        if current in visited:
            continue

        visited.add(current)

        if current == goal:
            end_time = time.time()
            return {
                "cost": g_score[current],
                "path": reconstruct_path(came_from, current),
                "visited": len(visited),
                "max_frontier": max_frontier,
                "time": end_time - start_time
            }

        for neighbor in get_neighbors(current, grid, tunnels):
            tentative_g = g_score[current] + cost(neighbor, grid)

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                if heuristic.__name__ == "h3":
                    h = heuristic(neighbor, goal, tunnels)
                else:
                    h = heuristic(neighbor, goal)

                f = tentative_g + h
                heapq.heappush(open_set, (f, neighbor))

    return None


def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def find_positions(grid):
    start = goal = None

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'P':
                start = (i, j)
            elif grid[i][j] == 'D':
                goal = (i, j)

    return start, goal