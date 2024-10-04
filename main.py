from plot_coordinates import get_sequence_data  # Import the function from plot_coordinates.py
from alarms import AlarmManager
from video_maker import VideoWriterState, release_video_writer
import json
import os

# Define the video parameters
output_file = "output_video.mp4"
if os.path.exists(output_file):
    os.remove(output_file)  # Delete the existing video file


codec = 'mp4v'  # Codec, e.g., 'mp4v' or 'XVID'
fps = 30        # Frames per second
frame_size = (640, 480)  # Example frame size, should match plot size

# Initialize VideoWriterState
video_writer_state = VideoWriterState(output_file, codec, fps, frame_size)
video_writer_state.initialize_writer()  # Initialize the writer before use


def check_dependencies():
    """
    Checks if all required dependencies are installed.
    Prints an error message and exits if any dependency is missing.
    """
    import sys
    import subprocess

    required_modules = ['csv', 'matplotlib']  # List all required modules here

    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            print(f"Module '{module}' is not installed.")
            print("Attempting to install the missing modules...")
            try:
                # Attempt to install the missing module
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
            except Exception as e:
                print(f"Failed to install '{module}'. Please install it manually. Error: {e}")
                sys.exit(1)  # Exit if installation fails

def getFullSequenceData(data_json_path, sequence_json_path):
    """
    Extracts the sequence name, tags, cranes, and geofence zones by reading from data.json and sequence_data.json.

    Parameters:
    - data_json_path (str): Path to the data.json file.
    - sequence_json_path (str): Path to the sequence_data.json file.

    Returns:
    - sequence_name (str): The selected sequence.
    - tags (dict): A dictionary of all tags from data.json.
    - cranes (list): A list of crane tags (filtered from tags).
    - geofence_zones (list): A list of quadrilateral zones from sequence_data.json for the selected sequence.
    """
    
    # Load data.json
    with open(data_json_path, 'r') as data_file:
        data = json.load(data_file)
    
    # Extract sequence name and tags from data.json
    sequence_name = data['settings']['selected_sequence']
    tags = data['tags']

    # Filter out crane tags (where tag_type is "Crane")
    cranes = [tag_info for tag_info in tags.values() if tag_info['tag_type'] == "Crane"]

    # Load sequence_data.json
    with open(sequence_json_path, 'r') as sequence_file:
        sequence_data = json.load(sequence_file)

    # Extract geofence zones for the selected sequence
    geofence_zones = sequence_data['sequence'].get(sequence_name, {}).get('quadrilaterals', [])

    return sequence_name, tags, cranes, geofence_zones

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def remove_row_by_index(coordinate_data, index):
    """
    Removes a row from the coordinate data at the specified index.

    Args:
    coordinate_data (list of lists): The matrix containing the coordinate data.
    index (int): The index of the row to be removed.
    """
    if index < len(coordinate_data):
        del coordinate_data[index]  # or coordinate_data.pop(index)
    else:
        print("Index out of range")

    
def getCoordinateBounds(coordinate_data):
    """
    Calculates the minimum and maximum bounds for X, Y, and Z coordinates 
    from a given matrix of coordinate data.

    Args:
    coordinate_data (list of lists): A matrix where each row contains data in the order:
                                     [Sequence Number, Tag Serial Number, Position X, Position Y, Position Z, Information String, Calculation Timestamp]

    Returns:
    tuple: A tuple containing the minimum and maximum values for X, Y, and Z coordinates:
           (xLow, xHigh, yLow, yHigh, zLow, zHigh)
    """
    # Initialize min and max bounds for X, Y, Z with None
    xLow, xHigh = None, None
    yLow, yHigh = None, None
    zLow, zHigh = None, None

    # Iterate through the coordinate data
    for row in coordinate_data:
        try:
            # Extract X, Y, Z coordinates as floats
            x = float(row[2])
            y = float(row[3])
            z = float(row[4])

            # Update X bounds
            if xLow is None or x < xLow:
                xLow = x
            if xHigh is None or x > xHigh:
                xHigh = x

            # Update Y bounds
            if yLow is None or y < yLow:
                yLow = y
            if yHigh is None or y > yHigh:
                yHigh = y

            # Update Z bounds
            if zLow is None or z < zLow:
                zLow = z
            if zHigh is None or z > zHigh:
                zHigh = z

        except ValueError:
            # Ignore the row if coordinates are not valid floats
            continue

    # Return the bounds as a tuple
    return xLow, xHigh, yLow, yHigh, zLow, zHigh

