#pragma once

#include <stdint.h>
#include "LiquidCrystalVirtual.h"

class LiquidCrystalMock : public ILcdDevice {
private:
    uint8_t _max_x;
    uint8_t _max_y;
    char _blank_ch;
    int16_t _cursor_x;
    int16_t _cursor_y;

public:
    LiquidCrystalMock(uint8_t max_x = 16, uint8_t max_y = 2, char blank_ch = '_');
    virtual ~LiquidCrystalMock() override {}

    void set_cursor(uint8_t x, uint8_t y) override;
    void print(const char* text) override;

    void init();
    void clear();
    void home();
    void end();

    void back_light() {}
    void no_back_light() {}
    void display() {}
    void no_display() {}
    void cursor() {}
    void no_cursor() {}
    void blink() {}
    void no_blink() {}
    void scroll_display_left() {}
    void scroll_display_right() {}
    void left_to_right() {}
    void right_to_left() {}
    void autoscroll() {}
    void no_autoscroll() {}
};












