#include <iostream>
#include <string>
#include <set>

namespace ERR {
    const int BAD_UNIT = 1;
    const int BAD_USAGE = 2;
}

const float start = 118;

void print_usage(){
    std::cerr << "usage: weightloss <value> <lb|st|kg>"
                  << std::endl;
}

int show_weight(float value, std::string unit){
    float value_kg;
    if (unit == "kg")
    {
        value_kg = value;
    } else if (unit == "lb")
    {
        value_kg = value * 2.2;
    } else if (unit == "st")
    {
        value_kg = value * 2.2 / 14;
    } else {
        std::cout << "Bad unit '" << unit << "'. "
                  << "Use kg, lb, or st."
                  << std::endl;
        return ERR::BAD_UNIT;
    }
    float value_lb = value_kg * 2.2;
    float value_st = value_lb / 14;
    float diff = start - value_kg;
    std::cout.precision(4);
    std::cout << value_kg << "kg "
              << value_st << "st "
              << value_lb << "lb "
              << "(lost " << diff << "kg)"
              << std::endl;
    return 0;
}

int main(int argc, const char** argv) {
    if(argc < 3){
        print_usage();
        return ERR::BAD_USAGE;
    }
    float value = std::stof(argv[1]);
    return show_weight(value, argv[2]);
}
