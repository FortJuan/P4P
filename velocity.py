import csv
import math

def exportVelocity(coordinate_data, file_path):
    """
    Exports velocity data from coordinate_data to a CSV file.
    
    Args:
    coordinate_data (list of lists): Data outputted from getCoordinateData.
    file_path (str): Path to the CSV file to export data.

    The function calculates velocity in km/h for each tag and skips invalid data points.
    The time in the CSV will be in seconds since the earliest time step.
    """
    invalid_data_count = 0
    total_data_count = 0
    valid_data = []

    # Dictionary to store previous coordinates and time for each tag
    previous_data = {}

    # Find the earliest timestamp in the data
    valid_timestamps = [float(data_point[6]) for data_point in coordinate_data if data_point[6].replace('.', '', 1).isdigit()]
    if not valid_timestamps:
        raise ValueError("No valid timestamps found in coordinate_data.")
    
    earliest_time = min(valid_timestamps)

    for data_point in coordinate_data:
        total_data_count += 1
        tag_id = data_point[1]
        try:
            # Ensure valid data for positions and timestamps
            x = float(data_point[2])
            y = float(data_point[3])
            z = float(data_point[4])
            timestamp = float(data_point[6])

            # Adjust time to be in seconds since the earliest timestamp
            relative_time = timestamp - earliest_time

            # Check if this tag has previous data to calculate velocity
            if tag_id in previous_data:
                prev_x, prev_y, prev_z, prev_timestamp = previous_data[tag_id]
                time_diff = timestamp - prev_timestamp

                # Skip if time difference is 0 to avoid division by zero
                if time_diff > 0:
                    # Calculate distance in meters
                    distance = math.sqrt((x - prev_x)**2 + (y - prev_y)**2 + (z - prev_z)**2)

                    # Convert velocity from m/s to km/h
                    velocity_kmh = (distance / time_diff) * 3.6

                    # Skip absurd velocities (> 180 km/h)
                    if velocity_kmh <= 180:
                        # Correct the order: first timestamp, then velocity
                        valid_data.append([tag_id, relative_time, velocity_kmh])

            # Update previous data for this tag
            previous_data[tag_id] = (x, y, z, timestamp)

        except (ValueError, IndexError):
            # Count invalid data points (missing or malformed entries)
            invalid_data_count += 1
            continue

    # Write valid data to CSV
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Tag_ID', 'Timestamp_s', 'Velocity_kmph'])
        csvwriter.writerows(valid_data)

    # Calculate and print the invalid data rate
    invalid_data_rate = (invalid_data_count / total_data_count) * 100
    print(f"Invalid data collection rate: {invalid_data_rate:.2f}%")
