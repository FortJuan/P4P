clear;
clc;

% Initialize an array to store hazard timestamps (in seconds)
%hazard_timestamps = [5,10,14,33,55,69,80,88,108,115,130];

% Example: You can manually add timestamps or dynamically generate them.
% This will simulate adding hazards occurring at different times (in seconds).
%hazard_timestamps = [5, 15, 25, 35, 45, 65, 85, 105, 125, 145, 165, 180, 200, 220];

% Read hazard times from the CSV file
filename = 'hazard_times.csv';

% Load the timestamps from the CSV file
hazard_timestamps_unix = csvread(filename);

% Use the first timestamp as the start time (time = 0), but exclude it from the hazard timestamps
start_time = hazard_timestamps_unix(1);  % First timestamp is the start time

% Remove the first timestamp (start time) from the list of hazard timestamps
hazard_timestamps_unix = hazard_timestamps_unix(2:end);

% Convert from UNIX timestamps to relative times (seconds from the start time)
hazard_timestamps = hazard_timestamps_unix - start_time;

% Display the converted hazard timestamps
disp('Hazard timestamps (in seconds from start):');
disp(hazard_timestamps);


% Define time range bins for the histogram (adjust according to your needs)
time_bins = 0:20:240; % Example: 0 to 240 seconds, with 20-second intervals

% Create a figure for the histogram plot
figure('Position', [100, 100, 800, 600]); % Set an initial size for the figure
hold on;

% Create a histogram plot for the hazards over time
histogram(hazard_timestamps, time_bins, 'FaceColor', [0.2 0.2 0.8], 'EdgeColor', 'k');

% Add labels, title, and grid
xlabel('Time (s)', 'FontSize', 12);
ylabel('Number of Hazards', 'FontSize', 12);
title('Hazards Over Time', 'FontSize', 14);
grid on;

% Set axes properties to match the aesthetic
set(gca, 'FontSize', 12, 'LineWidth', 1.5);
axis tight; % Adjust the axis limits

% Display total number of hazards
total_hazards = length(hazard_timestamps);
annotation('textbox', [0.75, 0.8, 0.1, 0.1], 'String', sprintf('Total Hazards: %d', total_hazards), 'FitBoxToText', 'on', 'BackgroundColor', 'white');

% Add dynamic interaction with slider (to adjust bin width dynamically)
smooth_slider = uicontrol('Style', 'slider', 'Min', 10, 'Max', 60, 'Value', 20, 'Units', 'normalized', 'Position', [0.15 0.02 0.7 0.03], 'Tag', 'bin_slider');
smooth_label = uicontrol('Style', 'text', 'String', 'Bin Width: 20 seconds', 'Units', 'normalized', 'Position', [0.4 0.06 0.2 0.03]);

% Update plot based on slider value
smooth_slider.Callback = @(src, event) update_histogram(src.Value, hazard_timestamps, smooth_label);

hold off;

% Function to update the histogram plot based on the bin width slider
function update_histogram(bin_width, hazard_timestamps, smooth_label)
    % Update the bin width label
    set(smooth_label, 'String', sprintf('Bin Width: %.1f seconds', bin_width));
    
    % Recalculate the time bins based on new bin width
    max_time = max(hazard_timestamps);
    time_bins = 0:bin_width:(max_time + bin_width);
    
    % Update the histogram plot with new bin width
    clf; % Clear current figure
    histogram(hazard_timestamps, time_bins, 'FaceColor', [0.2 0.2 0.8], 'EdgeColor', 'k');
    
    % Reapply labels, title, and grid
    xlabel('Time (s)', 'FontSize', 12);
    ylabel('Number of Hazards', 'FontSize', 12);
    title('Hazards Over Time', 'FontSize', 14);
    grid on;
    
    % Display total number of hazards
    total_hazards = length(hazard_timestamps);
    annotation('textbox', [0.75, 0.8, 0.1, 0.1], 'String', sprintf('Total Hazards: %d', total_hazards), 'FitBoxToText', 'on', 'BackgroundColor', 'white');
    
    axis tight; % Adjust the axis limits
end
