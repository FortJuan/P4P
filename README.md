 # P4P Crane Anti-collision UI and Alarms

## Introduction
This repository contains all the necessary files and resources for demostrative purposes of the UI functionality. It is designed to [visualise and send alarms to the web application]. Below is a guide on how to navigate through the repository and understand the structure of the key files.

Key features of this repository:
- [Extracts the data from log files]
- [Updates JSON files with relevant information]
- [Outputs video of frames stitched together]

## Table of Contents
- [main.py](#main.py)
- [plot_coordinates.py](#plot_coordinates.py)
- [tag_manager.py](#tag_manager.py)
- [media](./media)
- [data.json](#data.json)
- [sequence_data.json](#sequence_data.json)
- [Other]
- [Usage](#usage)
- [Installation](#installation)

## [main.py]
**Description**:  
[main.py is the file that runs the code logic]
On lines 226 and 227, change selected_data_set and selected_sequence to explore the different functionality of the different datasets and sequences. Here is a list of the different Datasets and Sequence types.

List of Datasets
- "Dataset 1"
- "Dataset 2"
- "Dataset 3"
- "Dataset 4"
- "Dataset 5"
- "Dataset 6"

List of Working Sequences
- "Steelmaking Sequence"
- "Tandem Lift"
- "Bricklayers Lift"

## [plot_coordinates.py]
**Description**:  
[This file is responsible for the creation of the visualisations. Every time it is called, it creates a frame using matplotlib and appends it to the VideoMaker. The same frame can be sent as a PNG to the web application]

## [tag_manager.py]
**Description**:  
[This function uses the manages tags created in tag.py and creates the functionality to update the information to the JSON files. It is also responsible for updating the alert data to the JSON files also.]

## [media]
**Description**:  
[This folder contains the relevant media used in the visuals including background map and the tag type images.]

## [data.json]
**Description**:  
[This file contains the relevant tag information as well as settings that change the way the code is being run. This file is updated throughout the running of the code. Using threading techniques, it is both able to be read and written to at fast speeds. This allows for the full-duplex communication between the Raspberry Pi (a.k.a local code) and web application if a connection is established.]

## [sequence_data.json]
**Description**:  
[This file is not written to during the running of the code. It contains the relevant information that is used to instantiate sequences including the coordinates that make up the shapes of geofences and the colour the geofence is plotteds. It also contains the paths to the different datasets that are stored locally]

## [Outputs]
**Description**:
[The first major output is output_video.mp4 which is a stitched together video of the frames visualising the data from the beginning to the end of the selected dataset. To explore how the graphs for Hazards over time and Velocity over time were created, refer to the 2 Matlab files 'hazards.m' and 'velocity_readings.m' which work by reading the hazard and velocity data that is exported into the CSV files.]

## [Other]
**Description**:  
[The other files contribute to the functionality of the directory and set up methods and classes for the Tag, Sequence, and AlarmManager classes.]


## Usage
[Once in the main directory, type python main.py into the terminal to run the code]
- 

## Installation
[Download the ZIP file of the project from the GitHub Repository Link and extract it on local device. Running main.py should automatically download the Python dependencies. For best results, use Python 3.11]
- [GitHub Repository Link](https://github.com/FortJuan/P4P)


