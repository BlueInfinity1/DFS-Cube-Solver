import numpy as np


class CubePuzzle:
    """Represents the 3D puzzle grid."""
    
    def __init__(self, size):
        """
        size: (x, y, z) dimensions of the puzzle cube.
        """
        self.size = size
        
        # Initialize grid with 0's, meaning "empty"
        self.grid = np.zeros(size, dtype=int)
    
    
    def fits(self, piece, position):
        """
        Check if a piece can be placed at the given position without overlap.
        """
        for x, y, z in piece.shape:
            px, py, pz = x + position[0], y + position[1], z + position[2]
            
            # Check out-of-bounds
            if px < 0 or px >= self.size[0] or \
               py < 0 or py >= self.size[1] or \
               pz < 0 or pz >= self.size[2]:
                return False
            
            # Check if already occupied
            if self.grid[px, py, pz] != 0:
                return False
        
        return True
    
    
    def place_piece(self, piece, position, piece_id):
        """Place a piece on the grid using piece_id."""
        for x, y, z in piece.shape:
            px, py, pz = x + position[0], y + position[1], z + position[2]
            self.grid[px, py, pz] = piece_id  # Mark the cell with the piece's ID
    
    
    def remove_piece(self, piece, position):
        """Remove a piece from the grid (for backtracking)."""
        for x, y, z in piece.shape:
            px, py, pz = x + position[0], y + position[1], z + position[2]
            self.grid[px, py, pz] = 0  # Reset to empty
    
    
    def print_grid(self):
        """Print the cube state layer by layer (along the z-axis)."""
        print("\nCurrent Cube State:")
        
        for z in range(self.size[2]):
            print(f"Layer {z}:")
            
            for x in range(self.size[0]):
                # Create a row from the y-values
                row = " ".join(str(self.grid[x, y, z]) for y in range(self.size[1]))
                print(row)
            
            print("")  # Blank line between layers