def stretchData(coordinateData, previous_range, new_range):
    """
    Rescales the X, Y, Z coordinates in coordinateData based on the given ranges.

    Args:
    coordinateData (list of lists): The coordinate data to be rescaled.
                                    Format: [Sequence Number, Tag Serial Number, Position X, Position Y, Position Z, Information String, Calculation Timestamp]
    previous_range (tuple): A 6-tuple with the previous min/max of X, Y, Z coordinates in the form: 
                            (X_min, X_max, Y_min, Y_max, Z_min, Z_max).
    new_range (tuple): A 6-tuple with the new min/max of X, Y, Z coordinates in the form: 
                       (X_min, X_max, Y_min, Y_max, Z_min, Z_max).

    Returns:
    list of lists: A new list with rescaled coordinate data.
    """
    
    def rescale(value, old_min, old_max, new_min, new_max):
        """Rescale a value from one range to another."""
        if old_max - old_min == 0:
            return value  # Avoid division by zero, return the same value if the old range is zero
        return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    
    # Unpack previous and new ranges for readability
    prev_x_min, prev_x_max, prev_y_min, prev_y_max, prev_z_min, prev_z_max = previous_range
    new_x_min, new_x_max, new_y_min, new_y_max, new_z_min, new_z_max = new_range

    # Initialize the new list for stretched data
    stretchedCoordinateData = []

    for row in coordinateData:
        try:
            # Extract X, Y, Z and convert them to floats
            x = float(row[2])
            y = float(row[3])
            z = float(row[4])

            # Rescale each coordinate
            new_x = rescale(x, prev_x_min, prev_x_max, new_x_min, new_x_max)
            new_y = rescale(y, prev_y_min, prev_y_max, new_y_min, new_y_max)
            new_z = rescale(z, prev_z_min, prev_z_max, new_z_min, new_z_max)

            # Append the updated row to the new dataset with the rescaled X, Y, Z
            stretchedCoordinateData.append([
                row[0],  # Sequence Number
                row[1],  # Tag Serial Number
                new_x,   # Rescaled Position X
                new_y,   # Rescaled Position Y
                new_z,   # Rescaled Position Z
                row[5],  # Information String
                row[6]   # Calculation Timestamp
            ])

        except (ValueError, IndexError):
            # Skip rows where X, Y, Z are not valid (either missing or non-numeric)
            continue

    return stretchedCoordinateData

def main():
    # Check for dependencies
    check_dependencies()

    # Import the required function after checking dependencies
    from coordinate_extractor import getCoordinateData
    from plot_coordinates import plot_coordinates
    from datetime import datetime
    import time
    from tag import Tag
    from tag_manager import TagManager
    from velocity import exportVelocity
    import os

    # Load the sequence data from the JSON file
    file_path = os.path.join(os.getcwd(), "sequence_data.json")  # Path to your JSON file
    sequence_data = load_json_data(file_path)

    # Select the dataset and sequence (change these values to your actual selection)
    selected_data_set = "Dataset 1"  # You can dynamically select this based on user input or logic
    selected_sequence = "Steelmaking Sequence"  # Example sequence name

    dataset_path, quadrilaterals, colour = get_sequence_data(sequence_data, selected_sequence, selected_data_set)

    
    
    # Define the path to the log file
    #log_file_path = r"C:\Users\juani\OneDrive\Desktop\MECHENG700\code\coord_log (1).log" # change depending on log file path
    log_file_path = os.path.join(os.getcwd(), dataset_path)
    # Call the function to get the coordinate data
    print(log_file_path)

    # Initialize the Alarm Manager
    alarm_manager = AlarmManager()
    
    # Add current JSON data
    tag_manager = TagManager('data.json')
    
    # Update settings if needed
    tag_manager.update_settings(selected_data_set="Dataset 2", selected_sequence="Steelmaking Sequence")

    # Load updated settings
    selected_data_set = tag_manager.data['settings'].get('selected_data_set', 'Default Dataset')
    selected_sequence = tag_manager.data['settings'].get('selected_sequence', 'Default Sequence')
    print(f"Loaded settings: DataSet - {selected_data_set}, Sequence - {selected_sequence}")

    coordinate_data = getCoordinateData(log_file_path)
    
    previous_range = getCoordinateBounds(coordinate_data)
    
    new_range = 0.00,74.25,0.00,34.20,0.50,7.15
    
    coordinate_data = stretchData(coordinate_data,previous_range,new_range)
    
    csv_output_path = os.path.join(os.getcwd(), "velocity_dataset_5.csv")
    exportVelocity(coordinate_data, csv_output_path)
    
