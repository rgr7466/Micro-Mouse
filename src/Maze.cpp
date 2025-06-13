#include "Maze.h"
#include <iostream>

using namespace std;

Maze::Maze(const path& mazefile) 
    : mazeData_{Maze::parseMazeFile(mazefile)}
    , size_{mazeData_.size()}
{}

size_t Maze::getSize() const noexcept{
    return size_;
}

bool Maze::hasWall(int row, int col, wall dir) const {
    return mazeData_[row][col] & dir;
}

// CHATGPT GENERATED WILL MOST LIKELY IMPLEMENT ON OWN JUST TIRED : ()
vector<vector<uint8_t>> Maze::parseMazeFile(const path& mazefile) {
    // 1) Read all non-empty lines
    std::ifstream in{mazefile};
    if (!in) throw std::runtime_error("Cannot open " + mazefile.string());
    std::vector<std::string> lines;
    for (std::string line; std::getline(in, line); ) {
        if (!line.empty()) lines.push_back(line);
    }
    if (lines.empty())
        throw std::runtime_error("Empty maze file");

    // 2) Compute maze dimensions
    int textRows = static_cast<int>(lines.size());
    int textCols = static_cast<int>(lines[0].size());
    int R = (textRows - 1) / 2;    // number of maze rows
    int C = (textCols - 1) / 4;    // number of maze cols

    // 3) Prepare an R×C grid, all walls cleared
    std::vector<std::vector<uint8_t>> grid(R, std::vector<uint8_t>(C, 0));

    // 4) Scan each cell for its four walls
    for (int r = 0; r < R; ++r) {
        for (int c = 0; c < C; ++c) {
            int tr = 2*r,    tc = 4*c;     // top-left corner in text coords
            int mr = tr + 1, mc = tc + 2;  // cell-center row/col

            // North wall: three '-' between o's on line tr
            if (lines[tr].substr(tc+1, 3) == "---")
                grid[r][c] |= static_cast<uint8_t>(wall::N);

            // South wall: same pattern on line tr+2
            if (lines[tr+2].substr(tc+1, 3) == "---")
                grid[r][c] |= static_cast<uint8_t>(wall::S);

            // West wall: '|' immediately left of cell center
            if (lines[mr][tc] == '|')
                grid[r][c] |= static_cast<uint8_t>(wall::W);

            // East wall: '|' immediately right of cell center
            if (lines[mr][tc+4] == '|')
                grid[r][c] |= static_cast<uint8_t>(wall::E);

            // (Optional) detect start/goal markers at center:
            // char mid = lines[mr][mc];
            // if (mid == 'S') start_ = {r,c};
            // if (mid == 'G') goal_  = {r,c};
        }
    }

    return grid;
}


