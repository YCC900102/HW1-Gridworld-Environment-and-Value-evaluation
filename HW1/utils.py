import numpy as np

ACTIONS = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)
}

ACTION_SYMBOL = {
    'U': '↑',
    'D': '↓',
    'L': '←',
    'R': '→'
}

def in_grid(x, y, size):
    return 0 <= x < size and 0 <= y < size

def evaluate_policy(grid_size, start, end, obstacles, gamma=0.9, theta=1e-4):
    V = np.zeros((grid_size, grid_size))
    policy = np.full((grid_size, grid_size), ' ', dtype=str)

    # Convert obstacle list to set for fast lookup
    obstacle_set = set(map(tuple, obstacles))

    def is_terminal(i, j):
        return (i, j) == tuple(end)

    def is_obstacle(i, j):
        return (i, j) in obstacle_set

    while True:
        delta = 0
        for i in range(grid_size):
            for j in range(grid_size):
                if is_terminal(i, j) or is_obstacle(i, j):
                    continue
                v = V[i, j]
                new_v = 0
                for action in ACTIONS:
                    dx, dy = ACTIONS[action]
                    ni, nj = i + dx, j + dy
                    if not in_grid(ni, nj, grid_size) or is_obstacle(ni, nj):
                        ni, nj = i, j  # stay if hit wall or obstacle
                    reward = 0 if (ni, nj) == tuple(end) else -1
                    new_v += 0.25 * (reward + gamma * V[ni, nj])
                V[i, j] = new_v
                delta = max(delta, abs(v - V[i, j]))
        if delta < theta:
            break

    # Build greedy policy
    for i in range(grid_size):
        for j in range(grid_size):
            if is_terminal(i, j):
                policy[i, j] = 'G'
            elif is_obstacle(i, j):
                policy[i, j] = 'X'
            else:
                best_action = None
                best_value = float('-inf')
                for action, (dx, dy) in ACTIONS.items():
                    ni, nj = i + dx, j + dy
                    if not in_grid(ni, nj, grid_size) or is_obstacle(ni, nj):
                        ni, nj = i, j
                    reward = 0 if (ni, nj) == tuple(end) else -1
                    value = reward + gamma * V[ni, nj]
                    if value > best_value:
                        best_value = value
                        best_action = action
                policy[i, j] = ACTION_SYMBOL[best_action]
    return V, policy
