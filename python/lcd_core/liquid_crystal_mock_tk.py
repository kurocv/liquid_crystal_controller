#!/usr/bin/python
# coding: UTF-8

import copy
import time
import tkinter as tk
from tkinter import ttk
import queue
from lcd_core.liquid_crystal_mock import LiquidCrystalMock

class LiquidCrystalMockTk(tk.Tk, LiquidCrystalMock):
    def __init__(self, queue, size_x, size_y, blank_ch):
        tk.Tk.__init__(self)
        LiquidCrystalMock.__init__(self, size_x, size_y, blank_ch)
        self.title("LiquidCrystalEmulator")
        self.geometry("1100x550")
        self.bind_all("<Button-1>", lambda event: event.widget.focus_set() if not isinstance(event.widget, str) else None)
        self.queue = queue
        self.size_x = size_x
        self.size_y = size_y
        self.blank_ch = blank_ch
        self.lock = False

        # 点滅・タイマー用の初期化
        self.add_time = 0
        self.last_time = int(time.time() * 1000)
        self._blink_state = True

        # --- UIレイアウト用のフレーム作成 ---
        # 液晶表示エリア
        self.lcd_frame = tk.Frame(self)
        self.lcd_frame.pack(pady=20)
        
        self.label = tk.Label(
            self.lcd_frame, text=self.vram_text, 
            font=("Courier", 32, "bold"), background="blue", foreground="white"
        )
        self.label.pack()

        # 設定コントロール用フレーム
        self.ctrl_frame = tk.Frame(self)
        self.ctrl_frame.pack(pady=10, padx=20, fill="x")

        # 1. ドロップダウンリスト（液晶サイズ変更）
        tk.Label(self.ctrl_frame, text="LCD Size:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.size_combo = ttk.Combobox(self.ctrl_frame, values=["16x2", "20x4", "8x1", "16x1", "16x4", "40x2"], state="readonly")
        self.size_combo.set(f"{size_x}x{size_y}")
        self.size_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.size_combo.bind("<<ComboboxSelected>>", self.on_size_changed)

        # 2. 各種機能のオンオフチェックボックス
        self.chk_frame = tk.LabelFrame(self.ctrl_frame, text="Functions")
        self.chk_frame.grid(row=1, column=0, columnspan=3, sticky="we", padx=5, pady=10)

        # blink
        self.blink_var = tk.BooleanVar(value=self._blink_on)
        self.chk_blink = tk.Checkbutton(self.chk_frame, text="Blink", variable=self.blink_var, command=self.sync_checkboxes)
        self.chk_blink.pack(side="left", padx=10)

        # autoscroll
        self.scroll_var = tk.BooleanVar(value=self._autoscroll_on)
        self.chk_scroll = tk.Checkbutton(self.chk_frame, text="Autoscroll", variable=self.scroll_var, command=self.sync_checkboxes)
        self.chk_scroll.pack(side="left", padx=10)

        # right_to_left (ONで右から左、OFFで左から右)
        self.rtl_var = tk.BooleanVar(value=(self._cursor_direction == -1))
        self.chk_rtl = tk.Checkbutton(self.chk_frame, text="Right to Left", variable=self.rtl_var, command=self.sync_checkboxes)
        self.chk_rtl.pack(side="left", padx=10)

        # backlight
        self.bg_var = tk.BooleanVar(value=self._backlight_on)
        self.chk_bg = tk.Checkbutton(self.chk_frame, text="Backlight", variable=self.bg_var, command=self.sync_checkboxes)
        self.chk_bg.pack(side="left", padx=10)

        # 操作用ボタン（Clear, Scroll Left, Scroll Right）
        self.btn_frame = tk.LabelFrame(self.ctrl_frame, text="Operations")
        self.btn_frame.grid(row=2, column=0, columnspan=3, sticky="we", padx=5, pady=10)

        self.btn_clear = tk.Button(self.btn_frame, text="Clear", command=self.on_clear_clicked)
        self.btn_clear.pack(side="left", padx=10, pady=5)

        self.btn_home = tk.Button(self.btn_frame, text="Home", command=self.on_home_clicked)
        self.btn_home.pack(side="left", padx=10, pady=5)

        self.btn_scroll_l = tk.Button(self.btn_frame, text="Scroll Left", command=self.on_scroll_l_clicked)
        self.btn_scroll_l.pack(side="left", padx=10, pady=5)

        self.btn_scroll_r = tk.Button(self.btn_frame, text="Scroll Right", command=self.on_scroll_r_clicked)
        self.btn_scroll_r.pack(side="left", padx=10, pady=5)

        self.btn_cursor_up = tk.Button(self.btn_frame, text="Cursor Up", command=self.cursor_up)
        self.btn_cursor_up.pack(side="left", padx=10, pady=5)

        self.btn_cursor_down = tk.Button(self.btn_frame, text="Cursor Down", command=self.cursor_down)
        self.btn_cursor_down.pack(side="left", padx=10, pady=5)

        self.btn_cursor_left = tk.Button(self.btn_frame, text="Cursor Left", command=self.cursor_left)
        self.btn_cursor_left.pack(side="left", padx=10, pady=5)

        self.btn_cursor_right = tk.Button(self.btn_frame, text="Cursor Right", command=self.cursor_right)
        self.btn_cursor_right.pack(side="left", padx=10, pady=5)

        # テキストエリア（文字入力＆エンターで挿入）
        tk.Label(self.ctrl_frame, text="Input Text (Press Enter):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.entry = tk.Entry(self.ctrl_frame, width=40)
        self.entry.grid(row=3, column=1, columnspan=2, sticky="w", padx=5, pady=5)
        self.entry.bind("<Return>", self.on_entry_enter)

        self.status_label = tk.Label(self.ctrl_frame, text="", font=("Consolas", 12), fg="gray")
        self.status_label.grid(row=4, column=0, columnspan=3, sticky="w", padx=5, pady=5)

        # 定期的にキューをチェックするループを開始
        self.check_queue()

    def check_queue(self):
        # 1. 前回の実行からの経過時間を計算して蓄積
        now = int(time.time() * 1000)
        self.add_time += now - self.last_time
        self.last_time = now

        # 400ms経ったら点滅状態（ON / OFF）を反転させる
        if self.add_time > 400:
            self._blink_state = not self._blink_state  # True/False を入れ替えるフラグ（初期値はTrueにする）
            self.add_time = 0

        need_update = False
        try:
            # キューからデータを取り出す（なければ空のエラーが出る）
            while True:
                self.queue.get_nowait()
                need_update = True
        except queue.Empty:
            pass

        # バックライトの見た目（背景色）を同期
        if self._backlight_on:
            self.label.config(background="blue", foreground="white")
        else:
            self.label.config(background="#26269b", foreground="darkgray")


        # 3. 画面の描画処理
        # 「点滅フラグが変わった（400ms経過）」、または「loop側からデータ更新が来た」場合に画面を書き換える
        if need_update or self.add_time == 0:
            
            # もし `blink` が有効、かつ 点滅タイミングがONのときだけカーソルを「▪」に変える
            # （※もしblinkのON/OFF機能を付けないなら、単に if self._blink_state: だけでもOKです）
            if self._blink_on and self._blink_state:
                # 40×2の内部メモリ（VRAM）をコピー
                tt = copy.deepcopy(self._vram)
                
                # カーソルがメモリの有効範囲内にいるときだけ
                if 0 <= self._vram_cursor_x < self._INTERNAL_WIDTH and 0 <= self._vram_cursor_y < self._INTERNAL_HEIGHT:
                    tt[self._vram_cursor_y][self._vram_cursor_x] = "▪"
                
                # コピーした「tt」を使って画面用の文字列（テキスト）を作る（vram_textのロジックを応用）
                rendered_text = self.render_vram(tt)
                self.label.config(text=rendered_text)
            else:
                # 通常時はそのままの画面を表示
                self.label.config(text=self.vram_text)

        self.status_label.config(
            text=f"Cursor: ({self.cursor_x}, {self.cursor_y}) | Scroll Offset X: {self._scroll_offset_x}"
        )

        # 100ミリ秒後に、再度この check_queue を実行する（tkinterの仕組み）
        self.after(100, self.check_queue)

    @property
    def vram_text(self):
        return self.render_vram()
    def render_vram(self, target_vram=None):
        """
        指定されたVRAM（未指定ならself._vram）から、
        現在の液晶サイズに合わせて文字を切り出してTkinter用に整形する（ロジックの集約）
        """
        # 引数がなければ、自分自身の _vram を使う
        if target_vram is None:
            target_vram = self._vram

        lines = []

        # 【4行モード: 16x4 または 20x4】
        if self._max_y == 4:
            display_map = [
                (0, 0),               # 画面1行目 -> 内部1行目の左側
                (1, 0),               # 画面2行目 -> 内部2行目の左側
                (0, self._max_x),     # 画面3行目 -> 内部1行目の右側 (16文字目、または20文字目から)
                (1, self._max_x)      # 画面4行目 -> 内部2行目の右側
            ]
            for iy, base_x in display_map:
                line_chars = []
                for x in range(self._max_x):
                    internal_x = (self._scroll_offset_x + base_x + x) % self._INTERNAL_WIDTH
                    line_chars.append(target_vram[iy][internal_x])
                lines.append("".join(line_chars))

        # 【1行モード: 16x1】
        elif self._max_y == 1 and self._max_x == 16:
            # print(target_vram)
            line_chars = []
            # 左半分 (8文字)
            for x in range(8):
                internal_x = (self._scroll_offset_x + x) % self._INTERNAL_WIDTH
                line_chars.append(target_vram[0][internal_x])
            # 右半分 (8文字)
            for x in range(8):
                internal_x = (self._scroll_offset_x + x) % self._INTERNAL_WIDTH
                line_chars.append(target_vram[1][internal_x])
            # 8x1 指定なら全体から最初の8文字だけを切り出す
            lines.append("".join(line_chars)[:self._max_x])

        # 【通常の2行: 16x2, 40x2】
        else:
            for y in range(self._max_y):
                line_chars = []
                for x in range(self._max_x):
                    internal_x = (self._scroll_offset_x + x) % self._INTERNAL_WIDTH
                    line_chars.append(target_vram[y][internal_x])
                lines.append("".join(line_chars))
                
        return "\n".join(lines)

    def on_size_changed(self, event):
        """ドロップダウンリストでサイズが変更されたときの処理"""
        selected = self.size_combo.get()  # 例: "20x4"
        x_str, y_str = selected.split("x")
        
        self._max_x = int(x_str)
        self._max_y = int(y_str)
        
        self.home()
        # self.clear()

        # self.blink_var.set(self._blink_on)
        # self.scroll_var.set(self._autoscroll_on)
        # self.rtl_var.set(self._cursor_direction == -1)
        # self.bg_var.set(self._backlight_on)

    def sync_checkboxes(self):
        """チェックボックスの状態を液晶モックのフラグに反映する"""
        # blink
        if self.blink_var.get(): self.blink()
        else: self.no_blink()
        
        # autoscroll
        if self.scroll_var.get(): self.autoscroll()
        else: self.no_autoscroll()
        
        # right_to_left
        if self.rtl_var.get(): self.right_to_left()
        else: self.left_to_right()
        
        # backlight
        if self.bg_var.get(): self.backlight()
        else: self.no_backlight()

    def on_entry_enter(self, event):
        """テキストエリアでエンターキーが押されたときの処理"""
        input_text = self.entry.get()
        if input_text:
            self.print(input_text)  # 現在のカーソル位置に文字列を書き込み
            self.entry.delete(0, tk.END)  # 入力欄をクリア

    def on_clear_clicked(self):
        self.clear()

        self.blink_var.set(self._blink_on)
        self.scroll_var.set(self._autoscroll_on)
        self.rtl_var.set(self._cursor_direction == -1)
        self.bg_var.set(self._backlight_on)

    def on_home_clicked(self):
        self.home()

    def on_scroll_l_clicked(self):
        self.scroll_display_left()

    def on_scroll_r_clicked(self):
        self.scroll_display_right()

    def cursor_left(self):
        self.set_cursor(self.cursor_x - 1 if self.cursor_x > 0 else 0, self.cursor_y)
    
    def cursor_right(self):
        self.set_cursor(self.cursor_x + 1 if self.cursor_x < self._max_x - 1 else self._max_x - 1, self.cursor_y)

    def cursor_up(self):
        self.set_cursor(self.cursor_x, self.cursor_y - 1)

    def cursor_down(self):
        self.set_cursor(self.cursor_x, self.cursor_y + 1)





