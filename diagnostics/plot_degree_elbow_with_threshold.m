function fig = plot_degree_elbow_with_threshold(degrees, std_vals, threshold_pct)
% -------------------------------------------------------------------------
% PLOT_DEGREE_ELBOW_WITH_THRESHOLD
%
% Plots WM standard deviation (or CoV) versus polynomial degree,
% along with relative improvement (%) and a threshold for diminishing returns.
%
% It highlights:
%   • The "elbow degree"  → first degree where improvement < threshold
%   • The "chosen degree" → previous degree (last meaningful improvement)
%
% INPUTS:
%   degrees       : vector of polynomial degrees tested
%   std_vals      : WM std or CoV per degree (lower = better)
%   threshold_pct : improvement threshold (%) for stopping criterion
%
% EXAMPLE:
%   plot_degree_elbow_with_threshold(1:6, [0.12 0.10 0.099 0.098 0.097 0.096], 10)
%
% -------------------------------------------------------------------------
% Elior Drori, Mezer Lab 2025
% -------------------------------------------------------------------------

if nargin < 3
    threshold_pct = 10; % default 10%
end

% Compute positive improvements (% decrease in std)
rel_improvement = -diff(std_vals) ./ std_vals(1:end-1) * 100;

% Detect elbow (first drop below threshold)
below_thresh = find(rel_improvement < threshold_pct, 1, 'first');

if ~isempty(below_thresh)
    elbow_degree = degrees(below_thresh + 1); % first failing degree
    best_degree  = degrees(below_thresh);     % previous (kept) degree
else
    elbow_degree = NaN;
    best_degree  = degrees(end);
end

% Create figure
fig = figure('Name','Polynomial Degree Elbow Analysis','Color','w','WindowState','maximized');
FontSize = 18;
yyaxis left
plot(degrees, std_vals, '-o','LineWidth',1);
ylabel('WM std (or CoV)'); hold on;
ax = gca;
ax.FontSize = FontSize;
ax.YLim(1) = 0;
yyaxis right
h=plot(degrees(2:end), rel_improvement, '--','LineWidth',1);
ylabel('Improvement (%)');
xlabel('Polynomial Degree');
title(sprintf('Elbow Analysis (Threshold = %.1f%%)', threshold_pct));
grid on
axis square

% Threshold line
yline(threshold_pct, '-', sprintf('Threshold: Δstd = %.1f%%', threshold_pct), ...
    'LabelHorizontalAlignment','left','LabelVerticalAlignment','bottom',...
    'Color',h.Color,'FontSize',FontSize);

% Mark elbow and chosen degrees
if ~isnan(elbow_degree)
    xline(elbow_degree, 'k:', sprintf('Elbow = %d', elbow_degree),'FontSize',FontSize);
end
xline(best_degree, 'k:', sprintf('Chosen = %d', best_degree),'FontSize',FontSize);
% Legend
legend({'std','Δstd (%)'}, 'Location','east','FontSize',FontSize);

% Annotate points with improvement values
for ii = 1:length(rel_improvement)
    hor = 'left';
    if ii == length(rel_improvement)
        hor = 'right';
    end
    text(degrees(ii+1), rel_improvement(ii), sprintf('%.1f%%', rel_improvement(ii)), ...
        'VerticalAlignment','top','HorizontalAlignment',hor,'FontSize',FontSize);
end

% Print summary
fprintf('\n[Elbow Analysis Results]\n');
fprintf(' Improvement threshold = %.1f%%\n', threshold_pct);
if ~isnan(elbow_degree)
    fprintf(' → Elbow degree   = %d (first below threshold)\n', elbow_degree);
    fprintf(' → Chosen degree  = %d (last meaningful improvement)\n', best_degree);
else
    fprintf(' → No elbow detected below %.1f%%; using max tested degree = %d\n', ...
        threshold_pct, best_degree);
end
fprintf(' ------------------------------------------------------\n\n');

end
