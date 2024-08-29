import pathlib
import os
import math
import argparse
import subprocess
from PIL import Image
from PIL.ExifTags import TAGS
from PIL import ExifTags


magick='magick'

def get_exif_line(image):
    exif = image.getexif()
    # {TAGS.get(tag): value for tag, value in info.items()}
    data = {}

    for key, value in exif.get_ifd(ExifTags.Base.ExifOffset).items():
        tag = ExifTags.TAGS.get(key, key)
        data[tag] = value

    if any(data):
        return f"{data.get('LensModel', '')} 1/{str(1/data.get('ExposureTime', 1))} f/{data.get('FNumber', '')} - ISO {data.get('ISOSpeedRatings', '')}"

    return None

def add_frame(input, output, line1, line2, line3):
    image = Image.open(input)

    phi = 1.618033
    l,w = image.size
    frame_width = int((math.sqrt(math.pow(l+w,2) + ((4*l*w)/phi)) - l - w) / 4)
    fontsize = int(frame_width / 6)
    line_spacing = fontsize / 3
    fontname = "Verdana"

    lines = [line1, line2, line3]

    command = f"""{magick} \\
            {image.filename} \\
            -write mpr:orig \\
            +delete \\
            mpr:orig -bordercolor White -border {frame_width} +write mpr:border"""

    line_offset = int(frame_width - fontsize - line_spacing)

    for line in lines:
        if line == "exif":
            line = get_exif_line(image)

        if line:
            command += " +delete \\\n"
            line = line.replace('\'', '\'\'')
            command += f"mpr:border -gravity Southwest -pointsize {fontsize} -font {fontname} -fill Black -draw \'text {frame_width},{line_offset} \"{line}\"\' +write mpr:border"
            line_offset = int(line_offset - fontsize - line_spacing)

    command += f" {output}"
    return command

parser = argparse.ArgumentParser("frame")
parser.add_argument("input", help="The image to add a frame to")
parser.add_argument("output", help="The image to create")
parser.add_argument("line1", help="The top line caption")
parser.add_argument("line2", help="The second line caption")
parser.add_argument("line3", help="The third line")
args = parser.parse_args()

command = add_frame(args.input, args.output, args.line1, args.line2, args.line3)

pathlib.Path(args.output).unlink(missing_ok=True)
subdir = os.path.split(args.output)[0]

if subdir:
    os.makedirs(subdir, exist_ok=True)

print(command)

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()  
p_status = p.wait()
