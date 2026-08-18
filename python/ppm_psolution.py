import sys
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
    
def main():
    INPUT_DIR = "../tests/input/"
    OUTPUT_DIR = "../tests/output_python/"

    try: 
        # T1: t1_simple.ppm
        img1 = readImage(INPUT_DIR + "t1_simple.ppm")

        # grayscale
        img1_gray = grayscale(img1)
        writeImage(OUTPUT_DIR + "t1_simple_gray.ppm", img1_gray)

        # invert
        img1_invert = invert(img1)
        writeImage(OUTPUT_DIR + "t1_simple_invert.ppm", img1_invert)

        # horizontal flip
        img1_hflip = hflip(img1)
        writeImage(OUTPUT_DIR + "t1_simple_hflip.ppm", img1_hflip)

    except ValueError as e: 
        print(f"Error: {e}", file=sys.stderr)

    try: 

        # T2: t2_realistic.ppm
        img2 = readImage(INPUT_DIR + "t2_realistic.ppm")

        # grayscale
        img2_gray = grayscale(img2)
        writeImage(OUTPUT_DIR + "t2_realistic_gray.ppm", img2_gray)

        # invert
        img2_invert = invert(img2)
        writeImage(OUTPUT_DIR + "t2_realistic_invert.ppm", img2_invert)

        # horizontal flip
        img2_hflip = hflip(img2)
        writeImage(OUTPUT_DIR + "t2_realistic_hflip.ppm", img2_hflip)

    except ValueError as e: 
        print(f"Error: {e}", file=sys.stderr)

    try:

        # T3: t3_lowmax.ppm 
        # invert
        img3 = readImage(INPUT_DIR + "t3_lowmax.ppm")

        img3_invert = invert(img3)
        writeImage(OUTPUT_DIR + "t3_lowmax_invert.ppm", img3_invert)

    except ValueError as e: 
        print(f"Error: {e}", file=sys.stderr)

    print("All Python outputs written to ../tests/output_python/")

if __name__ == "__main__": 
    main() 