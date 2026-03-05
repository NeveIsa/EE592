% sol.m
% Total variation image interpolation solution.
% Implements both L2 and total variation methods using iterative optimization.

% Load original image and setup
Uorig = double(imread('tv_img_interp.png'));
[m, n] = size(Uorig);

% Create 50% mask of known pixels.
rand('state', 1029);
Known = rand(m,n) > 0.5;

fprintf('Image size: %d x %d\n', m, n);
fprintf('Known pixels: %d (%.1f%%)\n', nnz(Known), 100*nnz(Known)/(m*n));

% ========== L2 Variation Interpolation ==========
% Minimize: sum((U(i,j) - U(i-1,j))^2 + (U(i,j) - U(i,j-1))^2)
% subject to: U(i,j) = Uorig(i,j) for (i,j) in Known
% This is equivalent to solving a linear system via iterative smoothing.

fprintf('\nSolving L2 Variation...\n');
Ul2 = Uorig .* Known + mean(Uorig(Known)) * ~Known;

% Iterative gradient descent / smoothing
max_iter = 500;
lambda = 0.1;  % step size
tol = 1e-6;

for iter = 1:max_iter
    % Gradient of L2 variation objective
    dU = zeros(m, n);

    % Vertical differences
    for i = 2:m
        for j = 1:n
            dU(i,j) = dU(i,j) + 2*(Ul2(i,j) - Ul2(i-1,j));
            dU(i-1,j) = dU(i-1,j) - 2*(Ul2(i,j) - Ul2(i-1,j));
        end
    end

    % Horizontal differences
    for i = 1:m
        for j = 2:n
            dU(i,j) = dU(i,j) + 2*(Ul2(i,j) - Ul2(i,j-1));
            dU(i,j-1) = dU(i,j-1) - 2*(Ul2(i,j) - Ul2(i,j-1));
        end
    end

    % Update (only unknown pixels)
    Ul2_old = Ul2;
    Ul2(~Known) = Ul2(~Known) - lambda * dU(~Known);

    % Check convergence
    if mod(iter, 100) == 0
        change = norm(Ul2 - Ul2_old, 'fro') / norm(Ul2_old, 'fro');
        fprintf('  Iteration %d, Change: %.2e\n', iter, change);
        if change < tol
            fprintf('  Converged at iteration %d\n', iter);
            break;
        end
    end
end

% ========== Total Variation Interpolation ==========
% Minimize: sum(|U(i,j) - U(i-1,j)| + |U(i,j) - U(i,j-1)|)
% Using proximal gradient descent with smoothed absolute value

fprintf('\nSolving Total Variation...\n');
Utv = Uorig .* Known + mean(Uorig(Known)) * ~Known;

max_iter_tv = 500;
lambda_tv = 0.05;
epsilon = 1e-3;  % smoothing parameter for absolute value

for iter = 1:max_iter_tv
    % Smoothed gradient of TV objective
    % |x| ≈ sqrt(x^2 + epsilon^2) for small epsilon
    dU = zeros(m, n);

    % Vertical differences with smoothed absolute value
    for i = 2:m
        for j = 1:n
            diff = Utv(i,j) - Utv(i-1,j);
            grad = diff / sqrt(diff^2 + epsilon^2);
            dU(i,j) = dU(i,j) + grad;
            dU(i-1,j) = dU(i-1,j) - grad;
        end
    end

    % Horizontal differences
    for i = 1:m
        for j = 2:n
            diff = Utv(i,j) - Utv(i,j-1);
            grad = diff / sqrt(diff^2 + epsilon^2);
            dU(i,j) = dU(i,j) + grad;
            dU(i,j-1) = dU(i,j-1) - grad;
        end
    end

    % Update (only unknown pixels)
    Utv_old = Utv;
    Utv(~Known) = Utv(~Known) - lambda_tv * dU(~Known);

    % Check convergence
    if mod(iter, 100) == 0
        change = norm(Utv - Utv_old, 'fro') / norm(Utv_old, 'fro');
        fprintf('  Iteration %d, Change: %.2e\n', iter, change);
        if change < tol
            fprintf('  Converged at iteration %d\n', iter);
            break;
        end
    end
end

% ========== Visualization ==========
% Create figure with masked image, L2 reconstruction, TV reconstruction, and original
figure(1); clf;
colormap gray;

% Masked (obscured) image - shows only known pixels
subplot(2,2,1);
imagesc(Known.*Uorig + 256-150*Known);
title('Masked Image (50% Known)');
axis image;
colorbar;

% L2 reconstructed image
subplot(2,2,2);
imagesc(Ul2);
title('L_2 Reconstruction');
axis image;
colorbar;

% Total variation reconstructed image
subplot(2,2,3);
imagesc(Utv);
title('Total Variation Reconstruction');
axis image;
colorbar;

% Original image
subplot(2,2,4);
imagesc(Uorig);
title('Original Image');
axis image;
colorbar;

% Save figure to file
saveas(gcf, 'reconstruction_results.png');
fprintf('\nPlot saved to reconstruction_results.png\n');

% Display reconstruction errors
l2_error = norm(Ul2(~Known) - Uorig(~Known)) / norm(Uorig(~Known));
tv_error = norm(Utv(~Known) - Uorig(~Known)) / norm(Uorig(~Known));

fprintf('\nReconstruction Errors (on unknown pixels):\n');
fprintf('L2 Variation: %.4f\n', l2_error);
fprintf('Total Variation: %.4f\n', tv_error);
