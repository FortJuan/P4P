
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
    
def main():
    # Check for dependencies
    check_dependencies()

    # Import the required function after checking dependencies
    from coordinate_extractor import getCoordinateData
    from plot_coordinates import plot_coordinates
    from tag import Tag
    from tag_manager import TagManager
    import os
    
    
    # Define the path to the log file
    #log_file_path = r"C:\Users\juani\OneDrive\Desktop\MECHENG700\code\coord_log (1).log" # change depending on log file path
    log_file_path = os.path.join(os.getcwd(), "coord_log (1).log")
    # Call the function to get the coordinate data
    print(log_file_path)
    coordinate_data = getCoordinateData(log_file_path)
    #print(coordinate_data)
    
    # Add current JSON data
    tag_manager = TagManager('data.json')
    
    # Update settings if needed
    tag_manager.update_settings(selected_data_set="Dataset 2", selected_sequence="Steelmaking Sequence")

    # Load updated settings
    selected_data_set = tag_manager.data['settings'].get('selected_data_set', 'Default Dataset')
    selected_sequence = tag_manager.data['settings'].get('selected_sequence', 'Default Sequence')
    print(f"Loaded settings: DataSet - {selected_data_set}, Sequence - {selected_sequence}")

    # Create Tag instances
    tag1 = Tag("RFID", "001AFC", 85.5, (10, 20, 5), coordinate_data[0][6])
    tag2 = Tag("NFC", "002BFD", 90.0, (15, 25, 5), coordinate_data[0][6])
    tag3 = Tag("UHF", "003CFE", 75.3, (20, 30, 5), coordinate_data[0][6])

    print("\nI addded a path\n")
    # Add tags to the manager (and save to JSON)
    tag_manager.add_or_update_tag(tag1)
    tag_manager.add_or_update_tag(tag2)
    tag_manager.add_or_update_tag(tag3)
    
    tag_manager.add_alert("Hazard Alert", "Violation of crane seperation", "2024-05-02T16:04:03Z")
    print("\nI finished updating JSON file\n")
    # Define the bounds for the graph
    xLow = 18.00
    xHigh = 25.00
    yLow = 2.00
    yHigh = 6.00
    zLow = 0.75
    zHigh = 1.50

    # Plot the coordinates with the defined bounds
    plot_coordinates(coordinate_data, xLow, xHigh, yLow, yHigh, zLow, zHigh, toggle_names=True)

if __name__ == '__main__':
    main()