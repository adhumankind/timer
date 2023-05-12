import time
import tkinter as tk
import threading
from pynput import keyboard, mouse


class GlobalEventHook:
    def __init__(self, event_handler):
        self.event_handler = event_handler

        # 注册键盘和鼠标事件
        self.keyboard_controller = keyboard.Controller()
        self.keyboard_listener = keyboard.Listener(on_press=self.on_keyboard_event)
        self.keyboard_listener.start()
        self.mouse_controller = mouse.Controller()
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_event, on_move=self.on_mouse_event)
        self.mouse_listener.start()

    def on_keyboard_event(self, key):
        self.event_handler()
        return True

    def on_mouse_event(self, x, y, button=None, pressed=None):
        self.event_handler()
        return True


class Timer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("计时器")
        self.root.geometry("250x150")
        self.root.config(bg="#0e1621")
        self.root.attributes("-topmost", True)  # 窗口置顶

        self.start_time = time.time()
        self.last_action_time = time.time()
        self.is_stopped = True  # 用于标记计时器是否停止
        self.need_update = True  # 用于标记是否需要更新时间

        self.time_label = tk.Label(self.root, text="00:00", fg="#40d9ff", bg="#0e1621", font=("Courier New", 60, "bold"))
        self.time_label.pack(pady=20)
        self.time_label.config(highlightthickness=1, highlightbackground="#40d9ff")

        self.event_hook = GlobalEventHook(self.on_action)
        self.thread = threading.Thread(target=self.run_background, daemon=True)  # 创建后台线程
        self.thread.start()
        self.init_animation()

        self.root.mainloop()

    def run_background(self):
        while True:
            if self.need_update or not self.is_stopped:
                elapsed_time = time.time() - self.last_action_time

                if elapsed_time > 1:
                    elapsed_time = 0

                cur_time = time.strftime("%M:%S", time.gmtime(time.time() - self.start_time - elapsed_time))
                self.time_label.config(text=cur_time)
                self.need_update = False

            time.sleep(0.1)

    def on_action(self):
        if not self.is_stopped:
            self.reset_timer()
            self.need_update = True

        self.last_action_time = time.time()

        if self.is_stopped:
            self.start_time = time.time()
            self.is_stopped = False
            self.need_update = True

    def reset_timer(self):
        self.start_time = time.time()
        self.last_action_time = time.time()

    def stop_timer(self):
        self.is_stopped = True
        self.reset_timer()

    def init_animation(self):
        self.bg_canvas = tk.Canvas(self.root, width=250, height=150, highlightthickness=0, bg="#0e1621")
        self.bg_canvas.pack()

        self.line_pos = 0
        self.line_dir = 1
        self.line_rectangle = self.bg_canvas.create_rectangle(10, 10, 240, 60, outline="#00e5ff", width=2)
        self.bg_canvas.create_text(10, 90, text="Powered by ChatAi", anchor=tk.W, font=("Courier New", 8), fill="#40d9ff")

        self.animate_line()

    def animate_line(self):
        self.line_pos += 2 * self.line_dir
        if self.line_pos >= 50:
            self.line_dir = -1
        elif self.line_pos <= 0:
            self.line_dir = 1

        self.bg_canvas.delete(self.line_rectangle)
        self.line_rectangle = self.bg_canvas.create_rectangle(10, 10 + self.line_pos, 240, 60 + self.line_pos, outline="#00e5ff", width=2)

        self.root.after(10, self.animate_line)


if __name__ == '__main__':
    timer = Timer()
