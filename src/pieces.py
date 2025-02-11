import numpy as np
from itertools import product

class PuzzlePiece:
    """Represents a 3D puzzle piece with rotation capabilities."""
    
    def __init__(self, shape, description=""):
        """
        shape: List of (x, y, z) coordinates defining the piece.
        description: A string description of the piece.
        """
        self.shape = np.array(shape)  # Store original shape as a NumPy array
        self.description = description


    def rotate(self, axis, angle):
        """Rotate the piece around the given axis by the specified angle."""
        angle = np.radians(angle)  # Convert degrees to radians
        
        # Rotation matrices for x, y, and z axes
        rotations = {
            'x': np.array([[1, 0, 0],
                           [0, np.cos(angle), -np.sin(angle)],
                           [0, np.sin(angle), np.cos(angle)]]),
            
            'y': np.array([[np.cos(angle), 0, np.sin(angle)],
                           [0, 1, 0],
                           [-np.sin(angle), 0, np.cos(angle)]]),
            
            'z': np.array([[np.cos(angle), -np.sin(angle), 0],
                           [np.sin(angle), np.cos(angle), 0],
                           [0, 0, 1]])
        }
        
        rotation_matrix = rotations[axis]
        rotated_shape = np.dot(self.shape, rotation_matrix.T)  # Rotate each point by using a transposed rotation matrix
        
        # Round to nearest int so the coordinates remain integers
        return PuzzlePiece(
            rotated_shape.round().astype(int).tolist(),
            description = self.description
        )


    def generate_orientations(self):
        """Generate all unique rotations (0, 90, 180, 270 degrees on each axis)."""
        seen = set()
        unique_orientations = []
        
        for angles in product([0, 90, 180, 270], repeat=3):
            piece = self.rotate('x', angles[0]).rotate('y', angles[1]).rotate('z', angles[2])
            
            # Normalize: subtract minimum value so that the smallest coordinate becomes (0,0,0)
            normalized = piece.shape - piece.shape.min(axis=0)
            
            # Create a canonical representation (sorted tuple of tuples)
            canonical = tuple(sorted(map(tuple, normalized)))
            
            if canonical not in seen:
                seen.add(canonical)
                unique_orientations.append(
                    PuzzlePiece(normalized.tolist(), description=self.description)
                )
        
        return unique_orientations


    def get_grid_representation(self):
        """
        Returns a grid representation of the piece.
        
        If all cells share the same z value, a dictionary with a single key is returned.
        If the piece spans exactly 2 distinct z-levels, returns a dictionary with two keys (one for each layer).
        Each grid is a list of lists where 1 indicates an occupied cell and 0 indicates an empty cell.
        Returns None if the piece spans more than 2 layers.
        """
        # Find unique z values
        unique_z = sorted(np.unique(self.shape[:, 2]))
        
        if len(unique_z) == 1:
            layer = unique_z[0]
            mask = self.shape[:, 2] == layer
            coords = self.shape[mask]
            xs = coords[:, 0]
            ys = coords[:, 1]
            min_x, max_x = int(xs.min()), int(xs.max())
            min_y, max_y = int(ys.min()), int(ys.max())
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            grid = [[0 for _ in range(width)] for _ in range(height)]
            
            for x, y, z in coords:
                grid[int(y - min_y)][int(x - min_x)] = 1
            
            return {layer: grid}
        
        elif len(unique_z) == 2:
            grids = {}
            
            for layer in unique_z:
                mask = self.shape[:, 2] == layer
                coords = self.shape[mask]
                xs = coords[:, 0]
                ys = coords[:, 1]
                min_x, max_x = int(xs.min()), int(xs.max())
                min_y, max_y = int(ys.min()), int(ys.max())
                width = max_x - min_x + 1
                height = max_y - min_y + 1
                grid = [[0 for _ in range(width)] for _ in range(height)]
                
                for x, y, z in coords:
                    grid[int(y - min_y)][int(x - min_x)] = 1
                
                grids[layer] = grid
            
            return grids
        
        else:
            return None
