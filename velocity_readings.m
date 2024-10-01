% MATLAB script to read velocity CSV and plot velocity-time graph

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

figure;
hold on;

% Plot each tag's data
for i = 1:length(unique_tags)
    tag = unique_tags(i);
    tag_data = data(tag_ids == tag, :);
    plot(tag_data.Timestamp_s, tag_data.Velocity_kmph, 'DisplayName', sprintf('Tag %d', tag), 'Color', colors(i,:));
end

% Add labels and title
xlabel('Time (s)');
ylabel('Velocity (km/h)');
title('Velocity-Time Plot for Tags');
legend('show');
grid on;
hold off;
