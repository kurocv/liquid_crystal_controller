#include "LiquidCrystalController.h"

LiquidCrystalController::LiquidCrystalController(ILcdDevice* lcd, uint32_t now, uint8_t size_x, uint8_t size_y, uint8_t max_tasks, char blank_ch)
    : vlcd(lcd, size_x, size_y, blank_ch),
      ptmlcd(&vlcd, now, max_tasks)
{
}

void LiquidCrystalController::print(const char* text, int16_t x, int16_t y) {
    vlcd.print(text, x, y);
}
void LiquidCrystalController::print_t(const char* text, int16_t x, int16_t y, uint32_t life_time, uint32_t delay_time) {
    ptmlcd.print(text, x, y, life_time, delay_time);
}
void LiquidCrystalController::blink(const char* text, int16_t x, int16_t y, uint32_t life_time, uint32_t effect_speed, uint32_t delay_time) {
    ptmlcd.blink(text, x, y, life_time, effect_speed, delay_time);
}
void LiquidCrystalController::slide(const char* text, int16_t x, int16_t y, uint8_t width, uint32_t life_time, uint32_t effect_speed, int8_t direction, uint32_t delay_time) {
    ptmlcd.slide(text, x, y, width, life_time, effect_speed, direction, delay_time);
}
void LiquidCrystalController::knight(const char* text, int16_t x, int16_t y, uint8_t width, uint32_t life_time, uint32_t effect_speed, int8_t direction, uint32_t delay_time) {
    ptmlcd.knight(text, x, y, width, life_time, effect_speed, direction, delay_time);
}
void LiquidCrystalController::update(uint32_t now) {
    ptmlcd.update(now);
    vlcd.flush();
}











