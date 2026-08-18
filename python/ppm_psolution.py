import sys
from pathlib import Path
def readImgPPM(fileName):

    # parse header information  
    with open(fileName, "r") as file: 
        magic = file.readline().strip()
        if magic != "P3": 
            raise ValueError("Error: Unsupported PPM format")
        dimensionLine = file.readline() 
        dimensions = dimensionLine.split()
        if(len(dimensions) != 2):
            raise ValueError("Error: Incorrectly formatted image dimensions")
        width = int(dimensions[0])
        height = int(dimensions[1])
        maxColorLine = file.readline().strip() 
        maxColor = int(maxColorLine) 
        if width <= 0 or height <= 0 or maxColor <= 0: 
            raise ValueError ("Error: Incorrectly formatted PPM image header")

        # get pixels 
        indColors = [
            int(num)
            for line in file 
            for num in line.split() 
        ]

        if len(indColors) % 3 != 0: 
            raise ValueError("Error: Incorrectly formatted pixel data in PPM image")

        pixelArray = [
            (indColors[i], indColors[i+1], indColors[i+2])
            for i in range (0, len(indColors), 3) ]

        # normalize to 8-bit color scheme
        if maxColor != 255:
            scalar = 255.0 / maxColor 
            scaled_pixels = [] 
            for (r,g,b) in pixelArray:
                sr = int((r * scalar) + 0.5)
                sg = int((g * scalar) + 0.5)
                sb = int((b * scalar) + 0.5)
                scaled_pixels.append((sr, sg, sb))
            pixelArray = scaled_pixels 
    
    return (width, height, pixelArray) # represents the generic image type

def writeImgPPM(fileName, sourcePPM):
    width, height, pixelArray = sourcePPM
    with open(fileName, "w") as file: 
        # generic header informaiton
        file.write("P3\n")
        file.write(f"{width} {height}\n")
        file.write("255\n")
        for (r,g,b) in pixelArray: 
            file.write(f"{r} {g} {b}\n")

# generic reads and writes for all image types
READERS = {
    "ppm": readImgPPM
     #additional readers can go here 
 }

WRITERS = {
    "ppm": writeImgPPM
    # additional writers can go here 
}

# generic function implementations using above dictionaries
def readImage (fileName, fmt="ppm"):
    return READERS[fmt](fileName)

def writeImage(fileName, image, fmt="ppm"): 
    return WRITERS[fmt](fileName, image)

# Filters:

def grayscale(image): 
    width, height, pixelArray = image
    grayArray = []
    for (r,g,b) in pixelArray: 
        greyColor = (r + g + b) // 3
        grayArray.append((greyColor, greyColor, greyColor))
    return (width, height, grayArray)

def invert(image): 
    width, height, pixelArray = image
    maxColor = 255
    invertedArray = [ 
        ((maxColor - r), (maxColor - g), (maxColor - b))
        for (r, g, b) in pixelArray
    ]
    return (width, height, invertedArray)

def hflip(image): 
    width, height, pixelArray = image
    flippedArray = list(pixelArray)

    for i in range(height): 
        for j in range(width // 2): 
            first = (i * width) + j
            mirror = (i * width) + (width - j - 1)
            flippedArray[first], flippedArray[mirror] = flippedArray[mirror], flippedArray[first]

    return (width, height, flippedArray)

METHODS = {
    1: (grayscale, "_grayed"),
    2: (invert, "_inverted"),
    3: (hflip, "_hflipped"),
}

def listFileNames(dirPath):
    files = [p.stem for p in Path(dirPath).iterdir() if p.is_file() and p.suffix == ".ppm"]
    files.sort()
    return files

    
def main():
    INPUT_DIR = "../tests/input/"
    OUTPUT_DIR = "../tests/output_python/"

    fileNames = listFileNames(INPUT_DIR)

    keepGoing = True
    while keepGoing:
        print("Please select an image from the following inputs (1, 2, ...):")
        for i, name in enumerate(fileNames):
            print(f"{i + 1}. {name}")

        try:
            selectedFile = int(input())
        except ValueError:
            print("Error: Invalid image selection.", file=sys.stderr)
            sys.exit(1)

        if selectedFile < 1 or selectedFile > len(fileNames):
            print("Error: Invalid image selection.", file=sys.stderr)
            sys.exit(1)

        imgName = fileNames[selectedFile - 1]

        try:
            initImg = readImage(INPUT_DIR + imgName + ".ppm")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        print("What do you want to do with the image (pick a number)?\n1. Remove Color \n2. Invert Color\n3. Flip Horizontally")

        try:
            methodNum = int(input())
        except ValueError:
            print("Error: Invalid method selection.", file=sys.stderr)
            sys.exit(1)

        if methodNum < 1 or methodNum > 3:
            print("Error: Invalid method selection.", file=sys.stderr)
            sys.exit(1)

        execMethod, suffix = METHODS[methodNum]
        prodImg = execMethod(initImg)
        newImgName = imgName + suffix + ".ppm"
        writeImage(OUTPUT_DIR + newImgName, prodImg)
        print(f"Output written to {OUTPUT_DIR + newImgName}")

        again = input("Process another image? (y/n): ").strip()
        if not again:
            print("Error: Invalid response.", file=sys.stderr)
            sys.exit(1)
        keepGoing = again[0] in ("y", "Y")

    print("Done.")

if __name__ == "__main__": 
    main() 