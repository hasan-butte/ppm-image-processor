#pragma once
#include "Image.h"

class PPMImage : public Image
{
public:
    PPMImage();
    PPMImage(int initW, int initH);
    void read(const std::string& fileName) override;
    void write(const std::string& fileName) override;
};