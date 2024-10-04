import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

def convert_plot_to_frame():
    # Save the current plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')  # Save current Matplotlib plot to the buffer
    buf.seek(0)
    
    # Open the image from the buffer
    img = Image.open(buf)
    
    # Convert the image to a format suitable for video (e.g., BGR for OpenCV)
    frame = np.array(img.convert('RGB'))  # Convert PIL image to RGB NumPy array
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR (OpenCV format)
    return frame

import cv2

class VideoWriterState:
    def __init__(self, output_file, codec, fps, frame_size=None):
        """
        Initializes VideoWriterState with output file, codec, fps, and frame size.
        :param output_file: Name of the output video file.
        :param codec: FourCC codec to use for the video writer.
        :param fps: Frames per second for the video.
        :param frame_size: Size of the video frames (width, height). Default is None.
        """
        self.output_file = output_file
        self.codec = codec
        self.fps = fps
        self.frame_size = frame_size
        self.video_writer = None
        self.last_frame_time = None  # Track when the last frame was added
    
    def initialize_writer(self):
        """
        Initializes the video writer if frame size is available.
        :raises ValueError: If frame size is not set before initializing the writer.
        """
        if self.frame_size is None:
            raise ValueError("Frame size must be set before initializing video writer.")
        
        # Initialize video writer with the given parameters
        fourcc = cv2.VideoWriter_fourcc(*self.codec)  # Codec, e.g., 'XVID' or 'mp4v'
        self.video_writer = cv2.VideoWriter(self.output_file, fourcc, self.fps, self.frame_size)

    def release(self):
        """Releases the video writer."""
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None

def add_frame(frame, video_writer_state):
    if video_writer_state.video_writer is None:
        raise ValueError("VideoWriterState is not properly initialized.")
    
    frame_np = np.array(frame)  # Convert frame to a NumPy array
    
    if video_writer_state.frame_size is None:
        video_writer_state.frame_size = (frame_np.shape[1], frame_np.shape[0])  # Set frame size on first frame

    frame_resized = cv2.resize(frame_np, video_writer_state.frame_size)  # Resize the frame
    
    current_time = time.time()
    
    # Handle holding frames for real-time playback
    if video_writer_state.last_frame_time is not None:
        elapsed_time = current_time - video_writer_state.last_frame_time
        target_time_per_frame = 1 / video_writer_state.fps
        
        num_repeats = max(1, int(elapsed_time / target_time_per_frame))
    else:
        num_repeats = 1  # First frame, no repeats needed
    
    # Write the frame multiple times to hold for real-time
    for _ in range(num_repeats):
        video_writer_state.video_writer.write(frame_resized)
    
    video_writer_state.last_frame_time = current_time  # Update last frame time

def release_video_writer(video_state: VideoWriterState):
    """Releases the video writer state."""
    video_state.release()
