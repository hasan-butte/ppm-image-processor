#include "PPMImage.h"

int main() {

    const std::string INPUT_DIR = "../tests/input/";
    const std::string OUTPUT_DIR = "../tests/output_cpp/";

    // first test case t1
    {
        PPMImage img;
        img.read(INPUT_DIR + "t1_simple.ppm");

        if(img.isValid())
        {
            // grayscale
            PPMImage gray = img;
            gray.grayscale();
            gray.write(OUTPUT_DIR + "t1_simple_gray.ppm");

            // invert
            PPMImage inv = img;
            inv.invert();
            inv.write(OUTPUT_DIR + "t1_simple_invert.ppm");

            // horizontal flip
            PPMImage flip = img;
            flip.hflip();
            flip.write(OUTPUT_DIR + "t1_simple_hflip.ppm");
        }

    }

    // second test case t2
    {
        PPMImage img;
        img.read(INPUT_DIR + "t2_realistic.ppm");

        if(img.isValid()) 
        {
            // grayscale
            PPMImage gray = img;
            gray.grayscale();
            gray.write(OUTPUT_DIR + "t2_realistic_gray.ppm");

            // invert
            PPMImage inv = img;
            inv.invert();
            inv.write(OUTPUT_DIR + "t2_realistic_invert.ppm");

            // horizontal flip
            PPMImage flip = img;
            flip.hflip();
            flip.write(OUTPUT_DIR + "t2_realistic_hflip.ppm");
        }
    }

    // third test case t3
    {
        PPMImage img;
        img.read(INPUT_DIR + "t3_lowmax.ppm");

        if(img.isValid()) 
        {
              // invert only
            PPMImage inv = img;
            inv.invert();
            inv.write(OUTPUT_DIR + "t3_lowmax_invert.ppm");
        }

    }

    std::cout << "All test outputs written to ../tests/output_cpp/" << std::endl;
    return 0;
}
