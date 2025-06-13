# -------- Makefile --------
# Tool chain
CXX      := g++
CXXFLAGS := -std=c++20 -Wall -Wextra -g

# Output executable name:
#   On Windows          → floodfill.exe
#   On Linux / macOS    → floodfill
BIN      := floodfill$(EXE)   # 'EXE' is empty on POSIX, '.exe' on Windows

# Default target: build the program
$(BIN): floodfill.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

# Helper target: build then run
.PHONY: run
run: $(BIN)
	./$(BIN)

# Clean up generated files
.PHONY: clean
clean:
	@echo "Removing $(BIN)…"
	-@rm -f $(BIN)
# --------------------------
