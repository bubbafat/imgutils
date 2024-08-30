```text
usage: frame [-h] 
              -input INPUT  
              -output OUTPUT 
             [-method METHOD]
             [-caption CAPTION] 
             [-font FONT] 
             [-color COLOR]
             [-fontcolor FONTCOLOR]
```

|Command|Description|
|-------|-----------|
|-input|The input image file.|
|-output|The created file. If it exists it is overwriten.The path is created as needed.|
|-method|One of "golden", "nn%", "nn" - nn% defines the percentage of the longest edge to use as the frame width, "nn" is pixel width. "golden" applies the golden ratio.|
|-caption|A caption line to add to the lower left (aligned with the image). Can be used multiple times. The font size will scale as more lines are added.|
|-font|The font to use. Defaults: Arial|
|-color|The color of the border. Default: White|
|-fontcolor|The color of the caption font. Default: Black|

Example:

```sh
frame -input file.jpg -output framed.jpg
```

This will add a white frame using the default golden ratio with no captions.

```sh
frame -input file.jpg -output framed.jpg -method 7% -caption "This is line one" -caption "This is line two"
```

```sh
frame -input file.jpg -output framed.jpg -font Helvetica -fontcolor Blue -color Yellow -method 7% -caption "This is line one" -caption "This is line two"
```

