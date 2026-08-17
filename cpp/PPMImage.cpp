#include "PPMImage.h"

PPMImage::PPMImage() : Image() {}
PPMImage::PPMImage(int initW, int initH) : Image(initW, initH) {};


void PPMImage::read(const std::string& fileName)
{
    // parsing PPM header information 
    std::ifstream image;
    image.open(fileName);
    if (!image) { 
        reset("Error: File " + fileName + " could not be opened.\n");
        return;  
    }

    std::string magicChar;
    std::getline(image, magicChar);
    if (magicChar != "P3")
    {
        reset("Error: This type of PPM image format is not supported.\n");
        return;
    }

    if (!(image >> width >> height >> maxColor) || (width <= 0 || height <= 0 || maxColor <= 0))
    {
        reset("Error: Incorrectly formatted PPM file.\n");
        return; 
    }

    int total{ width * height };
    PixelArray.clear();
    PixelArray.reserve(total);

    // encode PixelArray
    Pixel currPixel;
    for (int i{ 0 }; i < total; ++i)
    {
        if (!(image >> currPixel.r >> currPixel.g >> currPixel.b))
        {
            reset("Error: Incorrect pixel format in PPM file.\n");
            return;
        }
        PixelArray.push_back(currPixel);
    }

    // 8-bit normalization for color saturation 
    if (maxColor != 255)
    {
        double scalar = 255.0 / maxColor; 

        for (auto& p : PixelArray)
        {
            p.r = int((p.r * scalar) + 0.5);
            p.g = int((p.g * scalar) + 0.5);
            p.b = int((p.b * scalar) + 0.5);
        }

        maxColor = 255;
    }
    image.close();
}

void PPMImage::write(const std::string& fileName)
{
    std::ofstream image;
    image.open(fileName);
    if (!image) { std::cerr << " Image could not be opened ";  return; }

     // writing PPM header information
     image << "P3" << std::endl;
     image << width << " " << height << std::endl;
     image << maxColor << std::endl;
     Pixel currPixel; 

      // decode PixelArray
      for (int i{ 0 }; i < height; ++i)
      {
        for (int j{ 0 }; j < width; ++j)
        { 
            currPixel = at(i, j);
            image << currPixel.r << " " << currPixel.g << " " << currPixel.b << " ";
        }
        image << std::endl;
      }

    image.close();
}





