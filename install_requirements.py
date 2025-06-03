import subprocess
import sys

REQUIRED_PACKAGES = [
    'pandas',
    'numpy',
    'matplotlib',
    'seaborn',
    'PyQt5',
    'pyperclip',
    'svgwrite',
    'requests',
]

def ensure_pip():
    try:
        import pip
    except ImportError:
        print("pip is not installed. Attempting to install pip...")
        import urllib.request
        import os
        import tempfile
        get_pip_url = 'https://bootstrap.pypa.io/get-pip.py'
        with tempfile.TemporaryDirectory() as tmpdir:
            get_pip_path = os.path.join(tmpdir, 'get-pip.py')
            urllib.request.urlretrieve(get_pip_url, get_pip_path)
            subprocess.check_call([sys.executable, get_pip_path])
        print("pip installed successfully.")

def install_missing_packages():
    import importlib
    ensure_pip()
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            # Handle PyQt5 special import
            if pkg == 'PyQt5':
                importlib.import_module('PyQt5.QtWidgets')
            else:
                importlib.import_module(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"Installing missing packages: {missing}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])
    else:
        print("All required packages are already installed.")

if __name__ == '__main__':
    install_missing_packages()
