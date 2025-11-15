#!/usr/bin/env python3
"""
Simple script to run the Streamlit app
"""

import subprocess
import sys
import os

if __name__ == "__main__":
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to script directory
    os.chdir(script_dir)
    
    # Run streamlit
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])

