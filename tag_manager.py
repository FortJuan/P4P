import json
import threading
import time
from pathlib import Path

class TagManager:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.data = self.load_data()
        self.lock = threading.Lock()
        self.last_save_time = time.time()
        if not self.file_path.exists():
            self.save_data()  # Ensure the file is created if it doesn't exist

    def load_data(self):
        if self.file_path.exists() and self.file_path.stat().st_size > 0:
            with open(self.file_path, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {"settings": {}, "tags": {}, "alerts": []}  # Return an empty dictionary if JSON is corrupted
        else:
            return {"settings": {}, "tags": {}, "alerts": []}

    def save_data(self):
        with self.lock:
            try:
                with open(self.file_path, 'w') as file:
                    json.dump(self.data, file, indent=4)
            except Exception as e:
                print(f"Failed to save data: {e}")

    def add_or_update_tag(self, tag):
        #with self.lock: # Temporarily comment out - might be so temporary
            self.data['tags'][tag.get_tag_id()] = {
                'tag_type': tag.get_tag_type(),
                'battery': tag.get_battery(),
                'location': tag.get_location(),
                'timestamp': tag.get_timestamp()
            }
            # Force immediate save for testing
            self.save_data()
            #current_time = time.time()
            #if current_time - self.last_save_time >= 0.1:
            #    self.save_data()
            #    self.last_save_time = current_time
            
    def update_settings(self, selected_data_set=None, selected_sequence=None):
        if selected_data_set is not None:
            self.data['settings']['selected_data_set'] = selected_data_set
        if selected_sequence is not None:
            self.data['settings']['selected_sequence'] = selected_sequence
        self.save_data()
    
    def get_tag_type(self, serial_number):
        """Retrieve the tag type for a given serial number."""
        return self.data['tags'].get(serial_number, {}).get('tag_type', None)
    
    def add_alert(self, alert_name, alert_message, timestamp):
        #with self.lock:
            # Ensure 'alerts' key exists
            if 'alerts' not in self.data:
                self.data['alerts'] = []
            self.data['alerts'].append({
                "name": alert_name,
                "message": alert_message,
                "timestamp": timestamp
            })
            self.purge_old_alerts()
            self.save_data()
    
    def purge_old_alerts(self):
        # Sort the alerts by timestamp in descending order
        self.data['alerts'].sort(key=lambda x: x['timestamp'], reverse=True)
        # Keep only the 10 most recent
        self.data['alerts'] = self.data['alerts'][:10]

    def remove_alerts(self):
        #with self.lock:
            self.data['alerts'] = []
            self.save_data()