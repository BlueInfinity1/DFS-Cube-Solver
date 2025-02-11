# Cube Puzzle Solver

## Overview

This project is a Depth First Search (DFS)-based solver for a 3D cube puzzle. It uses a combination of randomization and the Minimum Remaining Value (MRV) heuristic to explore placements of puzzle pieces within a cube.

The current configuration in `main.py` is set for a simple 2x2x2 cube, but the same approach can be extended to a 3x3x3 cube (such as the [Soma Cube](https://en.wikipedia.org/wiki/Soma_cube)) or any NxNxN cube, but the performance may suffer with bigger values of N (see the **Performance** section).


## Features
- **3D Puzzle Grid:** Represented using NumPy arrays.
- **Puzzle Pieces with Rotation:** Each piece can generate all unique orientations.
- **DFS with Backtracking and MRV Heuristic:** Candidate moves are evaluated and ordered to prune the search space.
- **Verbose Step-by-Step Debugging:** Optionally prints detailed placement information and grid representations.

## Project Structure
- **puzzle.py:** Contains the `CubePuzzle` class.
- **pieces.py:** Contains the `PuzzlePiece` class and definitions for the puzzle pieces.
- **solver.py:** Contains the `CubeSolver` class which implements the DFS solver with MRV.
- **main.py:** The entry point to run the solver.

## MRV Heuristic

Our heuristic is a straightforward implementation that only considers the remaining available space after placing a piece. For each candidate move (i.e., a specific orientation and placement position for a piece), the solver simulates the placement by marking the corresponding cells in a copy of the puzzle grid and then counts how many cells remain empty. The move that minimizes the number of empty cells is chosen first. This simple approach does not account for factors such as connectivity or the total number of legal moves available for the remaining pieces, but it effectively prunes the search space in many cases.

## Performance

**Worst-case performance:** O(m<sup>n</sup>)

In the worst-case scenario—where there are *n* pieces and each piece has, on average, *m* candidate moves (each representing a combination of orientation and placement)—the DFS solver's running time is exponential, roughly O(m<sup>n</sup>).

While there are more efficient approaches, the DFS approach with our simple MRV heuristic was chosen for the sake of simplicity in this demo.

## Sample Run and Output Images

Below are images demonstrating the various stages of the puzzle:

### 1. All 4 Blocks Used in the Sample Run
![All 4 Blocks](https://drive.google.com/uc?id=1c0QNqezJD66ptHpCg8MiCoiE-e92Wdjb)

### 2. Blocks in the Solution (Separated for Clarity)
![Separated Blocks](https://drive.google.com/uc?id=1GdGfYeFg-tJF6b8zavLwRN40MVjd2xev)

### 3. Blocks Placed Together to Form the Final Solution
![Solution Formation](https://drive.google.com/uc?id=1O_yO-3DtA3PIMRlT3mU-0I9jHaUEGTwB)

## Reading the sample run output (Example output.txt)

For example, the final solution state above can be represented as the following:

```
Current Cube State:
Layer 0:
1 3
1 4

Layer 1:
2 2
4 4
```

The output is printed layer by layer (each layer corresponds to a z-value):

- **Layer 0 (z = 0):**
  - The first row shows "1 3", meaning that the cell at row 0, column 0 contains a unit cube belonging to piece 1, and the cell at row 0, column 1 contains a unit cube belonging to piece 3.
  - The second row shows "1 4", so the cell at row 1, column 0 is occupied by a unit cube belonging to piece 1, and the cell at row 1, column 1 is occupied by a unit cube belonging to piece 4.

- **Layer 1 (z = 1):**
  - The first row "2 2" indicates that both cells in row 0 are occupied by unit cubes belonging to piece 2.
  - The second row "4 4" means that both cells in row 1 are occupied by unit cubes belonging to piece 4.

Here, each non-zero number represents the identifier of a placed piece, while "0" would denote an empty cell.

---
### Interpreting the Orientation Output

For a given piece, the solver lists its unique orientations. Consider the following output for a domino block that consists of 2 unit cubes:

```
Orientation 3: [[0, 0, 0], [0, 0, 1]]
Layer 0:
[1]
Layer 1:
[1]
```

This tells us:

- **Orientation 3:**  
  The piece, when rotated into its third unique orientation, has the unit cube positions at
  (0, 0, 0) and (0, 0, 1).

This means the piece with the given rotation consists of two cubes:
- One cube is at the origin (0, 0, 0).
- The other cube is directly above it (0, 0, 1) along the z-axis.

- **Grid Representation:**  
The solver also prints a grid view for each distinct z-layer:
- **Layer 0:**  
  The grid `[1]` indicates that in layer 0, the piece occupies one cell.
- **Layer 1:**  
  The grid `[1]` shows that in layer 1, the piece also occupies one cell.
  
This visual output confirms that Orientation 3 of the piece places one cube on layer 0 and the other on layer 1, aligned vertically.


---

Overall, these outputs help you verify:
- That each puzzle piece is correctly defined as a set of vectors.
- That the rotation functions are producing the correct unique orientations.
- And that the grid representation accurately reflects how the piece would cover cells in the puzzle when placed.
