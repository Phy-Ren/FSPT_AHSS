#!/usr/bin/env python3
"""Run the persistent U(1)^f insulator formula worker from any directory."""
from pathlib import Path
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from insulator.worker import main

if __name__ == '__main__':
    profile_directory = os.environ.get('U1_FORMULA_PROFILE_DIR')
    if not profile_directory:
        main()
    else:
        import cProfile
        import socket

        destination = Path(profile_directory)
        destination.mkdir(parents=True, exist_ok=True)
        profile = cProfile.Profile()
        try:
            profile.runcall(main)
        finally:
            profile.dump_stats(str(destination / ('worker-{}-{}.prof'.format(
                socket.gethostname(), os.getpid()))))
