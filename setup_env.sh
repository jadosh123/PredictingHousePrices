#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# Define the list of Python packages to install
PACKAGES=(
    "matplotlib"
    "seaborn"
    "pandas"
    "jupyter"
    "kaggle"
    "tensorflow_decision_forests"
    "numpy"
    "sklearn"
)

# Define the name for the virtual environment directory
VENV_DIR=".venv"

# --- Script Logic ---

echo "Starting Python environment setup..."

# 1. Check if python3 is available
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 command could not be found. Please install Python 3."
    exit 1
fi
echo "Found Python 3 installation."

# 2. Check if the virtual environment directory already exists
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment '$VENV_DIR' already exists. Skipping creation."
else
    # 3. Create the virtual environment
    echo "Creating virtual environment named '$VENV_DIR'..."
    python3 -m venv "$VENV_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
    echo "Virtual environment created successfully."
fi

# 4. Define the path to the pip executable within the virtual environment
# This ensures packages are installed in the correct environment,
# regardless of whether the environment is activated in the current shell.
VENV_PIP="$VENV_DIR/bin/pip"

# Check if the venv pip exists
if [ ! -f "$VENV_PIP" ]; then
    echo "Error: Could not find pip executable at '$VENV_PIP'."
    echo "Virtual environment setup might be incomplete."
    exit 1
fi

# 5. Install the packages using the virtual environment's pip
echo "Installing packages into '$VENV_DIR'..."
# Convert package array into a space-separated string for pip
package_list="${PACKAGES[*]}"
"$VENV_PIP" install $package_list

if [ $? -ne 0 ]; then
    echo "Error: Failed to install one or more packages."
    exit 1
fi
echo "All packages installed successfully."

# --- Completion ---
echo ""
echo "--------------------------------------------------"
echo "Setup complete!"
echo "To activate the virtual environment, run:"
echo "source $VENV_DIR/bin/activate"
echo "--------------------------------------------------"

exit 0
