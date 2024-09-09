import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import time
#from tag import Tag, predefined_tags
import matplotlib.colors as mcolors
from tag_manager import TagManager
from sequence import Sequence
from tag import Tag
import numpy as np
import os
import json

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
    # Instantiate Tag
    tag_manager = TagManager('data.json')
    
    # Get relevant sequence data:
    file_path = os.path.join(os.getcwd(), "sequence_data.json")
    sequence_data = load_json_data(file_path)
    selected_data_set = tag_manager.data['settings'].get('selected_data_set', 'Default Dataset')
    selected_sequence = tag_manager.data['settings'].get('selected_sequence', 'Default Sequence')
    path, quadrilaterals, colour = get_sequence_data(sequence_data, selected_sequence, selected_data_set)
    
    # Create Current Sequence:
    current_sequence = Sequence(selected_sequence, quadrilaterals, colour)
    
    fig, ax = plt.subplots()

    ax.set_xlim(xLow, xHigh)
    ax.set_ylim(yLow, yHigh)
    
    current_sequence.plot_geofence(ax, 0.5, colour)

    # Dictionary to store plot objects and their times
    plots = {}

    #initial_time = time.time()
    #initial_coordinate_time = float(coordinate_data[0][6])
    dtPrevious = datetime.fromtimestamp(int(initial_coordinate_time))
    uhPrevious = datetime.fromtimestamp(int(initial_time))
    text_obj = None
    
    for data_point in coordinate_data:
        serial_number, x, y, z, timestamp = data_point[1], float(data_point[2]), float(data_point[3]), float(data_point[4]), float(data_point[6])


# Previous plot_coordinates implementation

    # Metadata for the GIF
    #metadata = dict(title='Tag Movement', artist='user')
    #writer = animation.PillowWriter(fps=10, metadata=metadata)
    #gif_path = os.path.join(os.getcwd(), "plot_animation.gif")
    current_time = time.time()
    
        
    for data_point in coordinate_data:
        current_time = time.time()
        time_diff = current_time - initial_time
        coordinate_time_diff = float(coordinate_data[0][6]) - initial_coordinate_time
        serial_number, x, y, z, timestamp = data_point[1], float(data_point[2]), float(data_point[3]), float(data_point[4]), float(data_point[6])

        # Check if the data point falls within the display bounds
        if not (xLow <= x <= xHigh and yLow <= y <= yHigh):
            continue

        time_diff = current_time - initial_time
        coordinate_time_diff = timestamp - initial_coordinate_time
        time_since_added = time_diff - coordinate_time_diff

        # Normalize z for color gradient and create scatter plot
        color_value = (z - zLow) / (zHigh - zLow)
        color = plt.cm.viridis(color_value)
        scatter_plot = ax.scatter(x, y, color=color, alpha=1.0, label=serial_number if toggle_names else None)

        if serial_number not in plots:
            plots[serial_number] = []
        plots[serial_number].append((scatter_plot, current_time))
        #print('ADDED POINT \n')

        # Iterate through all points for the current tag and fade/remove old ones
        for plot, added_time in plots[serial_number]:
            elapsed_time = current_time - added_time
            alpha = max(0, 1 - elapsed_time)  # Fade out over 1 second
            plot.set_alpha(alpha)

            if elapsed_time > 1:
                plot.remove()
                #print('****REMOVED POINT\n')

        # Remove entries that have been fully removed from the screen
        plots[serial_number] = [(plot, added_time) for plot, added_time in plots[serial_number] if current_time - added_time <= 1]

        # Display time in the top right corner
        dt = datetime.fromtimestamp(int(timestamp))
        if (dt != dtPrevious):
            if text_obj is not None:
                text_obj.remove()
            text_obj = ax.text(0.95, 0.95, dt.strftime('%Y-%m-%d %H:%M:%S'), transform=ax.transAxes, fontsize=12,
                    verticalalignment='top', horizontalalignment='right')
            dtPrevious = dt

        if (((time_diff-coordinate_time_diff) < 0.1)):
            # Create a new Tag instance
            tag = Tag(serial_number, 50, (x, y, z), timestamp)
            # Update the tag in the JSON file
            tag_manager.add_or_update_tag(tag)
            break
        # Grab the current frame for the GIF
        #writer.grab_frame()
        #ax.cla()  # Clear the axis for the next frame

    plt.show()
    #plt.close(fig)
