# Data Center Cooling Infrastructure

We are managing a data center grid layout. The data center is modeled as an M * N matrix of server racks.

Some grids have highly efficient Cooling Intake Units (represented by a positive integer indicating their cooling capacity), some grids are standard Server Racks (represented by 0), and some grids are Structural Pillars (represented by -1), through which no cooling air or traffic can pass.

The Rules of Airflow:

- Cooling air can only flow between adjacent cells (Up, Down, Left, Right). It cannot move diagonally.
- As cooling air travels away from a Cooling Intake Unit, its capacity drops by exactly 1 unit for every step it takes.
- If air with a cooling capacity of $C$ moves to an adjacent cell, the capacity of the air entering that neighbor becomes $C - 1$.
- A standard server rack (0) can receive air from multiple directions, but it will naturally lock onto the maximum available cooling capacity that can reach it.

Task: Write a function that takes this M * N grid and updates all the standard server racks (0) with the maximum cooling capacity they can receive. If a server rack cannot be reached by any cooling intake unit because it's blocked by pillars, its value should remain 0.

Example Input:

```
grid = [
    [ 0,  -1,  3],
    [ 0,   0,  0],
    [ 0,  -1,  0]
]
```

Example Output:

```
[
    [ 0,  -1,  3],
    [ 0,   1,  2],
    [ 0,  -1,  1]
]
```
---

## Approach

To solve this problem, we can use a breadth-first search (BFS) approach starting from all the cooling intake units simultaneously.

### Data Structures:

- A queue to manage the BFS traversal.
- A result grid initialized with the same dimensions as the input grid, where we will store the maximum cooling capacity for each cell.

### Algorithm

- Initialize the queue with all the cooling intake units (positive integers) and their positions.
- For each cooling intake unit, enqueue its position and its cooling capacity.
- While the queue is not empty:
  - Dequeue the front element, which gives us the current position and the cooling capacity.
  - For each of the four possible directions (up, down, left, right):
    - Calculate the new position.
    - Check if the new position is within bounds and not a pillar (-1).
    - If the new position is a standard server rack (0) or has a lower cooling capacity as depicted in the result grid, update the result grid with the new cooling capacity (current capacity - 1) and enqueue the new position with the updated cooling capacity.

- Continue this process until the queue is empty. The result grid will then contain the maximum cooling capacity for each standard server rack.