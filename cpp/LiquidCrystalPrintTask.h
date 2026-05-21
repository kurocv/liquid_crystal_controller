#pragma once

#include <stdint.h>

enum class EffectType {
    NONE,
    BLINK,
    SLIDE,
    KNIGHT
};

struct EvaluateResult {
    char text[41];
    int16_t x;
    int16_t y;
};

class LiquidCrystalPrintTask {
public:
    bool is_active;
    char text[41]; 
    int16_t x;
    int16_t y;
    uint8_t width;
    uint32_t life_time;
    uint32_t registered_time;

    EffectType effect_type;
    uint32_t delay_time;
    uint32_t effect_speed;
    int8_t effect_param;

public:
    LiquidCrystalPrintTask();
    EvaluateResult get_erase_data() const;
    EvaluateResult evaluate(uint32_t now);
};













