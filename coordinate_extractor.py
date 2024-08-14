import csv

def getCoordinateData(log_file_path):
    """
    Extracts coordinate data from a log file and returns it as a matrix.

    Args:
    log_file_path (str): Path to the log file to be read.

    Returns:
    list of lists: A matrix where each row contains extracted data in the order:
                    [Sequence Number, Tag Serial Number, Position X, Position Y, Position Z, Information String, Calculation Timestamp]
    """
    # Initialize an empty matrix to store the extracted data
    coordinateData = []

    # Open and read the log file
    with open(log_file_path, 'r') as file:
        for line in file:
            # Remove any leading/trailing whitespace characters (like newline)
            line = line.strip()
            
            # Check if the line starts with the expected log prefix
            if line.startswith('$PEKIO,COORD'):
                # Split the line by commas to extract individual fields
                fields = line.split(',')

                # Extract relevant data from the fields
                # Sequence Number: the third item in the split list (index 2)
                sequence_number = fields[2]

                # Tag’s Serial Number: the fourth item in the split list (index 3)
                tag_serial_number = fields[3]

                # Tag’s Position: the fifth to seventh items in the split list (indexes 4 to 6)
                # This can be empty, so default to empty strings if not present
                position_x = fields[4] if len(fields) > 4 else ''
                position_y = fields[5] if len(fields) > 5 else ''
                position_z = fields[6] if len(fields) > 6 else ''

                # Information String: the eighth item in the split list (index 7)
                # It may be empty, so default to an empty string if not present
                information_string = fields[7] if len(fields) > 7 else ''

                # Calculation’s Timestamp: the ninth item in the split list (index 8)
                calculation_timestamp = fields[8] if len(fields) > 8 else ''

                # Append the extracted data as a row in the matrix
                coordinateData.append([
                    sequence_number,           # Column 0: Sequence Number
                    tag_serial_number,        # Column 1: Tag’s Serial Number
                    position_x,               # Column 2: Position X
                    position_y,               # Column 3: Position Y
                    position_z,               # Column 4: Position Z
                    information_string,       # Column 5: Information String
                    calculation_timestamp     # Column 6: Calculation’s Timestamp
                ])

    # Return the matrix of coordinate data
    return coordinateData