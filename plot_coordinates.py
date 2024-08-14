import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import time
from tag import Tag, predefined_tags
import matplotlib.colors as mcolors

def plot_coordinates(coordinate_data, xLow, xHigh, yLow, yHigh, zLow, zHigh, toggle_names=False, save_as_gif=True, gif_filename='animation.gif'):
    """
    Plot tag coordinates on a 2D graph with real-time animation.
    
    Args:
    coordinate_data (list of lists): Matrix containing tag data.
    xLow, xHigh (float): Bounds for the X-axis.
    yLow, yHigh (float): Bounds for the Y-axis.
    zLow, zHigh (float): Bounds for the Z-axis to color gradient.
    toggle_names (bool): Toggle to show/hide tag names on the plot.
    save_as_gif (bool): Flag to save the animation as a GIF.
    gif_filename (str): Filename for saving the GIF.
    """
    # Initialize the figure and axis
    fig, ax = plt.subplots()
    
    # Set the axis limits
    ax.set_xlim(xLow, xHigh)
    ax.set_ylim(yLow, yHigh)

    # Initialize a dictionary to store plot objects for each tag
    plots = {}

    # Initialize the writer if saving as GIF
    writer = None
    if save_as_gif:
        metadata = dict(title='Tag Animation', artist='ChatGPT')
        writer = animation.PillowWriter(fps=15, metadata=metadata)

    def update(frame):
        """Update function for the animation."""
        current_time = time.time()
        
        # Clear the axis for the new frame
        ax.clear()
        ax.set_xlim(xLow, xHigh)
        ax.set_ylim(yLow, yHigh)
        
        for data_point in coordinate_data:
            serial_number, x, y, z, timestamp = data_point[1], float(data_point[2]), float(data_point[3]), float(data_point[4]), float(data_point[6])
            
            # Check if the data point falls within the display bounds
            if not (xLow <= x <= xHigh and yLow <= y <= yHigh):
                continue

            # Convert timestamp to a datetime object
            dt = datetime.fromtimestamp(timestamp)
            time_diff = current_time - timestamp

            # If the tag is new, prompt for name and color
            if serial_number not in predefined_tags:
                name = input(f"Enter name for new tag {serial_number}: ")
                print("Choose a color from the following:")
                available_colors = list(mcolors.CSS4_COLORS.keys())[:8]
                for i, color in enumerate(available_colors):
                    print(f"{i + 1}: {color}")
                color_choice = int(input("Enter the number corresponding to your chosen color: ")) - 1
                color = available_colors[color_choice]

                predefined_tags[serial_number] = Tag(serial_number, name, color)

            # Get the tag instance
            tag = predefined_tags[serial_number]
            tag.update_coordinates(x, y, z, timestamp)

            # Plot the tag's position
            color_value = (z - zLow) / (zHigh - zLow)  # Normalize z for the color gradient
            color = plt.cm.viridis(color_value)


# I BELIEVE EVERYTHING ABOVE THIS LINE IS FUNCTIONING AS INTENDED. EVERYTHING BELOW THIS LINE HOWEVER I AM NOT AS SURE  
# #I WILL NEED TO CHANGE HOW THE DATA IS APPENDED TO THE ANIMATION TO MAKE THE ANIMATION LEGIT

            # If the tag doesn't have a plot object yet, create one
            if serial_number not in plots:
                plots[serial_number] = ax.scatter(x, y, color=color, label=tag.name if toggle_names else None)
            else:
                # Update the existing plot
                plots[serial_number].set_offsets([x, y])
                plots[serial_number].set_color(color)

            # Display time in the top right corner
            ax.text(0.95, 0.95, dt.strftime('%Y-%m-%d %H:%M:%S'), transform=ax.transAxes, fontsize=12,
                    verticalalignment='top', horizontalalignment='right')

        return list(plots.values())

    # Create the animation
    ani = animation.FuncAnimation(fig, update, frames=len(coordinate_data), interval=100, blit=False)

    # Save the animation as a GIF if requested
    if save_as_gif and writer:
        with writer.saving(fig, gif_filename, dpi=100):
            for frame in range(len(coordinate_data)):
                update(frame)
                writer.grab_frame()

    # Display the plot
    if not save_as_gif:
        plt.show()