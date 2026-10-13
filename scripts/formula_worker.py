#!/usr/bin/env python3
"""Run the persistent U(1)^f insulator formula worker from any directory."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from insulator.worker import main

if __name__ == '__main__':
    main()
