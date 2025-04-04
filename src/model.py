import numpy as np


def compute_linear_regression(X, y, alpha=0.01, max_iterations=1000):
    # Add column of ones
    X = np.hstack([np.ones((X.shape[0], 1)), X])

    # Flatten y array to 1 dimensional array
    y = y.flatten()
    n = X.shape[1]
    weights = np.zeros(n)

    # Set tolerance
    tolerance = 1e-6

    for i in range(max_iterations):
        gradients = gradient(X, y, weights)
        weights -= alpha * gradients
        new_cost = compute_cost(X, y, weights)

        # Convergence check
        gradient_magnitude = np.linalg.norm(gradients)
        if gradient_magnitude <= tolerance:
            break

    return weights, new_cost


def compute_cost(X, y, weights):
    # Calculate the cost
    cost = 0
    predictions = np.dot(X, weights)
    residuals = y - predictions
    cost = np.sum(residuals**2) / (2 * len(y))
    return cost


def gradient(X, y, weights):
    # Calculate the bias and weight gradients
    predictions = np.dot(X, weights)
    residuals = y - predictions
    gradients = -2 * np.dot(X.T, residuals) / len(y)
    return gradients


def compute_r_squared(X, y, weights):
    # Add column of ones
    X = np.hstack([np.ones((X.shape[0], 1)), X])

    predictions = np.dot(X, weights)

    # Compute R squared
    residuals_fit = np.sum((y - predictions) ** 2)
    residuals_mean = np.sum((y - np.mean(y)) ** 2)
    r_squared = 1 - (residuals_fit / residuals_mean)
    print("R squared:", r_squared)


def generate_random_linear_dataset(num_samples=100, num_features=2,
                                   noise_std_dev=2.5, random_seed=42):
    np.random.seed(random_seed)

    # True weights and bias (can be adjusted to change relationship)
    true_weights = np.array([3.0, -1.5])
    true_bias = 5.0

    # Generate feature matrix X
    X = np.random.randn(num_samples, num_features) * 5

    y_true = np.dot(X, true_weights) + true_bias
    noise = np.random.randn(num_samples) * noise_std_dev
    y = y_true + noise

    return X, y
