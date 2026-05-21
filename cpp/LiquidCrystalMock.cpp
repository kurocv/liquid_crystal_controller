#include "LiquidCrystalMock.h"
#include <iostream>
#include <string.h>
#include <stdlib.h>

LiquidCrystalMock::LiquidCrystalMock(uint8_t max_x, uint8_t max_y, char blank_ch) {
    _max_x = max_x;
    _max_y = max_y;
    _blank_ch = blank_ch;
    _cursor_x = 0;
    _cursor_y = 0;
}

void LiquidCrystalMock::init() {
    clear();
}

void LiquidCrystalMock::clear() {
    for (uint8_t y = 0; y < _max_y; ++y) {
        for (uint8_t x = 0; x < _max_x; ++x) {
            std::cout << _blank_ch;
        }
        std::cout << "\n";
    }
    std::cout << "\033[" << (int)_max_y << "A\r" << std::flush;
    _cursor_x = 0;
    _cursor_y = 0;
}

void LiquidCrystalMock::set_cursor(uint8_t x, uint8_t y) {
    uint8_t target_x = x % _max_x;
    uint8_t target_y = y % _max_y;

    int16_t move_x = target_x - _cursor_x;
    int16_t move_y = target_y - _cursor_y;

    _cursor_x = target_x;
    _cursor_y = target_y;

    if (move_y > 0) std::cout << "\033[" << move_y << "B";
    else if (move_y < 0) std::cout << "\033[" << abs(move_y) << "A";

    if (move_x > 0) std::cout << "\033[" << move_x << "C";
    else if (move_x < 0) std::cout << "\033[" << abs(move_x) << "D";

    std::cout << std::flush;
}

void LiquidCrystalMock::home() {
    set_cursor(0, 0);
}

void LiquidCrystalMock::end() {
    set_cursor(_max_x - 1, _max_y - 1);
}

void LiquidCrystalMock::print(const char* text) {
    int16_t remaining_width = _max_x - _cursor_x;
    if (remaining_width <= 0) return;

    int16_t i = 0;
    while (text[i] != '\0' && i < remaining_width) {
        char ch = text[i];
        if (ch == ' ') {
            ch = _blank_ch;
        }
        std::cout << ch;
        i++;
    }
    std::cout << std::flush;
    _cursor_x += i;
}













