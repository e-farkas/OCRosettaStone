import sys
import os

filepath = sys.argv[1]

if not os.path.isfile(filepath):
    print("File does not exist")
    sys.exit()

with open(filepath) as fp:
    lines = fp.readlines()

with open(filepath, "w") as fp:
    fp.writelines([item for item in lines[:-1]])

file_str = ''
with open(filepath) as fp:
    file_str = fp.read()
    file_str = ''.join([i for i in file_str if i.isalnum() or i.isspace() ])

with open(filepath, "w") as fp:
    fp.write(file_str)
