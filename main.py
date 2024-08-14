
def check_dependencies():
    """
    Checks if all required dependencies are installed.
    Prints an error message and exits if any dependency is missing.
    """
    import sys
    import subprocess

    required_modules = ['csv']  # List all required modules here

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

    # Define the path to the log file
    log_file_path = r"C:\Users\juani\OneDrive\Desktop\MECHENG700\code\coord_log (1).log" # change depending on log file path
    
    # Call the function to get the coordinate data
    coordinate_data = getCoordinateData(log_file_path)
    
    # Print the resulting matrix of coordinate data
    for row in coordinate_data:
        print(row)

if __name__ == '__main__':
    main()