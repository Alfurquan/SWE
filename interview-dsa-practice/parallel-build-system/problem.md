# The Parallel Build System
We are designing the core engine for a distributed build system (similar to Bazel or Make). You are given a set of software packages that need to be compiled.

Each package takes a specific amount of time to build. However, some packages depend on others. A package can only start building once all of its dependencies have completely finished building.

Because we are running this in a massive datacenter, assume we have an unlimited number of build servers. This means any packages that have their dependencies met can be built simultaneously in parallel.

Task: Write a function that takes the build times and the dependency rules, and returns the minimum total time required to successfully build all the packages. If it is impossible to build all packages, return -1.

Input Format:
You will receive a dictionary mapping package names (strings) to a tuple containing two elements:

- An integer representing the build_time for that package.

- A list of strings representing the dependencies (packages that must be built before this package can start).

Example Input:
```python
packages = {
    "TaskA": (10, ["TaskB", "TaskC"]),
    "TaskB": (5, ["TaskD"]),
    "TaskC": (20, ["TaskD"]),
    "TaskD": (8, [])
}
```

Example Output:
```
28
```

## Approach:

To solve this problem, we can use a topological sorting approach to calculate the minimum time required to build all packages. Here's a step-by-step outline of the approach:

1. **Build a Graph**: Create a directed graph where each package is a node, and there is a directed edge from package A to package B if package B depends on package A. This will help us visualize the dependencies between packages.

2. **Calculate In-Degrees**: For each package, calculate the in-degree (number of dependencies) and store it in a dictionary.

3. **Initialize a Queue**: Use a queue to keep track of packages that have no dependencies (in-degree of 0). These packages can be built immediately.

4. **Initialize a max_time Dictionary**: Create a dictionary to keep track of the maximum time required to build each package, initialized to 0.

5. **Initialize max completion time variable**: We will also maintain a variable to keep track of the maximum completion time across all packages.

6. **Process the Queue**: While the queue is not empty:
   - Dequeue a package.
   - Update the total time by adding the build time of the dequeued package.
   - For each dependent package (packages that depend on the dequeued package):
     - Decrease the in-degree of the dependent package by 1.
     - Update the maximum time for the dependent package to be the maximum of its current max time and the total time after building the dequeued package.
     - Update the overall maximum completion time if the dependent package's max time is greater than the current maximum completion time.
     - If the in-degree of the dependent package becomes 0, enqueue it.

7. **Check for Cycles**: After processing the queue, if there are still packages with non-zero in-degrees, it means there is a cycle in the dependencies, and it's impossible to build all packages. In this case, return -1. Else, return the maximum completion time.