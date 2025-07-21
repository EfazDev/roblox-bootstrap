import platform
import subprocess
import sys
import os
current_path_location = os.path.dirname(os.path.abspath(__file__))
if platform.system() == "Windows": subprocess.run([sys.executable, "Main.py"], cwd=current_path_location, shell=False)
elif platform.system() == "Darwin" and not ("--update-mode" in sys.argv): subprocess.run([sys.executable, "Main.py", "-s"], cwd=current_path_location, shell=False)