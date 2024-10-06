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
            #add_timestamp()
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
            self.tag_manager.remove_alert(tag_id, alarm_type)

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
        for tag_id, tag in tags.items():
            tag_type = tag['tag_type']
            currently_in_geofence = self.check_geofence(tag, geofence_zones)
            currently_in_crane_zone = self.check_crane_zone(tag, cranes)

            # Proximity checks for all sequences
            for other_tag_id, other_tag in tags.items():
                if other_tag_id != tag_id and other_tag['tag_type'] == "Operator" and tag_type == "Forklift":
                    close_to_operator = self.check_forklift_operator_proximity(tag, other_tag)
                    if close_to_operator:
                        self.trigger_alarm(tag_id, "forklift_operator_proximity", 
                                           f"{tag_type} {tag_id} is too close to Operator {other_tag_id}")
                    else:
                        self.reset_alarm(tag_id, "forklift_operator_proximity")

            # Alarm checks for geofence and crane zones
            if tag_type in ["Operator", "Forklift"]:
                if currently_in_geofence:
                    self.trigger_alarm(tag_id, "geofence", "Entered geofence zone")
                else:
                    self.reset_alarm(tag_id, "geofence")

                if sequence_name != "Bricklayers Lift":  # Exclude Bricklayers Lift from crane zone checks
                    if currently_in_crane_zone:
                        self.trigger_alarm(tag_id, "crane_zone", "Entered crane zone")
                    else:
                        self.reset_alarm(tag_id, "crane_zone")

        # Crane-to-crane proximity checks
        if sequence_name != "Tandem Lift":
            for i, crane_a in enumerate(cranes):
                for j, crane_b in enumerate(cranes):
                    if i != j:
                        close_to_another_crane = self.check_crane_proximity(crane_a, crane_b)
                        if close_to_another_crane:
                            self.trigger_alarm(i, "crane_proximity", "Crane proximity alert")
                            self.trigger_alarm(j, "crane_proximity", "Crane proximity alert")
                        else:
                            self.reset_alarm(i, "crane_proximity")
                            self.reset_alarm(j, "crane_proximity")


