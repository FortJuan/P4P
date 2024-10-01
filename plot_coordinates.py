import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import time
#from tag import Tag, predefined_tags
import matplotlib.colors as mcolors
from tag_manager import TagManager
from sequence import Sequence
from PIL import Image
from tag import Tag
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
import json

# Helper function to plot crane barriers
def plotCraneBarrier(ax, tag_id, tag_type, x, y, z, crane_plots):
    """
    Plots a red circle around the crane's position representing its barrier.

    Parameters:
    - ax (matplotlib.axes.Axes): The axis on which to plot.
    - tag_id (str): The unique identifier for the tag.
    - tag_type (str): The type of the tag (Crane).
    - x, y, z (float): The X, Y coordinates and Z height of the crane.
    - crane_plots (dict): A dictionary to track existing crane plots (keyed by tag_id).
    """
    if tag_type == "Crane":
        # If this crane (tag_id) already has a circle, remove it first
        if tag_id in crane_plots:
            crane_plots[tag_id].remove()

        # Plot the new crane barrier (a circle with radius equal to the crane's Z-coordinate)
        crane_circle = plt.Circle((x, y), radius=z, color='red', alpha=0.5, fill=True)
        ax.add_patch(crane_circle)

        # Store the new plot reference, keyed by tag_id
        crane_plots[tag_id] = crane_circle

def get_sequence_data(data, sequence_name, dataset_name):
    # Extracting the path for the dataset
    dataset_path = data['data_set'][dataset_name]['path'] if dataset_name in data['data_set'] else None

    # Extracting quadrilaterals and colour for the sequence
    if sequence_name in data['sequence']:
        sequence_info = data['sequence'][sequence_name]
        quadrilaterals = [tuple(tuple(coord) for coord in quad) for quad in sequence_info['quadrilaterals']]
        colour = sequence_info['colour']
    else:
        quadrilaterals, colour = None, None

    return dataset_path, quadrilaterals, colour

def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def plot_icons(ax, tag_type, x, y, zoom=0.05):
    """
    Plots an icon on a given axis based on tag_type at specified (x, y) coordinates with a given zoom level.

    Parameters:
    - ax (matplotlib.axes.Axes): The axis on which to plot the icons.
    - tag_type (str): The type of the tag (e.g., 'Forklift', 'Crane', 'Operator').
    - x (float): The x-coordinate for the icon placement.
    - y (float): The y-coordinate for the icon placement.
    - zoom (float): The zoom level for the icon size.
    """

    # Define the media file path
    media_file_path = os.path.join(os.getcwd(), "./media")

    # Dictionary to hold paths for different tag types
    icon_paths = {
        'Forklift': os.path.join(media_file_path, 'forklift.png'),
        'Crane': os.path.join(media_file_path, 'crane.png'),
        'Operator': os.path.join(media_file_path, 'operator.png')
    }

    # Check if the provided tag_type is in the predefined dictionary
    if tag_type not in icon_paths:
        raise ValueError(f"Invalid tag_type: {tag_type}. Choose from {list(icon_paths.keys())}.")

    # Load the appropriate icon image
    icon_path = icon_paths[tag_type]
    icon_image = Image.open(icon_path)

    # Create an OffsetImage for the icon
    imagebox = OffsetImage(icon_image, zoom=zoom)

    # Place the icon at the given coordinates on the provided axis
    ab = AnnotationBbox(imagebox, (x, y), frameon=False)
    ax.add_artist(ab)

