from flet import (
    UserControl,
    Column,
    Row,
    Text,
    ElevatedButton,
    Container,
    MainAxisAlignment,
    Markdown,
    MarkdownExtensionSet,
    TextOverflow,
    Divider,
    TextField,
    TextButton,
    Checkbox,
    Slider,
    colors
)
import threading
import subprocess
import adblog
import sys
import time
import os
import datetime

import cmd as CMD


class Terminal(UserControl):
    def __init__(self):
        super().__init__()
        self.start_time = None
        self.save_log_file_enable = False

    def build(self):
        self.log_container = TextField("", text_size=12, height=600, expand=True, multiline=True, read_only=True,
                                       autofocus=True, max_lines=20000)
        self.log_tag = TextField(hint_text="多个tag用空格隔开，如_V_TAG1 _V_TAG2", width=400, autofocus=False)
        self.start_record_btn = TextButton("录制视频", on_click=lambda e: self.start_record())
        self.stop_record_btn = TextButton("停止录制", on_click=lambda e: self.stop_record(), visible=False, width=160)
        self.save_log_file_switch = Checkbox(label="log保存到文件", on_change=lambda e: self.logCheckboxChanged())
        self.terminal = Column(
            [
                Row([
                    ElevatedButton(text="清空日志", on_click=lambda e: self.cleanLog()),
                    ElevatedButton(text="打印log", on_click=lambda e: self.cleanLog()),
                    #  self.save_log_file_switch,
                    #  self.log_tag,
                    ElevatedButton(text="导出日志",
                                   on_click=lambda e: adblog.magazine_log_to_file(f"{self.log_container.value}")),
                ]),
                Row([
                    TextButton(text="截屏", on_click=lambda e: CMD.screen_shot()),
                    self.start_record_btn,
                    self.stop_record_btn,
                    TextButton(text=f"清除截屏和录屏(慎用!)", on_click=lambda e: CMD.clear_screenshots_and_videos(),
                               width=180)
                ]),
                Divider(height=1),
                Container(self.log_container, expand=True)
            ],
            alignment=MainAxisAlignment.START,
            expand=True)
        self.expand = True
        # adblog.default_magazine_log(self.log_container)
        return self.terminal

    def logCheckboxChanged(self):
        self.save_log_file_enable = self.save_log_file_switch.value

    def capture_logcat(tags, output_file_path):
        try:
            # 使用subprocess运行adb logcat命令，将多个标签以空格分隔传递给-s参数，并将输出重定向到指定文件
            subprocess.run(['adb', 'logcat', '-s', *tags], stdout=output_file_path, stderr=subprocess.STDOUT, text=True)
        except Exception as e:
            print(f"Error capturing logcat: {e}")

    def saveLog2File(self):
        try:
            # 使用subprocess运行adb logcat命令，将输出重定向到指定文件
            tags = self.log_tag.value
            if not tags:
                tags = ["_V_MS-"]
            parent_folder = "logs"  # 父文件夹名称
            # 获取当前日期作为文件名的一部分
            current_date = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            # 构建文件名，例如：2023-12-07.log
            log_file_name = f"{current_date}.log"

            # 构建完整的日志文件路径
            log_file_path = os.path.join(parent_folder, log_file_name)

            # 确保父文件夹存在，如果不存在则创建它
            if not os.path.exists(parent_folder):
                os.makedirs(parent_folder)
            # 打开文件以保存日志
            with open(log_file_path, "a") as log_file:
                self.capture_logcat(tags, log_file)
        except Exception as e:
            print(f"Error capturing logcat: {e}")

    def cleanLog(self):
        print("clean log")
        self.log_container.value = ""
        self.log_container.update()
        tags = self.log_tag.value.split()
        if not tags:
            tags = ["_V_MS-"]
        adblog.log_by_tag(self.log_container, tags)
        self.log_container.update()

    def start_record(self):
        self.start_time = time.time()  # 记录开始时间
        self.video_name = CMD.screen_record()
        self.start_record_btn.visible = False
        self.stop_record_btn.visible = True
        self.start_record_btn.update()
        self.stop_record_btn.update()
        # 创建一个线程来更新计时
        threading.Thread(target=self.update_time_count).start()

    def stop_record(self):
        self.start_time = None  # 重置开始时间
        self.stop_record_btn.text = "正在导出..."
        self.stop_record_btn.update()
        CMD.stop_screen_record(self.video_name)
        self.start_record_btn.visible = True
        self.stop_record_btn.visible = False
        self.start_record_btn.update()
        self.stop_record_btn.update()

    def update_time_count(self):
        while self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.stop_record_btn.text = f"已录制{int(elapsed_time)}s...点击停止"
            self.stop_record_btn.update()