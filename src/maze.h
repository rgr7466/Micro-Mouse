#ifndef MAZE_H
#define MAZE_H
#include <iostream>
#include <cstddef>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <vector>

using std::size_t;
using std::vector;
using std::filesystem::path;

class Maze {
    public:
        // wall enum representing each cardinal direction as 8 bit integers 
        enum wall: uint8_t{N = 0b1000, S = 0b0100, E = 0b0010, W = 0b0001};

        // file constructor
        explicit Maze(const path& mazefile);

        // Getter Methods
        size_t getSize() const;


        bool hasWall(int row, int col, wall dir) const;

        //setters i dont think I need it as maze should be immutable
    private:

        int size_;

        vector<vector<uint8_t>> mazeData_;
        
        static vector<vector<uint8_t>> parseMazeFile(const path& mazefile);
        
};
#endif 
