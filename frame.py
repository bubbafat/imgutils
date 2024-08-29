import pathlib
import os
import math
import argparse
import subprocess
from PIL import Image

magick='magick'

def add_frame(input, output, line1, line2):
    image = Image.open(input)

    phi = 1.618033
    l,w = image.size
    frame_width = int((math.sqrt(math.pow(l+w,2) + ((4*l*w)/phi)) - l - w) / 4)
    fontsize = int(frame_width / 6)
    line_spacing = fontsize / 3
    fontname = "Verdana"
    line1_offset = int(frame_width - fontsize - line_spacing)
    line2_offset = int(line1_offset - fontsize - line_spacing)

    line1 = line1.replace('\'', '\'\'')
    line2 = line2.replace('\'', '\'\'')

    command = f"""{magick} \\
            {image.filename} \\
            -write mpr:orig \\
            +delete \\
            mpr:orig -bordercolor White -border {frame_width} +write mpr:border +delete \\
            mpr:border -gravity Southwest -pointsize {fontsize} -font {fontname} -fill Black -draw \'text {frame_width},{line1_offset} \"{line1}\"\' +write mpr:line1 +delete \\
            mpr:line1 -gravity Southwest -pointsize {fontsize} -font {fontname} -fill Black -draw \'text {frame_width},{line2_offset} \"{line2}\"\' \\
            {output}            
    """

    return command

parser = argparse.ArgumentParser("frame")
parser.add_argument("input", help="The image to add a frame to")
parser.add_argument("output", help="The image to create")
parser.add_argument("line1", help="The top line caption")
parser.add_argument("line2", help="The second line caption")
args = parser.parse_args()

command = add_frame(args.input, args.output, args.line1, args.line2)

pathlib.Path(args.output).unlink(missing_ok=True)

print(command)

p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()  
p_status = p.wait()
