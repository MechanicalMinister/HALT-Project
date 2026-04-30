clear all

startVal = 3;                      % Starting number
step = 2;                          % Increment
numFiles = 9;                      % How many files to load
cutoff = 0;                    % Cutoff for cycle range in meters
%seal_l = 0.004;                   % Length of the seal used
Bin_edges = linspace(0, 0.3, 1000); % Edge specifications for histogram bins
fields = {'CylPos1', 'CylPos2', 'CylPos3'};   % field names as strings

for k = 1:numFiles
    idx = startVal + (k-1)*step;              % generates 1, 3, 5, 7, ...
    filename = sprintf('Data_%d.mat', idx);   % build filename
    Data(k) = load(filename);                    % store in struct array
end

for j = 1:3
    for i = 1:numFiles
        rf = rainflow(Data(i).OutData.(fields{j}), Data(i).OutData.time);
        rf_filtered = rf(rf(:, 2) >= cutoff, :);
        rf_truncated(i).data_set.Cylinders(j).Cylinder = rf_filtered;   % store matrix in field "data"
    end
end

compiled_ranges = cell(1,numFiles); %Creates cell array with cells matching number of files

for i = 1:numFiles %Loop over number of files
    compiled_ranges{i} = []; %Fills each cell with empty matrix
end

% Loop over the main struct (1x9)
for i = 1:numel(rf_truncated)

    % Get the inner struct (1x1)
    inner1 = rf_truncated(i);

    % Get the 1x3 struct inside it (assuming field names don't matter, use dynamic field access)
    fNames1 = inner1.data_set.Cylinders;

    for j = 1:numel(fNames1)
         inner2 = fNames1(j);  % This is 1x3 struct

        %fNames2 = inner2;

        for k = 1:numel(inner2)
            mat = inner2.Cylinder;  % This is a matrix with 5 columns

            % Skip empty matrices
            if isempty(mat)
                continue
            end

            % Take the second column
            col2 = mat(:,2);

            % Check the first column
            firstCol = mat(:,1);

            % Find indices where first column == 1
            idxDouble = firstCol == 1;

            % Duplicate these values
            col2_dup = [col2; col2(idxDouble)];

            % Append to result
            compiled_ranges{i} = [compiled_ranges{i}; col2_dup];
        end
    end
end

figure
tiledlayout(3,3)

%Loop of raw position data figures
for i = 1:9
    nexttile
    plot(Data(1).OutData.time, Data(i).OutData.CylPos1)
    hold on
    plot(Data(1).OutData.time, Data(i).OutData.CylPos2)
    hold on
    plot(Data(1).OutData.time, Data(i).OutData.CylPos3)
    legend('Cyl1', 'Cyl2', 'Cyl3')
    xlabel('Time since measurement start [s]')
    ylabel('Position of cylinders [m]')
    ylim([0.13 0.55])
    title(sprintf('Dataset %d', i*2+1))
end

figure
tiledlayout(3,3)

%Loop of histogram figures
for i = 1:9
    nexttile
    histogram(compiled_ranges{i}, Bin_edges)
    yscale('log')
    xlabel('Cylinder movement range [m]')
    ylabel('No. of occurences')
    title(sprintf('Dataset %d', i*2+1))
    ylim([0.6 10000])
end

%% Mean velocity check

mean_v = [];

for i = 1:numFiles
    mean_v(1, i) = sum(Data(i).OutData.Wind1VelX);
end

for i = 1:numFiles
    mean_v(1, i) = mean_v(i)/length(Data(i).OutData.Wind1VelX);
end
mean_v
%% Maximum cylinder speed
% Load Data
clc;

for i = 1:numFiles
    file_id = i*2+1;
    File_Name = sprintf('Data_%d.mat', file_id);
    S.("data_" + file_id) = load(File_Name);
end

% Extract specific data (Cylinder velocity)

% time for all sets
for i = 1:numFiles
    file_id = i*2+1;
    File_Name = sprintf('Data_%d.mat', file_id);
    Time.("data_" + file_id) = S.("data_" + file_id).OutData.Time;
end

% Three Cylinder velocities for all sets
for i = 1:numFiles
    file_id = i*2+1;
    File_Name = sprintf('Data_%d.mat', file_id);
    CylVel.("data_" + file_id) = [S.("data_" + file_id).OutData.CylVel1, S.("data_" + file_id).OutData.CylVel2, S.("data_" + file_id).OutData.CylVel3];
end

% Find largest velocity

for k = 1:numFiles % loop over different datasets
    file_id = k*2+1;
    for j = 1:3 % loop over different cylinders
        for i = 1:length(CylVel.data_3) % loop over individual data points
            if (i == 1 && j == 1 && k == 1)
                Max_vel = CylVel.("data_" + file_id)(i,j);
            elseif CylVel.("data_" + file_id)(i,j) > Max_vel
                Max_vel = CylVel.("data_" + file_id)(i,j);
            end
        end
    end
end