#!/usr/bin/python
# coding: UTF-8


class LiquidCrystalPrintTask:
    def __init__(self):
        self.is_active = False  # このタスクが現在有効かどうか
        self.text = ""
        self.x = 0
        self.y = 0
        self.width = 0
        self.life_time = 0      # 表示する長さ（ミリ秒）。0なら永続
        self.registered_time = 0   # 表示を開始した時刻（ミリ秒）

        # エフェクト用の汎用設定変数枠
        self.effect_type = "NONE"  # "NONE", "BLINK", "SLIDE"
        self.delay_time = 0     # 表示開始前の待機時間（ミリ秒）。0なら待機なしで即表示
        self.effect_speed = 0
        self.effect_param = 0  # スライド方向（1:右、-1:左）などを格納

    def get_erase_data(self):
        return " " * self.width, self.x, self.y

    def evaluate(self, now):
        effect_start_time = self.registered_time + self.delay_time
        elapsed = now - effect_start_time

        if self.delay_time > 0 and elapsed < 0:
            # まだ待機時間中なので、窓の幅（width）と同じ長さの空白を返して、液晶には何も出さない
            return " " * self.width, self.x, self.y


        if self.life_time > 0 and elapsed >= self.life_time:
            self.is_active = False
            return self.get_erase_data()

        if self.effect_type == "NONE":
            return self.text, self.x, self.y

        # 点滅 (BLINK)
        elif self.effect_type == "BLINK":
            if (elapsed // self.effect_speed) % 2 == 0:
                return self.text, self.x, self.y
            else:
                return " " * len(self.text), self.x, self.y

        # スライド (SLIDE)
        elif self.effect_type == "SLIDE":
            frames = elapsed // self.effect_speed
            # current_text_x = self.x + (frames * self.effect_param)
            max_scroll = self.width + len(self.text)
            frames = frames % max_scroll
            if self.effect_param > 0:
                # ─── 右方向に流れるスライド ───
                # 左から空白を挿入し、窓の幅（width）に合わせて文字を切り出す
                raw_text = " " * frames + self.text
                text = raw_text[:self.width].ljust(self.width, " ")
            else:
                # ─── 左方向に流れるスライド ───
                raw_text = " " * self.width + self.text
                text = raw_text[frames : len(raw_text)].ljust(self.width, " ")
            return text, self.x, self.y
        # ナイトライダー (KNIGHT)
        elif self.effect_type == "KNIGHT":
            frames = elapsed // self.effect_speed
            max_spaces = self.width - len(self.text)
            if max_spaces <= 0:
                return self.text, self.x, self.y

            cycle = max_spaces * 2
            current_step = frames % cycle

            # ─── 【追加】右スタートのロジック ───
            # effect_param が負（例: -1）なら、時間を半分（片道分）進めた状態から始める
            if self.effect_param < 0:
                current_step = (current_step + max_spaces) % cycle

            # ─── 往復の空白数の計算 ───
            if current_step <= max_spaces:
                spaces_count = current_step
            else:
                spaces_count = cycle - current_step

            text = (" " * spaces_count + self.text).ljust(self.width, " ")
            return text, self.x, self.y

        return self.text, self.x, self.y

