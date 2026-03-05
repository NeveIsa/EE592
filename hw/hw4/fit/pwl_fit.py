import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# Load data from MATLAB file
import re

with open('pwl_fit_data.m', 'r') as f:
    content = f.read()

# Extract x data
x_match = re.search(r'x = \[(.*?)\];', content, re.DOTALL)
x_str = x_match.group(1).replace('\n', '').replace(' ', '')
x_data = np.array([float(val) for val in x_str.split(';') if val.strip()])

# Extract y data
y_match = re.search(r'y = \[(.*?)\];', content, re.DOTALL)
y_str = y_match.group(1).replace('\n', '').replace(' ', '')
y_data = np.array([float(val) for val in y_str.split(';') if val.strip()])

print("Data loaded:")
print(f"  x range: [{x_data.min():.3f}, {x_data.max():.3f}]")
print(f"  y range: [{y_data.min():.3f}, {y_data.max():.3f}]")
print(f"  Number of data points: {len(x_data)}")
print()

def fit_pwl_convex(x_data, y_data, num_internal_knots):
    """
    Fit a convex piecewise-linear function using least squares.

    Uses the slope-based parameterization: f(x) = alpha_i * x + beta_i on [a_{i-1}, a_i]
    Constraints:
    - Continuity at knots
    - Convexity (non-decreasing slopes): slope_{i} <= slope_{i+1}
    """

    # Set up knot points (including endpoints)
    knots = np.linspace(0, 1, num_internal_knots + 2)
    K = len(knots) - 1  # Number of segments

    print(f"Fitting with {num_internal_knots} internal knots (total {len(knots)} knots)")
    print(f"  Knots: {knots}")

    # Initial guess: linear interpolation between endpoints
    m0 = (y_data[-1] - y_data[0]) / (x_data[-1] - x_data[0])
    b0 = y_data[0]

    # Parameters: slopes s_i and intercepts b_i for each segment
    # We have K segments, so 2K parameters
    # Order: [s_0, b_0, s_1, b_1, ..., s_{K-1}, b_{K-1}]
    x0 = np.zeros(2*K)
    for i in range(K):
        x0[2*i] = m0  # slope
        x0[2*i + 1] = b0 + m0 * knots[i]  # intercept adjusted for knot position

    def objective(params):
        """Least squares fitting error"""
        error = 0
        for i, (xi, yi) in enumerate(zip(x_data, y_data)):
            # Find which segment xi belongs to
            seg = np.searchsorted(knots, xi) - 1
            seg = np.clip(seg, 0, K-1)

            # Evaluate piecewise linear function
            s_i = params[2*seg]
            b_i = params[2*seg + 1]
            f_xi = s_i * xi + b_i

            error += (f_xi - yi)**2
        return error

    def continuity_constraints(params):
        """Ensure continuity at knots: f_{i-1}(a_i) = f_i(a_i)"""
        constraints = []
        for i in range(1, K):
            a_i = knots[i]
            # Left side: segment i-1
            f_left = params[2*(i-1)] * a_i + params[2*(i-1) + 1]
            # Right side: segment i
            f_right = params[2*i] * a_i + params[2*i + 1]
            constraints.append(f_left - f_right)
        return np.array(constraints)

    def convexity_constraint(params):
        """Ensure convexity: slope_i <= slope_{i+1}"""
        constraints = []
        for i in range(K-1):
            slope_i = params[2*i]
            slope_next = params[2*(i+1)]
            constraints.append(slope_next - slope_i)  # Should be >= 0
        return np.array(constraints)

    # Set up constraints for scipy.optimize.minimize
    cons = []

    # Continuity constraints: g(x) = 0
    for i in range(1, K):
        cons.append({
            'type': 'eq',
            'fun': lambda params, seg=i: (
                params[2*(seg-1)] * knots[seg] + params[2*(seg-1) + 1] -
                (params[2*seg] * knots[seg] + params[2*seg + 1])
            )
        })

    # Convexity constraints: g(x) >= 0
    for i in range(K-1):
        cons.append({
            'type': 'ineq',
            'fun': lambda params, seg=i: params[2*(seg+1)] - params[2*seg]
        })

    # Optimize
    result = minimize(objective, x0, method='SLSQP', constraints=cons,
                     options={'ftol': 1e-10, 'maxiter': 1000})

    if not result.success:
        print(f"  Warning: Optimization did not converge: {result.message}")

    params = result.x
    cost = result.fun

    return knots, params, cost

