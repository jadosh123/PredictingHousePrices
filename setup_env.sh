#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
VENV_NAME=".venv" # Name of the virtual environment directory (using .venv is common)
# List of packages to install
PACKAGES=(
    "numpy"
    "matplotlib"
    "seaborn"
    "pandas"
    "jupyter" # Added Jupyter
)

# --- Helper Functions ---
# Function to print informational messages
print_info() {
    echo "INFO: $1"
}

# Function to print success messages
print_success() {
    # Using ANSI escape codes for green color (optional)
    echo -e "\033[0;32mSUCCESS: $1\033[0m"
}

# Function to print error messages and exit
print_error() {
    # Using ANSI escape codes for red color (optional)
    echo -e "\033[0;31mERROR: $1\033[0m" >&2
    exit 1
}

# --- Main Script ---
print_info "Starting environment setup..."
print_info "This script will create a Python virtual environment named '$VENV_NAME'"
print_info "in the current directory and install required packages."
print_info "Make sure you run this script from the root of your project repository."
echo "--------------------------------------------------"

# 1. Check for Python 3
print_info "Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    # If python3 not found, try python
    if ! command -v python &> /dev/null; then
         print_error "Python 3 (or python) command not found. Please install Python 3."
    else
        PYTHON_CMD=$(command -v python)
        # Verify it's Python 3
        if ! $PYTHON_CMD -c 'import sys; exit(0 if sys.version_info.major == 3 else 1)'; then
             print_error "Found 'python', but it's not Python 3. Please install or ensure Python 3 is available as 'python3' or 'python'."
        fi
         print_info "Using 'python' command."
    fi
else
    PYTHON_CMD=$(command -v python3)
    print_info "Using 'python3' command."
fi
print_info "Found Python 3 at: $($PYTHON_CMD -c 'import sys; print(sys.executable)')"
$PYTHON_CMD --version # Print version for confirmation

# 2. Check if the virtual environment directory already exists
if [ -d "$VENV_NAME" ]; then
    print_info "Virtual environment '$VENV_NAME' already exists. Skipping creation."
else
    # 3. Create the virtual environment
    print_info "Creating virtual environment '$VENV_NAME'..."
    if ! $PYTHON_CMD -m venv "$VENV_NAME"; then
        print_error "Failed to create the virtual environment. Check Python installation and permissions."
    fi
    print_success "Virtual environment '$VENV_NAME' created."
fi

# 4. Determine the Python executable path within the venv for installing packages
#    Using the Python executable inside the venv is more reliable than finding pip directly
print_info "Determining Python executable within '$VENV_NAME'..."
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    # Linux or macOS
    PYTHON_IN_VENV="$VENV_NAME/bin/python"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
     # Windows (Git Bash, Cygwin, potentially WSL detecting as Linux)
     PYTHON_IN_VENV="$VENV_NAME/Scripts/python.exe"
else
    # Unknown OS type - make a best guess or error out
    print_info "Warning: Unrecognized OS type '$OSTYPE'. Assuming Linux/macOS style path for venv Python."
    PYTHON_IN_VENV="$VENV_NAME/bin/python"
    # Alternatively: print_error "Unsupported operating system for venv path detection: $OSTYPE"
fi

# Check if the Python executable exists inside the venv
if [ ! -f "$PYTHON_IN_VENV" ]; then
    print_error "Could not find Python executable at expected location: '$PYTHON_IN_VENV'. Venv creation might have failed partially."
fi
print_info "Using Python from venv: $PYTHON_IN_VENV"

# 5. Upgrade pip and Install packages using the venv's Python/pip
print_info "Upgrading pip within the virtual environment..."
# Use '-m pip' which is the recommended way to invoke pip
if ! "$PYTHON_IN_VENV" -m pip install --upgrade pip; then
    print_error "Failed to upgrade pip."
fi

print_info "Installing packages: ${PACKAGES[*]} ..." # [*] expands to separate words
# Use "${PACKAGES[@]}" for safer expansion if package names had spaces (unlikely but good practice)
if ! "$PYTHON_IN_VENV" -m pip install "${PACKAGES[@]}"; then
    print_error "Failed to install one or more packages."
fi
print_success "Required packages installed successfully."

# 6. Provide activation instructions (Critical Step!)
#    The script itself CANNOT activate the environment for the user's parent shell.
#    It runs in a subshell, and environment changes are lost when the script exits.
print_info "--------------------------------------------------"
print_success "Setup script finished!"
print_info "The virtual environment '$VENV_NAME' is ready and packages are installed."
echo ""
print_info "IMPORTANT: You now need to ACTIVATE the environment in your current terminal session."
print_info "Run the appropriate command below from your project root directory:"
echo ""
print_info "On Linux or macOS (bash/zsh):"
echo "  source $VENV_NAME/bin/activate"
echo ""
print_info "On Linux or macOS (fish shell):"
echo "  source $VENV_NAME/bin/activate.fish"
echo ""
print_info "On Windows (Git Bash or MSYS):"
echo "  source $VENV_NAME/Scripts/activate"
echo ""
print_info "On Windows (Command Prompt - cmd.exe):"
echo "  %cd%\\$VENV_NAME\\Scripts\\activate.bat"
echo ""
print_info "On Windows (PowerShell):"
echo "  .\\$VENV_NAME\\Scripts\\Activate.ps1"
print_info "(If PowerShell activation fails due to execution policy, you might need to run:"
print_info " Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)"
echo ""
print_info "Once activated, your terminal prompt should change (e.g., show '(.venv)')"
print_info "indicating you are using the virtual environment."
print_info "To start the classic Jupyter Notebook server, run: jupyter notebook"
print_info "To deactivate later, simply run: deactivate"
print_info "--------------------------------------------------"

exit 0