"""Rebuild every items/statements/Dxx.json and clarity/Dxx.json from the topic scripts here."""
import runpy
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
for p in sorted(HERE.glob("D*.py")):
    runpy.run_path(str(p), run_name="__main__")
    print("wrote", p.stem)
