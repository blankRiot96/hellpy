import subprocess
import sys

with open("test_ip.txt") as f:
    ip = f.read()


subprocess.run(
    [sys.executable, "main.py", f"--ip={ip}", "--window=1", "--model-id=CUBE_MAN"]
)
