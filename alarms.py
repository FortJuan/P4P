import csv
import time

def add_timestamp():
    # Get the current time as a Unix timestamp
    current_time_unix = int(time.time())
    
    # Open the CSV file in append mode and add the timestamp to a new line
    with open('hazard_times.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_time_unix])

class AlarmManager:
    def __init__(self, tag_manager):
        # Store active alarms to avoid duplicates (keyed by tag_id and alarm_type)
        self.active_alarms = {}
        self.tag_manager = tag_manager

    def check_proximity(self, tag_a, tag_b, threshold):
        """
        Check if two tags (e.g., cranes or forklifts/operators) are within the proximity threshold.
        """
        x_a, y_a, z_a = tag_a['location']
        x_b, y_b, z_b = tag_b['location']
        distance = ((x_a - x_b) ** 2 + (y_a - y_b) ** 2) ** 0.5  # Hypotenuse (X, Y distance)
        return distance < threshold

    def check_geofence(self, tag, geofence_zones):
        """
        Check if the tag is inside any geofence zones.
        """
        x, y, _ = tag['location']
        for zone in geofence_zones:
            if self.is_within_zone(x, y, zone):
                return True
        return False

    def check_crane_zone(self, tag, cranes):
        """
        Check if the tag is within any crane's circular zone.
        """
        x, y, _ = tag['location']
        for crane in cranes:  # Iterate over list of cranes
            crane_x, crane_y, crane_z = crane['location']
            distance = ((x - crane_x) ** 2 + (y - crane_y) ** 2) ** 0.5
            if distance < crane_z:  # Circle radius is crane's height (z)
                return True
        return False

    def is_within_zone(self, x, y, zone):
        """
        Check if (x, y) is within a quadrilateral zone.
        """
        from matplotlib.path import Path
        polygon = Path(zone)
        return polygon.contains_point((x, y))

    def trigger_alarm(self, tag_id, alarm_type, message):
        """
        Trigger an alarm and avoid duplicate alarms.
        """
        if tag_id not in self.active_alarms:
            self.active_alarms[tag_id] = {}

        if alarm_type not in self.active_alarms[tag_id]:
            # Trigger the alarm for the first time
            self.active_alarms[tag_id][alarm_type] = True
            print(f"ALARM: {message} for {tag_id}")
            # Add code to send the alarm information, e.g., logging or sending notifications
            add_timestamp()
            timestamp = time.time()
            alert_name = alarm_type
            self.tag_manager.add_alert(tag_id, alert_name, message, timestamp)
        return True

    def reset_alarm(self, tag_id, alarm_type):
        """
        Reset the alarm once the condition no longer applies.
        """
        if tag_id in self.active_alarms and alarm_type in self.active_alarms[tag_id]:
            del self.active_alarms[tag_id][alarm_type]

    def check_forklift_operator_proximity(self, tag_a, tag_b):
        """
        Check proximity between a forklift and an operator (3-meter threshold).
        """
        return self.check_proximity(tag_a, tag_b, threshold=3.0)

    def check_crane_proximity(self, crane_a, crane_b):
        """
        Check proximity between two cranes (5-meter threshold).
        """
        return self.check_proximity(crane_a, crane_b, threshold=5.0)

    def run_alarm_checks(self, sequence_name, tags, cranes, geofence_zones):
        """
        Run all relevant alarm checks based on the sequence.
        """
        for tag_id, tag in tags.items():
            tag_type = tag['tag_type']

            # Sequence: Steelmaking Sequence
            if sequence_name == "Steelmaking Sequence":
                if tag_type in ["Operator", "Forklift"]:
                    if self.check_geofence(tag, geofence_zones):
                        self.trigger_alarm(tag_id, "geofence", "Entered geofence zone")
                    if self.check_crane_zone(tag, cranes):
                        self.trigger_alarm(tag_id, "crane_zone", "Entered crane zone")
                    
                    # Check Forklift and Operator proximity (3 meters)
                    for other_tag_id, other_tag in tags.items():
                        if other_tag_id != tag_id and other_tag['tag_type'] == "Operator":
                            if self.check_forklift_operator_proximity(tag, other_tag):
                                self.trigger_alarm(tag_id, "forklift_operator_proximity", 
                                    f"Forklift {tag_id} is too close to Operator {other_tag_id}")

            # Sequence: Tandem Lift (cranes can be close)
            elif sequence_name == "Tandem Lift":
                if tag_type in ["Operator", "Forklift"]:
                    if self.check_geofence(tag, geofence_zones):
                        self.trigger_alarm(tag_id, "geofence", "Entered geofence zone")
                    # No crane proximity alarms

            # Sequence: Bricklayers Lift (operators can be in crane zone)
            elif sequence_name == "Bricklayers Lift":
                if tag_type == "Forklift":
                    if self.check_geofence(tag, geofence_zones):
                        self.trigger_alarm(tag_id, "geofence", "Entered geofence zone")
                    if self.check_crane_zone(tag, cranes):
                        self.trigger_alarm(tag_id, "crane_zone", "Entered crane zone")

        # Check crane proximity if sequence allows (excluding Tandem Lift)
        if sequence_name != "Tandem Lift":
            # Check crane-to-crane proximity (5 meters)
            for i, crane_a in enumerate(cranes):
                for j, crane_b in enumerate(cranes):
                    if i != j and self.check_crane_proximity(crane_a, crane_b):
                        self.trigger_alarm(i, "crane_proximity", "Crane proximity alert")
                        self.trigger_alarm(j, "crane_proximity", "Crane proximity alert")
