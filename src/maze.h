#ifndef MAZE_H
#define MAZE_H
#include <iostream>
#include <filesystem>
using namespace std;

class maze {
    public:
        // wall enum representing each cardinal direction as 8 bit integers 
        enum wall: uint8_t{N = 0b1000, S = 0b0100, E = 0b0010, W = 0b0001};

        explicit maze(const std::filesystem::path& mazefile);
        explicit maze(std::size_t x, std::size_t y);

        // Getter Methods
        int getSize() const;
        bool isWall(int x, int y, wall w);

        //setters i dont think I need it
    private:
        int size;
        
};
#endif;
