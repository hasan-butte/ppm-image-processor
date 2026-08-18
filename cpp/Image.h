#pragma once

#include <algorithm> 
#include <fstream> 
#include <iostream>
#include <vector> 
#include <string> 

struct Pixel { int r, g, b; };

class Image // abstract class 
{
public:
    Image();
    Image(int initW, int initH);
    int getWidth() const; 
    int getHeight() const; 
    bool isValid() const;
    virtual void reset(const std::string& issue);
    virtual ~Image() = default;
    virtual void read(const std::string& fileName) = 0;
    virtual void write(const std::string& fileName) = 0;

    //filters
    void grayscale(); 
    void invert();
    void hflip();


protected:
    int width, height;
    std::vector<Pixel> PixelArray;
    Pixel& at(int i, int j) {return PixelArray.at((width * i) + j);}
    int maxColor{ 255 };
};