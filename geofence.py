class Geofence:
    def __init__(self, name: str, quadrilaterals: list, background_image: str):
        """
        Initialize the Geofence with a name, list of quadrilateral coordinates, and background image path.
        
        :param name: Name of the geofence.
        :param quadrilaterals: List of quadrilaterals, where each quadrilateral is a list of four (x, y) tuples.
        :param background_image: Path to the background image.
        """
        self.name = name
        self.quadrilaterals = quadrilaterals
        self.background_image = background_image

        # Validate the provided quadrilaterals
        self.validate_quadrilaterals()

    def validate_quadrilaterals(self):
        """
        Validates that each quadrilateral in the list is a valid quadrilateral.
        A valid quadrilateral should have exactly 4 points, and the points should not be collinear.
        """
        for quadrilateral in self.quadrilaterals:
            if len(quadrilateral) != 4:
                raise ValueError(f"Quadrilateral {quadrilateral} does not have exactly 4 points.")
            if not self.is_valid_quadrilateral(quadrilateral):
                raise ValueError(f"Quadrilateral {quadrilateral} is not valid.")

    def is_valid_quadrilateral(self, quadrilateral: list) -> bool:
        """
        Checks if the given quadrilateral is valid by ensuring that no three points are collinear.
        
        :param quadrilateral: A list of four (x, y) tuples.
        :return: True if valid, False otherwise.
        """
        def area(p1, p2, p3):
            return abs(p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))

        # Ensure no three consecutive points are collinear (area should not be zero)
        for i in range(4):
            p1 = quadrilateral[i]
            p2 = quadrilateral[(i + 1) % 4]
            p3 = quadrilateral[(i + 2) % 4]
            if area(p1, p2, p3) == 0:
                return False

        return True

# Example usage:
# geofence = Geofence("Test Zone", [[(1, 2), (1, 3), (2, 3), (2, 2)], [(3, 4), (3, 5), (4, 5), (4, 4)]], "path/to/image.png")
