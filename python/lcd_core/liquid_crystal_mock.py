#!/usr/bin/python
# coding: UTF-8

class LiquidCrystalMock:
    def __init__(self, max_x=16, max_y=2, blank_ch="_"):
        self._max_x = max_x
        self._max_y = max_y
        self._blank_ch = blank_ch

        self._scroll_offset_x = 0
        # チップ内部（VRAM）の物理的な書き込みアドレス
        self._vram_cursor_x = 0
        self._vram_cursor_y = 0
        self._backlight_on = True

        # 物理チップの仕様：どんなサイズの液晶でも内部メモリは必ず 40文字 × 2行 固定
        self._INTERNAL_WIDTH = 40
        self._INTERNAL_HEIGHT = 2
        # 内部メモリを 40文字 × 2行 で初期確保
        self._vram = [[self._blank_ch] * self._INTERNAL_WIDTH for _ in range(self._INTERNAL_HEIGHT)]

        self._cursor_direction = 1 
        self._autoscroll_on = False 
        self._blink_on = True

        # 未実装
        self._cursor_on = False
        self._display_on = True

    def init(self):
        self.clear()
    def clear(self):
        self._vram = [[self._blank_ch] * self._INTERNAL_WIDTH for _ in range(self._INTERNAL_HEIGHT)]
        self.set_cursor(0, 0)
        self._scroll_offset_x = 0
        self.no_autoscroll()
    def set_cursor(self, x, y):
        """
        指定された画面上の(x, y)を、各液晶サイズ特有の「内部物理メモリアドレス」にマッピングする
        """
        # --- 4行液晶 (16x4, 20x4) のルール ---
        if self._max_y == 4:
            if y == 0:   self._vram_cursor_x, self._vram_cursor_y = x, 0  # 1行目: 内部1行目の先頭
            elif y == 1: self._vram_cursor_x, self._vram_cursor_y = x, 1  # 2行目: 内部2行目の先頭
            elif y == 2: self._vram_cursor_x, self._vram_cursor_y = x + self._max_x, 0  # 3行目: 1行目のすぐ右の続き
            elif y == 3: self._vram_cursor_x, self._vram_cursor_y = x + self._max_x, 1  # 4行目: 2行目のすぐ右の続き

        # --- 【修正】1行液晶かつ16文字（16x1）の特殊ルール ---
        elif self._max_y == 1 and self._max_x == 16:
            if x < 8:
                self._vram_cursor_x, self._vram_cursor_y = x, 0
            else:
                self._vram_cursor_x, self._vram_cursor_y = (x - 8), 1

        # --- 通常の2行液晶 (16x2, 40x2, 8x1) のルール ---
        else:
            self._vram_cursor_x = x
            self._vram_cursor_y = y % self._INTERNAL_HEIGHT

    def home(self):
        self.set_cursor(0, 0)
        self._scroll_offset_x = 0
    def print(self, arg):
        arg = str(arg).replace(" ", self._blank_ch)
        for ch in arg:
            # 物理メモリ（40文字×2行）の範囲内のときだけ書き込む
            if 0 <= self._vram_cursor_x < self._INTERNAL_WIDTH and 0 <= self._vram_cursor_y < self._INTERNAL_HEIGHT:
                self._vram[self._vram_cursor_y][self._vram_cursor_x] = ch
            
            # カーソルを、現在のカーソル移動方向に1マス進める
            self._vram_cursor_x += self._cursor_direction
            # 物理メモリの範囲を超えたら、次の行にワープする（ただし、物理メモリは40x2で固定なので、行数は2行まで）
            if self._vram_cursor_x >= self._INTERNAL_WIDTH:
                self._vram_cursor_x = 0
                self._vram_cursor_y = (self._vram_cursor_y + 1) % self._INTERNAL_HEIGHT
            else:
                if self._vram_cursor_x < 0:
                    self._vram_cursor_x = self._INTERNAL_WIDTH - 1
                    self._vram_cursor_y = (self._vram_cursor_y - 1) % self._INTERNAL_HEIGHT

            # 【16x1 液晶専用のアドレス自動ワープ処理】
            if self._max_y == 1 and self._max_x == 16:
                if self._cursor_direction == 1:
                    # 右に進んでいる時：物理1行目の8マス目に達したら、物理2行目の0マス目にワープ
                    if self._vram_cursor_x == 8 and self._vram_cursor_y == 0:
                        self._vram_cursor_x = 0
                        self._vram_cursor_y = 1
                else:
                    # 左に進んでいる（文字反転）時：物理2行目の左端を割り込んだら、物理1行目の7マス目にワープ
                    if self._vram_cursor_x == -1 and self._vram_cursor_y == 1:
                        self._vram_cursor_x = 7
                        self._vram_cursor_y = 0


            # オートスクロールがONなら、カーソルと「逆方向」に画面をずらす（_scroll_offset_xをいじる）
            if self._autoscroll_on:
                if self._cursor_direction == 1:
                    # カーソルが右に動いたので、画面は左（+1）にズラす
                    self.scroll_display_left()
                else:
                    # カーソルが左に動いたので、画面は右（-1）にズラす
                    self.scroll_display_right()
    def backlight(self):
        self._backlight_on = True
    def no_backlight(self):
        self._backlight_on = False

    def display(self):
        self._display_on = True
    def no_display(self):
        self._display_on = False
    def cursor(self):
        self._cursor_on = True
    def no_cursor(self):
        self._cursor_on = False
    def blink(self):
        self._blink_on = True
    def no_blink(self):
        self._blink_on = False

    def scroll_display_left(self):
        self._scroll_offset_x = (self._scroll_offset_x + 1) % self._INTERNAL_WIDTH
    def scroll_display_right(self):
        self._scroll_offset_x = (self._scroll_offset_x - 1) % self._INTERNAL_WIDTH
    def left_to_right(self):
        self._cursor_direction = 1
    def right_to_left(self):
        self._cursor_direction = -1
    def autoscroll(self):
        self._autoscroll_on = True
    def no_autoscroll(self):
        self._autoscroll_on = False


    @property
    def cursor_x(self):
        if self._max_y == 4:
            if self._vram_cursor_x >= self._max_x:
                return self._vram_cursor_x - self._max_x
            return self._vram_cursor_x
        # --- 【修正】16x1液晶のときの逆算 ---
        elif self._max_y == 1 and self._max_x == 16:
            if self._vram_cursor_y == 1:
                return self._vram_cursor_x + 8
            return self._vram_cursor_x
        else:
            return self._vram_cursor_x
    @property
    def cursor_y(self):
        if self._max_y == 4:
            if self._vram_cursor_x >= self._max_x:
                return self._vram_cursor_y + 2
            return self._vram_cursor_y
        # --- 【修正】1行液晶なら、サイズに関わらず見た目のYは常に0 ---
        elif self._max_y == 1:
            return 0
        else:
            return self._vram_cursor_y


if __name__ == "__main__":
    lcd = LiquidCrystalMock(16, 2, "_")
    lcd.init()
    lcd.print("Hello, World!")
    lcd.set_cursor(0, 1)
    lcd.print("Line 2 here.")
    print("".join(lcd._vram[0]))
    print("".join(lcd._vram[1]))