def evaluate_pwl(x, knots, params):
    """Evaluate piecewise-linear function at point x"""
    K = len(knots) - 1
    seg = np.searchsorted(knots, x) - 1
    seg = np.clip(seg, 0, K-1)

    s_i = params[2*seg]
    b_i = params[2*seg + 1]
    return s_i * x + b_i

# First, fit the affine case (0 internal knots)
print("=" * 70)
print("FITTING RESULTS")
print("=" * 70)
print()

# Affine fit (a = (0, 1), no internal knots)
print("Affine fit (0 internal knots):")
knots_affine = np.array([0.0, 1.0])
# For affine: f(x) = alpha * x + beta
# We want to minimize sum((alpha * x_i + beta - y_i)^2)
# This is a least-squares problem
A_affine = np.column_stack([x_data, np.ones_like(x_data)])
params_affine, _, _, _ = np.linalg.lstsq(A_affine, y_data, rcond=None)
alpha_affine, beta_affine = params_affine
cost_affine = np.sum((params_affine[0] * x_data + params_affine[1] - y_data)**2)
results = [(0, knots_affine, np.array([alpha_affine, beta_affine]), cost_affine)]
print(f"  Knots: {knots_affine}")
print(f"  Least-squares fitting cost: {cost_affine:.6f}")
print(f"  f(x) = {alpha_affine:.5f} * x + ({beta_affine:.5f})")
print()

# Fit with 1, 2, and 3 internal knots
for num_knots in [1, 2, 3]:
    knots, params, cost = fit_pwl_convex(x_data, y_data, num_knots)
    results.append((num_knots, knots, params, cost))
    print(f"  Least-squares fitting cost: {cost:.6f}")
    print()

# Create plots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for idx, (num_knots, knots, params, cost) in enumerate(results):
    ax = axes[idx]

    # Plot data points
    ax.scatter(x_data, y_data, s=30, alpha=0.6, color='blue', label='Data points')

    # Plot fitted function
    x_fine = np.linspace(0, 1, 500)
    if num_knots == 0:
        # Affine case
        y_fine = np.array([params[0] * xi + params[1] for xi in x_fine])
    else:
        y_fine = np.array([evaluate_pwl(xi, knots, params) for xi in x_fine])
    ax.plot(x_fine, y_fine, 'r-', linewidth=2, label='PWL fit')

    # Plot and mark knots
    if num_knots == 0:
        y_knots = np.array([params[0] * k + params[1] for k in knots])
    else:
        y_knots = np.array([evaluate_pwl(k, knots, params) for k in knots])
    ax.plot(knots, y_knots, 'go', markersize=8, label='Knots', markerfacecolor='none',
            markeredgewidth=2)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    if num_knots == 0:
        ax.set_title(f'Affine fit (0 internal knots)\nCost: {cost:.6f}')
    else:
        ax.set_title(f'{num_knots} internal knot(s)\nCost: {cost:.6f}')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('pwl_fit_results.png', dpi=150, bbox_inches='tight')
print("Plot saved to pwl_fit_results.png")
plt.show()

# Print function coefficients
print("\nFitted function coefficients: f(x) = max_i(alpha_i * x + beta_i)")
print("=" * 70)
for num_knots, knots, params, cost in results:
    K = len(knots) - 1
    if num_knots == 0:
        print(f"\nAffine fit (0 internal knots) - Cost: {cost:.6f}")
        alpha_i = params[0]
        beta_i = params[1]
        print(f"  f(x) = {alpha_i:8.5f} * x + ({beta_i:8.5f})")
    else:
        print(f"\n{num_knots} internal knot(s) - Cost: {cost:.6f}")
        print("  Segments:")
        for i in range(K):
            alpha_i = params[2*i]
            beta_i = params[2*i + 1]
            print(f"    f_{i}(x) = {alpha_i:8.5f} * x + ({beta_i:8.5f})")
        print(f"  f(x) = max( ", end="")
        terms = []
        for i in range(K):
            alpha_i = params[2*i]
            beta_i = params[2*i + 1]
            terms.append(f"{alpha_i:8.5f}*x + {beta_i:8.5f}")
        print(" , ".join(terms) + " )")
