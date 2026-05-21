#pragma once

#include <stdint.h>
#include <stddef.h>

class ILcdDevice {
public:
    virtual void set_cursor(uint8_t x, uint8_t y) = 0;
    virtual void print(const char* text) = 0;
    virtual ~ILcdDevice() {}
};

class LiquidCrystalVirtual {
private:
    ILcdDevice* _lcd;
    uint8_t _max_x;
    uint8_t _max_y;
    char _blank_ch;
    char** _vram;
    bool _is_dirty;

public:
    LiquidCrystalVirtual(ILcdDevice* lcd, uint8_t size_x = 16, uint8_t size_y = 2, char blank_ch = ' ');
    ~LiquidCrystalVirtual();

    uint8_t max_x() const;
    uint8_t max_y() const;
    bool is_dirty() const;

    void clear();
    void print(const char* text, int16_t x, int16_t y);
    void print_clipped(const char* text, int16_t x, int16_t y, int16_t clip_left, int16_t clip_right);
    void flush();
};












