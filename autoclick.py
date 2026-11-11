import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk
import pyautogui

# Tắt tính năng fail-safe mặc định của pyautogui nếu muốn (cẩn thận khi dùng)
# pyautogui.FAILSAFE = True


class AutoClickerApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Python Auto Clicker Pro")
    self.root.geometry("380x420")
    self.root.resizable(False, False)

    self.is_running = False
    self.click_thread = None

    # Biến lưu trữ giá trị
    self.delay_var = tk.DoubleVar(value=0.1)
    self.button_var = tk.StringVar(value="left")
    self.click_type_var = tk.StringVar(value="single")

    self.create_widgets()

    # Lắng nghe phím nóng toàn cục (đơn giản bằng cách check focus hoặc dùng thư viện pynput nếu cần nâng cao)
    # Ở đây dùng bind cửa sổ cho đơn giản, hoặc bạn có thể tối ưu thêm.
    self.root.bind("<F6>", lambda event: self.start_clicking())
    self.root.bind("<F7>", lambda event: self.stop_clicking())

  def create_widgets(self):
    # Tiêu đề
    title_label = tk.Label(
        self.root,
        text="AUTO CLICKER",
        font=("Arial", 16, "bold"),
        fg="#2c3e50",
    )
    title_label.pack(pady=10)

    # Khung cài đặt thời gian
    settings_frame = tk.LabelFrame(
        self.root, text=" Tùy chỉnh khoảng thời gian ", font=("Arial", 10, "bold")
    )
    settings_frame.pack(fill="x", padx=15, pady=5, ipadx=5, ipady=5)

    tk.Label(settings_frame, text="Thời gian nghỉ giữa các click (giây):").pack(
        anchor="w", padx=5, pady=2
    )
    self.delay_entry = tk.Entry(
        settings_frame, textvariable=self.delay_var, font=("Arial", 11)
    )
    self.delay_entry.pack(fill="x", padx=5, pady=2)

    # Khung tùy chỉnh chuột
    mouse_frame = tk.LabelFrame(
        self.root, text=" Tùy chọn chuột ", font=("Arial", 10, "bold")
    )
    mouse_frame.pack(fill="x", padx=15, pady=5, ipadx=5, ipady=5)

    tk.Label(mouse_frame, text="Nút chuột:").pack(anchor="w", padx=5, pady=2)
    mouse_btn_frame = tk.Frame(mouse_frame)
    mouse_btn_frame.pack(anchor="w", padx=5)

    tk.Radiobutton(
        mouse_btn_frame,
        text="Trái",
        variable=self.button_var,
        value="left",
    ).pack(side="left", padx=5)
    tk.Radiobutton(
        mouse_btn_frame,
        text="Phải",
        variable=self.button_var,
        value="right",
    ).pack(side="left", padx=5)
    tk.Radiobutton(
        mouse_btn_frame,
        text="Giữa",
        variable=self.button_var,
        value="middle",
    ).pack(side="left", padx=5)

    tk.Label(mouse_frame, text="Kiểu click:").pack(
        anchor="w", padx=5, pady=(5, 2)
    )
    type_frame = tk.Frame(mouse_frame)
    type_frame.pack(anchor="w", padx=5)

    tk.Radiobutton(
        type_frame,
        text="Click đơn",
        variable=self.click_type_var,
        value="single",
    ).pack(side="left", padx=5)
    tk.Radiobutton(
        type_frame,
        text="Click đúp",
        variable=self.click_type_var,
        value="double",
    ).pack(side="left", padx=5)

    # Trạng thái và hướng dẫn phím tắt
    info_frame = tk.Frame(self.root)
    info_frame.pack(fill="x", padx=15, pady=10)

    self.status_label = tk.Label(
        info_frame,
        text="Trạng thái: Đang dừng",
        font=("Arial", 10, "bold"),
        fg="red",
    )
    self.status_label.pack(anchor="w")

    hotkey_info = tk.Label(
        info_frame,
        text="Phím tắt: [F6] Bắt đầu  |  [F7] Dừng lại",
        font=("Arial", 9, "italic"),
        fg="gray",
    )
    hotkey_info.pack(anchor="w", pady=2)

    # Khung nút bấm điều khiển
    btn_frame = tk.Frame(self.root)
    btn_frame.pack(fill="x", padx=15, pady=5)

    self.start_btn = tk.Button(
        btn_frame,
        text="Bắt đầu (F6)",
        bg="#2ecc71",
        fg="white",
        font=("Arial", 10, "bold"),
        command=self.start_clicking,
    )
    self.start_btn.pack(side="left", expand=True, fill="x", padx=2)

    self.stop_btn = tk.Button(
        btn_frame,
        text="Dừng (F7)",
        bg="#e74c3c",
        fg="white",
        font=("Arial", 10, "bold"),
        command=self.stop_clicking,
        state="disabled",
    )
    self.stop_btn.pack(side="right", expand=True, fill="x", padx=2)

  def click_worker(self):
    while self.is_running:
      try:
        delay = self.delay_var.get()
        if delay < 0:
          delay = 0.01
      except tk.TclError:
        delay = 0.1

      button = self.button_var.get()
      clicks = 2 if self.click_type_var.get() == "double" else 1

      # Thực hiện click tại vị trí con trỏ chuột hiện tại
      pyautogui.click(button=button, clicks=clicks)
      time.sleep(delay)

  def start_clicking(self):
    if not self.is_running:
      try:
        # Kiểm tra giá trị nhập vào hợp lệ
        val = self.delay_var.get()
        if val < 0:
          raise ValueError
      except ValueError:
        messagebox.showerror(
            "Lỗi", "Vui lòng nhập số hợp lệ cho thời gian nghỉ!"
        )
        return

      self.is_running = True
      self.status_label.config(text="Trạng thái: Đang chạy...", fg="green")
      self.start_btn.config(state="disabled")
      self.stop_btn.config(state="normal")

      # Chạy vòng lặp click trong một luồng riêng để GUI không bị đơ
      self.click_thread = threading.Thread(target=self.click_worker)
      self.click_thread.daemon = True
      self.click_thread.start()

  def stop_clicking(self):
    if self.is_running:
      self.is_running = False
      self.status_label.config(text="Trạng thái: Đang dừng", fg="red")
      self.start_btn.config(state="normal")
      self.stop_btn.config(state="disabled")


if __name__ == "__main__":
  root = tk.Tk()
  app = AutoClickerApp(root)
  root.mainloop()
