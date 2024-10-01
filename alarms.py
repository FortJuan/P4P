class AlarmManager:
    def __init__(self):
        # A dictionary to store active alarms to avoid duplicates (keyed by tag_id)
        self.active_alarms = {}

    def check_in_red_zone(self, tag_id, x, y, red_zones):
        """
        Check if the entity (forklift/operator) is within any red zone.

        Parameters:
        - tag_id (str): Unique identifier for the tag (forklift/operator).
        - x, y (float): The X, Y coordinates of the entity.
        - red_zones (list): List of quadrilaterals defining the red zones.

        Returns:
        - alarm_triggered (bool): Whether an alarm is triggered.
        """
        for zone in red_zones:
            if self.is_within_zone(x, y, zone):
                if tag_id not in self.active_alarms:
                    # Trigger the alarm for the first time
                    self.active_alarms[tag_id] = True
                    return True  # Alarm triggered
                return False  # Already in alarm state, no new alarm
        # If entity is no longer in any red zone, remove from active alarms
        if tag_id in self.active_alarms:
            del self.active_alarms[tag_id]
        return False

    def is_within_zone(self, x, y, zone):
        """
        Check if (x, y) is within the given quadrilateral (zone).
        """
        # Use a point-in-polygon algorithm to check if (x, y) is within the zone
        # Assuming zone is a list of four corner points [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        from matplotlib.path import Path
        polygon = Path(zone)
        return polygon.contains_point((x, y))