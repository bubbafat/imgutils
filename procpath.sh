#!/bin/zsh

for file in $1/*.jpg; python frame.py -input $file -output $file:h/framed/$file:t -caption "{Make} {Model} {LensModel}" -caption "{FocalLength}mm 1/{ExposureTime}, f/{FNumber}, ISO: {ISOSpeedRatings}" -font Helvetica -method 8% 

