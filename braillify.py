#!./venv/bin/python
# -*- coding: utf-8 -*-
#  Copyright (c) Eugene Pisarchick 2019. Distributed under GPL 3.0, see LICENSE.txt

import time

import PIL.Image
import PIL.ImageEnhance
import argparse
import numpy as np

parser = argparse.ArgumentParser(
    description="A little program that converts images to braille patterns. Distributed under GPL 3.0",
    epilog="example usage: ./braillify.py -i sample.jpg -s=0.9 -w 60 -t")
parser.add_argument("-i", dest="source", required=True,
                    help="path to the image (required)")
parser.add_argument("--inv", dest="invert", action="store_const", const=False, default=True,
                    help="invert image")
parser.add_argument("-t", dest="time", action="store_const", const=True, default=False,
                    help="print execution time after completion")
parser.add_argument("-w", dest="width", type=int, required=False, default=40,
                    help="output width, in characters (40 by default)")
parser.add_argument("-s", dest="stretch_y", type=float, required=False, default=1,
                    help="factor for scaling the image vertically (1 by default)")
parser.add_argument("-c", dest="contrast", type=float, required=False, default=1,
                    help="additional contrast (1 by default)")
parser.add_argument("-o", dest="output", required=False, default="",
                    help="output file (prints to STDOUT by default)")

args = parser.parse_args()
# print(args)

source = args.source
stretch_y = args.stretch_y
width = args.width
contrast = args.contrast
output = args.output

start = time.perf_counter()
parser.parse_args()
image: PIL.Image.Image = PIL.Image.open(source, "r")

image = image.convert("L")
enchancer = PIL.ImageEnhance.Contrast(image)
image = enchancer.enhance(contrast)

scale = width/(image.size[0]//2)
image = image.resize((2*int((image.size[0]*scale)//2), 4*int((image.size[1]*stretch_y*scale)//4)))

# image.save("preprocess.png")

image = image.convert(mode="1")


def to_braille(img: PIL.Image.Image) -> str:
    # noinspection PyTypeChecker
    brailles = open("braille.txt").readlines()
    brailles = [l[0] for l in brailles]
    pix = np.array(img)
    mat = np.array([[0, 3],
                    [1, 4],
                    [2, 5],
                    [6, 7]])
    mat = 2**mat
    out = ""
    for i in range(0, pix.shape[0], 4):
        for j in range(0, pix.shape[1], 2):
            window: np.array = pix[i:i+4, j:j+2]
            if args.invert:
                window = 1-window
            window = window*mat
            out += brailles[window.sum()]
        out += "\n"
    return out


if output == "":
    print(to_braille(image))
else:
    with open(output, "w+") as f:
        f.write(to_braille(image))

# image.save("output.png")

end = time.perf_counter()
if args.time:
    print(f"Done in {end - start:.3f} s")
