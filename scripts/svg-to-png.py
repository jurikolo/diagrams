import argparse
import fnmatch
import logging
import os
import subprocess
import sys

logger = logging.getLogger()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

parser = argparse.ArgumentParser(description="This program resizes SVG files in provided directory and converts to PNG")
parser.add_argument("--dir", default="./",
                    help="Specify directory with SVG files")
args = parser.parse_args()

file_list = []
for path, folders, files in os.walk(args.dir):
    for file in files:
        if fnmatch.fnmatch(file, '*.svg') and not fnmatch.fnmatch(file, '*resized.svg'):
            file_list.append(os.path.join(path, file))

for filename in file_list:
    try:
        subprocess.run(["/bin/rm", filename[:-4] + "-resized" + filename[-4:]])
    except Exception as e:
        logger.debug(e)
    try:
        subprocess.run(["/bin/rm", filename[:-4] + ".png"])
    except Exception as e:
        logger.debug(e)
    subprocess.run(f"rsvg-convert -a --width 256 -f svg {filename} -o {filename[:-4]}-resized{filename[-4:]}", shell=True)
    subprocess.run(f"ffmpeg -i {filename[:-4]}-resized{filename[-4:]} -vf scale=w=256:h=256 {filename[:-4]}.png", shell=True)
    print(filename[:-4] + "-resized" + filename[-4:])
