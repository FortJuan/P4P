import matplotlib.pyplot as plt
import numpy as np

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
    
    def plot(self, ax, opacity):
        for quadrilateral in self.quadrilaterals:
            poly = plt.Polygon(quadrilateral, closed=True, fill=True, color='blue', alpha=opacity)
            ax.add_patch(poly)
    
class Sequence:
    def __init__(self, name, geofence_coordinates):
        self.name = name
        self.geofence = Geofence(geofence_coordinates)
    
    def plot_geofence(self, ax, opacity):
        self.geofence.plot(ax, opacity)

    def check_hazards(self, tag_data):
        # Placeholder for complex hazard checking logic
        pass

    def add_alert(self, alert_name, alert_message, timestamp):
        # This method would interact with the JSON data structure to add alerts
        alert = {"name": alert_name, "message": alert_message, "timestamp": timestamp}
        # Assuming data is a dictionary loaded from JSON where alerts are stored
        data['alerts'].append(alert)
        # Function to save the updated data back to JSON would be called here

# Example usage
#fig, ax = plt.subplots()
#sequence = Sequence("Steelmaking Sequence", [[(1, 2), (1, 3), (2, 3), (2, 2)], [(3, 4), (3, 5), (4, 5), (4, 4)]])
#sequence.plot_geofence(ax, 0.5)
#plt.show()
