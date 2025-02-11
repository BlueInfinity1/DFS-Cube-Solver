import numpy as np
import random


class CubeSolver:
    """DFS-based solver for the cube puzzle with MRV heuristic and step-by-step printing."""
    
    def __init__(self, puzzle, pieces, verbose=False, require_input=True):
        self.puzzle = puzzle
        
        self.pieces = pieces  # List of available pieces
        
        self.verbose = verbose
        
        self.require_input_to_proceed = require_input


    def solve(self):
        """Starts the DFS search to place all pieces."""
        return self.dfs(0)


    def dfs(self, index):
        """Recursive DFS solver with backtracking."""
        if index == len(self.pieces):  # All pieces placed
            return True
        
        piece = self.pieces[index]
        
        orientations = piece.generate_orientations()
        
        if self.verbose:
            print(f"\nProcessing Piece {index+1}: {piece.description}")
            print(f"Unique orientations available: {len(orientations)}")
            
            for i, orient in enumerate(orientations):
                print(f"Orientation {i+1}: {orient.shape.tolist()}")
                
                grid_repr = orient.get_grid_representation()
                if grid_repr is not None:
                    for layer, grid in grid_repr.items():
                        print(f"Layer {layer}:")
                        for row in grid:
                            print(row)
        
        random.shuffle(orientations)  # Randomize orientation order
        
        # MRV: Generate all possible positions and sort them based on an estimated cost
        positions = [
            (x, y, z)
            for x in range(self.puzzle.size[0])
            for y in range(self.puzzle.size[1])
            for z in range(self.puzzle.size[2])
        ]
        
        positions.sort(key=lambda pos: self.estimate_empty_space(pos, piece))
        
        for orientation in orientations:
            for position in positions:
                if self.puzzle.fits(orientation, position):
                    
                    # Place the piece with an identifier (using index + 1)
                    self.puzzle.place_piece(orientation, position, index + 1)
                    
                    if self.verbose:
                        print(f"\nPlaced piece {index+1} at position {position} using orientation: {orientation.shape.tolist()}")
                        
                        grid_repr = orientation.get_grid_representation()
                        if grid_repr is not None:
                            for layer, grid in grid_repr.items():
                                print(f"Layer {layer}:")
                                for row in grid:
                                    print(row)
                        
                        self.puzzle.print_grid()
                        
                        if self.require_input_to_proceed:
                            input("Press Enter to continue...")
                    
                    if self.dfs(index + 1):
                        return True  # Found a complete solution
                    
                    # Backtrack: remove the piece and print the state
                    self.puzzle.remove_piece(orientation, position)
                    
                    if self.verbose:
                        print(f"\nRemoved piece {index+1} from position {position} (Backtracking)")
                        self.puzzle.print_grid()
                        
                        if self.require_input_to_proceed:
                            input("Press Enter to continue...")
        
        return False  # No solution found from this configuration


    def estimate_empty_space(self, pos, piece):
        """
        Estimate remaining empty spaces if the piece is placed at pos.
        Fewer empty spaces means the piece is placed in a more constrained location.
        """
        temp_grid = self.puzzle.grid.copy()
        
        for x, y, z in piece.shape:
            px, py, pz = x + pos[0], y + pos[1], z + pos[2]
            
            if 0 <= px < self.puzzle.size[0] and 0 <= py < self.puzzle.size[1] and 0 <= pz < self.puzzle.size[2]:
                temp_grid[px, py, pz] = 1
        
        return np.sum(temp_grid == 0)  # Count how many cells remain empty
