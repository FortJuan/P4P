% MATLAB script to read velocity CSV and plot velocity-time graph with smoothing
clear

% Read the CSV file
data = readtable('velocity_dataset_5.csv');

% Extract relevant columns
tag_ids = data.Tag_ID;
timestamps = data.Timestamp_s;
velocities = data.Velocity_kmph;

% Get the unique tag IDs
unique_tags = unique(tag_ids);

% Prepare a color map for the tags
colors = lines(length(unique_tags));

% Create a figure and slider for setting the smoothing window
figure;
smooth_slider = uicontrol('Style', 'slider', 'Min', 0, 'Max', 5, 'Value', 0, 'Units', 'normalized', 'Position', [0.15 0.02 0.7 0.03]);
smooth_label = uicontrol('Style', 'text', 'String', 'Smoothing Window: 0 seconds', 'Units', 'normalized', 'Position', [0.4 0.06 0.2 0.03]);

axes_handle = axes();  % Create an axes for plotting

hold(axes_handle, 'on');

% Set up a callback function to update the plot based on the slider value
smooth_slider.Callback = @(src, event) update_plot(src.Value, data, unique_tags, colors, smooth_label, axes_handle);

% Initial plot without smoothing
update_plot(0, data, unique_tags, colors, smooth_label, axes_handle);

hold(axes_handle, 'off');

% Function definition must go here at the end of the script
function update_plot(smooth_time, data, unique_tags, colors, smooth_label, axes_handle)
    % Clear only the current axes, not the whole figure
    cla(axes_handle);
    
    % Update the smooth label to reflect the current smoothing window
    set(smooth_label, 'String', sprintf('Smoothing Window: %.1f seconds', smooth_time));
    
    % Plot each tag's data with or without smoothing
    for i = 1:length(unique_tags)
        tag = unique_tags(i);
        tag_data = data(data.Tag_ID == tag, :);
        
        % Apply smoothing if the smoothing time is greater than 0
        if smooth_time > 0
            % Determine the number of data points corresponding to the smoothing time
            time_diff = diff(tag_data.Timestamp_s);
            avg_time_step = mean(time_diff);  % Estimate average time step
            
            % Calculate the number of points to smooth over
            smooth_points = round(smooth_time / avg_time_step);
            smoothed_velocity = movmean(tag_data.Velocity_kmph, smooth_points);  % Moving average
            
            % Plot the smoothed data
            plot(axes_handle, tag_data.Timestamp_s, smoothed_velocity, 'DisplayName', sprintf('Tag %d', tag), 'Color', colors(i,:));
        else
            % Plot raw data if smoothing is not applied
            plot(axes_handle, tag_data.Timestamp_s, tag_data.Velocity_kmph, 'DisplayName', sprintf('Tag %d', tag), 'Color', colors(i,:));
        end
    end
    
    % Add labels and title
    xlabel(axes_handle, 'Time (s)');
    ylabel(axes_handle, 'Velocity (km/h)');
    title(axes_handle, 'Velocity-Time Plot for Tags');
    legend(axes_handle, 'show');
    grid(axes_handle, 'on');
end
