#pragma once

#include <stdint.h>
#include "LiquidCrystalVirtual.h"
#include "LiquidCrystalPrintTask.h"

class LiquidCrystalPrintTaskManager {
private:
    LiquidCrystalVirtual* vlcd;
    uint8_t max_tasks;
    LiquidCrystalPrintTask* tasks;
    uint32_t current_loop_time;
    uint8_t _max_x;
    uint8_t _max_y;

    LiquidCrystalPrintTask* _get_free_task();

public:
    LiquidCrystalPrintTaskManager(LiquidCrystalVirtual* virtual_lcd, uint32_t now, uint8_t max_t = 32);
    ~LiquidCrystalPrintTaskManager();

    bool is_active_task_exist() const;
    void all_tasks_deactivate();
    void all_tasks_erase();

    void print(const char* text, int16_t x, int16_t y, uint32_t life_time, uint32_t delay_time = 0);
    void blink(const char* text, int16_t x, int16_t y, uint32_t life_time, uint32_t effect_speed = 500, uint32_t delay_time = 0);
    void slide(const char* text, int16_t x, int16_t y, uint8_t width, uint32_t life_time, uint32_t effect_speed = 500, int8_t effect_param = 1, uint32_t delay_time = 0);
    void knight(const char* text, int16_t x, int16_t y, uint8_t width, uint32_t life_time, uint32_t effect_speed = 500, int8_t effect_param = 1, uint32_t delay_time = 0);

    void update(uint32_t now);
};







