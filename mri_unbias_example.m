%% run_mri_unbias_example
% Example script demonstrating MRI intensity bias correction using mri_unbias.
clear; clc; close all;

fprintf('\n=== Running mri_unbias example script ===\n\n');

% Load example data
fprintf('Loading example data\n');
example_dir = fullfile(fileparts(which('mri_unbias')),'example_data');
input_image_path = fullfile(example_dir,'t1_fl3d_FA30.nii.gz');
wm_mask_path = fullfile(example_dir,'WM_mask.nii.gz');

img = niftiread(input_image_path);
wm_mask = niftiread(wm_mask_path) > 0;

% Set parameters
poly_degree = 3; % Polynomial degree for white matter bias field

% Run bias correction
[img_corrected, bias_field] = mri_unbias(img,wm_mask,poly_degree);

% Prepare output directory
fprintf('Writing output images and visualization figure.\n');
out_dir = fullfile(example_dir,'output');
if ~exist(out_dir,'dir')
    mkdir(out_dir);
end

% Save output images
iminfo = niftiinfo(input_image_path);

out_names = compose('t1_fl3d_FA30_%s_poly%d.nii', ...
    ["unbiased"; "bias_estimation"], poly_degree);

niftiwrite(img_corrected, fullfile(out_dir, out_names{1}), ...
    iminfo, 'Compressed', true);
niftiwrite(bias_field, fullfile(out_dir, out_names{2}), ...
    iminfo, 'Compressed', true);

% Visualization
slice_idx = 78;
fig = figure('Name', 'MRI Bias Correction', 'Color', 'w');

subplot(1, 2, 1); % Original image
imshow(imrotate(img(:, :, slice_idx), 90), [0 300]);
title('Raw T1w Image');
text(5, 5, sprintf('Slice %d', slice_idx), 'Color', 'w', ...
    'VerticalAlignment', 'top', 'FontWeight', 'bold');

subplot(1, 2, 2); % Corrected image
imshow(imrotate(img_corrected(:, :, slice_idx), 90), [0 2]);
title('Unbiased T1w Image');
text(5, 5, sprintf('Slice %d', slice_idx), 'Color', 'w', ...
    'VerticalAlignment', 'top', 'FontWeight', 'bold');

saveas(fig, fullfile(out_dir, 'before_after_visualization.png'));
close(fig);

fprintf('Outputs saved in: %s\n',out_dir);

%% Diagnostics for polynomial degree selection
% -------------------------------------------------------------------------
% This script:
%   1. Tests several polynomial degrees
%   2. Runs bias correction using mri_unbias
%   3. Measures WM intensity uniformity (std or CoV)
%   4. Plots elbow analysis to pick optimal degree
% -------------------------------------------------------------------------
% --- Setup ---
degrees = 1:6;            % range of polynomial degrees to test
n_degrees = numel(degrees);
std_vals = zeros(1, n_degrees);  % preallocate results

% --- Loop over degrees ---
for idx = 1:n_degrees
    d = degrees(idx);
    fprintf('\nTesting polynomial degree = %d\n', d);

    % Run bias correction on this degree
    [img_corr, ~] = mri_unbias(img, wm_mask, d);

    % Extract intensities inside WM mask
    wm_vals = img_corr(wm_mask);

    % Compute metric: either std or CoV
    std_vals(idx) = std(wm_vals(:));  % standard deviation
    % OR for Coefficient of Variation:
    % std_vals(idx) = std(wm_vals(:)) / mean(wm_vals(:));

end

% --- Elbow analysis (10% threshold default) ---
fig = plot_degree_elbow_with_threshold(degrees, std_vals, 10);
saveas(fig, fullfile(out_dir, 'diagnostics_polynomial_degree_selection.png'));
