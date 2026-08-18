#include "PPMImage.h"
#include <filesystem> 

namespace fs = std::filesystem; 
std::vector<std::string> fileNames(const std::string& dirPath);

int main() {

    const std::string INPUT_DIR = "../tests/input/";
    const std::string OUTPUT_DIR = "../tests/output_cpp/";
    std::vector<std::string> imgNames = fileNames(INPUT_DIR);

    bool keepGoing = true;
    while (keepGoing)
    {
        std::cout << "Please select an image from the following inputs (1, 2, ...):\n";
        for(std::size_t i = 0; i < imgNames.size(); i++)
            {
                std::cout << i + 1 << ". " << imgNames.at(i) << std::endl;
            }
        int selectedFile;
        if (!(std::cin >> selectedFile) || selectedFile < 1 || selectedFile > static_cast<int>(imgNames.size()))
        {
            std::cerr << "Error: Invalid image selection.\n";
            return -1;
        }

        std::string imgName = imgNames.at(selectedFile - 1);
        PPMImage initImg;
        initImg.read(INPUT_DIR + imgName + ".ppm");

        if(!initImg.isValid())
            return -1;

        std::cout << "What do you want to do with the image (pick a number)?\n1. Remove Color \n2. Invert Color\n3. Flip Horizontally" << std::endl;

        int methodNum;
        if (!(std::cin >> methodNum))
        {
            std::cerr << "Error: Invalid method selection.\n";
            return -1;
        }

        PPMImage prodImg = initImg;
        std::string newImgName;
        switch(methodNum)
        {
            case 1:
                prodImg.grayscale();
                newImgName = imgName + "_grayed.ppm";
                break;
            case 2:
                prodImg.invert();
                newImgName = imgName + "_inverted.ppm";
                break;
            case 3:
                prodImg.hflip();
                newImgName = imgName + "_h_flipped.ppm";
                break;
            default:
                std::cout << "Invalid method selected";
                return -1;
        }

        prodImg.write(OUTPUT_DIR + newImgName);
        std::cout << "Output written to " << OUTPUT_DIR + newImgName << std::endl;

        std::cout << "Process another image? (y/n): ";
        char again;
        std::cin >> again;
        keepGoing = (again == 'y' || again == 'Y');
    }

    std::cout << "Done." << std::endl;
    return 0;
}

std::vector<std::string> fileNames(const std::string& dirPath)
{
    std::vector<std::string> files; 
    for (const auto& entry : fs::directory_iterator(dirPath))
        {
            if(entry.is_regular_file() && entry.path().extension() == ".ppm")
                files.push_back(entry.path().filename().stem().string());
        }
    std::sort(files.begin(), files.end());
    return files; 
}

