from datetime import datetime
import matplotlib.colors as mcolors

class Tag:
    """A class to represent a tag with serial number, coordinates, name, and color."""

    def __init__(self, serial_number, name=None, color=None):
        """
        Initialize a new tag.
        
        Args:
        serial_number (str): Unique identifier for the tag.
        name (str): Human-readable name for the tag.
        color (str): Color name for plotting the tag.
        """
        self.serial_number = serial_number
        self.name = name
        self.color = color
        self.x = None
        self.y = None
        self.z = None
        self.last_ping = None

    def update_coordinates(self, x, y, z, timestamp):
        """
        Update the tag's coordinates and timestamp.
        
        Args:
        x (float): X coordinate.
        y (float): Y coordinate.
        z (float): Z coordinate.
        timestamp (float): Unix timestamp of the last ping.
        """
        self.x = x
        self.y = y
        self.z = z
        self.last_ping = datetime.fromtimestamp(timestamp)

# Example of pre-initialized tag
predefined_tags = {
    "0x000EBC": Tag("0x000EBC", "Crane", "blue")  # Predefined tag
}