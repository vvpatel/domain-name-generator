#!/usr/bin/env python3
"""
Simple runner script to execute the domain name generator from project root.
"""
import sys
import os

# Add src to path
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_dir)

# Import and run main
from generate_themed_names import main

if __name__ == '__main__':
    main()
