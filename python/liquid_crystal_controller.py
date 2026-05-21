#!/usr/bin/python
# coding: UTF-8

import queue
import threading
import time
from lcd_core.liquid_crystal_mock_tk import LiquidCrystalMockTk
from liquid_crystal_virtual import LiquidCrystalVirtual
from liquid_crystal_print_task_manager import LiquidCrystalPrintTaskManager

class LiquidCrystalController:
    def __init__(self, lcd, now, size_x=16, size_y=2, max_tasks=32, blank_ch=" "):
        self.vlcd = LiquidCrystalVirtual(lcd, size_x, size_y, blank_ch)
        self.ptmlcd = LiquidCrystalPrintTaskManager(self.vlcd, now, max_tasks)

    def print(self, text, x, y):
        """【通常表示】指定した内容をずっと表示"""
        self.vlcd.print(text, x, y)

    def print_t(self, text, x, y, life_time, delay_time=0):
        """【一時表示】指定時間（ms）が経つと自動で消える"""
        self.ptmlcd.print(
            text, x, y, life_time, delay_time=delay_time
        )

    def blink(self, text, x, y, life_time, effect_speed=500, delay_time=0):
        """【一時点滅】指定時間（ms）が経つと自動で消える点滅"""
        self.ptmlcd.blink(
            text, x, y, life_time, effect_speed=effect_speed, delay_time=delay_time
        )

    def slide(self, text, x, y, width, life_time, effect_speed=100, direction=1, delay_time=0):
        """【一時スライド】指定幅(width)の窓の中で文字が削られながら流れる"""
        # direction -> 1: 右に流れる, -1: 左に流れる
        self.ptmlcd.slide(
            text, x, y, width, life_time, effect_speed=effect_speed, effect_param=direction, delay_time=delay_time
        )

    def knight(self, text, x, y, width, life_time, effect_speed=100, direction=1, delay_time=0):
        """【一時ナイトライダー】指定幅(width)の窓の中で往復する。direction=-1で右スタート"""
        self.ptmlcd.knight(
            text, x, y, width, life_time, effect_speed=effect_speed, effect_param=direction, delay_time=delay_time
        )

    def update(self, now):
        self.ptmlcd.update(now)
        self.vlcd.flush()

def loop(data_queue, vlcd:LiquidCrystalController):
    while True:
        now = int(time.time() * 1000)
        vlcd.update(now)
        
        data_queue.put("update")
        time.sleep(0.05)

if __name__ == "__main__":
    shared_queue = queue.Queue()
    size_x = 20
    size_y = 4
    lcd = LiquidCrystalMockTk(shared_queue, size_x, size_y, blank_ch="_")
    now = int(time.time() * 1000)
    vlcd = LiquidCrystalController(lcd, now, size_x=size_x, size_y=size_y)

    vlcd.print("LCD", 17, 0)
    vlcd.print_t("Hello, World!", 0, 0, 3000, delay_time=10000)
    vlcd.blink("Blinking", 3, 1, 10000, effect_speed=500)
    vlcd.slide("Sliding", 0, 2, 20, 10000, effect_speed=100, direction=1)
    vlcd.knight("Knight", 0, 3, 20, 10000, effect_speed=100, direction=-1)

    # vlcd.knight("***", 0, 0, 10, 100000, effect_speed=100)
    # vlcd.knight("***", 0, 1, 10, 100000, effect_speed=100, delay_time=200)
    # vlcd.knight("***", 0, 2, 10, 100000, effect_speed=100, delay_time=400)
    # vlcd.knight("***", 0, 3, 10, 100000, effect_speed=100, delay_time=600)

    # vlcd.knight("***", 10, 0, 10, 100000, effect_speed=100, direction=-1)
    # vlcd.knight("***", 10, 1, 10, 100000, effect_speed=100, direction=-1, delay_time=200)
    # vlcd.knight("***", 10, 2, 10, 100000, effect_speed=100, direction=-1, delay_time=400)
    # vlcd.knight("***", 10, 3, 10, 100000, effect_speed=100, direction=-1, delay_time=600)

    # vlcd.slide("*************************", -25, 0, 45, 100000, effect_speed=100, direction=1)
    # vlcd.slide("*************************", -25, 1, 45, 100000, effect_speed=100, direction=1, delay_time=400)
    # vlcd.slide("*************************", -25, 2, 45, 100000, effect_speed=100, direction=1, delay_time=800)
    # vlcd.slide("*************************", -25, 3, 45, 100000, effect_speed=100, direction=1, delay_time=1200)

    loop_thread = threading.Thread(
        target=loop, args=(shared_queue, vlcd,), daemon=True
    )
    loop_thread.start()

    lcd.mainloop()



