class AlarmManager:
    def __init__(self):
        # Nested dictionary to store active alarms (keyed by tag_id and alarm_type)
        self.active_alarms = {}

    def check_in_red_zone(self, tag_id, x, y, red_zones):
        """
        Check if the entity (forklift/operator) is within any red zone.
        """
        for zone in red_zones:
            if self.is_within_zone(x, y, zone):
                return self.trigger_alarm(tag_id, "proximity", red_zone=True)
        return self.reset_alarm(tag_id, "proximity")

    def check_crane_proximity(self, crane_a, crane_b):
        """
        Check if two cranes are too close to each other (e.g., within a certain distance).
        """
        x_a, y_a, z_a = crane_a['coordinates']
        x_b, y_b, z_b = crane_b['coordinates']
        proximity_threshold = 10.0  # Define your proximity threshold here
        
        distance = ((x_a - x_b) ** 2 + (y_a - y_b) ** 2) ** 0.5
        if distance < proximity_threshold:
            return self.trigger_alarm(crane_a['id'], "crane_proximity"), self.trigger_alarm(crane_b['id'], "crane_proximity")
        return self.reset_alarm(crane_a['id'], "crane_proximity"), self.reset_alarm(crane_b['id'], "crane_proximity")

    def check_geofence_alarm(self, tag_id, x, y, geofence_zones):
        """
        Check if the entity is violating a geofence boundary.
        """
        for zone in geofence_zones:
            if self.is_within_zone(x, y, zone):
                return self.trigger_alarm(tag_id, "geofence", geofence=True)
        return self.reset_alarm(tag_id, "geofence")

    def is_within_zone(self, x, y, zone):
        """
        Check if (x, y) is within the given zone, which can be either a polygon (list of points)
        or a circle (defined by center and radius).
    
        Parameters:
        - x, y (float): Coordinates of the point to check.
        - zone (tuple or list): The zone can either be:
        1. A list of polygon vertices [(x1, y1), (x2, y2), ...]
        2. A tuple representing a circle (center_x, center_y, radius)
    
        Returns:
        - bool: True if the point is within the zone, False otherwise.
        """
        # Case 1: If the zone is a polygon (list of points)
        if isinstance(zone, list):
            from matplotlib.path import Path
            polygon = Path(zone)
            return polygon.contains_point((x, y))

        # Case 2: If the zone is a circle (tuple with center and radius)
        elif isinstance(zone, tuple) and len(zone) == 3:
            center_x, center_y, radius = zone
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            return distance <= radius

        return False

    def trigger_alarm(self, tag_id, alarm_type, **kwargs):
        """
        Trigger an alarm if it hasn't already been triggered.
        """
        if tag_id not in self.active_alarms:
            self.active_alarms[tag_id] = {}

        if alarm_type not in self.active_alarms[tag_id]:
            # Alarm triggered for the first time
            self.active_alarms[tag_id][alarm_type] = True
            print(f"Alarm triggered: {alarm_type} for tag: {tag_id}")
            return True
        return False  # Alarm was already active

    def reset_alarm(self, tag_id, alarm_type):
        """
        Reset the alarm if it was previously active.
        """
        if tag_id in self.active_alarms and alarm_type in self.active_alarms[tag_id]:
            del self.active_alarms[tag_id][alarm_type]
            print(f"Alarm reset: {alarm_type} for tag: {tag_id}")
            return True
        return False