import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import time
#from tag import Tag, predefined_tags
import matplotlib.colors as mcolors
import numpy as np

def plot_coordinates(coordinate_data, xLow, xHigh, yLow, yHigh, zLow, zHigh, toggle_names=False):
    """
    Plot tag coordinates on a 2D graph with real-time animation and save as a GIF.
    
    Args:
    coordinate_data (list of lists): Matrix containing tag data.
    xLow, xHigh (float): Bounds for the X-axis.
    yLow, yHigh (float): Bounds for the Y-axis.
    zLow, zHigh (float): Bounds for the Z-axis to color gradient.
    toggle_names (bool): Toggle to show/hide tag names on the plot.
    """
    fig, ax = plt.subplots()

    ax.set_xlim(xLow, xHigh)
    ax.set_ylim(yLow, yHigh)

    # Dictionary to store plot objects and their times
    plots = {}

    initial_time = time.time()
    initial_coordinate_time = float(coordinate_data[0][6])
    dtPrevious = datetime.fromtimestamp(int(initial_coordinate_time))
    text_obj = None

    # Metadata for the GIF
    metadata = dict(title='Tag Movement', artist='user')
    writer = animation.PillowWriter(fps=10, metadata=metadata)
    gif_path = r"C:\Users\juani\OneDrive\Desktop\MECHENG700\code\plot_animation.gif"

    with writer.saving(fig, gif_path, 100):
        for data_point in coordinate_data:
            current_time = time.time()
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
            print('ADDED POINT \n')

            # Iterate through all points for the current tag and fade/remove old ones
            for plot, added_time in plots[serial_number]:
                elapsed_time = current_time - added_time
                alpha = max(0, 1 - elapsed_time)  # Fade out over 1 second
                plot.set_alpha(alpha)

                if elapsed_time > 1:
                    plot.remove()
                    print('****REMOVED POINT\n')

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

            # Grab the current frame for the GIF
            writer.grab_frame()
            #ax.cla()  # Clear the axis for the next frame

    plt.close(fig)