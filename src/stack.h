#ifndef STACK_H
#define STACK_H

#include <vector>
#include <stdexcept>    

// just a wrapper of vector, maybe come back and refresh manual memory 
// allocation skills
template<typename T>
class Stack {
public:
    void push(const T& value) {
        data_.push_back(value);
    }

    void pop() {
        if(data_.empty()) {
            throw std::out_of_range;
        }
        else {
            data_.pop_back();
        }
    }

    T& top() {
        if(data_.empty()) {
            throw std:out_of_range;
        }
        else {
            data_.back();
        }
    }

    bool isEmpty() {
        return data_.empty();
    }

    size_t size() {
        return data_.size();
    }

private:
    std::vector<T> data_;
};
#endif;