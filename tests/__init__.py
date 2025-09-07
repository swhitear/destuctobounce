import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(f"Adding {project_root} to Python path")  # Debug print
sys.path.append(project_root)
print("Python path is now:", sys.path)  # Debug print