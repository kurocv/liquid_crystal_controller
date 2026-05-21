#include "LiquidCrystalPrintTaskManager.h"
#include <string.h>
#include <stdio.h>

LiquidCrystalPrintTaskManager::LiquidCrystalPrintTaskManager(LiquidCrystalVirtual* virtual_lcd, uint32_t now, uint8_t max_t) {
    vlcd = virtual_lcd;
    max_tasks = max_t;
    tasks = new LiquidCrystalPrintTask[max_tasks];
    current_loop_time = now;
    _max_x = vlcd->max_x();
    _max_y = vlcd->max_y();
}

LiquidCrystalPrintTaskManager::~LiquidCrystalPrintTaskManager() {
    delete[] tasks;
}

LiquidCrystalPrintTask* LiquidCrystalPrintTaskManager::_get_free_task() {
    for (uint8_t i = 0; i < max_tasks; ++i) {
        if (!tasks[i].is_active) return &tasks[i];
    }
    return nullptr;
}

bool LiquidCrystalPrintTaskManager::is_active_task_exist() const {
    for (uint8_t i = 0; i < max_tasks; ++i) {
        if (tasks[i].is_active) return true;
    }
    return false;
}

void LiquidCrystalPrintTaskManager::all_tasks_deactivate() {
    for (uint8_t i = 0; i < max_tasks; ++i) {
        tasks[i].is_active = false;
    }
}

void LiquidCrystalPrintTaskManager::all_tasks_erase() {
    for (uint8_t i = 0; i < max_tasks; ++i) {
        if (tasks[i].is_active) {
            tasks[i].get_erase_data();
        }
    }
}

void LiquidCrystalPrintTaskManager::print(const char* text, int16_t x, int16_t y, uint32_t life_time, uint32_t delay_time) {
    LiquidCrystalPrintTask* t = _get_free_task();
    if (t == nullptr) return;
    
    snprintf(t->text, sizeof(t->text), "%s", text);
    t->x = x;
    t->y = y;
    t->width = strlen(text);
    t->life_time = life_time;
    t->delay_time = delay_time;
    t->registered_time = current_loop_time;
    t->effect_type = EffectType::NONE;
    t->is_active = true;
    
    vlcd->print(t->text, t->x, t->y);
}

void LiquidCrystalPrintTaskManager::blink(const char* text, int16_t x, int16_t y, uint32_t life_time, uint32_t effect_speed, uint32_t delay_time) {
    LiquidCrystalPrintTask* t = _get_free_task();
    if (t == nullptr) return;

    snprintf(t->text, sizeof(t->text), "%s", text);
    t->x = x;
    t->y = y;
    t->width = strlen(text);
    t->life_time = life_time;
    t->delay_time = delay_time;
    t->registered_time = current_loop_time;
    t->effect_type = EffectType::BLINK;
    t->effect_speed = effect_speed;
    t->is_active = true;

    vlcd->print(t->text, t->x, t->y);
}

void LiquidCrystalPrintTaskManager::slide(const char* text, int16_t x, int16_t y, uint8_t width, uint32_t life_time, uint32_t effect_speed, int8_t effect_param, uint32_t delay_time) {
    LiquidCrystalPrintTask* t = _get_free_task();
    if (t == nullptr) return;

    snprintf(t->text, sizeof(t->text), "%s", text);
    t->x = x;
    t->y = y;
    t->width = width;
    t->life_time = life_time;
    t->delay_time = delay_time;
    t->registered_time = current_loop_time;
    t->effect_type = EffectType::SLIDE;
    t->effect_speed = effect_speed;
    t->effect_param = effect_param;
    t->is_active = true;

    vlcd->print(t->text, t->x, t->y);
}

void LiquidCrystalPrintTaskManager::knight(const char* text, int16_t x, int16_t y, uint8_t width, uint32_t life_time, uint32_t effect_speed, int8_t effect_param, uint32_t delay_time) {
    LiquidCrystalPrintTask* t = _get_free_task();
    if (t == nullptr) return;

    snprintf(t->text, sizeof(t->text), "%s", text);
    t->x = x;
    t->y = y;
    t->width = width;
    t->life_time = life_time;
    t->delay_time = delay_time;
    t->registered_time = current_loop_time;
    t->effect_type = EffectType::KNIGHT;
    t->effect_speed = effect_speed;
    t->effect_param = effect_param;
    t->is_active = true;

    vlcd->print(t->text, t->x, t->y);
}

void LiquidCrystalPrintTaskManager::update(uint32_t now) {
    current_loop_time = now;
    if (!is_active_task_exist()) return;

    for (uint8_t i = 0; i < max_tasks; ++i) {
        if (!tasks[i].is_active) continue;

        EvaluateResult res = tasks[i].evaluate(now);
        vlcd->print(res.text, res.x, res.y);
    }
}












