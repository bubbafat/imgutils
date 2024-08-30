import pathlib
import os
import math
import argparse
import subprocess
from PIL import Image
from PIL.ExifTags import TAGS
from PIL import ExifTags


magick='magick'

def get_frame_size(image, method):
    if method == "golden":
        phi = 1.618033
        l,w = image.size
        return int((math.sqrt(math.pow(l+w,2) + ((4*l*w)/phi)) - l - w) / 4)
        
    if method.endswith('%'):
        pct = int(method[:-1])
        return max(image.size) * (pct / 100)
    
    return int(method)


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

def add_frame(config):
    image = Image.open(config.input)

    frame_width = get_frame_size(image, config.method)

    # adapt font size by the number of lines but never more than 1/4 of the framing height
    fontsize = 0
    line_spacing = 0

    if config.caption and len(config.caption) > 0:
        fontsize = min(int(frame_width / (len(config.caption)*2)), frame_width / 4)
        line_spacing = fontsize / 3

    fontname = config.font

    command = f"""{magick} \\
            {image.filename} \\
            -write mpr:orig \\
            +delete \\
            mpr:orig -bordercolor {config.color} -border {frame_width} +write mpr:border"""

    line_offset = int(frame_width - fontsize - line_spacing)

    if config.caption:
        for line in config.caption:
            if line == "exif":
                line = get_exif_line(image)

            if line:
                command += " +delete \\\n"
                line = line.replace('\'', '\'\'')
                command += f"mpr:border -gravity Southwest -pointsize {fontsize} -font {fontname} -fill {config.fontcolor} -draw \'text {frame_width},{line_offset} \"{line}\"\' +write mpr:border"
                line_offset = int(line_offset - fontsize - line_spacing)

    command += f" {config.output}"
    return command

parser = argparse.ArgumentParser("frame")
parser.add_argument("-input", help="The image to add a frame to", required=True)
parser.add_argument("-output", help="The image to create", required=True)
parser.add_argument("-method", help="The framing method. (golden | N% | N)", default='golden')
parser.add_argument("-caption", help="A caption line", action='append', required=False)
parser.add_argument("-font", help="The name of the font to use (default: Arial))", required=False, default="Arial")
parser.add_argument("-color", help="The color of the border (default: White)", required=False, default="White")
parser.add_argument("-fontcolor", help="The color of the font (default: Black)", required=False, default="Black")
args = parser.parse_args()

command = add_frame(args)

pathlib.Path(args.output).unlink(missing_ok=True)
subdir = os.path.split(args.output)[0]

if subdir:
    os.makedirs(subdir, exist_ok=True)

print(command)

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()  
p_status = p.wait()
