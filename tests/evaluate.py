from src.main import compute_linear_regression
import numpy as np
import sys

sys.path.append('./src/')


VERBOSE = False


def noisy_case():
    if VERBOSE:
        print("Noisy case")
    X = np.array(
        [
            [-2.912, 8.045],
            [-1.078, -3.956],
            [5.067, 5.032],
            [7.921, 2.084],
            [-6.935, -7.023],
            [6.912, -9.978],
            [-0.934, 4.056],
            [-5.932, -9.912],
            [-8.045, 8.978],
            [-1.056, 3.089],
        ]
    )
    y = np.array([[16], [-6], [18], [15], [-18],
                 [-10], [10], [-23], [13], [8]])
    ref_weights = np.array([3, 1, 2])  # corresponds to y = 3 + 1*x1 + 2*x2
    try:
        weights, cost = compute_linear_regression(
            X, y, alpha=0.01, max_iterations=10_000
        )
    except Exception as e:
        if VERBOSE:
            print(e)
        return 0
    weight_diff = np.sqrt(np.mean(np.subtract(weights, ref_weights) ** 2))
    if VERBOSE:
        print(f"Weight difference: {weight_diff}")
    if weight_diff < 0.06:
        return 100
    elif weight_diff < 5e-2:
        if VERBOSE:
            print("90")
        return 90
    elif weight_diff < 5e-1:
        if VERBOSE:
            print("80")
        return 80
    else:
        if VERBOSE:
            print("50")
        return 50


def simple_case():
    if VERBOSE:
        print("Simple case")
    X = np.array(
        [
            [-3, 8],
            [-1, -4],
            [5, 5],
            [8, 2],
            [-7, -7],
            [7, -10],
            [-1, 4],
            [-6, -10],
            [-8, 9],
            [-1, 3],
        ]
    )
    y = np.array([[16], [-6], [18], [15], [-18],
                 [-10], [10], [-23], [13], [8]])
    ref_weights = np.array([3, 1, 2])  # corresponds to y = 3 + 1*x1 + 2*x2
    try:
        weights, cost = compute_linear_regression(
            X, y, alpha=0.01, max_iterations=10_000
        )
    except Exception as e:
        if VERBOSE:
            print(e)
        return 0
    weight_diff = np.sqrt(np.mean(np.subtract(weights, ref_weights) ** 2))
    if VERBOSE:
        print(f"Weight difference: {weight_diff}")
    if weight_diff < 5e-4:
        if VERBOSE:
            print("100")
        return 100
    elif weight_diff < 1e-3:
        if VERBOSE:
            print("90")
        return 90
    elif weight_diff < 2e-2:
        if VERBOSE:
            print("80")
        return 80
    else:
        if VERBOSE:
            print("50")
        return 50


if __name__ == "__main__":
    grades = [
        noisy_case(),
        simple_case(),
    ]
    grade = sum(grades) / len(grades)
    print(f"Grade: {grade}")
    print(grades)
