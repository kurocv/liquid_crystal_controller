#!/usr/bin/python
# coding: UTF-8

import queue
import threading
import time
from lcd_core.liquid_crystal_mock_tk import LiquidCrystalMockTk
from liquid_crystal_virtual import LiquidCrystalVirtual
from liquid_crystal_print_task import LiquidCrystalPrintTask

class LiquidCrystalPrintTaskManager:
    def __init__(self, vlcd:LiquidCrystalVirtual, now, max_tasks=32):
        self.vlcd = vlcd
        self.max_tasks = max_tasks
        self.tasks = [LiquidCrystalPrintTask() for _ in range(self.max_tasks)]
        self.current_loop_time = now
        self._max_x = vlcd.max_x
        self._max_y = vlcd.max_y
    def _get_now_ms(self):
        return self.current_loop_time
    def _get_free_task(self):
        for t in self.tasks:
            if not t.is_active: return t
        return None
    def is_active_task_exist(self):
        for t in self.tasks:
            if t.is_active: return True
        return False
    def all_tasks_deactivate(self):
        for t in self.tasks:
            if t.is_active:
                t.is_active = False
    def all_tasks_erase(self):
        for t in self.tasks:
            if t.is_active:
                t.get_erase_data()

    def print(self, text, x, y, life_time, delay_time=0):
        t = self._get_free_task()
        if t == None: return
        t.text = text
        t.x = x
        t.y = y
        t.width = len(str(text))
        t.life_time = life_time
        t.delay_time = delay_time
        t.registered_time = self._get_now_ms()
        t.is_active = True
        self.vlcd.print(t.text, t.x, t.y)
    def blink(self, text, x, y, life_time, effect_speed=500, delay_time=0):
        t = self._get_free_task()
        if t == None: return
        t.text = text
        t.x = x
        t.y = y
        t.width = len(str(text))
        t.life_time = life_time
        t.delay_time = delay_time
        t.registered_time = self._get_now_ms()
        t.is_active = True
        t.effect_type = "BLINK"
        t.effect_speed = effect_speed
        self.vlcd.print(t.text, t.x, t.y)
    def slide(self, text, x, y, width, life_time, effect_speed=500, effect_param=1, delay_time=0):
        t = self._get_free_task()
        if t == None: return
        t.text = text
        t.x = x
        t.y = y
        t.width = width
        t.life_time = life_time
        t.delay_time = delay_time
        t.registered_time = self._get_now_ms()
        t.is_active = True
        t.effect_type = "SLIDE"
        t.effect_speed = effect_speed
        t.effect_param = effect_param
        self.vlcd.print(t.text, t.x, t.y)
    def knight(self, text, x, y, width, life_time, effect_speed=500, effect_param=1, delay_time=0):
        t = self._get_free_task()
        if t == None: return
        t.text = text
        t.x = x
        t.y = y
        t.width = width
        t.life_time = life_time
        t.delay_time = delay_time
        t.registered_time = self._get_now_ms()
        t.is_active = True
        t.effect_type = "KNIGHT"
        t.effect_speed = effect_speed
        t.effect_param = effect_param
        self.vlcd.print(t.text, t.x, t.y)

    def update(self, now):
        self.current_loop_time = now
        if not self.is_active_task_exist(): return

        for t in self.tasks:
            if not t.is_active: continue

            text, tx, ty = t.evaluate(now)
            self.vlcd.print(text, tx, ty)

def loop(data_queue, vlcd, pm):
    while True:
        now = int(time.time() * 1000)
        pm.update(now)

        vlcd.flush()
        data_queue.put("update")
        time.sleep(0.05)

if __name__ == "__main__":
    shared_queue = queue.Queue()
    size_x = 20
    size_y = 4
    lcd = LiquidCrystalMockTk(shared_queue, size_x, size_y, blank_ch="_")
    vlcd = LiquidCrystalVirtual(lcd, size_x=size_x, size_y=size_y)
    now = int(time.time() * 1000)
    pm = LiquidCrystalPrintTaskManager(vlcd, now)
    pm.print("Hello, World!", 0, 0, 3000, delay_time=10000)
    pm.blink("Blinking", 3, 1, 10000, effect_speed=500)
    pm.slide("Sliding", 0, 2, 20, 10000, effect_speed=100, effect_param=-1)
    pm.knight("Knight", 0, 3, 20, 10000, effect_speed=100, effect_param=-1)

    loop_thread = threading.Thread(
        target=loop, args=(shared_queue, vlcd, pm,), daemon=True
    )
    loop_thread.start()

    lcd.mainloop()



