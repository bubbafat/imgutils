#!/bin/zsh

for file in $1/*.jpg; python3 frame.py -input $file -output $file:h/framed/$file:t -caption "{Make} {Model} {LensModel}" -caption "{FocalLength}mm 1/{ExposureTime}, f/{FNumber}, ISO: {ISOSpeedRatings}" -font Helvetica -long 2048 -method 8% 

