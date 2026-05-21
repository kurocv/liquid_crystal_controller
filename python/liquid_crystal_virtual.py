#!/usr/bin/python
# coding: UTF-8

import queue
import threading
import time
from lcd_core.liquid_crystal_mock_tk import LiquidCrystalMockTk

class LiquidCrystalVirtual:
    def __init__(self, lcd, size_x=16, size_y=2, blank_ch=" "):
        self.lcd = lcd
        self._max_x = size_x
        self._max_y = size_y
        self._blank_ch = blank_ch
        self._vram = [[self._blank_ch] * self._max_x for _ in range(self._max_y)]
        self._is_dirty = False
    @property
    def max_x(self):
        return self._max_x
    @property
    def max_y(self):
        return self._max_y
    def clear(self):
        for y in range(self._max_y):
            for x in range(self._max_x):
                self._vram[y][x] = self._blank_ch
        self._is_dirty = True

    def print(self, text, x, y):
        if y < 0 or y >= self._max_y:
            return
        for i, ch in enumerate(str(text)):
            tx = x + i
            if 0 <= tx < self._max_x:
                if self._vram[y][tx] != ch:
                    self._vram[y][tx] = ch
                    self._is_dirty = True

    def print_clipped(self, text, x, y, clip_left, clip_right):
        """指定した列の範囲（clip_left ～ clip_right）内だけに文字を描画する（マスク処理）"""
        # 入力されたクリップ範囲をVRAMの有効幅に収める
        w_left = max(0, clip_left)
        w_right = min(self._max_x - 1, clip_right)
        
        if y < 0 or y >= self._max_y:
            return

        for i, ch in enumerate(str(text)):
            tx = x + i
            # クリップ範囲の内側、かつVRAMの範囲内にある文字だけを書き込む
            if w_left <= tx <= w_right:
                if self._vram[y][tx] != ch:
                    self._vram[y][tx] = ch
                    self._is_dirty = True

    def flush(self):
        if not self._is_dirty: return
        for y in range(self._max_y):
            self.lcd.set_cursor(0, y)
            self.lcd.print("".join(self._vram[y]))
        self._is_dirty = False


def loop(data_queue, vlcd):
    while True:
        vlcd.flush()

        data_queue.put("update")
        time.sleep(0.05)

if __name__ == "__main__":
    shared_queue = queue.Queue()
    size_x = 16
    size_y = 4
    lcd = LiquidCrystalMockTk(shared_queue, size_x, size_y, blank_ch="_")
    vlcd = LiquidCrystalVirtual(lcd, size_x=size_x, size_y=size_y)
    vlcd.clear()
    vlcd.print_clipped("Hello, World!", 0, 0, 2, 4)
    vlcd.print("Blinking Text", 0, 1)
    vlcd.print("Sliding Text", 2, 2)
    vlcd.print("Knight Rider", 3, 3)
    loop_thread = threading.Thread(
        target=loop, args=(shared_queue, vlcd, ), daemon=True
    )
    loop_thread.start()

    lcd.mainloop()



