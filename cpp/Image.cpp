#include "Image.h"

Image::Image() : width(0), height(0) {}

Image::Image(int initW, int initH) : width(initW), height(initH)
{
    PixelArray.reserve(width * height);
}

int Image::getWidth() const
{
    return width; 
}

int Image::getHeight() const
{
    return height; 
}

void Image::reset(const std::string& issue)
{
    std::cerr << issue; 
    width = height = 0; 
    PixelArray.clear(); 
    PixelArray.shrink_to_fit(); 
}

/*-----------Filters-----------*/

void Image::grayscale()
{
    int greyVal;
    for (auto& p : PixelArray)
    {
        greyVal = (p.r + p.g + p.b) / 3;
        p.r = p.g = p.b = greyVal;
    }
}

/* maxColor will always be 255, assumes 8-bit normalization
* from read decoding methods */
void Image::invert()
{
    for (auto& p : PixelArray)
    {
        p.r = maxColor - p.r;
        p.g = maxColor - p.g;
        p.b = maxColor - p.b;
    }
}

void Image::hflip()
{
    for (int i{ 0 }; i < height; ++i)
    {
        for (int j{ 0 }; j < width / 2; ++j)
        {
            std::swap(at(i, j), at(i, (width - j - 1)));
        }
    }
}

