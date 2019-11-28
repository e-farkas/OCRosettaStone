import subprocess
import sys

if __name__ == "__main__":

    subprocess.call(["python", "text_detection.py", sys.argv[1]])
    subprocess.call(["tesseract", "cropped_py.jpg", "out", "--psm", "11"])
    subprocess.call(["python", "text_process.py", "out.txt"])