def plot_coordinates(coordinate_data, xLow, xHigh, yLow, yHigh, zLow, zHigh, initial_time, initial_coordinate_time, toggle_names=False):
    """
    Plot tag coordinates on a 2D graph with real-time animation and save as a GIF.
    
    Args:
    coordinate_data (list of lists): Matrix containing tag data.
    xLow, xHigh (float): Bounds for the X-axis.
    yLow, yHigh (float): Bounds for the Y-axis.
    zLow, zHigh (float): Bounds for the Z-axis to color gradient.
    toggle_names (bool): Toggle to show/hide tag names on the plot.
    """
    # Instantiate Tag Manager
    tag_manager = TagManager('data.json')
    
    # Define the media files directory path
    media_file_path = os.path.join(os.getcwd(), "./media")
    bg_image_path = os.path.join(media_file_path, 'mapBackground.png')  # Update with your background image path
    bg_image = Image.open(bg_image_path)
    
    # Get relevant sequence data:
    file_path = os.path.join(os.getcwd(), "sequence_data.json")
    sequence_data = load_json_data(file_path)
    selected_data_set = tag_manager.data['settings'].get('selected_data_set', 'Default Dataset')
    selected_sequence = tag_manager.data['settings'].get('selected_sequence', 'Default Sequence')
    path, quadrilaterals, colour = get_sequence_data(sequence_data, selected_sequence, selected_data_set)
    
    # Create Current Sequence:
    current_sequence = Sequence(selected_sequence, quadrilaterals, colour)
    
    fig, ax = plt.subplots()

    ax.imshow(bg_image, extent=[xLow, xHigh, yLow, yHigh], aspect='auto', alpha=0.5)

    ax.set_xlim(xLow, xHigh)
    ax.set_ylim(yLow, yHigh)
    
    
    
    current_sequence.plot_geofence(ax, 0.25, colour)

    # Dictionary to store plot objects and their times
    plots = {}

    # Dictionary to track crane barrier plots
    crane_plots = {}

    #initial_time = time.time()
    #initial_coordinate_time = float(coordinate_data[0][6])
    dtPrevious = datetime.fromtimestamp(int(initial_coordinate_time))
    uhPrevious = datetime.fromtimestamp(int(initial_time))
    text_obj = None
    
    #for data_point in coordinate_data:
    #    serial_number, x, y, z, timestamp = data_point[1], float(data_point[2]), float(data_point[3]), float(data_point[4]), float(data_point[6])

    current_time = time.time()

    # Dictionary to track the most recent instance of each tag
    latest_tag_data = {}
    
        
    for data_point in coordinate_data:
        current_time = time.time()
        #time_diff = current_time - initial_time
        #coordinate_time_diff = float(coordinate_data[0][6]) - initial_coordinate_time
        serial_number, x, y, z, timestamp = data_point[1], float(data_point[2]), float(data_point[3]), float(data_point[4]), float(data_point[6])

        # Check if the data point falls within the display bounds
        if not (xLow <= x <= xHigh and yLow <= y <= yHigh):
            continue

        # Let's say it has been 14 seconds since we started plotting,
        # The current point we are looking it has only been 13 seconds since starting
        # Therefore, we are looking at a point that should have been plotted 1 second ago.
        time_diff = current_time - initial_time # E.g: 17-3=14
        coordinate_time_diff = timestamp - initial_coordinate_time # E.g: 15-2=13
        time_since_added = time_diff - coordinate_time_diff # E.g 14-13=1

        # Normalize z for color gradient and create scatter plot
        color_value = (z - zLow) / (zHigh - zLow)
        color = plt.cm.viridis(color_value)
        scatter_plot = ax.scatter(x, y, color=color, alpha=1.0, label=serial_number if toggle_names else None)

        if serial_number not in plots:
            plots[serial_number] = []
        plots[serial_number].append((scatter_plot, timestamp))
        #print('ADDED POINT \n')

        # Store the latest instance of each tag in the dictionary
        latest_tag_data[serial_number] = (x, y, z, timestamp, color)
        

        # Iterate through all points for the current tag and fade/remove old ones
        for plot, added_time in plots[serial_number]:
            elapsed_time = timestamp - added_time
            alpha = max(0, 1 - elapsed_time)  # Fade out over 1 second
            plot.set_alpha(alpha)

            if elapsed_time > 1:
                plot.remove()
                #print('****REMOVED POINT\n')

        # Remove entries that have been fully removed from the screen
        plots[serial_number] = [(plot, added_time) for plot, added_time in plots[serial_number] if timestamp - added_time <= 1]

        if ((time_since_added < 0.1)): # This makes sure you are updating the JSON file with the new tag info
            # Display time in the top right corner
            dt = datetime.fromtimestamp(int(timestamp))
            if (dt != dtPrevious):
                if text_obj is not None:
                    text_obj.remove()
                text_obj = ax.text(0.95, 0.95, dt.strftime('%Y-%m-%d %H:%M:%S'), transform=ax.transAxes, fontsize=12,
                    verticalalignment='top', horizontalalignment='right')
            
            #tag_type = tag_manager.get_tag_type(serial_number)
            
            # Create a new Tag instance
            #tag = Tag(tag_type, serial_number, 50, (x, y, z), timestamp)
            
            # Plot the icon of the tag type at the correct location
            #plot_icons(ax, tag_type, x, y, zoom=0.03)
            
            # Update the tag in the JSON file
            #tag_manager.add_or_update_tag(tag)
            #tag.get_tag_type(tag)

            # Here, before breaking, process and plot the latest known instances of **all** tags
            for serial, (x_last, y_last, z_last, ts_last, color_last) in latest_tag_data.items():
                # Plot the last known position for each tag
                ax.scatter(x_last, y_last, color=color_last, alpha=1.0)  # Scatter for last known tag position
                tag_type = tag_manager.get_tag_type(serial)


                print(f"Processing tag_id: {serial}, tag_type: {tag_type}")
                # Ensure only "Crane" tag_type calls the function
                if tag_type == "Crane":
                    print("Plotting Crane circle \n")
                    # If the tag is a crane, plot the crane barrier
                    plotCraneBarrier(ax, serial, tag_type, x_last, y_last, z_last, crane_plots)

                # Create a new Tag instance
                tag = Tag(tag_type, serial, 50, (x_last, y_last, z_last), ts_last)
                # Update the tag in the JSON file
                tag_manager.add_or_update_tag(tag)
            
                # Plot the icon of the tag type at the correct location
                plot_icons(ax, tag_type, x_last, y_last, zoom=0.03)

                #plot_icons(ax, tag_type, x_last, y_last, zoom=0.03)  # Icon for the last known position


            break # Don't look at future data just yet, therefore break
        
        # Grab the current frame for the GIF
        #writer.grab_frame()
        #ax.cla()  # Clear the axis for the next frame

    plt.show()
    #plt.close(fig)