#xLow, xHigh, yLow, yHigh, zLow, zHigh
    """
    # Define the bounds for the graph
    xLow = 18.00
    xHigh = 25.00
    yLow = 2.00
    yHigh = 6.00
    zLow = 0.75
    zHigh = 1.50
    """
    xLow, xHigh, yLow, yHigh, zLow, zHigh = getCoordinateBounds(coordinate_data)
    print(xLow, xHigh, yLow, yHigh, zLow, zHigh)
    
    #print(coordinate_data)
    

    # Create Tag instances
    tag1 = Tag("Forklift", "0x000EBC", 85.5, (10, 20, 5), coordinate_data[0][6])
    tag3 = Tag("Operator", "0x001A2C", 75.3, (20, 30, 5), coordinate_data[0][6])
    tag2 = Tag("Crane", "0x001A79", 90.0, (15, 25, 5), coordinate_data[1][6])
    

    print("\nI addded a path\n")

    tag_manager.remove_tags()
    # Add tags to the manager (and save to JSON)
    tag_manager.add_or_update_tag(tag1)
    tag_manager.add_or_update_tag(tag2)
    tag_manager.add_or_update_tag(tag3)
    
    tag_manager.remove_alerts()
    tag_manager.add_alert("Hazard Alert", "Forklift entered restricted zone", "2024-05-02T16:04:03Z")
    print("\nI finished updating JSON file\n")

    
    
    
    # Beginning of the actual plotting:
    initial_time = time.time()
    print(initial_time)
    initial_coordinate_time = float(coordinate_data[0][6])
    print(initial_coordinate_time)
    time_offset = initial_time - initial_coordinate_time

    # Plot the coordinates with the defined bounds
    while (len(coordinate_data) > 4):
        current_time = time.time()
        time_diff = current_time - initial_time
        coordinate_time_diff = float(coordinate_data[0][6]) - initial_coordinate_time
        while ((time_diff-coordinate_time_diff) > 1.5):
            remove_row_by_index(coordinate_data, 0) # Remove the first row of coordinate data
            #print("Removed row")
            if (len(coordinate_data) > 0):
                coordinate_time_diff = float(coordinate_data[0][6]) - initial_coordinate_time
            else:
                break
        # Plot a single plot with the updated coordinate data
        plot_coordinates(coordinate_data, xLow, xHigh, yLow, yHigh, zLow, zHigh, initial_time, initial_coordinate_time, toggle_names=True, video_writer_state=video_writer_state)

        # Reupdate sequence and tag information within main.py
        data_json_path = os.path.join(os.getcwd(), "data.json")
        sequence_json_path = os.path.join(os.getcwd(), "sequence_data.json")

        sequence_name, tags, cranes, geofence_zones = getFullSequenceData(data_json_path, sequence_json_path)

        # Run the alarm checks based on the sequence
        alarm_manager.run_alarm_checks(sequence_name, tags, cranes, geofence_zones)

        #print(f"Sequence Name: {sequence_name}")
        #print(f"Tags: {tags}")
        #print(f"Cranes: {cranes}")
        #print(f"Geofence Zones: {geofence_zones}")

        #input("Press Enter to continue...")
        #break

    # Release the video writer once the plotting is complete
    release_video_writer(video_writer_state)
    print ("Run complete\n")    

if __name__ == '__main__':
    main()