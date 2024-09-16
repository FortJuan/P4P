import time

class Tag:
    def __init__(self, tag_type: str, tag_id: str, battery: float, location: tuple, timestamp: float = None):
        """
        Initializes the Tag object with type, ID, battery percentage, location, and timestamp.

        :param tag_type: The type of the tag as a string.
        :param tag_id: The unique identifier for the tag as a string.
        :param battery: The battery percentage of the tag, a value from 0 to 100.
        :param location: The latest location of the tag as a tuple (X, Y, Z).
        :param timestamp: The Unix timestamp of the last update. If not provided, sets to current time.
        """
        self.tag_type = tag_type
        self.tag_id = tag_id
        self.battery = battery
        self.location = location
        self.timestamp = timestamp if timestamp is not None else time.time()
    
    # Getters
    def get_tag_type(self):
        return self.tag_type
    
    def get_tag_id(self):
        return self.tag_id
    
    def get_battery(self):
        return self.battery
    
    def get_location(self):
        return self.location
    
    def get_timestamp(self):
        return self.timestamp
    
    # Setters
    def set_tag_type(self, new_type: str):
        self.tag_type = new_type
    
    def set_tag_id(self, new_id: str):
        self.tag_id = new_id
    
    def set_battery(self, new_battery: float):
        if 0 <= new_battery <= 100:
            self.battery = new_battery
        else:
            raise ValueError("Battery percentage must be between 0 and 100.")
    
    def set_location(self, new_location: tuple):
        if len(new_location) == 3:
            self.location = new_location
        else:
            raise ValueError("Location must be a tuple of three coordinates (X, Y, Z).")
    
    def set_timestamp(self, new_timestamp: float):
        self.timestamp = new_timestamp

# Example usage
#tag = Tag("RFID", "001AFC", 85.5, (10, 20, 5))
#print(tag.get_location())  # Outputs: (10, 20, 5)
#tag.set_battery(90)
#print(tag.get_battery())  # Outputs: 90