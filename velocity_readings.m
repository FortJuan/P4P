% MATLAB script to read velocity CSV and plot velocity-time graph with smoothing

clear

% Read the CSV file
data = readtable('velocity_dataset_5.csv');

% Clean the data by removing rows with missing or invalid values
data = rmmissing(data); % Remove rows with missing data

% Extract relevant columns
tag_ids = data.Tag_ID;
timestamps = data.Timestamp_s;
velocities = data.Velocity_kmph;

% Get unique tag IDs
unique_tags = unique(tag_ids);

% Prepare a color map for the tags
colors = lines(length(unique_tags));

% Create a figure and slider for setting the smoothing window
figure('Position', [100, 100, 800, 600]); % Set an initial size for the figure
smooth_slider = uicontrol('Style', 'slider', 'Min', 0, 'Max', 5, 'Value', 0, 'Units', 'normalized', 'Position', [0.15 0.02 0.7 0.03], 'Tag', 'smooth_slider');
smooth_label = uicontrol('Style', 'text', 'String', 'Smoothing Window: 0 seconds', 'Units', 'normalized', 'Position', [0.4 0.06 0.2 0.03]);

% Adjust the position of the axes to leave space for the slider and label
axes_handle = axes('Position', [0.1, 0.15, 0.85, 0.75]); % [left, bottom, width, height] with more bottom space for UI controls

hold(axes_handle, 'on');

% Store plot handles for each tag
plot_handles = gobjects(length(unique_tags), 1);

% Initial plot without smoothing
for i = 1:length(unique_tags)
    tag = unique_tags(i);
    tag_data = data(data.Tag_ID == tag, :);
    
    % Ensure there is enough data for this tag to plot
    if isempty(tag_data) || height(tag_data) < 2
        warning('Tag %d has insufficient data and will be skipped.', tag);
        continue;
    end
    
    % Plot raw data initially
    plot_handles(i) = plot(axes_handle, tag_data.Timestamp_s, tag_data.Velocity_kmph, 'DisplayName', sprintf('Tag %d', tag), 'Color', colors(i,:));
end

% Set up a callback function to update the plot based on the slider value
smooth_slider.Callback = @(src, event) update_plot(src.Value, data, unique_tags, plot_handles, colors, smooth_label);

% Add labels and title
xlabel(axes_handle, 'Time (s)');
ylabel(axes_handle, 'Velocity (km/h)');
title(axes_handle, 'Velocity-Time Plot for Tags');
legend(axes_handle, 'show');
grid(axes_handle, 'on');

hold(axes_handle, 'off');

% Function definition must go here at the end of the script
function update_plot(smooth_time, data, unique_tags, plot_handles, colors, smooth_label)
    % Update the smooth label to reflect the current smoothing window
    set(smooth_label, 'String', sprintf('Smoothing Window: %.1f seconds', smooth_time));
    
    % Update each tag's plot with smoothing
    for i = 1:length(unique_tags)
        tag = unique_tags(i);
        tag_data = data(data.Tag_ID == tag, :);
        
        % Ensure there is enough data for this tag to plot
        if isempty(tag_data) || height(tag_data) < 2
            warning('Tag %d has insufficient data and will be skipped.', tag);
            continue;
        end
        
        % Apply smoothing if the smoothing time is greater than 0
        if smooth_time > 0
            % Determine the number of data points corresponding to the smoothing time
            time_diff = diff(tag_data.Timestamp_s);
            avg_time_step = mean(time_diff);  % Estimate average time step
            
            % Calculate the number of points to smooth over
            if avg_time_step > 0
                smooth_points = round(smooth_time / avg_time_step);
            else
                smooth_points = 1;  % Avoid division by zero, use minimum smoothing
            end
            
            % Ensure smoothing window is valid
            if smooth_points > 1 && smooth_points <= height(tag_data)
                % Apply moving average smoothing
                smoothed_velocity = movmean(tag_data.Velocity_kmph, smooth_points);
            else
                % If smoothing points exceed data points, use raw data
                smoothed_velocity = tag_data.Velocity_kmph;
            end
        else
            % Plot raw data if smoothing is not applied
            smoothed_velocity = tag_data.Velocity_kmph;
        end
        
        % Update the plot handle for this tag
        set(plot_handles(i), 'YData', smoothed_velocity);
    end
end
