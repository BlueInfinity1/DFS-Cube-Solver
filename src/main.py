from puzzle import CubePuzzle
from pieces import PuzzlePiece
from solver import CubeSolver

# Define puzzle size (a 2x2x2 cube)
puzzle = CubePuzzle((2, 2, 2))

# Define pieces for the 2x2x2 puzzle.
# Total cells needed: 8.
# We'll use:
# - Piece A: L-shaped 3-cube piece.
# - Piece B: Domino (2 cubes) along the z-axis.
# - Piece C: Domino (2 cubes) along the y-axis.
# - Piece D: Single cube.
#
# When placed correctly, these pieces cover:
# Piece A: 3 cells
# Piece B: 2 cells
# Piece C: 2 cells
# Piece D: 1 cell
# Total: 3 + 2 + 2 + 1 = 8

# The order of the pieces can be freely changed, and this can strongly affect how the search process unfolds.
# Since the 2x2x2 puzzle is simple, certain piece configurations will often result in trivial solutions (i.e. includes no backtracking, just placing 4 pieces).

pieces = [    
    # Piece B: Domino along the z-axis
    PuzzlePiece([
        (1, 1, 0),
        (1, 1, 1)
    ], description="Piece B: Domino along the z-axis"),
    
    # Piece C: Domino along the y-axis
    PuzzlePiece([
        (0, 0, 1),
        (0, 1, 1)
    ], description="Piece C: Domino along the y-axis"),
    
    # Piece D: Single cube
    PuzzlePiece([
        (1, 0, 1)
    ], description="Piece D: Single cube"),

    # Piece A: L-shaped 3-cube piece
    PuzzlePiece([
        (0, 0, 0),
        (1, 0, 0),
        (0, 1, 0)
    ], description="Piece A: L-shaped 3-cube piece"),
]

# Instantiate the solver in verbose mode without requiring input to proceed
solver = CubeSolver(puzzle, pieces, verbose=True, require_input=False)

if solver.solve():
    print("Solution found!")
    puzzle.print_grid()
else:
    print("No solution found.")
