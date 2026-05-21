#include "LiquidCrystalMock.h"
#include "LiquidCrystalController.h"
#include <chrono>
#include <unistd.h>

#define LCD_WIDTH 20
#define LCD_HEIGHT 4

uint32_t get_current_time_ms() {
    auto now = std::chrono::system_clock::now().time_since_epoch();
    return std::chrono::duration_cast<std::chrono::milliseconds>(now).count();
}

int main() {
    LiquidCrystalMock mockLcd(LCD_WIDTH, LCD_HEIGHT, '_');
    mockLcd.init();

    LiquidCrystalController lcdCtrl(&mockLcd, get_current_time_ms(), LCD_WIDTH, LCD_HEIGHT);

    lcdCtrl.print("LCD", 17, 0);
    lcdCtrl.print_t("Hello, World!", 0, 0, 3000, 10000);
    lcdCtrl.blink("Blinking", 3, 1, 10000, 500);
    lcdCtrl.slide("Sliding", 0, 2, 20, 10000, 100, 1);
    lcdCtrl.knight("Knight", 0, 3, 20, 10000, 100, -1);

    while (true) {
        lcdCtrl.update(get_current_time_ms());
        usleep(10000);
    }
}












