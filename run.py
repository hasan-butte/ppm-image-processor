import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CPP_DIR = ROOT / "cpp"
PYTHON_DIR = ROOT / "python"

CPP_BINARY = CPP_DIR / "ppm_csolution"
CPP_SOURCES = [CPP_DIR / "Image.cpp", CPP_DIR / "PPMImage.cpp", CPP_DIR / "ppm_csolution.cpp"]
PYTHON_SCRIPT = PYTHON_DIR / "ppm_psolution.py"


def cpp_binary_is_stale():
    if not CPP_BINARY.exists():
        return True
    binary_mtime = CPP_BINARY.stat().st_mtime
    watched = list(CPP_DIR.glob("*.cpp")) + list(CPP_DIR.glob("*.h"))
    return any(f.stat().st_mtime > binary_mtime for f in watched)


def compile_cpp():
    print("Compiling C++ solution...", flush=True)
    cmd = ["g++", "-std=c++17", "-O2", "-o", str(CPP_BINARY)] + [str(s) for s in CPP_SOURCES]
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print("Error: compilation failed.", file=sys.stderr)
        sys.exit(1)


def run_cpp():
    if cpp_binary_is_stale():
        compile_cpp()
    subprocess.run([str(CPP_BINARY)], cwd=CPP_DIR)


def run_python():
    subprocess.run([sys.executable, str(PYTHON_SCRIPT)], cwd=PYTHON_DIR)


def read_stdin_line():
    # Reads byte-by-byte instead of using input(), which over-reads and
    # buffers ahead when stdin is piped rather than a live terminal. That
    # would swallow input meant for the subprocess launched right after.
    chars = []
    while True:
        b = os.read(0, 1)
        if not b or b == b"\n":
            break
        chars.append(b.decode())
    return "".join(chars)


def main():
    print("Which solution would you like to run?")
    print("1) C++")
    print("2) Python")
    print("> ", end="", flush=True)
    choice = read_stdin_line().strip()

    if choice == "1":
        run_cpp()
    elif choice == "2":
        run_python()
    else:
        print("Invalid choice.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
