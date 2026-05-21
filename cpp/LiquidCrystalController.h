#pragma once

#include <stdint.h>
#include "LiquidCrystalVirtual.h"
#include "LiquidCrystalPrintTaskManager.h"

class LiquidCrystalController {
private:
    LiquidCrystalVirtual vlcd;
    LiquidCrystalPrintTaskManager ptmlcd;

public:
    LiquidCrystalController(ILcdDevice* lcd, uint32_t now, uint8_t size_x = 16, uint8_t size_y = 2, uint8_t max_tasks = 32, char blank_ch = ' ');
    ~LiquidCrystalController() {}

    void print(const char* text, int16_t x, int16_t y);
    void print_t(const char* text, int16_t x, int16_t y, uint32_t life_time, uint32_t delay_time = 0);
    void blink(const char* text, int16_t x, int16_t y, uint32_t life_time, uint32_t effect_speed = 500, uint32_t delay_time = 0);
    void slide(const char* text, int16_t x, int16_t y, uint8_t width, uint32_t life_time, uint32_t effect_speed = 100, int8_t direction = 1, uint32_t delay_time = 0);
    void knight(const char* text, int16_t x, int16_t y, uint8_t width, uint32_t life_time, uint32_t effect_speed = 100, int8_t direction = 1, uint32_t delay_time = 0);
    void update(uint32_t now);
};











