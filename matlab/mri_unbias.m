function [img_corrected, bias_field] = mri_unbias(img,wm_mask,poly_degree)
% -------------------------------------------------------------------------
% MRI_UNBIAS
%
% This function estimates and corrects intensity bias in a 3D image by
% fitting an n-th degree 3D polynomial to a white-matter mask.
%
% The polynomial models the smooth bias field under the assumption that
% the masked region (i.e., white matter) should have uniform intensity,
% and all variation within it arises from bias. The estimated bias field
% is then used to correct the entire image.
% -------------------------------------------------------------------------
% INPUTS
% -------------------------------------------------------------------------
% img          : 3D image data
% wm_mask      : binary 3D mask (same dimensions as 'image') defining the
%                region assumed to be uniform (e.g., white matter)
% poly_degree  : degree of the 3D polynomial (default = 3)
% -------------------------------------------------------------------------
% OUTPUTS
% -------------------------------------------------------------------------
% img_corrected   : bias-corrected 3D image
% bias_field      : estimated 3D bias field
% -------------------------------------------------------------------------
% Elior Drori, Mezer Lab, The Hebrew University of Jerusalem (2023)
% -------------------------------------------------------------------------

% Check for required dependency (PolyfitnTools)
if ~exist('polyfitn', 'file') || ~exist('polyvaln', 'file')
    error(['Required toolbox "PolyfitnTools" not found. ' ...
           'Please install it from MATLAB File Exchange: ' ...
           'https://www.mathworks.com/matlabcentral/fileexchange/34765-polyfitn']);
end

% Handle default inputs
if ~exist('poly_degree','var') || isempty(poly_degree)
    poly_degree = 3;
end
if ~exist('wm_mask','var') || isempty(wm_mask)
    wm_mask = true(size(img));
end
wm_mask = logical(wm_mask);

fprintf('[MRI_UNBIAS]: Estimating and correcting biased image using %d-degree 3D polynomial...',poly_degree)

% Prepare coordinate grids
[i, j, k] = size(img);
[xgrid, ygrid, zgrid] = ndgrid(1:i, 1:j, 1:k);

% Flatten grids for polynomial fitting
x = xgrid(:);
y = ygrid(:);
z = zgrid(:);

% Extract masked voxels
vox_masked = img(wm_mask);
x_masked = xgrid(wm_mask);
y_masked = ygrid(wm_mask);
z_masked = zgrid(wm_mask);

% Polynomial fitting
poly_model = polyfitn([x_masked, y_masked, z_masked], vox_masked, poly_degree);

% Evaluate polynomial over entire image
bias_field = reshape(polyvaln(poly_model, [x, y, z]), size(xgrid));

% Apply bias correction
img_corrected = img ./ bias_field;
fprintf(' done.\n');