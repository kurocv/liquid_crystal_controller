#include "LiquidCrystalPrintTask.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

LiquidCrystalPrintTask::LiquidCrystalPrintTask() {
    is_active = false;
    text[0] = '\0';
    x = 0;
    y = 0;
    width = 0;
    life_time = 0;
    registered_time = 0;
    effect_type = EffectType::NONE;
    delay_time = 0;
    effect_speed = 0;
    effect_param = 0;
}

EvaluateResult LiquidCrystalPrintTask::get_erase_data() const {
    EvaluateResult result;
    result.x = x;
    result.y = y;
    
    uint8_t len = (width < sizeof(result.text) - 1) ? width : sizeof(result.text) - 1;
    memset(result.text, ' ', len);
    result.text[len] = '\0';
    
    return result;
}

EvaluateResult LiquidCrystalPrintTask::evaluate(uint32_t now) {
    EvaluateResult result;
    result.x = x;
    result.y = y;

    uint32_t effect_start_time = registered_time + delay_time;
    int32_t elapsed = (int32_t)(now - effect_start_time);

    if (delay_time > 0 && elapsed < 0) {
        return get_erase_data();
    }

    if (life_time > 0 && (uint32_t)elapsed >= life_time) {
        is_active = false;
        return get_erase_data();
    }

    uint16_t text_len = strlen(text);

    if (effect_type == EffectType::NONE) {
        snprintf(result.text, sizeof(result.text), "%s", text);
        return result;
    }

    else if (effect_type == EffectType::BLINK) {
        if (effect_speed == 0 || (elapsed / effect_speed) % 2 == 0) {
            snprintf(result.text, sizeof(result.text), "%s", text);
        } else {
            memset(result.text, ' ', text_len);
            result.text[text_len] = '\0';
        }
        return result;
    }

    else if (effect_type == EffectType::SLIDE) {
        if (effect_speed == 0) {
            snprintf(result.text, sizeof(result.text), "%s", text);
            return result;
        }
        uint32_t frames = (elapsed / effect_speed) % (width + text_len);

        memset(result.text, ' ', width);
        result.text[width] = '\0';

        if (effect_param > 0) {
            for (uint16_t i = 0; i < text_len; ++i) {
                uint16_t tx = frames + i;
                if (tx < width) result.text[tx] = text[i];
            }
        } else {
            int16_t start_idx = frames - width;
            for (uint16_t i = 0; i < width; ++i) {
                int16_t text_pos = start_idx + i;
                if (text_pos >= 0 && text_pos < text_len) result.text[i] = text[text_pos];
            }
        }
        return result;
    }

    else if (effect_type == EffectType::KNIGHT) {
        int16_t max_spaces = width - text_len;
        if (max_spaces <= 0 || effect_speed == 0) {
            snprintf(result.text, sizeof(result.text), "%s", text);
            return result;
        }

        uint32_t frames = elapsed / effect_speed;
        uint16_t cycle = max_spaces * 2;
        uint16_t current_step = frames % cycle;

        if (effect_param < 0) {
            current_step = (current_step + max_spaces) % cycle;
        }

        uint16_t spaces_count = (current_step <= max_spaces) ? current_step : (cycle - current_step);

        memset(result.text, ' ', width);
        result.text[width] = '\0';
        for (uint16_t i = 0; i < text_len; ++i) {
            if (spaces_count + i < width) result.text[spaces_count + i] = text[i];
        }
        return result;
    }

    snprintf(result.text, sizeof(result.text), "%s", text);
    return result;
}












