
import importlib
import subprocess
import sys

required_libraries = [
    "pandas", "numpy", "h3==3.7.6", "matplotlib", "seaborn",
    "scikit-learn", "keras", "xgboost", "seaborn", "lightgbm"
]

for lib in required_libraries:
    try:
        importlib.import_module(lib)
        print(f"✔ {lib} is already installed.")
    except ImportError:
        print(f"✘ {lib} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
