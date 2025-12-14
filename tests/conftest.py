# tests/conftest.py
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # repo root
root_str = str(ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)
