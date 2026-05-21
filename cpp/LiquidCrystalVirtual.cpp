#include "LiquidCrystalVirtual.h"

// コンストラクタ
LiquidCrystalVirtual::LiquidCrystalVirtual(ILcdDevice* lcd, uint8_t size_x, uint8_t size_y, char blank_ch) {
    _lcd = lcd;
    _max_x = size_x;
    _max_y = size_y;
    _blank_ch = blank_ch;
    _is_dirty = false;

    _vram = new char*[_max_y];
    for (uint8_t y = 0; y < _max_y; ++y) {
        _vram[y] = new char[_max_x + 1];
        for (uint8_t x = 0; x < _max_x; ++x) {
            _vram[y][x] = _blank_ch;
        }
        _vram[y][_max_x] = '\0';
    }
}

// デストラクタ
LiquidCrystalVirtual::~LiquidCrystalVirtual() {
    for (uint8_t y = 0; y < _max_y; ++y) {
        delete[] _vram[y];
    }
    delete[] _vram;
}

uint8_t LiquidCrystalVirtual::max_x() const { return _max_x; }
uint8_t LiquidCrystalVirtual::max_y() const { return _max_y; }
bool LiquidCrystalVirtual::is_dirty() const { return _is_dirty; }

void LiquidCrystalVirtual::clear() {
    for (uint8_t y = 0; y < _max_y; ++y) {
        for (uint8_t x = 0; x < _max_x; ++x) {
            _vram[y][x] = _blank_ch;
        }
    }
    _is_dirty = true;
}

void LiquidCrystalVirtual::print(const char* text, int16_t x, int16_t y) {
    if (y < 0 || y >= _max_y) return;

    int16_t i = 0;
    while (text[i] != '\0') {
        int16_t tx = x + i;
        if (tx >= 0 && tx < _max_x) {
            if (_vram[y][tx] != text[i]) {
                _vram[y][tx] = text[i];
                _is_dirty = true;
            }
        }
        i++;
    }
}

void LiquidCrystalVirtual::print_clipped(const char* text, int16_t x, int16_t y, int16_t clip_left, int16_t clip_right) {
    if (y < 0 || y >= _max_y) return;

    int16_t w_left = (clip_left > 0) ? clip_left : 0;
    int16_t w_right = (clip_right < _max_x - 1) ? clip_right : _max_x - 1;

    int16_t i = 0;
    while (text[i] != '\0') {
        int16_t tx = x + i;
        if (tx >= w_left && tx <= w_right) {
            if (_vram[y][tx] != text[i]) {
                _vram[y][tx] = text[i];
                _is_dirty = true;
            }
        }
        i++;
    }
}

void LiquidCrystalVirtual::flush() {
    if (!_is_dirty) return;
    if (_lcd == nullptr) return;

    for (uint8_t y = 0; y < _max_y; ++y) {
        _lcd->set_cursor(0, y);
        _lcd->print(_vram[y]);
    }
    _is_dirty = false;
}











